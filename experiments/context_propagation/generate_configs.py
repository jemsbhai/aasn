"""Generate experiment configs for all model x agent type x mitigation combinations.

Creates YAML config files for the full experiment matrix and a run script
that executes them sequentially with checkpointing.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness.config import AgentType, ExperimentConfig, LLMConfig, MitigationConfig, MitigationType

# --- Model definitions ---
MODELS = {
    # Ollama models
    "qwen2.5-coder-7b": LLMConfig(
        provider="ollama",
        base_url="http://localhost:11434/v1",
        model="qwen2.5-coder:7b",
        api_key="ollama",
    ),
    # llama.cpp models (via OpenAI-compatible server)
    # Default llama.cpp server port: 8080
    "bonsai-1.7b": LLMConfig(
        provider="llamacpp",
        base_url="http://localhost:8080/v1",
        model="Bonsai-1.7B",
        api_key="not-needed",
    ),
    "bonsai-4b": LLMConfig(
        provider="llamacpp",
        base_url="http://localhost:8080/v1",
        model="Bonsai-4B",
        api_key="not-needed",
    ),
    "bonsai-8b": LLMConfig(
        provider="llamacpp",
        base_url="http://localhost:8080/v1",
        model="Bonsai-8B",
        api_key="not-needed",
    ),
    "llama-3.2-3b": LLMConfig(
        provider="llamacpp",
        base_url="http://localhost:8080/v1",
        model="Llama-3.2-3B-Instruct-Q4_K_M",
        api_key="not-needed",
    ),
    "phi-3.5-mini": LLMConfig(
        provider="llamacpp",
        base_url="http://localhost:8080/v1",
        model="Phi-3.5-mini-instruct-Q4_K_M",
        api_key="not-needed",
    ),
    "qwen3-8b": LLMConfig(
        provider="llamacpp",
        base_url="http://localhost:8080/v1",
        model="Qwen3-8B-Q4_K_M",
        api_key="not-needed",
    ),
}

AGENT_TYPES = [AgentType.CODING, AgentType.GENERAL_TASK, AgentType.SELF_REDESIGNING]

MITIGATIONS = {
    "none": MitigationConfig(strategy=MitigationType.NONE),
    "anchoring": MitigationConfig(
        strategy=MitigationType.CONTEXT_ANCHORING,
        anchor_interval=5,
        fidelity_threshold=0.5,
    ),
    "store": MitigationConfig(strategy=MitigationType.STRUCTURED_STORE),
    "checksum": MitigationConfig(strategy=MitigationType.CHECKSUMMING, num_invariants=5),
    "breaker": MitigationConfig(
        strategy=MitigationType.CIRCUIT_BREAKER,
        rot_rate_threshold=0.1,
        lookback_window=3,
    ),
}

GGUF_PATHS = {
    "bonsai-1.7b": r"E:\data\code\claudecode\epistemic-edge\models\bonsai-1.7b\Bonsai-1.7B.gguf",
    "bonsai-4b": r"E:\data\code\claudecode\epistemic-edge\models\bonsai-4b\Bonsai-4B.gguf",
    "bonsai-8b": r"E:\data\code\claudecode\epistemic-edge\models\bonsai-8b\Bonsai-8B.gguf",
    "llama-3.2-3b": r"E:\data\code\claudecode\epistemic-edge\models\llama-3.2-3b\Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    "phi-3.5-mini": r"E:\data\code\claudecode\epistemic-edge\models\phi-3.5-mini\Phi-3.5-mini-instruct-Q4_K_M.gguf",
    "qwen3-8b": r"E:\data\code\claudecode\epistemic-edge\models\qwen3-8b\Qwen3-8B-Q4_K_M.gguf",
}


def generate_configs(output_dir: Path) -> list[Path]:
    """Generate all experiment config files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    configs = []

    for model_name, llm_config in MODELS.items():
        for agent_type in AGENT_TYPES:
            for mit_name, mit_config in MITIGATIONS.items():
                name = f"{model_name}_{agent_type.value}_{mit_name}"

                config = ExperimentConfig(
                    name=name,
                    description=f"Model={model_name}, Agent={agent_type.value}, Mitigation={mit_name}",
                    seed=42,
                    agent_type=agent_type,
                    num_generations=20,
                    num_runs=5,
                    llm=llm_config,
                    mitigation=mit_config,
                    output_dir=Path("results"),
                    log_level="INFO",
                    embedding_model="all-MiniLM-L6-v2",
                )

                config_path = output_dir / f"{name}.yaml"
                config.to_yaml(config_path)
                configs.append(config_path)

    return configs


