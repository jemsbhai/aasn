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


async def run_experiment(config: ExperimentConfig) -> None:
    """Run a complete experiment with multiple independent runs."""
    setup_logging(config.log_level)
    set_seed(config.seed)
    logger = logging.getLogger("experiment")

    logger.info("=" * 60)
    logger.info("Experiment: %s", config.name)
    logger.info("Agent type: %s", config.agent_type.value)
    logger.info("Generations: %d", config.num_generations)
    logger.info("Runs: %d", config.num_runs)
    logger.info("Model: %s", config.llm.model)
    logger.info("Mitigation: %s", config.mitigation.strategy.value)
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

    # Run independent experiments
    all_metrics = []
    for run_id in range(config.num_runs):
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

        logger.info(
            "Run %d complete: final_fidelity=%.3f, avg_rot_rate=%.4f, total_drift=%.3f",
            run_id,
            chain_metrics.final_fidelity,
            chain_metrics.avg_rot_rate,
            chain_metrics.total_drift,
        )

    # Save aggregate summary
    output_dir = config.output_dir / config.name
    output_dir.mkdir(parents=True, exist_ok=True)

    aggregate = {
        "experiment": config.name,
        "agent_type": config.agent_type.value,
        "model": config.llm.model,
        "mitigation": config.mitigation.strategy.value,
        "num_runs": config.num_runs,
        "num_generations": config.num_generations,
        "results": {
            "avg_final_fidelity": float(np.mean([m.final_fidelity for m in all_metrics])),
            "std_final_fidelity": float(np.std([m.final_fidelity for m in all_metrics])),
            "avg_rot_rate": float(np.mean([m.avg_rot_rate for m in all_metrics])),
            "std_rot_rate": float(np.std([m.avg_rot_rate for m in all_metrics])),
            "avg_total_drift": float(np.mean([m.total_drift for m in all_metrics])),
            "std_total_drift": float(np.std([m.total_drift for m in all_metrics])),
        },
        "llm_stats": {
            "total_calls": llm.call_count,
            "total_tokens": llm.total_tokens_used,
        },
    }

    with open(output_dir / "aggregate_results.json", "w") as f:
        json.dump(aggregate, f, indent=2)

    logger.info("=" * 60)
    logger.info("Experiment complete: %s", config.name)
    logger.info("Final fidelity: %.3f +/- %.3f", aggregate["results"]["avg_final_fidelity"], aggregate["results"]["std_final_fidelity"])
    logger.info("Avg rot rate:   %.4f +/- %.4f", aggregate["results"]["avg_rot_rate"], aggregate["results"]["std_rot_rate"])
    logger.info("Total drift:    %.3f +/- %.3f", aggregate["results"]["avg_total_drift"], aggregate["results"]["std_total_drift"])
    logger.info("LLM calls: %d, tokens: %d", llm.call_count, llm.total_tokens_used)
    logger.info("Results saved to: %s", output_dir)
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

    asyncio.run(run_experiment(config))


if __name__ == "__main__":
    main()
