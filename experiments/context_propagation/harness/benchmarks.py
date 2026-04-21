"""Benchmark loading and evaluation.

Handles loading benchmark tasks from JSON files and evaluating
agent solutions against expected outputs.
"""

from __future__ import annotations

import json
import logging
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class BenchmarkLoader:
    """Loads benchmark tasks from the benchmarks directory."""

    def __init__(self, benchmark_dir: Path) -> None:
        self.benchmark_dir = benchmark_dir

    def load_coding_tasks(self) -> list[dict[str, Any]]:
        """Load coding benchmark tasks."""
        return self._load_from_dir(self.benchmark_dir / "coding")

    def load_general_tasks(self) -> list[dict[str, Any]]:
        """Load general task benchmarks."""
        return self._load_from_dir(self.benchmark_dir / "general")

    def load_prompt_tasks(self) -> list[dict[str, Any]]:
        """Load self-redesigning prompt benchmarks."""
        return self._load_from_dir(self.benchmark_dir / "prompt_design")

    def load_all(self, agent_type: str) -> list[dict[str, Any]]:
        """Load benchmarks appropriate for the given agent type."""
        loaders = {
            "coding": self.load_coding_tasks,
            "general_task": self.load_general_tasks,
            "self_redesigning": self.load_prompt_tasks,
        }
        loader = loaders.get(agent_type, self.load_general_tasks)
        return loader()

    def _load_from_dir(self, directory: Path) -> list[dict[str, Any]]:
        """Load all JSON task files from a directory."""
        tasks = []
        if not directory.exists():
            logger.warning("Benchmark directory does not exist: %s", directory)
            return tasks

        for path in sorted(directory.glob("*.json")):
            try:
                with open(path) as f:
                    data = json.load(f)
                if isinstance(data, list):
                    tasks.extend(data)
                else:
                    tasks.append(data)
            except Exception as e:
                logger.warning("Failed to load benchmark %s: %s", path, e)

        logger.info("Loaded %d tasks from %s", len(tasks), directory)
        return tasks


class Evaluator:
    """Evaluates agent solutions against benchmark expectations."""

    def __init__(self, timeout_seconds: int = 30) -> None:
        self.timeout = timeout_seconds

    async def evaluate(self, task: dict[str, Any], solution: str) -> float:
        """Evaluate a solution against a task.

        Args:
            task: Benchmark task with 'type', 'expected', etc.
            solution: Agent's solution string.

        Returns:
            Score between 0.0 and 1.0.
        """
        task_type = task.get("type", "exact_match")

        if task_type == "code_execution":
            return self._eval_code_execution(task, solution)
        elif task_type == "exact_match":
            return self._eval_exact_match(task, solution)
        elif task_type == "contains":
            return self._eval_contains(task, solution)
        elif task_type == "function_test":
            return self._eval_function_test(task, solution)
        else:
            logger.warning("Unknown task type: %s, defaulting to exact_match", task_type)
            return self._eval_exact_match(task, solution)

    def _eval_exact_match(self, task: dict[str, Any], solution: str) -> float:
        """Check if solution exactly matches expected output."""
        expected = task.get("expected", "")
        return 1.0 if solution.strip() == expected.strip() else 0.0

    def _eval_contains(self, task: dict[str, Any], solution: str) -> float:
        """Check if solution contains all expected substrings."""
        expected_items = task.get("expected", [])
        if isinstance(expected_items, str):
            expected_items = [expected_items]

        if not expected_items:
            return 0.0

        matches = sum(1 for item in expected_items if item.lower() in solution.lower())
        return matches / len(expected_items)

    def _eval_code_execution(self, task: dict[str, Any], solution: str) -> float:
        """Execute code solution and check output against expected."""
        # Extract code from markdown fences if present
        code = self._extract_code(solution)
        expected = task.get("expected", "")

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False, encoding="utf-8"
            ) as f:
                f.write(code)
                f.flush()
                result = subprocess.run(
                    [sys.executable, f.name],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                )
            output = result.stdout.strip()
            if result.returncode != 0:
                logger.debug("Code execution failed: %s", result.stderr[:200])
                return 0.0
            return 1.0 if output == expected.strip() else 0.0

        except subprocess.TimeoutExpired:
            logger.debug("Code execution timed out")
            return 0.0
        except Exception as e:
            logger.debug("Code evaluation error: %s", e)
            return 0.0

    def _eval_function_test(self, task: dict[str, Any], solution: str) -> float:
        """Execute code solution and run test cases against it."""
        code = self._extract_code(solution)
        test_cases = task.get("test_cases", [])

        if not test_cases:
            return 0.0

        # Build test script: solution code + test assertions
        test_code = code + "\n\n"
        test_code += "import sys\n"
        test_code += "_passed = 0\n"
        test_code += f"_total = {len(test_cases)}\n"

        for tc in test_cases:
            call = tc.get("call", "")
            expected = tc.get("expected", "")
            test_code += f"""
try:
    _result = {call}
    if _result == {expected}:
        _passed += 1
except Exception:
    pass
"""
        test_code += "print(f'{_passed}/{_total}')\n"

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False, encoding="utf-8"
            ) as f:
                f.write(test_code)
                f.flush()
                result = subprocess.run(
                    [sys.executable, f.name],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                )

            if result.returncode != 0:
                return 0.0

            output = result.stdout.strip()
            if "/" in output:
                passed, total = output.split("/")
                return int(passed) / int(total)
            return 0.0

        except subprocess.TimeoutExpired:
            return 0.0
        except Exception as e:
            logger.debug("Function test error: %s", e)
            return 0.0

    @staticmethod
    def _extract_code(text: str) -> str:
        """Extract Python code from markdown code fences if present."""
        if "```python" in text:
            parts = text.split("```python")
            if len(parts) > 1:
                code = parts[1].split("```")[0]
                return code.strip()
        elif "```" in text:
            parts = text.split("```")
            if len(parts) > 1:
                return parts[1].strip()
        return text.strip()
