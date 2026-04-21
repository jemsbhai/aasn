"""Rich feedback generation for high-bandwidth inter-generational transfer.

Provides per-task error analysis, failure pattern detection, and
cumulative memory across generations. This is the high-bandwidth
channel condition for the phase transition experiments.

The key insight from Meta-Harness (Lee et al., 2026): richer access to
prior experience enables improvement rather than degradation. This module
implements analogous rich feedback for prompt-level evolution.
"""

from __future__ import annotations

import logging
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class TaskResult:
    """Detailed result for a single benchmark task."""

    task_id: str
    task_type: str
    task_prompt: str
    solution: str
    score: float
    passed: bool
    error_category: str  # "correct", "wrong_answer", "runtime_error", "timeout", "empty"
    error_detail: str  # Specific error message or comparison


@dataclass
class GenerationMemory:
    """Memory snapshot for a single generation, stored cumulatively."""

    generation: int
    avg_score: float
    num_passed: int
    num_failed: int
    total_tasks: int
    top_failure_patterns: list[str]
    successful_strategies: list[str]
    prompt_length: int
    score_delta: float  # Change from previous generation


class RichFeedbackGenerator:
    """Generates high-bandwidth feedback from evaluation results."""

    async def generate_task_results(
        self,
        tasks: list[dict[str, Any]],
        solutions: list[str],
        scores: list[float],
        evaluator: Any,
    ) -> list[TaskResult]:
        """Analyze each task result in detail.

        Args:
            tasks: Benchmark task definitions.
            solutions: Agent's solutions.
            scores: Evaluation scores.
            evaluator: The evaluator instance for error categorization.

        Returns:
            List of detailed TaskResult objects.
        """
        results = []
        for task, solution, score in zip(tasks, solutions, scores):
            task_id = task.get("id", "unknown")
            task_type = task.get("type", "unknown")
            task_prompt = task.get("prompt", "")
            passed = score >= 0.5

            # Categorize the error
            error_category, error_detail = self._categorize_error(
                task, solution, score
            )

            results.append(TaskResult(
                task_id=task_id,
                task_type=task_type,
                task_prompt=task_prompt[:200],  # Truncate for memory
                solution=solution[:500],  # Truncate for memory
                score=score,
                passed=passed,
                error_category=error_category,
                error_detail=error_detail,
            ))

        return results

    def build_generation_memory(
        self,
        generation: int,
        task_results: list[TaskResult],
        prev_prompt_length: int,
        prev_avg_score: float = 0.0,
    ) -> GenerationMemory:
        """Build a memory snapshot for this generation.

        Args:
            generation: Current generation number.
            task_results: Detailed results from evaluation.
            prev_prompt_length: Length of this generation's prompt.
            prev_avg_score: Previous generation's average score.

        Returns:
            GenerationMemory for cumulative storage.
        """
        scores = [r.score for r in task_results]
        avg_score = sum(scores) / len(scores) if scores else 0.0
        num_passed = sum(1 for r in task_results if r.passed)
        num_failed = len(task_results) - num_passed

        # Find top failure patterns
        failure_categories = Counter(
            r.error_category for r in task_results if not r.passed
        )
        top_failures = [
            f"{cat}: {count} tasks" for cat, count in failure_categories.most_common(5)
        ]

        # Identify successful strategies from passing tasks
        successful = [r for r in task_results if r.passed]
        strategies = self._extract_strategies(successful)

        return GenerationMemory(
            generation=generation,
            avg_score=avg_score,
            num_passed=num_passed,
            num_failed=num_failed,
            total_tasks=len(task_results),
            top_failure_patterns=top_failures,
            successful_strategies=strategies,
            prompt_length=prev_prompt_length,
            score_delta=avg_score - prev_avg_score if generation > 0 else 0.0,
        )

    def format_rich_feedback(
        self,
        generation: int,
        task_results: list[TaskResult],
        cumulative_memory: list[GenerationMemory],
    ) -> str:
        """Format high-bandwidth feedback for the spawning instruction.

        This is the key function: it constructs the rich feedback channel
        that enables improvement rather than degradation.

        Args:
            generation: Current generation number.
            task_results: Detailed results from current evaluation.
            cumulative_memory: All generation memories so far.

        Returns:
            Rich feedback string for the spawning prompt.
        """
        sections = []

        # --- Section 1: Current generation summary ---
        scores = [r.score for r in task_results]
        avg_score = sum(scores) / len(scores) if scores else 0.0
        num_passed = sum(1 for r in task_results if r.passed)
        num_failed = len(task_results) - num_passed

        sections.append(
            f"=== Generation {generation} Results ===\n"
            f"Overall: {avg_score:.3f} average score ({num_passed} passed, {num_failed} failed)"
        )

        # --- Section 2: Failure analysis (most valuable for improvement) ---
        failed_results = [r for r in task_results if not r.passed]
        if failed_results:
            sections.append("\n--- Failure Analysis ---")

            # Group by error category
            by_category: dict[str, list[TaskResult]] = {}
            for r in failed_results:
                by_category.setdefault(r.error_category, []).append(r)

            for category, results in sorted(
                by_category.items(), key=lambda x: -len(x[1])
            ):
                sections.append(f"\n{category} ({len(results)} tasks):")
                # Show up to 3 specific examples per category
                for r in results[:3]:
                    sections.append(f"  Task: {r.task_id}")
                    sections.append(f"  Problem: {r.task_prompt[:150]}")
                    sections.append(f"  Error: {r.error_detail[:200]}")
                    if r.solution:
                        # Show first few lines of the failed solution
                        sol_preview = "\n    ".join(r.solution.split("\n")[:5])
                        sections.append(f"  Your output:\n    {sol_preview}")
                    sections.append("")

        # --- Section 3: Success patterns ---
        passed_results = [r for r in task_results if r.passed]
        if passed_results:
            sections.append(f"\n--- Successful Patterns ({num_passed} tasks) ---")
            # Group by task type
            by_type: dict[str, int] = {}
            for r in passed_results:
                by_type[r.task_type] = by_type.get(r.task_type, 0) + 1
            for task_type, count in sorted(by_type.items(), key=lambda x: -x[1]):
                sections.append(f"  {task_type}: {count} passed")

        # --- Section 4: Cumulative memory (cross-generational knowledge) ---
        if cumulative_memory:
            sections.append("\n--- Cross-Generational Memory ---")
            sections.append("Score trajectory across all generations:")
            for mem in cumulative_memory:
                trend = ""
                if mem.score_delta > 0.01:
                    trend = " (improved)"
                elif mem.score_delta < -0.01:
                    trend = " (declined)"
                sections.append(
                    f"  Gen {mem.generation}: {mem.avg_score:.3f} "
                    f"({mem.num_passed}/{mem.total_tasks} passed){trend}"
                )

            # Persistent failure patterns across generations
            all_failures: Counter[str] = Counter()
            for mem in cumulative_memory:
                for pattern in mem.top_failure_patterns:
                    category = pattern.split(":")[0]
                    all_failures[category] += 1

            if all_failures:
                sections.append("\nRecurring failure patterns across generations:")
                for pattern, count in all_failures.most_common(5):
                    sections.append(
                        f"  {pattern}: appeared in {count}/{len(cumulative_memory)} generations"
                    )

            # Strategies that correlated with improvement
            improving_gens = [
                m for m in cumulative_memory if m.score_delta > 0.01
            ]
            if improving_gens:
                sections.append("\nStrategies from improving generations:")
                for mem in improving_gens[-3:]:  # Last 3 improving gens
                    for strategy in mem.successful_strategies[:2]:
                        sections.append(f"  Gen {mem.generation}: {strategy}")

        # --- Section 5: Actionable recommendations ---
        sections.append("\n--- Key Takeaways for Improvement ---")
        if failed_results:
            top_category = max(
                by_category.items(), key=lambda x: len(x[1])
            )
            sections.append(
                f"1. Highest-impact fix: address '{top_category[0]}' errors "
                f"({len(top_category[1])} failures)"
            )
        if cumulative_memory and len(cumulative_memory) >= 2:
            recent_trend = cumulative_memory[-1].avg_score - cumulative_memory[-2].avg_score
            if recent_trend < 0:
                sections.append(
                    "2. Performance declined from previous generation. "
                    "Consider reverting recent prompt changes."
                )
            else:
                sections.append(
                    "2. Performance improved from previous generation. "
                    "Build on the current approach."
                )

        return "\n".join(sections)

    def _categorize_error(
        self,
        task: dict[str, Any],
        solution: str,
        score: float,
    ) -> tuple[str, str]:
        """Categorize why a task failed.

        Returns:
            Tuple of (error_category, error_detail).
        """
        if score >= 0.5:
            return "correct", "Task passed"

        if not solution or not solution.strip():
            return "empty_output", "No solution generated"

        task_type = task.get("type", "unknown")

        # Code tasks
        if task_type in ("humaneval", "mbpp", "function_test", "code_execution"):
            if "def " not in solution and "```" not in solution:
                return "no_code_generated", "Response did not contain Python code"
            if "import" in solution and "Error" in solution:
                return "import_error", "Solution had import issues"
            # Check if it looks like code was generated but was wrong
            return "wrong_logic", f"Code produced incorrect output for task {task.get('id', '')}"

        # Multiple choice
        if task_type == "multiple_choice":
            expected = task.get("expected_answer", "")
            return "wrong_choice", f"Selected wrong answer (expected: {expected})"

        # Math
        if task_type == "gsm8k":
            expected = task.get("expected_answer", "")
            return "wrong_calculation", f"Incorrect numeric answer (expected: {expected})"

        # Code reasoning
        if task_type == "code_reasoning":
            expected = task.get("expected_answer", "")
            return "wrong_prediction", f"Incorrect output prediction (expected: {expected})"

        # Generic
        return "incorrect", f"Score {score:.2f} below threshold"

    def _extract_strategies(self, passed_results: list[TaskResult]) -> list[str]:
        """Extract brief strategy descriptions from successful tasks."""
        strategies = []
        type_counts = Counter(r.task_type for r in passed_results)
        for task_type, count in type_counts.most_common(3):
            strategies.append(
                f"Strong on {task_type} tasks ({count} passed)"
            )
        return strategies


