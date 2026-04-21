"""Experiment configuration models."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class AgentType(str, Enum):
    """Types of agents used in context propagation experiments."""

    CODING = "coding"
    GENERAL_TASK = "general_task"
    SELF_REDESIGNING = "self_redesigning"


class MitigationType(str, Enum):
    """Context rot mitigation strategies."""

    NONE = "none"
    CONTEXT_ANCHORING = "context_anchoring"
    STRUCTURED_STORE = "structured_store"
    CHECKSUMMING = "checksumming"
    CIRCUIT_BREAKER = "circuit_breaker"


class FeedbackMode(str, Enum):
    """Feedback channel bandwidth for inter-generational transfer."""

    SCORE_ONLY = "score_only"  # Low bandwidth: aggregate scores only
    RICH = "rich"  # High bandwidth: per-task errors, traces, cumulative memory


class LLMConfig(BaseModel):
    """Configuration for the LLM backend."""

    provider: str = "ollama"
    base_url: str = "http://localhost:11434/v1"
    model: str = "qwen2.5-coder:14b"
    temperature: float = 0.7
    max_tokens: int = 4096
    api_key: str = "ollama"  # Ollama doesn't need a real key but the client requires one


class BenchmarkConfig(BaseModel):
    """Configuration for benchmark evaluation."""

    benchmark_dir: Path = Path("benchmarks")
    coding_tasks: list[str] = Field(default_factory=lambda: ["humaneval_subset", "custom"])
    general_tasks: list[str] = Field(default_factory=lambda: ["reasoning", "instruction_following"])
    prompt_tasks: list[str] = Field(default_factory=lambda: ["code_generation", "analysis"])
    eval_timeout_seconds: int = 30
    task_sample_size: int | None = None  # If set, randomly sample N tasks per run


class MitigationConfig(BaseModel):
    """Configuration for context rot mitigations."""

    strategy: MitigationType = MitigationType.NONE

    # Context anchoring params
    anchor_interval: int = 5  # Evaluate against C_0 every N generations
    fidelity_threshold: float = 0.5  # F_r threshold for regeneration

    # Structured store params
    store_path: Path = Path("results/context_store")

    # Checksumming params
    num_invariants: int = 5  # Number of semantic invariants to generate

    # Circuit breaker params
    rot_rate_threshold: float = 0.1  # Max acceptable rot rate rho
    lookback_window: int = 3  # Generations to average rot rate over


class ExperimentConfig(BaseModel):
    """Top-level experiment configuration."""

    # Experiment identity
    name: str = "baseline"
    description: str = ""
    seed: int = 42

    # Agent configuration
    agent_type: AgentType = AgentType.CODING
    num_generations: int = 20
    spawning_prompt: str = ""  # Initial P_0 (loaded from file if empty)
    spawning_prompt_file: Path | None = None

    # Feedback configuration
    feedback_mode: FeedbackMode = FeedbackMode.SCORE_ONLY

    # LLM configuration
    llm: LLMConfig = Field(default_factory=LLMConfig)

    # Benchmark configuration
    benchmarks: BenchmarkConfig = Field(default_factory=BenchmarkConfig)

    # Mitigation configuration
    mitigation: MitigationConfig = Field(default_factory=MitigationConfig)

    # Run configuration
    num_runs: int = 5  # Independent runs for statistical significance
    output_dir: Path = Path("results")
    log_level: str = "INFO"

    # Embedding model for semantic drift measurement
    embedding_model: str = "all-MiniLM-L6-v2"

    # Archival timestamp — set at experiment start, included in output path
    run_timestamp: str = ""

    def initialize_timestamp(self) -> str:
        """Set the timestamp for this experiment execution. Call once at start."""
        self.run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.run_timestamp

    def get_experiment_dir(self) -> Path:
        """Get the timestamped experiment directory."""
        if not self.run_timestamp:
            self.initialize_timestamp()
        return self.output_dir / self.name / self.run_timestamp

    def get_run_dir(self, run_id: int) -> Path:
        """Get output directory for a specific run."""
        return self.get_experiment_dir() / f"run_{run_id:03d}"

    def save_snapshot(self) -> None:
        """Save a frozen copy of this config to the experiment directory."""
        experiment_dir = self.get_experiment_dir()
        experiment_dir.mkdir(parents=True, exist_ok=True)
        self.to_yaml(experiment_dir / "config_snapshot.yaml")

    @classmethod
    def from_yaml(cls, path: Path) -> ExperimentConfig:
        """Load configuration from YAML file."""
        import yaml

        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def to_yaml(self, path: Path) -> None:
        """Save configuration to YAML file."""
        import yaml

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            yaml.dump(self.model_dump(mode="json"), f, default_flow_style=False, sort_keys=False)
