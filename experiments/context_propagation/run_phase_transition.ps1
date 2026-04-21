# Phase Transition Experiment Runner
# Runs both conditions: rich feedback then score-only control
# Safe to Ctrl+C at any time — resume with the same command.
#
# Usage:
#   .\run_phase_transition.ps1           # Start fresh
#   .\run_phase_transition.ps1 -Resume   # Resume from last checkpoint
#
# Estimated runtime: ~15 hours on RTX 4090 with Qwen2.5-Coder-7B

param(
    [switch]$Resume
)

$ErrorActionPreference = "Continue"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$resumeFlag = if ($Resume) { "--resume" } else { "" }
$startTime = Get-Date

Write-Host "============================================================"
Write-Host "Phase Transition Experiment"
Write-Host "Model: Qwen2.5-Coder-7B via Ollama"
Write-Host "Temperature: 0.3"
Write-Host "Generations: 50, Runs: 10, Tasks: 50"
Write-Host "Conditions: rich feedback + score-only control"
Write-Host "Resume mode: $Resume"
Write-Host "Started: $startTime"
Write-Host "============================================================"
Write-Host ""

# --- Condition 1: Rich feedback ---
Write-Host "=== CONDITION 1: Rich Feedback ===" -ForegroundColor Cyan
Write-Host "Estimated time: ~7.7 hours"
Write-Host "Start: $(Get-Date)"
Write-Host ""

if ($Resume) {
    python run_experiment.py --config configs/phase_transition_rich.yaml --resume
} else {
    python run_experiment.py --config configs/phase_transition_rich.yaml
}

$richEnd = Get-Date
$richDuration = $richEnd - $startTime
Write-Host ""
Write-Host "Rich feedback complete. Duration: $($richDuration.ToString('hh\:mm\:ss'))" -ForegroundColor Green
Write-Host ""

# --- Condition 2: Score-only control ---
Write-Host "=== CONDITION 2: Score-Only Control ===" -ForegroundColor Cyan
Write-Host "Estimated time: ~7.7 hours"
Write-Host "Start: $(Get-Date)"
Write-Host ""

if ($Resume) {
    python run_experiment.py --config configs/phase_transition_score_only.yaml --resume
} else {
    python run_experiment.py --config configs/phase_transition_score_only.yaml
}

$totalEnd = Get-Date
$totalDuration = $totalEnd - $startTime

Write-Host ""
Write-Host "============================================================"
Write-Host "EXPERIMENT COMPLETE" -ForegroundColor Green
Write-Host "Total duration: $($totalDuration.ToString('hh\:mm\:ss'))"
Write-Host "Results in:"
Write-Host "  results\qwen7b_rich_50gen\"
Write-Host "  results\qwen7b_score_only_50gen\"
Write-Host "============================================================"