class CumulativeMemoryStore:
    """Stores generation memories across the full chain.

    This is the high-bandwidth side channel that supplements
    prompt-mediated transfer. Analogous to Meta-Harness's filesystem.
    """

    def __init__(self) -> None:
        self._memories: list[GenerationMemory] = []

    def add(self, memory: GenerationMemory) -> None:
        """Add a generation's memory to the store."""
        self._memories.append(memory)

    def get_all(self) -> list[GenerationMemory]:
        """Get all stored memories."""
        return list(self._memories)

    def get_recent(self, n: int = 5) -> list[GenerationMemory]:
        """Get the N most recent memories."""
        return self._memories[-n:]

    def get_best_generation(self) -> GenerationMemory | None:
        """Get the memory from the highest-scoring generation."""
        if not self._memories:
            return None
        return max(self._memories, key=lambda m: m.avg_score)

    def get_trend(self) -> str:
        """Get a brief description of the performance trend."""
        if len(self._memories) < 2:
            return "insufficient data"
        scores = [m.avg_score for m in self._memories]
        if scores[-1] > scores[0] + 0.02:
            return "improving"
        elif scores[-1] < scores[0] - 0.02:
            return "degrading"
        return "stable"

    def clear(self) -> None:
        """Reset the store for a new run."""
        self._memories.clear()

    def to_dict(self) -> list[dict]:
        """Serialize for JSON storage."""
        return [
            {
                "generation": m.generation,
                "avg_score": m.avg_score,
                "num_passed": m.num_passed,
                "num_failed": m.num_failed,
                "total_tasks": m.total_tasks,
                "top_failure_patterns": m.top_failure_patterns,
                "successful_strategies": m.successful_strategies,
                "prompt_length": m.prompt_length,
                "score_delta": m.score_delta,
            }
            for m in self._memories
        ]
