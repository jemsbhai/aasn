"""Generational chain runner.

Orchestrates the spawning chain: runs each generation against benchmarks,
records results, spawns offspring, and applies mitigations.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .agents import BaseAgent, GenerationRecord, create_agent
from .config import ExperimentConfig, MitigationType
from .llm import LLMProvider

logger = logging.getLogger(__name__)


class ChainRunner:
    """Runs a multi-generation spawning chain and records all data."""

    def __init__(
        self,
        config: ExperimentConfig,
        llm: LLMProvider,
        benchmarks: list[dict[str, Any]],
        evaluator: Any,  # Will be typed properly when benchmarks.py is built
    ) -> None:
        self.config = config
        self.llm = llm
        self.benchmarks = benchmarks
        self.evaluator = evaluator
        self.history: list[GenerationRecord] = []
        self.context_store: list[dict[str, Any]] = []  # For structured store mitigation

    async def run(self, run_id: int) -> list[GenerationRecord]:
        """Execute a complete generational chain.

        Args:
            run_id: Identifier for this independent run.

        Returns:
            List of GenerationRecord for each generation.
        """
        run_dir = self.config.get_run_dir(run_id)
        run_dir.mkdir(parents=True, exist_ok=True)

        # Load initial spawning prompt
        initial_prompt = self._load_initial_prompt()
        current_prompt = initial_prompt
        self.history = []
        self.context_store = []

        logger.info(
            "Starting chain: run=%d, agent_type=%s, generations=%d, mitigation=%s",
            run_id,
            self.config.agent_type.value,
            self.config.num_generations,
            self.config.mitigation.strategy.value,
        )

        for gen in range(self.config.num_generations):
            logger.info("Generation %d/%d", gen, self.config.num_generations - 1)
            start_time = time.perf_counter()

            # Create agent with current prompt
            agent = create_agent(self.config.agent_type, self.llm, current_prompt)

            # Evaluate on benchmarks
            scores = await self._evaluate(agent, gen)

            # Build performance summary for spawning
            performance_summary = self._format_performance(scores, gen)

            # Apply mitigations before spawning
            should_regenerate = self._check_mitigations(gen, initial_prompt)

            if should_regenerate:
                # Circuit breaker or anchoring triggered: regenerate from ancestor
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

            # Update context store if using structured store mitigation
            if self.config.mitigation.strategy == MitigationType.STRUCTURED_STORE:
                self._update_context_store(gen, current_prompt, scores, performance_summary)

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
                },
            )
            self.history.append(record)

            # Save generation data to disk
            self._save_generation(run_dir, record)

            # Advance to offspring
            current_prompt = offspring_prompt

        # Save full chain summary
        self._save_chain_summary(run_dir)

        logger.info("Chain complete: run=%d, generations=%d", run_id, len(self.history))
        return self.history

    async def _evaluate(self, agent: BaseAgent, generation: int) -> dict[str, float]:
        """Evaluate an agent on all benchmarks."""
        scores: dict[str, float] = {}

        for task in self.benchmarks:
            task_id = task.get("id", "unknown")
            try:
                solution = await agent.solve_task(task)
                score = await self.evaluator.evaluate(task, solution)
                scores[task_id] = score
            except Exception as e:
                logger.warning("Task %s failed at gen %d: %s", task_id, generation, e)
                scores[task_id] = 0.0

        avg_score = sum(scores.values()) / len(scores) if scores else 0.0
        logger.info("Gen %d avg score: %.3f (%d tasks)", generation, avg_score, len(scores))
        return scores

    def _format_performance(self, scores: dict[str, float], generation: int) -> str:
        """Format benchmark scores into a summary for the spawning prompt."""
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
        """Check if any mitigation should trigger regeneration.

        Returns True if the chain should regenerate from an ancestor.
        """
        strategy = self.config.mitigation.strategy
        cfg = self.config.mitigation

        if strategy == MitigationType.NONE or generation < 2:
            return False

        if strategy == MitigationType.CONTEXT_ANCHORING:
            if generation % cfg.anchor_interval == 0 and self.history:
                # Check retention fidelity against generation 0
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
                # Compute rot rate over lookback window
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

    def _update_context_store(
        self,
        generation: int,
        prompt: str,
        scores: dict[str, float],
        performance_summary: str,
    ) -> None:
        """Add generation data to the structured context store."""
        self.context_store.append(
            {
                "generation": generation,
                "prompt_length": len(prompt),
                "scores": scores,
                "avg_score": sum(scores.values()) / len(scores) if scores else 0.0,
                "performance_summary": performance_summary,
            }
        )

    def _load_initial_prompt(self) -> str:
        """Load the initial spawning prompt P_0."""
        if self.config.spawning_prompt:
            return self.config.spawning_prompt

        if self.config.spawning_prompt_file:
            return self.config.spawning_prompt_file.read_text(encoding="utf-8")

        # Default prompts per agent type
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

    def _save_generation(self, run_dir: Path, record: GenerationRecord) -> None:
        """Save a single generation's data to disk."""
        gen_dir = run_dir / f"gen_{record.generation:03d}"
        gen_dir.mkdir(parents=True, exist_ok=True)

        # Save spawning prompt
        (gen_dir / "spawning_prompt.txt").write_text(record.spawning_prompt, encoding="utf-8")

        # Save offspring prompt
        (gen_dir / "offspring_prompt.txt").write_text(record.offspring_prompt, encoding="utf-8")

        # Save scores
        with open(gen_dir / "scores.json", "w") as f:
            json.dump(record.benchmark_scores, f, indent=2)

        # Save metadata
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
