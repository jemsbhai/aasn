"""CLI entry point for running context propagation experiments."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import random
import sys
from pathlib import Path

import numpy as np

# Add parent directory to path so harness package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness.benchmarks import BenchmarkLoader, Evaluator
from harness.chain import ChainRunner
from harness.config import ExperimentConfig
from harness.llm import LLMProvider
from harness.metrics import MetricsCalculator


def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def find_resume_dir(config: ExperimentConfig) -> Path | None:
    """Find the most recent incomplete experiment directory to resume.

    An experiment is incomplete if it has a checkpoint file indicating
    not all runs have finished.

    Returns:
        Path to resume directory, or None if no resumable run found.
    """
    experiment_base = config.output_dir / config.name
    if not experiment_base.exists():
        return None

    # Look for timestamped directories with checkpoint files
    candidates = sorted(experiment_base.iterdir(), reverse=True)
    for candidate in candidates:
        if not candidate.is_dir():
            continue
        checkpoint = candidate / "checkpoint.json"
        if checkpoint.exists():
            with open(checkpoint) as f:
                cp = json.load(f)
            if cp.get("completed_runs", 0) < cp.get("total_runs", 0):
                return candidate

    return None


async def run_experiment(config: ExperimentConfig, resume_dir: Path | None = None) -> None:
    """Run a complete experiment with multiple independent runs."""
    setup_logging(config.log_level)
    set_seed(config.seed)
    logger = logging.getLogger("experiment")

    # Determine output directory: resume or new
    if resume_dir:
        # Restore timestamp from existing directory
        config.run_timestamp = resume_dir.name
        experiment_dir = resume_dir
        with open(experiment_dir / "checkpoint.json") as f:
            checkpoint = json.load(f)
        start_run = checkpoint["completed_runs"]
        logger.info("RESUMING from %s (run %d/%d)", experiment_dir, start_run, config.num_runs)
    else:
        timestamp = config.initialize_timestamp()
        experiment_dir = config.get_experiment_dir()
        config.save_snapshot()
        start_run = 0

    logger.info("=" * 60)
    logger.info("Experiment: %s", config.name)
    logger.info("Output: %s", experiment_dir)
    logger.info("Agent type: %s", config.agent_type.value)
    logger.info("Feedback: %s", config.feedback_mode.value)
    logger.info("Generations: %d", config.num_generations)
    logger.info("Runs: %d (starting from %d)", config.num_runs, start_run)
    logger.info("Model: %s", config.llm.model)
    logger.info("Temperature: %s", config.llm.temperature)
    logger.info("Mitigation: %s", config.mitigation.strategy.value)
    logger.info("Task sample: %s", config.benchmarks.task_sample_size or "all")
    logger.info("=" * 60)

    # Initialize components
    llm = LLMProvider(config.llm)

    # Check LLM connection
    logger.info("Checking LLM connection...")
    if not await llm.check_connection():
        logger.error("Cannot reach LLM at %s. Is Ollama running?", config.llm.base_url)
        sys.exit(1)
    logger.info("LLM connection OK (model: %s)", config.llm.model)

    # Load benchmarks
    benchmark_dir = Path(__file__).resolve().parent / config.benchmarks.benchmark_dir
    loader = BenchmarkLoader(benchmark_dir)
    benchmarks = loader.load_all(config.agent_type.value)

    if not benchmarks:
        logger.error("No benchmarks found for agent type: %s", config.agent_type.value)
        sys.exit(1)
    logger.info("Loaded %d benchmark tasks", len(benchmarks))

    evaluator = Evaluator(timeout_seconds=config.benchmarks.eval_timeout_seconds)

    # Metrics calculator
    metrics_calc = MetricsCalculator(embedding_model_name=config.embedding_model)

    # Load metrics from already-completed runs if resuming
    all_metrics = []
    if start_run > 0:
        for prev_run_id in range(start_run):
            prev_metrics_path = config.get_run_dir(prev_run_id) / "metrics.json"
            if prev_metrics_path.exists():
                logger.info("Loading cached metrics for run %d", prev_run_id)
                # We'll recompute aggregate at the end, just need a placeholder
                all_metrics.append(None)

    # Run experiments starting from checkpoint
    for run_id in range(start_run, config.num_runs):
        logger.info("-" * 40)
        logger.info("Run %d/%d", run_id + 1, config.num_runs)
        logger.info("-" * 40)

        runner = ChainRunner(
            config=config,
            llm=llm,
            benchmarks=benchmarks,
            evaluator=evaluator,
        )

        history = await runner.run(run_id)
        chain_metrics = metrics_calc.compute_chain_metrics(history)
        all_metrics.append(chain_metrics)

        # Save metrics for this run
        run_dir = config.get_run_dir(run_id)
        with open(run_dir / "metrics.json", "w") as f:
            json.dump(metrics_calc.to_dict(chain_metrics), f, indent=2)

        # Update checkpoint after each completed run
        checkpoint = {
            "completed_runs": run_id + 1,
            "total_runs": config.num_runs,
            "last_completed_run_id": run_id,
        }
        with open(experiment_dir / "checkpoint.json", "w") as f:
            json.dump(checkpoint, f, indent=2)

        logger.info(
            "Run %d complete: final_fidelity=%.3f, avg_rot_rate=%.4f, total_drift=%.3f",
            run_id,
            chain_metrics.final_fidelity,
            chain_metrics.avg_rot_rate,
            chain_metrics.total_drift,
        )
        logger.info("Checkpoint saved: %d/%d runs complete", run_id + 1, config.num_runs)

    # Recompute aggregate from all run metrics on disk
    final_metrics = []
    for run_id in range(config.num_runs):
        metrics_path = config.get_run_dir(run_id) / "metrics.json"
        if metrics_path.exists():
            with open(metrics_path) as f:
                data = json.load(f)
            summary = data.get("summary", {})
            final_metrics.append(summary)

    aggregate = {
        "experiment": config.name,
        "timestamp": config.run_timestamp,
        "agent_type": config.agent_type.value,
        "feedback_mode": config.feedback_mode.value,
        "model": config.llm.model,
        "temperature": config.llm.temperature,
        "mitigation": config.mitigation.strategy.value,
        "num_runs": config.num_runs,
        "num_generations": config.num_generations,
        "task_sample_size": config.benchmarks.task_sample_size,
        "seed": config.seed,
        "results": {
            "avg_final_fidelity": float(np.mean([m.get("final_fidelity", 0) for m in final_metrics])),
            "std_final_fidelity": float(np.std([m.get("final_fidelity", 0) for m in final_metrics])),
            "avg_rot_rate": float(np.mean([m.get("avg_rot_rate", 0) for m in final_metrics])),
            "std_rot_rate": float(np.std([m.get("avg_rot_rate", 0) for m in final_metrics])),
            "avg_total_drift": float(np.mean([m.get("total_drift", 0) for m in final_metrics])),
            "std_total_drift": float(np.std([m.get("total_drift", 0) for m in final_metrics])),
        },
        "llm_stats": {
            "total_calls": llm.call_count,
            "total_tokens": llm.total_tokens_used,
        },
    }

    with open(experiment_dir / "aggregate_results.json", "w") as f:
        json.dump(aggregate, f, indent=2)

    # Mark experiment as complete in checkpoint
    checkpoint = {
        "completed_runs": config.num_runs,
        "total_runs": config.num_runs,
        "status": "complete",
    }
    with open(experiment_dir / "checkpoint.json", "w") as f:
        json.dump(checkpoint, f, indent=2)

    logger.info("=" * 60)
    logger.info("Experiment complete: %s", config.name)
    logger.info("Final fidelity: %.3f +/- %.3f", aggregate["results"]["avg_final_fidelity"], aggregate["results"]["std_final_fidelity"])
    logger.info("Avg rot rate:   %.4f +/- %.4f", aggregate["results"]["avg_rot_rate"], aggregate["results"]["std_rot_rate"])
    logger.info("Total drift:    %.3f +/- %.3f", aggregate["results"]["avg_total_drift"], aggregate["results"]["std_total_drift"])
    logger.info("LLM calls: %d, tokens: %d", llm.call_count, llm.total_tokens_used)
    logger.info("Results saved to: %s", experiment_dir)
    logger.info("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Run context propagation experiments")
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to experiment config YAML file",
    )
    parser.add_argument(
        "--agent-type",
        type=str,
        choices=["coding", "general_task", "self_redesigning"],
        help="Override agent type from config",
    )
    parser.add_argument(
        "--model",
        type=str,
        help="Override LLM model from config",
    )
    parser.add_argument(
        "--generations",
        type=int,
        help="Override number of generations",
    )
    parser.add_argument(
        "--runs",
        type=int,
        help="Override number of independent runs",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume the most recent incomplete experiment for this config",
    )

    args = parser.parse_args()
    config = ExperimentConfig.from_yaml(args.config)

    # Apply CLI overrides
    if args.agent_type:
        config.agent_type = args.agent_type
    if args.model:
        config.llm.model = args.model
    if args.generations:
        config.num_generations = args.generations
    if args.runs:
        config.num_runs = args.runs

    # Check for resume
    resume_dir = None
    if args.resume:
        resume_dir = find_resume_dir(config)
        if resume_dir:
            print(f"Resuming from: {resume_dir}")
        else:
            print("No incomplete experiment found to resume. Starting fresh.")

    asyncio.run(run_experiment(config, resume_dir=resume_dir))


if __name__ == "__main__":
    main()
