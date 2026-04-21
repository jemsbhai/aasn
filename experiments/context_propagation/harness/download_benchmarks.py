"""Benchmark downloader and standardizer.

Downloads canonical benchmarks from HuggingFace and converts them
into the standardized task format used by the experiment harness.

Supported benchmarks:
  Tier 1 (immediate): HumanEval, MBPP, GSM8K, ARC-Challenge, MMLU
  Tier 2 (next): CRUXEval, DS-1000, CodeContests, LiveCodeBench
  Tier 3 (planned): Tool-use QA
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

BENCHMARK_REGISTRY: dict[str, dict[str, Any]] = {
    # --- Coding benchmarks ---
    "humaneval": {
        "hf_dataset": "openai/openai_humaneval",
        "split": "test",
        "category": "coding",
        "description": "OpenAI HumanEval: 164 Python function completion tasks",
        "tier": 1,
    },
    "mbpp": {
        "hf_dataset": "google-research-datasets/mbpp",
        "split": "test",
        "category": "coding",
        "description": "Mostly Basic Python Problems: 500 test tasks",
        "tier": 1,
    },
    "cruxeval": {
        "hf_dataset": "cruxeval/cruxeval",
        "split": "test",
        "category": "coding",
        "description": "CRUXEval: code reasoning, input/output prediction",
        "tier": 2,
    },
    # --- General reasoning benchmarks ---
    "gsm8k": {
        "hf_dataset": "openai/gsm8k",
        "subset": "main",
        "split": "test",
        "category": "general",
        "description": "Grade School Math 8K: 1319 math word problems",
        "tier": 1,
    },
    "arc_challenge": {
        "hf_dataset": "allenai/ai2_arc",
        "subset": "ARC-Challenge",
        "split": "test",
        "category": "general",
        "description": "ARC-Challenge: 1172 science reasoning questions",
        "tier": 1,
    },
    "mmlu": {
        "hf_dataset": "cais/mmlu",
        "subset": "all",
        "split": "test",
        "category": "general",
        "description": "MMLU: Massive Multitask Language Understanding",
        "tier": 1,
        "sample_size": 200,  # Subset for tractability
    },
}


class BenchmarkDownloader:
    """Downloads and standardizes benchmarks from HuggingFace."""

    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def download(
        self,
        benchmark_name: str,
        force: bool = False,
        sample_size: int | None = None,
    ) -> Path:
        """Download a benchmark and save as standardized JSON.

        Args:
            benchmark_name: Key from BENCHMARK_REGISTRY.
            force: Re-download even if cached.
            sample_size: Override default sample size.

        Returns:
            Path to the downloaded benchmark JSON file.
        """
        if benchmark_name not in BENCHMARK_REGISTRY:
            raise ValueError(
                f"Unknown benchmark: {benchmark_name}. "
                f"Available: {list(BENCHMARK_REGISTRY.keys())}"
            )

        info = BENCHMARK_REGISTRY[benchmark_name]
        output_path = self.cache_dir / info["category"] / f"{benchmark_name}.json"

        if output_path.exists() and not force:
            logger.info("Benchmark %s already cached at %s", benchmark_name, output_path)
            return output_path

        logger.info("Downloading benchmark: %s (%s)", benchmark_name, info["description"])

        from datasets import load_dataset

        # Load from HuggingFace
        load_kwargs: dict[str, Any] = {"trust_remote_code": True}
        if "subset" in info:
            dataset = load_dataset(info["hf_dataset"], info["subset"], split=info["split"], **load_kwargs)
        else:
            dataset = load_dataset(info["hf_dataset"], split=info["split"], **load_kwargs)

        # Apply sampling if needed
        n = sample_size or info.get("sample_size")
        if n and len(dataset) > n:
            dataset = dataset.shuffle(seed=42).select(range(n))
            logger.info("Sampled %d examples from %s", n, benchmark_name)

        # Convert to standardized format
        converter = self._get_converter(benchmark_name)
        tasks = converter(dataset, benchmark_name)

        # Save
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)

        logger.info("Saved %d tasks to %s", len(tasks), output_path)
        return output_path

    def download_all(self, tier: int = 1, force: bool = False) -> dict[str, Path]:
        """Download all benchmarks up to the specified tier.

        Args:
            tier: Maximum tier to download (1, 2, or 3).
            force: Re-download even if cached.

        Returns:
            Dict mapping benchmark name to file path.
        """
        paths = {}
        for name, info in BENCHMARK_REGISTRY.items():
            if info["tier"] <= tier:
                try:
                    path = self.download(name, force=force)
                    paths[name] = path
                except Exception as e:
                    logger.error("Failed to download %s: %s", name, e)
        return paths

    def list_available(self) -> list[dict[str, Any]]:
        """List all available benchmarks with metadata."""
        return [
            {"name": name, **{k: v for k, v in info.items() if k != "hf_dataset"}}
            for name, info in BENCHMARK_REGISTRY.items()
        ]

    def list_cached(self) -> list[str]:
        """List benchmarks already downloaded."""
        cached = []
        for name, info in BENCHMARK_REGISTRY.items():
            path = self.cache_dir / info["category"] / f"{name}.json"
            if path.exists():
                cached.append(name)
        return cached

    def _get_converter(self, benchmark_name: str):
        """Get the appropriate converter function for a benchmark."""
        converters = {
            "humaneval": self._convert_humaneval,
            "mbpp": self._convert_mbpp,
            "gsm8k": self._convert_gsm8k,
            "arc_challenge": self._convert_arc,
            "mmlu": self._convert_mmlu,
            "cruxeval": self._convert_cruxeval,
        }
        return converters.get(benchmark_name, self._convert_generic)

    @staticmethod
    def _convert_humaneval(dataset, benchmark_name: str) -> list[dict[str, Any]]:
        """Convert HumanEval to standardized format."""
        tasks = []
        for item in dataset:
            task_id = item["task_id"]  # e.g., "HumanEval/0"
            prompt = item["prompt"]  # Function signature + docstring
            canonical = item["canonical_solution"]
            test_code = item["test"]
            entry_point = item["entry_point"]

            tasks.append({
                "id": f"humaneval_{task_id.replace('/', '_')}",
                "benchmark": benchmark_name,
                "type": "humaneval",
                "prompt": (
                    f"Complete the following Python function. Return ONLY the function body "
                    f"(the code that comes after the function signature). "
                    f"Do not repeat the signature or docstring.\n\n{prompt}"
                ),
                "function_signature": prompt,
                "canonical_solution": canonical,
                "test_code": test_code,
                "entry_point": entry_point,
            })
        return tasks

    @staticmethod
    def _convert_mbpp(dataset, benchmark_name: str) -> list[dict[str, Any]]:
        """Convert MBPP to standardized format."""
        tasks = []
        for item in dataset:
            task_id = item["task_id"]
            text = item["text"]  # Natural language description
            code = item["code"]  # Solution code
            test_list = item["test_list"]  # List of assert statements

            tasks.append({
                "id": f"mbpp_{task_id}",
                "benchmark": benchmark_name,
                "type": "mbpp",
                "prompt": (
                    f"Write a Python function to solve the following problem. "
                    f"Return only the code.\n\n{text}"
                ),
                "canonical_solution": code,
                "test_assertions": test_list,
            })
        return tasks

    @staticmethod
    def _convert_gsm8k(dataset, benchmark_name: str) -> list[dict[str, Any]]:
        """Convert GSM8K to standardized format."""
        tasks = []
        for i, item in enumerate(dataset):
            question = item["question"]
            answer_text = item["answer"]

            # Extract the final numeric answer (after ####)
            final_answer = answer_text.split("####")[-1].strip() if "####" in answer_text else ""

            tasks.append({
                "id": f"gsm8k_{i:04d}",
                "benchmark": benchmark_name,
                "type": "gsm8k",
                "prompt": (
                    f"Solve this math problem step by step. "
                    f"After your reasoning, write your final numeric answer "
                    f"on the last line prefixed with 'Answer: '.\n\n{question}"
                ),
                "expected_answer": final_answer,
                "full_solution": answer_text,
            })
        return tasks

    @staticmethod
    def _convert_arc(dataset, benchmark_name: str) -> list[dict[str, Any]]:
        """Convert ARC-Challenge to standardized format."""
        tasks = []
        for i, item in enumerate(dataset):
            question = item["question"]
            choices = item["choices"]
            answer_key = item["answerKey"]

            # Format choices
            choice_labels = choices["label"]
            choice_texts = choices["text"]
            formatted_choices = "\n".join(
                f"  {label}) {text}" for label, text in zip(choice_labels, choice_texts)
            )

            tasks.append({
                "id": f"arc_{i:04d}",
                "benchmark": benchmark_name,
                "type": "multiple_choice",
                "prompt": (
                    f"Answer the following science question. "
                    f"Reply with ONLY the letter of the correct answer.\n\n"
                    f"{question}\n{formatted_choices}"
                ),
                "expected_answer": answer_key,
                "choices": dict(zip(choice_labels, choice_texts)),
            })
        return tasks

    @staticmethod
    def _convert_mmlu(dataset, benchmark_name: str) -> list[dict[str, Any]]:
        """Convert MMLU to standardized format."""
        tasks = []
        for i, item in enumerate(dataset):
            question = item["question"]
            choices = item["choices"]
            answer_idx = item["answer"]  # 0-3 index

            labels = ["A", "B", "C", "D"]
            formatted_choices = "\n".join(
                f"  {labels[j]}) {choice}" for j, choice in enumerate(choices)
            )
            expected = labels[answer_idx]

            subject = item.get("subject", "general")

            tasks.append({
                "id": f"mmlu_{i:04d}_{subject}",
                "benchmark": benchmark_name,
                "type": "multiple_choice",
                "prompt": (
                    f"Answer the following question. "
                    f"Reply with ONLY the letter of the correct answer.\n\n"
                    f"{question}\n{formatted_choices}"
                ),
                "expected_answer": expected,
                "choices": dict(zip(labels, choices)),
                "subject": subject,
            })
        return tasks

    @staticmethod
    def _convert_cruxeval(dataset, benchmark_name: str) -> list[dict[str, Any]]:
        """Convert CRUXEval to standardized format."""
        tasks = []
        for i, item in enumerate(dataset):
            code = item.get("code", "")
            input_val = item.get("input", "")
            output_val = item.get("output", "")

            tasks.append({
                "id": f"cruxeval_{i:04d}",
                "benchmark": benchmark_name,
                "type": "code_reasoning",
                "prompt": (
                    f"Given the following Python code and input, predict the output.\n\n"
                    f"Code:\n```python\n{code}\n```\n\n"
                    f"Input: {input_val}\n\n"
                    f"What is the output? Reply with ONLY the output value."
                ),
                "code": code,
                "input": input_val,
                "expected_answer": output_val,
            })
        return tasks

    @staticmethod
    def _convert_generic(dataset, benchmark_name: str) -> list[dict[str, Any]]:
        """Generic converter for unknown benchmark formats."""
        tasks = []
        for i, item in enumerate(dataset):
            tasks.append({
                "id": f"{benchmark_name}_{i:04d}",
                "benchmark": benchmark_name,
                "type": "generic",
                "prompt": str(item.get("question", item.get("text", item.get("input", "")))),
                "expected_answer": str(item.get("answer", item.get("output", item.get("label", "")))),
                "raw": {k: str(v)[:500] for k, v in item.items()},
            })
        return tasks
