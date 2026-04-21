"""Generational chain runner.

Orchestrates the spawning chain: runs each generation against benchmarks,
records results, spawns offspring, and applies mitigations.

Supports two feedback modes:
- score_only: aggregate scores (low-bandwidth channel)
- rich: per-task error analysis + execution traces + cumulative memory (high-bandwidth)
"""

from __future__ import annotations

import json
import logging
import random
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .agents import BaseAgent, GenerationRecord, create_agent
from .config import ExperimentConfig, FeedbackMode, MitigationType
from .llm import LLMProvider
from .rich_feedback import CumulativeMemoryStore, RichFeedbackGenerator, TaskResult

logger = logging.getLogger(__name__)


class ChainRunner:
    """Runs a multi-generation spawning chain and records all data."""

    def __init__(
        self,
        config: ExperimentConfig,
        llm: LLMProvider,
        benchmarks: list[dict[str, Any]],
        evaluator: Any,
    ) -> None:
        self.config = config
        self.llm = llm
        self.evaluator = evaluator
        self.history: list[GenerationRecord] = []
        self.context_store: list[dict[str, Any]] = []

        # Apply task sampling if configured
        if config.benchmarks.task_sample_size and len(benchmarks) > config.benchmarks.task_sample_size:
            random.seed(config.seed)
            self.benchmarks = random.sample(benchmarks, config.benchmarks.task_sample_size)
            logger.info(
                "Sampled %d tasks from %d available",
                len(self.benchmarks),
                len(benchmarks),
            )
        else:
            self.benchmarks = benchmarks

        # Rich feedback components
        self.feedback_generator = RichFeedbackGenerator()
        self.memory_store = CumulativeMemoryStore()

    async def run(self, run_id: int) -> list[GenerationRecord]:
        """Execute a complete generational chain."""
        run_dir = self.config.get_run_dir(run_id)
        run_dir.mkdir(parents=True, exist_ok=True)

        initial_prompt = self._load_initial_prompt()
        current_prompt = initial_prompt
        self.history = []
        self.context_store = []
        self.memory_store.clear()

        logger.info(
            "Starting chain: run=%d, agent_type=%s, generations=%d, mitigation=%s, feedback=%s, tasks=%d",
            run_id,
            self.config.agent_type.value,
            self.config.num_generations,
            self.config.mitigation.strategy.value,
            self.config.feedback_mode.value,
            len(self.benchmarks),
        )

        for gen in range(self.config.num_generations):
            logger.info("Generation %d/%d", gen, self.config.num_generations - 1)
            start_time = time.perf_counter()

            agent = create_agent(self.config.agent_type, self.llm, current_prompt)

            # Evaluate on benchmarks — collect both scores AND solutions
            scores, solutions = await self._evaluate_with_solutions(agent, gen)

            # Generate feedback based on mode
            if self.config.feedback_mode == FeedbackMode.RICH:
                performance_summary = await self._generate_rich_feedback(gen, scores, solutions)
            else:
                performance_summary = self._format_score_only_feedback(scores, gen)

            # Apply mitigations before spawning
            should_regenerate = self._check_mitigations(gen, initial_prompt)

            if should_regenerate:
                ancestor_gen = self._find_best_ancestor()
                current_prompt = self.history[ancestor_gen].spawning_prompt
                logger.info(
                    "Mitigation triggered at gen %d: regenerating from ancestor gen %d",
                    gen,
                    ancestor_gen,
                )
                agent = create_agent(self.config.agent_type, self.llm, current_prompt)

            # Spawn offspring
            offspring_prompt = await agent.spawn_offspring(performance_summary)

            # Record this generation
            elapsed = time.perf_counter() - start_time
            record = GenerationRecord(
                generation=gen,
                agent_type=self.config.agent_type.value,
                spawning_prompt=current_prompt,
                offspring_prompt=offspring_prompt,
                benchmark_scores=scores,
                metadata={
                    "elapsed_seconds": elapsed,
                    "run_id": run_id,
                    "model": self.config.llm.model,
                    "mitigation": self.config.mitigation.strategy.value,
                    "feedback_mode": self.config.feedback_mode.value,
                    "num_tasks": len(self.benchmarks),
                },
            )
            self.history.append(record)

            # Save generation data
            self._save_generation(run_dir, record, performance_summary)

            current_prompt = offspring_prompt

        self._save_chain_summary(run_dir)

        logger.info("Chain complete: run=%d, generations=%d", run_id, len(self.history))
        return self.history

    async def _evaluate_with_solutions(
        self, agent: BaseAgent, generation: int
    ) -> tuple[dict[str, float], list[tuple[dict[str, Any], str, float]]]:
        """Evaluate agent and collect both scores and solutions.

        Returns:
            Tuple of (scores_dict, list of (task, solution, score) triples).
        """
        scores: dict[str, float] = {}
        solutions: list[tuple[dict[str, Any], str, float]] = []

        for task in self.benchmarks:
            task_id = task.get("id", "unknown")
            try:
                solution = await agent.solve_task(task)
                score = await self.evaluator.evaluate(task, solution)
                scores[task_id] = score
                solutions.append((task, solution, score))
            except Exception as e:
                logger.warning("Task %s failed at gen %d: %s", task_id, generation, e)
                scores[task_id] = 0.0
                solutions.append((task, "", 0.0))

        avg_score = sum(scores.values()) / len(scores) if scores else 0.0
        logger.info("Gen %d avg score: %.3f (%d tasks)", generation, avg_score, len(scores))
        return scores, solutions

    async def _generate_rich_feedback(
        self,
        generation: int,
        scores: dict[str, float],
        solutions: list[tuple[dict[str, Any], str, float]],
    ) -> str:
        """Generate high-bandwidth feedback with per-task analysis and cumulative memory."""
        # Build detailed task results
        tasks = [s[0] for s in solutions]
        solution_texts = [s[1] for s in solutions]
        score_values = [s[2] for s in solutions]

        task_results = await self.feedback_generator.generate_task_results(
            tasks, solution_texts, score_values, self.evaluator
        )

        # Build generation memory and add to cumulative store
        prompt_length = len(self.history[-1].spawning_prompt) if self.history else 0
        prev_avg = 0.0
        if self.history:
            prev_scores = self.history[-1].benchmark_scores
            prev_avg = sum(prev_scores.values()) / len(prev_scores) if prev_scores else 0.0
        gen_memory = self.feedback_generator.build_generation_memory(
            generation, task_results, prompt_length, prev_avg_score=prev_avg
        )
        self.memory_store.add(gen_memory)

        # Format rich feedback with cumulative memory
        feedback = self.feedback_generator.format_rich_feedback(
            generation, task_results, self.memory_store.get_all()
        )

        logger.info(
            "Rich feedback generated: %d chars, %d failure patterns, %d memories",
            len(feedback),
            len(gen_memory.top_failure_patterns),
            len(self.memory_store.get_all()),
        )

        return feedback

    def _format_score_only_feedback(self, scores: dict[str, float], generation: int) -> str:
        """Format low-bandwidth score-only feedback (original behavior)."""
        lines = [f"Generation {generation} benchmark results:"]
        for task_id, score in sorted(scores.items()):
            status = "PASS" if score >= 0.5 else "FAIL"
            lines.append(f"  - {task_id}: {score:.2f} ({status})")

        avg = sum(scores.values()) / len(scores) if scores else 0.0
        lines.append(f"  Average score: {avg:.2f}")

        if generation > 0 and self.history:
            prev_avg = sum(self.history[-1].benchmark_scores.values()) / len(
                self.history[-1].benchmark_scores
            )
            delta = avg - prev_avg
            direction = "improved" if delta > 0 else "declined"
            lines.append(f"  Trend: {direction} by {abs(delta):.2f} from previous generation")

        return "\n".join(lines)

    def _check_mitigations(self, generation: int, initial_prompt: str) -> bool:
        """Check if any mitigation should trigger regeneration."""
        strategy = self.config.mitigation.strategy
        cfg = self.config.mitigation

        if strategy == MitigationType.NONE or generation < 2:
            return False

        if strategy == MitigationType.CONTEXT_ANCHORING:
            if generation % cfg.anchor_interval == 0 and self.history:
                gen0_avg = sum(self.history[0].benchmark_scores.values()) / len(
                    self.history[0].benchmark_scores
                )
                current_avg = sum(self.history[-1].benchmark_scores.values()) / len(
                    self.history[-1].benchmark_scores
                )
                fidelity = current_avg / gen0_avg if gen0_avg > 0 else 0.0
                if fidelity < cfg.fidelity_threshold:
                    logger.info(
                        "Context anchoring: fidelity %.3f < threshold %.3f",
                        fidelity,
                        cfg.fidelity_threshold,
                    )
                    return True

        elif strategy == MitigationType.CIRCUIT_BREAKER:
            if len(self.history) >= cfg.lookback_window:
                recent = self.history[-cfg.lookback_window :]
                avgs = [
                    sum(r.benchmark_scores.values()) / len(r.benchmark_scores) for r in recent
                ]
                if len(avgs) >= 2:
                    rot_rate = (avgs[0] - avgs[-1]) / len(avgs)
                    if rot_rate > cfg.rot_rate_threshold:
                        logger.info(
                            "Circuit breaker: rot rate %.3f > threshold %.3f",
                            rot_rate,
                            cfg.rot_rate_threshold,
                        )
                        return True

        return False

    def _find_best_ancestor(self) -> int:
        """Find the generation with the best average benchmark score."""
        if not self.history:
            return 0
        best_gen = 0
        best_avg = 0.0
        for record in self.history:
            avg = sum(record.benchmark_scores.values()) / len(record.benchmark_scores)
            if avg > best_avg:
                best_avg = avg
                best_gen = record.generation
        return best_gen

    def _load_initial_prompt(self) -> str:
        """Load the initial spawning prompt P_0."""
        if self.config.spawning_prompt:
            return self.config.spawning_prompt

        if self.config.spawning_prompt_file:
            return self.config.spawning_prompt_file.read_text(encoding="utf-8")

        defaults = {
            "coding": (
                "You are an expert Python programmer. When given a programming task, "
                "write clean, correct, and efficient Python code. Include type hints. "
                "Handle edge cases. Return only the code, no explanations."
            ),
            "general_task": (
                "You are a careful and precise assistant. When given a task, think "
                "step by step before answering. Be concise but thorough. If unsure, "
                "say so rather than guessing."
            ),
            "self_redesigning": (
                "You are a versatile AI assistant. Approach each task methodically: "
                "1) Understand what is being asked. 2) Break the problem into parts. "
                "3) Solve each part carefully. 4) Verify your answer before responding."
            ),
        }
        return defaults.get(self.config.agent_type.value, defaults["general_task"])

    def _save_generation(
        self, run_dir: Path, record: GenerationRecord, feedback: str
    ) -> None:
        """Save a single generation's data to disk."""
        gen_dir = run_dir / f"gen_{record.generation:03d}"
        gen_dir.mkdir(parents=True, exist_ok=True)

        (gen_dir / "spawning_prompt.txt").write_text(record.spawning_prompt, encoding="utf-8")
        (gen_dir / "offspring_prompt.txt").write_text(record.offspring_prompt, encoding="utf-8")
        (gen_dir / "feedback.txt").write_text(feedback, encoding="utf-8")

        with open(gen_dir / "scores.json", "w") as f:
            json.dump(record.benchmark_scores, f, indent=2)

        with open(gen_dir / "metadata.json", "w") as f:
            json.dump(record.metadata, f, indent=2)

    def _save_chain_summary(self, run_dir: Path) -> None:
        """Save summary of the full chain."""
        summary = {
            "config": self.config.model_dump(mode="json"),
            "generations": len(self.history),
            "score_trajectory": [
                {
                    "generation": r.generation,
                    "avg_score": sum(r.benchmark_scores.values()) / len(r.benchmark_scores)
                    if r.benchmark_scores
                    else 0.0,
                    "prompt_length": len(r.spawning_prompt),
                }
                for r in self.history
            ],
        }

        with open(run_dir / "chain_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
