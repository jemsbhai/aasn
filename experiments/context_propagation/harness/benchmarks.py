"""Benchmark loading and evaluation.

Handles loading benchmark tasks from JSON files and evaluating
agent solutions against expected outputs. Supports canonical
benchmark formats: HumanEval, MBPP, GSM8K, ARC, MMLU, CRUXEval.
"""

from __future__ import annotations

import json
import logging
import re
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
        """Load self-redesigning prompt benchmarks (mix of coding + general)."""
        tasks = []
        tasks.extend(self._load_from_dir(self.benchmark_dir / "prompt_design"))
        # Also include a sample from coding and general for cross-domain testing
        coding = self._load_from_dir(self.benchmark_dir / "coding")
        general = self._load_from_dir(self.benchmark_dir / "general")
        # Take first 10 from each if available
        tasks.extend(coding[:10])
        tasks.extend(general[:10])
        return tasks

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
                with open(path, encoding="utf-8") as f:
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
    """Evaluates agent solutions against benchmark expectations.

    Supports evaluation types:
      - humaneval: HumanEval function completion with test cases
      - mbpp: MBPP with assertion-based tests
      - gsm8k: Math word problems with numeric answer extraction
      - multiple_choice: ARC, MMLU style A/B/C/D answers
      - code_reasoning: CRUXEval output prediction
      - function_test: Custom function tests with call/expected pairs
      - exact_match: Direct string comparison
      - contains: Substring matching
      - code_execution: Run code and check stdout
    """

    def __init__(self, timeout_seconds: int = 30) -> None:
        self.timeout = timeout_seconds

    async def evaluate(self, task: dict[str, Any], solution: str) -> float:
        """Evaluate a solution against a task.

        Args:
            task: Benchmark task with 'type' field determining eval method.
            solution: Agent's solution string.

        Returns:
            Score between 0.0 and 1.0.
        """
        task_type = task.get("type", "exact_match")

        evaluators = {
            "humaneval": self._eval_humaneval,
            "mbpp": self._eval_mbpp,
            "gsm8k": self._eval_gsm8k,
            "multiple_choice": self._eval_multiple_choice,
            "code_reasoning": self._eval_code_reasoning,
            "function_test": self._eval_function_test,
            "exact_match": self._eval_exact_match,
            "contains": self._eval_contains,
            "code_execution": self._eval_code_execution,
        }

        evaluator = evaluators.get(task_type)
        if evaluator is None:
            logger.warning("Unknown task type: %s, defaulting to exact_match", task_type)
            evaluator = self._eval_exact_match

        try:
            return evaluator(task, solution)
        except Exception as e:
            logger.debug("Evaluation error for %s: %s", task.get("id", "unknown"), e)
            return 0.0

    def _eval_humaneval(self, task: dict[str, Any], solution: str) -> float:
        """Evaluate HumanEval: combine function signature + solution + tests."""
        signature = task.get("function_signature", "")
        test_code = task.get("test_code", "")
        entry_point = task.get("entry_point", "")

        # Build complete code: signature + solution body + test
        code = self._extract_code(solution)

        # If solution includes the full function, use it directly
        # Otherwise, append solution as function body to signature
        if f"def {entry_point}" in code:
            full_code = code
        else:
            full_code = signature + "\n" + self._indent(code, 4)

        full_code += "\n\n" + test_code
        full_code += f"\n\ncheck({entry_point})\n"

        return self._run_code(full_code)

    def _eval_mbpp(self, task: dict[str, Any], solution: str) -> float:
        """Evaluate MBPP: run solution code + assertion tests."""
        code = self._extract_code(solution)
        test_assertions = task.get("test_assertions", [])

        if not test_assertions:
            return 0.0

        # Build test script
        full_code = code + "\n\n"
        passed = 0
        total = len(test_assertions)

        # Run each assertion separately to count passes
        full_code += f"_passed = 0\n_total = {total}\n"
        for assertion in test_assertions:
            full_code += f"""
try:
    {assertion}
    _passed += 1
except (AssertionError, Exception):
    pass
"""
        full_code += "print(f'{_passed}/{_total}')\n"

        result = self._run_code_with_output(full_code)
        if result and "/" in result:
            try:
                p, t = result.split("/")
                return int(p) / int(t)
            except (ValueError, ZeroDivisionError):
                return 0.0
        return 0.0

    def _eval_gsm8k(self, task: dict[str, Any], solution: str) -> float:
        """Evaluate GSM8K: extract numeric answer and compare."""
        expected = task.get("expected_answer", "").strip()
        if not expected:
            return 0.0

        # Extract numeric answer from solution
        extracted = self._extract_numeric_answer(solution)
        if extracted is None:
            return 0.0

        # Normalize both for comparison
        try:
            expected_num = self._parse_number(expected)
            extracted_num = self._parse_number(extracted)
            return 1.0 if abs(expected_num - extracted_num) < 1e-6 else 0.0
        except (ValueError, TypeError):
            return 1.0 if expected.strip() == extracted.strip() else 0.0

    def _eval_multiple_choice(self, task: dict[str, Any], solution: str) -> float:
        """Evaluate multiple choice (ARC, MMLU): extract letter answer."""
        expected = task.get("expected_answer", "").strip().upper()
        if not expected:
            return 0.0

        # Extract the letter answer from the solution
        extracted = self._extract_letter_answer(solution)
        return 1.0 if extracted == expected else 0.0

    def _eval_code_reasoning(self, task: dict[str, Any], solution: str) -> float:
        """Evaluate CRUXEval: compare predicted output."""
        expected = task.get("expected_answer", "").strip()
        if not expected:
            return 0.0

        # Clean solution - take last line or first non-empty line
        cleaned = solution.strip().split("\n")[-1].strip()
        # Remove quotes if present
        cleaned = cleaned.strip("'\"")
        expected = expected.strip("'\"")

        return 1.0 if cleaned == expected else 0.0

    def _eval_function_test(self, task: dict[str, Any], solution: str) -> float:
        """Evaluate custom function tests with call/expected pairs."""
        code = self._extract_code(solution)
        test_cases = task.get("test_cases", [])

        if not test_cases:
            return 0.0

        test_code = code + "\n\nimport sys\n_passed = 0\n"
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

        result = self._run_code_with_output(test_code)
        if result and "/" in result:
            try:
                p, t = result.split("/")
                return int(p) / int(t)
            except (ValueError, ZeroDivisionError):
                return 0.0
        return 0.0

    def _eval_exact_match(self, task: dict[str, Any], solution: str) -> float:
        expected = task.get("expected", task.get("expected_answer", ""))
        return 1.0 if solution.strip() == str(expected).strip() else 0.0

    def _eval_contains(self, task: dict[str, Any], solution: str) -> float:
        expected_items = task.get("expected", [])
        if isinstance(expected_items, str):
            expected_items = [expected_items]
        if not expected_items:
            return 0.0
        matches = sum(1 for item in expected_items if item.lower() in solution.lower())
        return matches / len(expected_items)

    def _eval_code_execution(self, task: dict[str, Any], solution: str) -> float:
        code = self._extract_code(solution)
        expected = task.get("expected", "")
        result = self._run_code_with_output(code)
        return 1.0 if result is not None and result == expected.strip() else 0.0

    # --- Helper methods ---

    def _run_code(self, code: str) -> float:
        """Run Python code, return 1.0 if exit code 0, else 0.0."""
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
            return 1.0 if result.returncode == 0 else 0.0
        except subprocess.TimeoutExpired:
            return 0.0
        except Exception:
            return 0.0

    def _run_code_with_output(self, code: str) -> str | None:
        """Run Python code and return stdout, or None on failure."""
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
            if result.returncode != 0:
                return None
            return result.stdout.strip()
        except (subprocess.TimeoutExpired, Exception):
            return None

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

    @staticmethod
    def _indent(code: str, spaces: int) -> str:
        """Indent each line of code by the given number of spaces."""
        prefix = " " * spaces
        return "\n".join(prefix + line if line.strip() else line for line in code.split("\n"))

    @staticmethod
    def _extract_numeric_answer(text: str) -> str | None:
        """Extract a numeric answer from text.

        Looks for patterns like 'Answer: 42', '#### 42', or the last number.
        """
        # Try "Answer: X" pattern
        match = re.search(r"[Aa]nswer:\s*([\d,.\-]+)", text)
        if match:
            return match.group(1).replace(",", "")

        # Try "#### X" pattern (GSM8K format)
        match = re.search(r"####\s*([\d,.\-]+)", text)
        if match:
            return match.group(1).replace(",", "")

        # Try last number in text
        numbers = re.findall(r"[\d,]+\.?\d*", text)
        if numbers:
            return numbers[-1].replace(",", "")

        return None

    @staticmethod
    def _extract_letter_answer(text: str) -> str:
        """Extract a single letter answer (A/B/C/D) from text."""
        text = text.strip()

        # If response is just a single letter
        if len(text) == 1 and text.upper() in "ABCD":
            return text.upper()

        # Try "Answer: X" pattern
        match = re.search(r"[Aa]nswer:\s*([A-Da-d])", text)
        if match:
            return match.group(1).upper()

        # Try "(X)" pattern
        match = re.search(r"\(([A-Da-d])\)", text)
        if match:
            return match.group(1).upper()

        # First letter in response
        for char in text:
            if char.upper() in "ABCD":
                return char.upper()

        return ""

    @staticmethod
    def _parse_number(s: str) -> float:
        """Parse a number string, handling commas and common formats."""
        s = s.strip().replace(",", "").replace("$", "").replace("%", "")
        return float(s)
