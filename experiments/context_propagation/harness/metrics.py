"""Context propagation metrics.

Measures context fidelity, semantic drift, knowledge compression,
and rot rate across generations.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import numpy as np

from .agents import GenerationRecord

logger = logging.getLogger(__name__)


@dataclass
class FidelityMetrics:
    """Fidelity measurements for a single generation."""

    generation: int
    retention_fidelity: float  # F_r: performance on original benchmarks
    transfer_fidelity: float  # F_t: performance on held-out benchmarks
    combined_fidelity: float  # F = alpha * F_r + (1-alpha) * F_t
    rot_rate: float | None  # rho = -dF/dg (None for gen 0)


@dataclass
class DriftMetrics:
    """Semantic drift measurements for a single generation."""

    generation: int
    cosine_similarity_to_p0: float  # sim(embed(P_g), embed(P_0))
    prompt_length: int
    prompt_length_ratio: float  # len(P_g) / len(P_0)


@dataclass
class ChainMetrics:
    """Aggregated metrics for a full generational chain."""

    fidelity: list[FidelityMetrics] = field(default_factory=list)
    drift: list[DriftMetrics] = field(default_factory=list)
    avg_rot_rate: float = 0.0
    max_rot_rate: float = 0.0
    final_fidelity: float = 0.0
    total_drift: float = 0.0  # 1 - final cosine similarity


class MetricsCalculator:
    """Calculates context propagation metrics from experiment history."""

    def __init__(
        self,
        embedding_model_name: str = "all-MiniLM-L6-v2",
        fidelity_alpha: float = 0.5,
    ) -> None:
        self.embedding_model_name = embedding_model_name
        self.fidelity_alpha = fidelity_alpha
        self._embedder = None

    def _get_embedder(self):
        """Lazy-load the sentence transformer model."""
        if self._embedder is None:
            from sentence_transformers import SentenceTransformer

            self._embedder = SentenceTransformer(self.embedding_model_name)
        return self._embedder

    def compute_fidelity(
        self,
        history: list[GenerationRecord],
        baseline_scores: dict[str, float] | None = None,
        held_out_scores: list[dict[str, float]] | None = None,
    ) -> list[FidelityMetrics]:
        """Compute context fidelity for each generation.

        Args:
            history: List of generation records from a chain run.
            baseline_scores: Gen 0 scores (computed from history[0] if None).
            held_out_scores: Optional held-out benchmark scores per generation.

        Returns:
            List of FidelityMetrics, one per generation.
        """
        if not history:
            return []

        # Use gen 0 as baseline
        if baseline_scores is None:
            baseline_scores = history[0].benchmark_scores

        baseline_avg = (
            sum(baseline_scores.values()) / len(baseline_scores) if baseline_scores else 1.0
        )

        results = []
        prev_fidelity = None

        for i, record in enumerate(history):
            # Retention fidelity: current performance / baseline performance
            current_avg = (
                sum(record.benchmark_scores.values()) / len(record.benchmark_scores)
                if record.benchmark_scores
                else 0.0
            )
            f_r = min(current_avg / baseline_avg, 1.0) if baseline_avg > 0 else 0.0

            # Transfer fidelity: from held-out benchmarks if available
            f_t = f_r  # Default to retention fidelity if no held-out data
            if held_out_scores and i < len(held_out_scores):
                ho = held_out_scores[i]
                ho_avg = sum(ho.values()) / len(ho) if ho else 0.0
                f_t = min(ho_avg / baseline_avg, 1.0) if baseline_avg > 0 else 0.0

            # Combined fidelity
            alpha = self.fidelity_alpha
            f_combined = alpha * f_r + (1 - alpha) * f_t

            # Rot rate: -dF/dg
            rot_rate = None
            if prev_fidelity is not None:
                rot_rate = prev_fidelity - f_combined  # Positive = degradation

            results.append(
                FidelityMetrics(
                    generation=record.generation,
                    retention_fidelity=f_r,
                    transfer_fidelity=f_t,
                    combined_fidelity=f_combined,
                    rot_rate=rot_rate,
                )
            )
            prev_fidelity = f_combined

        return results

    def compute_semantic_drift(self, history: list[GenerationRecord]) -> list[DriftMetrics]:
        """Measure semantic drift of spawning prompts from P_0.

        Uses sentence embeddings to compute cosine similarity between
        each generation's prompt and the original prompt.

        Args:
            history: List of generation records.

        Returns:
            List of DriftMetrics, one per generation.
        """
        if not history:
            return []

        prompts = [r.spawning_prompt for r in history]
        embedder = self._get_embedder()
        embeddings = embedder.encode(prompts, convert_to_numpy=True, normalize_embeddings=True)

        p0_embedding = embeddings[0]
        p0_length = len(prompts[0])

        results = []
        for i, record in enumerate(history):
            cosine_sim = float(np.dot(embeddings[i], p0_embedding))
            prompt_len = len(record.spawning_prompt)

            results.append(
                DriftMetrics(
                    generation=record.generation,
                    cosine_similarity_to_p0=cosine_sim,
                    prompt_length=prompt_len,
                    prompt_length_ratio=prompt_len / p0_length if p0_length > 0 else 1.0,
                )
            )

        return results

    def compute_chain_metrics(
        self,
        history: list[GenerationRecord],
        held_out_scores: list[dict[str, float]] | None = None,
    ) -> ChainMetrics:
        """Compute all metrics for a complete chain.

        Args:
            history: Full generation history from a chain run.
            held_out_scores: Optional held-out scores per generation.

        Returns:
            Aggregated ChainMetrics.
        """
        fidelity = self.compute_fidelity(history, held_out_scores=held_out_scores)
        drift = self.compute_semantic_drift(history)

        # Aggregate rot rates (skip gen 0 which has no rot rate)
        rot_rates = [f.rot_rate for f in fidelity if f.rot_rate is not None]
        avg_rot = float(np.mean(rot_rates)) if rot_rates else 0.0
        max_rot = float(np.max(rot_rates)) if rot_rates else 0.0

        final_fid = fidelity[-1].combined_fidelity if fidelity else 0.0
        total_drift = 1.0 - drift[-1].cosine_similarity_to_p0 if drift else 0.0

        return ChainMetrics(
            fidelity=fidelity,
            drift=drift,
            avg_rot_rate=avg_rot,
            max_rot_rate=max_rot,
            final_fidelity=final_fid,
            total_drift=total_drift,
        )

    def to_dict(self, metrics: ChainMetrics) -> dict:
        """Serialize ChainMetrics to a JSON-compatible dict."""
        return {
            "fidelity": [
                {
                    "generation": f.generation,
                    "retention_fidelity": f.retention_fidelity,
                    "transfer_fidelity": f.transfer_fidelity,
                    "combined_fidelity": f.combined_fidelity,
                    "rot_rate": f.rot_rate,
                }
                for f in metrics.fidelity
            ],
            "drift": [
                {
                    "generation": d.generation,
                    "cosine_similarity_to_p0": d.cosine_similarity_to_p0,
                    "prompt_length": d.prompt_length,
                    "prompt_length_ratio": d.prompt_length_ratio,
                }
                for d in metrics.drift
            ],
            "summary": {
                "avg_rot_rate": metrics.avg_rot_rate,
                "max_rot_rate": metrics.max_rot_rate,
                "final_fidelity": metrics.final_fidelity,
                "total_drift": metrics.total_drift,
            },
        }
