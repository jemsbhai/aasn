# Context Propagation Experiments

Experiments for "Context Propagation and Context Rot in Multi-Generation Agent Systems" (NeurIPS 2026).

## Overview

These experiments measure how context degrades across generations of self-redesigning agents, and evaluate four mitigation strategies.

## Structure

```
context_propagation/
├── harness/        # Agent spawning harness and evaluation
├── benchmarks/     # Coding benchmark task definitions
├── results/        # Experiment outputs (gitignored)
└── notebooks/      # Analysis and visualization notebooks
```

## Running Experiments

```powershell
# Set up environment
cd experiments/context_propagation
copy ..\..\..\.env.example .env
# Edit .env with your API keys

# Run baseline (no mitigations)
python harness/run_experiment.py --config configs/baseline.yaml

# Run with specific mitigation
python harness/run_experiment.py --config configs/context_anchoring.yaml
```

## Reproducibility

All experiments use:
- Pinned random seed: 42 (configurable)
- Pinned dependency versions (see requirements.txt)
- Logged hyperparameters and environment details
- Deterministic evaluation harness