def generate_run_script(configs: list[Path], output_path: Path) -> None:
    """Generate a PowerShell script to run all experiments with checkpointing."""
    lines = [
        "# Auto-generated experiment runner",
        "# Runs all experiment configurations with checkpointing",
        f"# Total configurations: {len(configs)}",
        "",
        '$ErrorActionPreference = "Continue"',
        "$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path",
        "$checkpointFile = Join-Path $scriptDir 'results\\.checkpoint'",
        "",
        "# Load checkpoint (list of completed experiment names)",
        "$completed = @()",
        "if (Test-Path $checkpointFile) {",
        "    $completed = Get-Content $checkpointFile",
        '    Write-Host "Resuming from checkpoint. $($completed.Count) experiments already completed."',
        "}",
        "",
        f"$total = {len(configs)}",
        "$current = 0",
        "",
    ]

    # Group configs by model for llama.cpp server management
    ollama_configs = [c for c in configs if "qwen2.5-coder" in c.stem]
    llamacpp_configs_by_model: dict[str, list[Path]] = {}
    for c in configs:
        for model_name in GGUF_PATHS:
            if model_name in c.stem:
                llamacpp_configs_by_model.setdefault(model_name, []).append(c)
                break

    # Ollama experiments first
    lines.append("# --- Ollama experiments ---")
    lines.append('Write-Host "Running Ollama experiments..."')
    for config_path in ollama_configs:
        name = config_path.stem
        lines.append(f"$current++")
        lines.append(f'if ($completed -notcontains "{name}") {{')
        lines.append(f'    Write-Host "[$current/$total] Running: {name}"')
        lines.append(f'    python run_experiment.py --config configs/generated/{config_path.name}')
        lines.append(f'    if ($LASTEXITCODE -eq 0) {{')
        lines.append(f'        Add-Content $checkpointFile "{name}"')
        lines.append(f'        Write-Host "  Completed: {name}"')
        lines.append(f'    }} else {{')
        lines.append(f'        Write-Host "  FAILED: {name}" -ForegroundColor Red')
        lines.append(f'    }}')
        lines.append(f'}} else {{')
        lines.append(f'    Write-Host "[$current/$total] Skipping (already done): {name}"')
        lines.append(f'}}')
        lines.append("")

    # llama.cpp experiments grouped by model
    lines.append("# --- llama.cpp experiments ---")
    lines.append("# NOTE: You must start the llama.cpp server manually for each model.")
    lines.append("# Example: .\\llama-server.exe -m <model.gguf> --port 8080 -ngl 99")
    lines.append("")

    for model_name, model_configs in llamacpp_configs_by_model.items():
        gguf_path = GGUF_PATHS[model_name]
        lines.append(f"# --- Model: {model_name} ---")
        lines.append(f'Write-Host ""')
        lines.append(f'Write-Host "=== Load model: {model_name} ==="')
        lines.append(f'Write-Host "Start llama.cpp server with:"')
        lines.append(f'Write-Host "  .\\llama-server.exe -m {gguf_path} --port 8080 -ngl 99"')
        lines.append(f'Write-Host "Press Enter when server is ready..."')
        lines.append(f'Read-Host')
        lines.append("")

        for config_path in model_configs:
            name = config_path.stem
            lines.append(f"$current++")
            lines.append(f'if ($completed -notcontains "{name}") {{')
            lines.append(f'    Write-Host "[$current/$total] Running: {name}"')
            lines.append(f'    python run_experiment.py --config configs/generated/{config_path.name}')
            lines.append(f'    if ($LASTEXITCODE -eq 0) {{')
            lines.append(f'        Add-Content $checkpointFile "{name}"')
            lines.append(f'        Write-Host "  Completed: {name}"')
            lines.append(f'    }} else {{')
            lines.append(f'        Write-Host "  FAILED: {name}" -ForegroundColor Red')
            lines.append(f'    }}')
            lines.append(f'}} else {{')
            lines.append(f'    Write-Host "[$current/$total] Skipping (already done): {name}"')
            lines.append(f'}}')
            lines.append("")

    lines.append('Write-Host ""')
    lines.append('Write-Host "All experiments complete."')
    lines.append('Write-Host "Results in: results/"')

    output_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    config_dir = Path(__file__).resolve().parent / "configs" / "generated"
    configs = generate_configs(config_dir)
    print(f"Generated {len(configs)} config files in {config_dir}")

    script_path = Path(__file__).resolve().parent / "run_all_experiments.ps1"
    generate_run_script(configs, script_path)
    print(f"Generated run script: {script_path}")

    # Summary
    print(f"\nExperiment matrix:")
    print(f"  Models:      {len(MODELS)}")
    print(f"  Agent types: {len(AGENT_TYPES)}")
    print(f"  Mitigations: {len(MITIGATIONS)}")
    print(f"  Total:       {len(configs)} configurations")
    print(f"  Runs/config: 5")
    print(f"  Generations: 20")
    print(f"\nNext steps:")
    print(f"  1. Download benchmarks: python download_benchmarks_cli.py --tier 1")
    print(f"  2. Run experiments:     .\\run_all_experiments.ps1")


if __name__ == "__main__":
    main()
