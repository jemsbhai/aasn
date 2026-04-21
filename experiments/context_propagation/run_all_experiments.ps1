# Auto-generated experiment runner
# Runs all experiment configurations with checkpointing
# Total configurations: 105

$ErrorActionPreference = "Continue"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$checkpointFile = Join-Path $scriptDir 'results\.checkpoint'

# Load checkpoint (list of completed experiment names)
$completed = @()
if (Test-Path $checkpointFile) {
    $completed = Get-Content $checkpointFile
    Write-Host "Resuming from checkpoint. $($completed.Count) experiments already completed."
}

$total = 105
$current = 0

# --- Ollama experiments ---
Write-Host "Running Ollama experiments..."
$current++
if ($completed -notcontains "qwen2.5-coder-7b_coding_none") {
    Write-Host "[$current/$total] Running: qwen2.5-coder-7b_coding_none"
    python run_experiment.py --config configs/generated/qwen2.5-coder-7b_coding_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen2.5-coder-7b_coding_none"
        Write-Host "  Completed: qwen2.5-coder-7b_coding_none"
    } else {
        Write-Host "  FAILED: qwen2.5-coder-7b_coding_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen2.5-coder-7b_coding_none"
}

$current++
if ($completed -notcontains "qwen2.5-coder-7b_coding_anchoring") {
    Write-Host "[$current/$total] Running: qwen2.5-coder-7b_coding_anchoring"
    python run_experiment.py --config configs/generated/qwen2.5-coder-7b_coding_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen2.5-coder-7b_coding_anchoring"
        Write-Host "  Completed: qwen2.5-coder-7b_coding_anchoring"
    } else {
        Write-Host "  FAILED: qwen2.5-coder-7b_coding_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen2.5-coder-7b_coding_anchoring"
}

$current++
if ($completed -notcontains "qwen2.5-coder-7b_coding_store") {
    Write-Host "[$current/$total] Running: qwen2.5-coder-7b_coding_store"
    python run_experiment.py --config configs/generated/qwen2.5-coder-7b_coding_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen2.5-coder-7b_coding_store"
        Write-Host "  Completed: qwen2.5-coder-7b_coding_store"
    } else {
        Write-Host "  FAILED: qwen2.5-coder-7b_coding_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen2.5-coder-7b_coding_store"
}

$current++
if ($completed -notcontains "qwen2.5-coder-7b_coding_checksum") {
    Write-Host "[$current/$total] Running: qwen2.5-coder-7b_coding_checksum"
    python run_experiment.py --config configs/generated/qwen2.5-coder-7b_coding_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen2.5-coder-7b_coding_checksum"
        Write-Host "  Completed: qwen2.5-coder-7b_coding_checksum"
    } else {
        Write-Host "  FAILED: qwen2.5-coder-7b_coding_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen2.5-coder-7b_coding_checksum"
}

$current++
if ($completed -notcontains "qwen2.5-coder-7b_coding_breaker") {
    Write-Host "[$current/$total] Running: qwen2.5-coder-7b_coding_breaker"
    python run_experiment.py --config configs/generated/qwen2.5-coder-7b_coding_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen2.5-coder-7b_coding_breaker"
        Write-Host "  Completed: qwen2.5-coder-7b_coding_breaker"
    } else {
        Write-Host "  FAILED: qwen2.5-coder-7b_coding_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen2.5-coder-7b_coding_breaker"
}

$current++
if ($completed -notcontains "qwen2.5-coder-7b_general_task_none") {
    Write-Host "[$current/$total] Running: qwen2.5-coder-7b_general_task_none"
    python run_experiment.py --config configs/generated/qwen2.5-coder-7b_general_task_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen2.5-coder-7b_general_task_none"
        Write-Host "  Completed: qwen2.5-coder-7b_general_task_none"
    } else {
        Write-Host "  FAILED: qwen2.5-coder-7b_general_task_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen2.5-coder-7b_general_task_none"
}

$current++
if ($completed -notcontains "qwen2.5-coder-7b_general_task_anchoring") {
    Write-Host "[$current/$total] Running: qwen2.5-coder-7b_general_task_anchoring"
    python run_experiment.py --config configs/generated/qwen2.5-coder-7b_general_task_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen2.5-coder-7b_general_task_anchoring"
        Write-Host "  Completed: qwen2.5-coder-7b_general_task_anchoring"
    } else {
        Write-Host "  FAILED: qwen2.5-coder-7b_general_task_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen2.5-coder-7b_general_task_anchoring"
}

$current++
if ($completed -notcontains "qwen2.5-coder-7b_general_task_store") {
    Write-Host "[$current/$total] Running: qwen2.5-coder-7b_general_task_store"
    python run_experiment.py --config configs/generated/qwen2.5-coder-7b_general_task_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen2.5-coder-7b_general_task_store"
        Write-Host "  Completed: qwen2.5-coder-7b_general_task_store"
    } else {
        Write-Host "  FAILED: qwen2.5-coder-7b_general_task_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen2.5-coder-7b_general_task_store"
}

$current++
if ($completed -notcontains "qwen2.5-coder-7b_general_task_checksum") {
    Write-Host "[$current/$total] Running: qwen2.5-coder-7b_general_task_checksum"
    python run_experiment.py --config configs/generated/qwen2.5-coder-7b_general_task_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen2.5-coder-7b_general_task_checksum"
        Write-Host "  Completed: qwen2.5-coder-7b_general_task_checksum"
    } else {
        Write-Host "  FAILED: qwen2.5-coder-7b_general_task_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen2.5-coder-7b_general_task_checksum"
}

$current++
if ($completed -notcontains "qwen2.5-coder-7b_general_task_breaker") {
    Write-Host "[$current/$total] Running: qwen2.5-coder-7b_general_task_breaker"
    python run_experiment.py --config configs/generated/qwen2.5-coder-7b_general_task_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen2.5-coder-7b_general_task_breaker"
        Write-Host "  Completed: qwen2.5-coder-7b_general_task_breaker"
    } else {
        Write-Host "  FAILED: qwen2.5-coder-7b_general_task_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen2.5-coder-7b_general_task_breaker"
}

$current++
if ($completed -notcontains "qwen2.5-coder-7b_self_redesigning_none") {
    Write-Host "[$current/$total] Running: qwen2.5-coder-7b_self_redesigning_none"
    python run_experiment.py --config configs/generated/qwen2.5-coder-7b_self_redesigning_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen2.5-coder-7b_self_redesigning_none"
        Write-Host "  Completed: qwen2.5-coder-7b_self_redesigning_none"
    } else {
        Write-Host "  FAILED: qwen2.5-coder-7b_self_redesigning_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen2.5-coder-7b_self_redesigning_none"
}

$current++
if ($completed -notcontains "qwen2.5-coder-7b_self_redesigning_anchoring") {
    Write-Host "[$current/$total] Running: qwen2.5-coder-7b_self_redesigning_anchoring"
    python run_experiment.py --config configs/generated/qwen2.5-coder-7b_self_redesigning_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen2.5-coder-7b_self_redesigning_anchoring"
        Write-Host "  Completed: qwen2.5-coder-7b_self_redesigning_anchoring"
    } else {
        Write-Host "  FAILED: qwen2.5-coder-7b_self_redesigning_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen2.5-coder-7b_self_redesigning_anchoring"
}

$current++
if ($completed -notcontains "qwen2.5-coder-7b_self_redesigning_store") {
    Write-Host "[$current/$total] Running: qwen2.5-coder-7b_self_redesigning_store"
    python run_experiment.py --config configs/generated/qwen2.5-coder-7b_self_redesigning_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen2.5-coder-7b_self_redesigning_store"
        Write-Host "  Completed: qwen2.5-coder-7b_self_redesigning_store"
    } else {
        Write-Host "  FAILED: qwen2.5-coder-7b_self_redesigning_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen2.5-coder-7b_self_redesigning_store"
}

$current++
if ($completed -notcontains "qwen2.5-coder-7b_self_redesigning_checksum") {
    Write-Host "[$current/$total] Running: qwen2.5-coder-7b_self_redesigning_checksum"
    python run_experiment.py --config configs/generated/qwen2.5-coder-7b_self_redesigning_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen2.5-coder-7b_self_redesigning_checksum"
        Write-Host "  Completed: qwen2.5-coder-7b_self_redesigning_checksum"
    } else {
        Write-Host "  FAILED: qwen2.5-coder-7b_self_redesigning_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen2.5-coder-7b_self_redesigning_checksum"
}

$current++
if ($completed -notcontains "qwen2.5-coder-7b_self_redesigning_breaker") {
    Write-Host "[$current/$total] Running: qwen2.5-coder-7b_self_redesigning_breaker"
    python run_experiment.py --config configs/generated/qwen2.5-coder-7b_self_redesigning_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen2.5-coder-7b_self_redesigning_breaker"
        Write-Host "  Completed: qwen2.5-coder-7b_self_redesigning_breaker"
    } else {
        Write-Host "  FAILED: qwen2.5-coder-7b_self_redesigning_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen2.5-coder-7b_self_redesigning_breaker"
}

# --- llama.cpp experiments ---
# NOTE: You must start the llama.cpp server manually for each model.
# Example: .\llama-server.exe -m <model.gguf> --port 8080 -ngl 99

# --- Model: bonsai-1.7b ---
Write-Host ""
Write-Host "=== Load model: bonsai-1.7b ==="
Write-Host "Start llama.cpp server with:"
Write-Host "  .\llama-server.exe -m E:\data\code\claudecode\epistemic-edge\models\bonsai-1.7b\Bonsai-1.7B.gguf --port 8080 -ngl 99"
Write-Host "Press Enter when server is ready..."
Read-Host

$current++
if ($completed -notcontains "bonsai-1.7b_coding_none") {
    Write-Host "[$current/$total] Running: bonsai-1.7b_coding_none"
    python run_experiment.py --config configs/generated/bonsai-1.7b_coding_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-1.7b_coding_none"
        Write-Host "  Completed: bonsai-1.7b_coding_none"
    } else {
        Write-Host "  FAILED: bonsai-1.7b_coding_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-1.7b_coding_none"
}

$current++
if ($completed -notcontains "bonsai-1.7b_coding_anchoring") {
    Write-Host "[$current/$total] Running: bonsai-1.7b_coding_anchoring"
    python run_experiment.py --config configs/generated/bonsai-1.7b_coding_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-1.7b_coding_anchoring"
        Write-Host "  Completed: bonsai-1.7b_coding_anchoring"
    } else {
        Write-Host "  FAILED: bonsai-1.7b_coding_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-1.7b_coding_anchoring"
}

$current++
if ($completed -notcontains "bonsai-1.7b_coding_store") {
    Write-Host "[$current/$total] Running: bonsai-1.7b_coding_store"
    python run_experiment.py --config configs/generated/bonsai-1.7b_coding_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-1.7b_coding_store"
        Write-Host "  Completed: bonsai-1.7b_coding_store"
    } else {
        Write-Host "  FAILED: bonsai-1.7b_coding_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-1.7b_coding_store"
}

$current++
if ($completed -notcontains "bonsai-1.7b_coding_checksum") {
    Write-Host "[$current/$total] Running: bonsai-1.7b_coding_checksum"
    python run_experiment.py --config configs/generated/bonsai-1.7b_coding_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-1.7b_coding_checksum"
        Write-Host "  Completed: bonsai-1.7b_coding_checksum"
    } else {
        Write-Host "  FAILED: bonsai-1.7b_coding_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-1.7b_coding_checksum"
}

$current++
if ($completed -notcontains "bonsai-1.7b_coding_breaker") {
    Write-Host "[$current/$total] Running: bonsai-1.7b_coding_breaker"
    python run_experiment.py --config configs/generated/bonsai-1.7b_coding_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-1.7b_coding_breaker"
        Write-Host "  Completed: bonsai-1.7b_coding_breaker"
    } else {
        Write-Host "  FAILED: bonsai-1.7b_coding_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-1.7b_coding_breaker"
}

$current++
if ($completed -notcontains "bonsai-1.7b_general_task_none") {
    Write-Host "[$current/$total] Running: bonsai-1.7b_general_task_none"
    python run_experiment.py --config configs/generated/bonsai-1.7b_general_task_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-1.7b_general_task_none"
        Write-Host "  Completed: bonsai-1.7b_general_task_none"
    } else {
        Write-Host "  FAILED: bonsai-1.7b_general_task_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-1.7b_general_task_none"
}

$current++
if ($completed -notcontains "bonsai-1.7b_general_task_anchoring") {
    Write-Host "[$current/$total] Running: bonsai-1.7b_general_task_anchoring"
    python run_experiment.py --config configs/generated/bonsai-1.7b_general_task_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-1.7b_general_task_anchoring"
        Write-Host "  Completed: bonsai-1.7b_general_task_anchoring"
    } else {
        Write-Host "  FAILED: bonsai-1.7b_general_task_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-1.7b_general_task_anchoring"
}

$current++
if ($completed -notcontains "bonsai-1.7b_general_task_store") {
    Write-Host "[$current/$total] Running: bonsai-1.7b_general_task_store"
    python run_experiment.py --config configs/generated/bonsai-1.7b_general_task_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-1.7b_general_task_store"
        Write-Host "  Completed: bonsai-1.7b_general_task_store"
    } else {
        Write-Host "  FAILED: bonsai-1.7b_general_task_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-1.7b_general_task_store"
}

$current++
if ($completed -notcontains "bonsai-1.7b_general_task_checksum") {
    Write-Host "[$current/$total] Running: bonsai-1.7b_general_task_checksum"
    python run_experiment.py --config configs/generated/bonsai-1.7b_general_task_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-1.7b_general_task_checksum"
        Write-Host "  Completed: bonsai-1.7b_general_task_checksum"
    } else {
        Write-Host "  FAILED: bonsai-1.7b_general_task_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-1.7b_general_task_checksum"
}

$current++
if ($completed -notcontains "bonsai-1.7b_general_task_breaker") {
    Write-Host "[$current/$total] Running: bonsai-1.7b_general_task_breaker"
    python run_experiment.py --config configs/generated/bonsai-1.7b_general_task_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-1.7b_general_task_breaker"
        Write-Host "  Completed: bonsai-1.7b_general_task_breaker"
    } else {
        Write-Host "  FAILED: bonsai-1.7b_general_task_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-1.7b_general_task_breaker"
}

$current++
if ($completed -notcontains "bonsai-1.7b_self_redesigning_none") {
    Write-Host "[$current/$total] Running: bonsai-1.7b_self_redesigning_none"
    python run_experiment.py --config configs/generated/bonsai-1.7b_self_redesigning_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-1.7b_self_redesigning_none"
        Write-Host "  Completed: bonsai-1.7b_self_redesigning_none"
    } else {
        Write-Host "  FAILED: bonsai-1.7b_self_redesigning_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-1.7b_self_redesigning_none"
}

$current++
if ($completed -notcontains "bonsai-1.7b_self_redesigning_anchoring") {
    Write-Host "[$current/$total] Running: bonsai-1.7b_self_redesigning_anchoring"
    python run_experiment.py --config configs/generated/bonsai-1.7b_self_redesigning_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-1.7b_self_redesigning_anchoring"
        Write-Host "  Completed: bonsai-1.7b_self_redesigning_anchoring"
    } else {
        Write-Host "  FAILED: bonsai-1.7b_self_redesigning_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-1.7b_self_redesigning_anchoring"
}

$current++
if ($completed -notcontains "bonsai-1.7b_self_redesigning_store") {
    Write-Host "[$current/$total] Running: bonsai-1.7b_self_redesigning_store"
    python run_experiment.py --config configs/generated/bonsai-1.7b_self_redesigning_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-1.7b_self_redesigning_store"
        Write-Host "  Completed: bonsai-1.7b_self_redesigning_store"
    } else {
        Write-Host "  FAILED: bonsai-1.7b_self_redesigning_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-1.7b_self_redesigning_store"
}

$current++
if ($completed -notcontains "bonsai-1.7b_self_redesigning_checksum") {
    Write-Host "[$current/$total] Running: bonsai-1.7b_self_redesigning_checksum"
    python run_experiment.py --config configs/generated/bonsai-1.7b_self_redesigning_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-1.7b_self_redesigning_checksum"
        Write-Host "  Completed: bonsai-1.7b_self_redesigning_checksum"
    } else {
        Write-Host "  FAILED: bonsai-1.7b_self_redesigning_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-1.7b_self_redesigning_checksum"
}

$current++
if ($completed -notcontains "bonsai-1.7b_self_redesigning_breaker") {
    Write-Host "[$current/$total] Running: bonsai-1.7b_self_redesigning_breaker"
    python run_experiment.py --config configs/generated/bonsai-1.7b_self_redesigning_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-1.7b_self_redesigning_breaker"
        Write-Host "  Completed: bonsai-1.7b_self_redesigning_breaker"
    } else {
        Write-Host "  FAILED: bonsai-1.7b_self_redesigning_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-1.7b_self_redesigning_breaker"
}

# --- Model: bonsai-4b ---
Write-Host ""
Write-Host "=== Load model: bonsai-4b ==="
Write-Host "Start llama.cpp server with:"
Write-Host "  .\llama-server.exe -m E:\data\code\claudecode\epistemic-edge\models\bonsai-4b\Bonsai-4B.gguf --port 8080 -ngl 99"
Write-Host "Press Enter when server is ready..."
Read-Host

$current++
if ($completed -notcontains "bonsai-4b_coding_none") {
    Write-Host "[$current/$total] Running: bonsai-4b_coding_none"
    python run_experiment.py --config configs/generated/bonsai-4b_coding_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-4b_coding_none"
        Write-Host "  Completed: bonsai-4b_coding_none"
    } else {
        Write-Host "  FAILED: bonsai-4b_coding_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-4b_coding_none"
}

$current++
if ($completed -notcontains "bonsai-4b_coding_anchoring") {
    Write-Host "[$current/$total] Running: bonsai-4b_coding_anchoring"
    python run_experiment.py --config configs/generated/bonsai-4b_coding_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-4b_coding_anchoring"
        Write-Host "  Completed: bonsai-4b_coding_anchoring"
    } else {
        Write-Host "  FAILED: bonsai-4b_coding_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-4b_coding_anchoring"
}

$current++
if ($completed -notcontains "bonsai-4b_coding_store") {
    Write-Host "[$current/$total] Running: bonsai-4b_coding_store"
    python run_experiment.py --config configs/generated/bonsai-4b_coding_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-4b_coding_store"
        Write-Host "  Completed: bonsai-4b_coding_store"
    } else {
        Write-Host "  FAILED: bonsai-4b_coding_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-4b_coding_store"
}

$current++
if ($completed -notcontains "bonsai-4b_coding_checksum") {
    Write-Host "[$current/$total] Running: bonsai-4b_coding_checksum"
    python run_experiment.py --config configs/generated/bonsai-4b_coding_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-4b_coding_checksum"
        Write-Host "  Completed: bonsai-4b_coding_checksum"
    } else {
        Write-Host "  FAILED: bonsai-4b_coding_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-4b_coding_checksum"
}

$current++
if ($completed -notcontains "bonsai-4b_coding_breaker") {
    Write-Host "[$current/$total] Running: bonsai-4b_coding_breaker"
    python run_experiment.py --config configs/generated/bonsai-4b_coding_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-4b_coding_breaker"
        Write-Host "  Completed: bonsai-4b_coding_breaker"
    } else {
        Write-Host "  FAILED: bonsai-4b_coding_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-4b_coding_breaker"
}

$current++
if ($completed -notcontains "bonsai-4b_general_task_none") {
    Write-Host "[$current/$total] Running: bonsai-4b_general_task_none"
    python run_experiment.py --config configs/generated/bonsai-4b_general_task_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-4b_general_task_none"
        Write-Host "  Completed: bonsai-4b_general_task_none"
    } else {
        Write-Host "  FAILED: bonsai-4b_general_task_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-4b_general_task_none"
}

$current++
if ($completed -notcontains "bonsai-4b_general_task_anchoring") {
    Write-Host "[$current/$total] Running: bonsai-4b_general_task_anchoring"
    python run_experiment.py --config configs/generated/bonsai-4b_general_task_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-4b_general_task_anchoring"
        Write-Host "  Completed: bonsai-4b_general_task_anchoring"
    } else {
        Write-Host "  FAILED: bonsai-4b_general_task_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-4b_general_task_anchoring"
}

$current++
if ($completed -notcontains "bonsai-4b_general_task_store") {
    Write-Host "[$current/$total] Running: bonsai-4b_general_task_store"
    python run_experiment.py --config configs/generated/bonsai-4b_general_task_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-4b_general_task_store"
        Write-Host "  Completed: bonsai-4b_general_task_store"
    } else {
        Write-Host "  FAILED: bonsai-4b_general_task_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-4b_general_task_store"
}

$current++
if ($completed -notcontains "bonsai-4b_general_task_checksum") {
    Write-Host "[$current/$total] Running: bonsai-4b_general_task_checksum"
    python run_experiment.py --config configs/generated/bonsai-4b_general_task_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-4b_general_task_checksum"
        Write-Host "  Completed: bonsai-4b_general_task_checksum"
    } else {
        Write-Host "  FAILED: bonsai-4b_general_task_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-4b_general_task_checksum"
}

$current++
if ($completed -notcontains "bonsai-4b_general_task_breaker") {
    Write-Host "[$current/$total] Running: bonsai-4b_general_task_breaker"
    python run_experiment.py --config configs/generated/bonsai-4b_general_task_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-4b_general_task_breaker"
        Write-Host "  Completed: bonsai-4b_general_task_breaker"
    } else {
        Write-Host "  FAILED: bonsai-4b_general_task_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-4b_general_task_breaker"
}

$current++
if ($completed -notcontains "bonsai-4b_self_redesigning_none") {
    Write-Host "[$current/$total] Running: bonsai-4b_self_redesigning_none"
    python run_experiment.py --config configs/generated/bonsai-4b_self_redesigning_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-4b_self_redesigning_none"
        Write-Host "  Completed: bonsai-4b_self_redesigning_none"
    } else {
        Write-Host "  FAILED: bonsai-4b_self_redesigning_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-4b_self_redesigning_none"
}

$current++
if ($completed -notcontains "bonsai-4b_self_redesigning_anchoring") {
    Write-Host "[$current/$total] Running: bonsai-4b_self_redesigning_anchoring"
    python run_experiment.py --config configs/generated/bonsai-4b_self_redesigning_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-4b_self_redesigning_anchoring"
        Write-Host "  Completed: bonsai-4b_self_redesigning_anchoring"
    } else {
        Write-Host "  FAILED: bonsai-4b_self_redesigning_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-4b_self_redesigning_anchoring"
}

$current++
if ($completed -notcontains "bonsai-4b_self_redesigning_store") {
    Write-Host "[$current/$total] Running: bonsai-4b_self_redesigning_store"
    python run_experiment.py --config configs/generated/bonsai-4b_self_redesigning_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-4b_self_redesigning_store"
        Write-Host "  Completed: bonsai-4b_self_redesigning_store"
    } else {
        Write-Host "  FAILED: bonsai-4b_self_redesigning_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-4b_self_redesigning_store"
}

$current++
if ($completed -notcontains "bonsai-4b_self_redesigning_checksum") {
    Write-Host "[$current/$total] Running: bonsai-4b_self_redesigning_checksum"
    python run_experiment.py --config configs/generated/bonsai-4b_self_redesigning_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-4b_self_redesigning_checksum"
        Write-Host "  Completed: bonsai-4b_self_redesigning_checksum"
    } else {
        Write-Host "  FAILED: bonsai-4b_self_redesigning_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-4b_self_redesigning_checksum"
}

$current++
if ($completed -notcontains "bonsai-4b_self_redesigning_breaker") {
    Write-Host "[$current/$total] Running: bonsai-4b_self_redesigning_breaker"
    python run_experiment.py --config configs/generated/bonsai-4b_self_redesigning_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-4b_self_redesigning_breaker"
        Write-Host "  Completed: bonsai-4b_self_redesigning_breaker"
    } else {
        Write-Host "  FAILED: bonsai-4b_self_redesigning_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-4b_self_redesigning_breaker"
}

# --- Model: bonsai-8b ---
Write-Host ""
Write-Host "=== Load model: bonsai-8b ==="
Write-Host "Start llama.cpp server with:"
Write-Host "  .\llama-server.exe -m E:\data\code\claudecode\epistemic-edge\models\bonsai-8b\Bonsai-8B.gguf --port 8080 -ngl 99"
Write-Host "Press Enter when server is ready..."
Read-Host

$current++
if ($completed -notcontains "bonsai-8b_coding_none") {
    Write-Host "[$current/$total] Running: bonsai-8b_coding_none"
    python run_experiment.py --config configs/generated/bonsai-8b_coding_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-8b_coding_none"
        Write-Host "  Completed: bonsai-8b_coding_none"
    } else {
        Write-Host "  FAILED: bonsai-8b_coding_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-8b_coding_none"
}

$current++
if ($completed -notcontains "bonsai-8b_coding_anchoring") {
    Write-Host "[$current/$total] Running: bonsai-8b_coding_anchoring"
    python run_experiment.py --config configs/generated/bonsai-8b_coding_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-8b_coding_anchoring"
        Write-Host "  Completed: bonsai-8b_coding_anchoring"
    } else {
        Write-Host "  FAILED: bonsai-8b_coding_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-8b_coding_anchoring"
}

$current++
if ($completed -notcontains "bonsai-8b_coding_store") {
    Write-Host "[$current/$total] Running: bonsai-8b_coding_store"
    python run_experiment.py --config configs/generated/bonsai-8b_coding_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-8b_coding_store"
        Write-Host "  Completed: bonsai-8b_coding_store"
    } else {
        Write-Host "  FAILED: bonsai-8b_coding_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-8b_coding_store"
}

$current++
if ($completed -notcontains "bonsai-8b_coding_checksum") {
    Write-Host "[$current/$total] Running: bonsai-8b_coding_checksum"
    python run_experiment.py --config configs/generated/bonsai-8b_coding_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-8b_coding_checksum"
        Write-Host "  Completed: bonsai-8b_coding_checksum"
    } else {
        Write-Host "  FAILED: bonsai-8b_coding_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-8b_coding_checksum"
}

$current++
if ($completed -notcontains "bonsai-8b_coding_breaker") {
    Write-Host "[$current/$total] Running: bonsai-8b_coding_breaker"
    python run_experiment.py --config configs/generated/bonsai-8b_coding_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-8b_coding_breaker"
        Write-Host "  Completed: bonsai-8b_coding_breaker"
    } else {
        Write-Host "  FAILED: bonsai-8b_coding_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-8b_coding_breaker"
}

$current++
if ($completed -notcontains "bonsai-8b_general_task_none") {
    Write-Host "[$current/$total] Running: bonsai-8b_general_task_none"
    python run_experiment.py --config configs/generated/bonsai-8b_general_task_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-8b_general_task_none"
        Write-Host "  Completed: bonsai-8b_general_task_none"
    } else {
        Write-Host "  FAILED: bonsai-8b_general_task_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-8b_general_task_none"
}

$current++
if ($completed -notcontains "bonsai-8b_general_task_anchoring") {
    Write-Host "[$current/$total] Running: bonsai-8b_general_task_anchoring"
    python run_experiment.py --config configs/generated/bonsai-8b_general_task_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-8b_general_task_anchoring"
        Write-Host "  Completed: bonsai-8b_general_task_anchoring"
    } else {
        Write-Host "  FAILED: bonsai-8b_general_task_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-8b_general_task_anchoring"
}

$current++
if ($completed -notcontains "bonsai-8b_general_task_store") {
    Write-Host "[$current/$total] Running: bonsai-8b_general_task_store"
    python run_experiment.py --config configs/generated/bonsai-8b_general_task_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-8b_general_task_store"
        Write-Host "  Completed: bonsai-8b_general_task_store"
    } else {
        Write-Host "  FAILED: bonsai-8b_general_task_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-8b_general_task_store"
}

$current++
if ($completed -notcontains "bonsai-8b_general_task_checksum") {
    Write-Host "[$current/$total] Running: bonsai-8b_general_task_checksum"
    python run_experiment.py --config configs/generated/bonsai-8b_general_task_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-8b_general_task_checksum"
        Write-Host "  Completed: bonsai-8b_general_task_checksum"
    } else {
        Write-Host "  FAILED: bonsai-8b_general_task_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-8b_general_task_checksum"
}

$current++
if ($completed -notcontains "bonsai-8b_general_task_breaker") {
    Write-Host "[$current/$total] Running: bonsai-8b_general_task_breaker"
    python run_experiment.py --config configs/generated/bonsai-8b_general_task_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-8b_general_task_breaker"
        Write-Host "  Completed: bonsai-8b_general_task_breaker"
    } else {
        Write-Host "  FAILED: bonsai-8b_general_task_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-8b_general_task_breaker"
}

$current++
if ($completed -notcontains "bonsai-8b_self_redesigning_none") {
    Write-Host "[$current/$total] Running: bonsai-8b_self_redesigning_none"
    python run_experiment.py --config configs/generated/bonsai-8b_self_redesigning_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-8b_self_redesigning_none"
        Write-Host "  Completed: bonsai-8b_self_redesigning_none"
    } else {
        Write-Host "  FAILED: bonsai-8b_self_redesigning_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-8b_self_redesigning_none"
}

$current++
if ($completed -notcontains "bonsai-8b_self_redesigning_anchoring") {
    Write-Host "[$current/$total] Running: bonsai-8b_self_redesigning_anchoring"
    python run_experiment.py --config configs/generated/bonsai-8b_self_redesigning_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-8b_self_redesigning_anchoring"
        Write-Host "  Completed: bonsai-8b_self_redesigning_anchoring"
    } else {
        Write-Host "  FAILED: bonsai-8b_self_redesigning_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-8b_self_redesigning_anchoring"
}

$current++
if ($completed -notcontains "bonsai-8b_self_redesigning_store") {
    Write-Host "[$current/$total] Running: bonsai-8b_self_redesigning_store"
    python run_experiment.py --config configs/generated/bonsai-8b_self_redesigning_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-8b_self_redesigning_store"
        Write-Host "  Completed: bonsai-8b_self_redesigning_store"
    } else {
        Write-Host "  FAILED: bonsai-8b_self_redesigning_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-8b_self_redesigning_store"
}

$current++
if ($completed -notcontains "bonsai-8b_self_redesigning_checksum") {
    Write-Host "[$current/$total] Running: bonsai-8b_self_redesigning_checksum"
    python run_experiment.py --config configs/generated/bonsai-8b_self_redesigning_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-8b_self_redesigning_checksum"
        Write-Host "  Completed: bonsai-8b_self_redesigning_checksum"
    } else {
        Write-Host "  FAILED: bonsai-8b_self_redesigning_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-8b_self_redesigning_checksum"
}

$current++
if ($completed -notcontains "bonsai-8b_self_redesigning_breaker") {
    Write-Host "[$current/$total] Running: bonsai-8b_self_redesigning_breaker"
    python run_experiment.py --config configs/generated/bonsai-8b_self_redesigning_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "bonsai-8b_self_redesigning_breaker"
        Write-Host "  Completed: bonsai-8b_self_redesigning_breaker"
    } else {
        Write-Host "  FAILED: bonsai-8b_self_redesigning_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): bonsai-8b_self_redesigning_breaker"
}

# --- Model: llama-3.2-3b ---
Write-Host ""
Write-Host "=== Load model: llama-3.2-3b ==="
Write-Host "Start llama.cpp server with:"
Write-Host "  .\llama-server.exe -m E:\data\code\claudecode\epistemic-edge\models\llama-3.2-3b\Llama-3.2-3B-Instruct-Q4_K_M.gguf --port 8080 -ngl 99"
Write-Host "Press Enter when server is ready..."
Read-Host

$current++
if ($completed -notcontains "llama-3.2-3b_coding_none") {
    Write-Host "[$current/$total] Running: llama-3.2-3b_coding_none"
    python run_experiment.py --config configs/generated/llama-3.2-3b_coding_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "llama-3.2-3b_coding_none"
        Write-Host "  Completed: llama-3.2-3b_coding_none"
    } else {
        Write-Host "  FAILED: llama-3.2-3b_coding_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): llama-3.2-3b_coding_none"
}

$current++
if ($completed -notcontains "llama-3.2-3b_coding_anchoring") {
    Write-Host "[$current/$total] Running: llama-3.2-3b_coding_anchoring"
    python run_experiment.py --config configs/generated/llama-3.2-3b_coding_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "llama-3.2-3b_coding_anchoring"
        Write-Host "  Completed: llama-3.2-3b_coding_anchoring"
    } else {
        Write-Host "  FAILED: llama-3.2-3b_coding_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): llama-3.2-3b_coding_anchoring"
}

$current++
if ($completed -notcontains "llama-3.2-3b_coding_store") {
    Write-Host "[$current/$total] Running: llama-3.2-3b_coding_store"
    python run_experiment.py --config configs/generated/llama-3.2-3b_coding_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "llama-3.2-3b_coding_store"
        Write-Host "  Completed: llama-3.2-3b_coding_store"
    } else {
        Write-Host "  FAILED: llama-3.2-3b_coding_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): llama-3.2-3b_coding_store"
}

$current++
if ($completed -notcontains "llama-3.2-3b_coding_checksum") {
    Write-Host "[$current/$total] Running: llama-3.2-3b_coding_checksum"
    python run_experiment.py --config configs/generated/llama-3.2-3b_coding_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "llama-3.2-3b_coding_checksum"
        Write-Host "  Completed: llama-3.2-3b_coding_checksum"
    } else {
        Write-Host "  FAILED: llama-3.2-3b_coding_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): llama-3.2-3b_coding_checksum"
}

$current++
if ($completed -notcontains "llama-3.2-3b_coding_breaker") {
    Write-Host "[$current/$total] Running: llama-3.2-3b_coding_breaker"
    python run_experiment.py --config configs/generated/llama-3.2-3b_coding_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "llama-3.2-3b_coding_breaker"
        Write-Host "  Completed: llama-3.2-3b_coding_breaker"
    } else {
        Write-Host "  FAILED: llama-3.2-3b_coding_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): llama-3.2-3b_coding_breaker"
}

$current++
if ($completed -notcontains "llama-3.2-3b_general_task_none") {
    Write-Host "[$current/$total] Running: llama-3.2-3b_general_task_none"
    python run_experiment.py --config configs/generated/llama-3.2-3b_general_task_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "llama-3.2-3b_general_task_none"
        Write-Host "  Completed: llama-3.2-3b_general_task_none"
    } else {
        Write-Host "  FAILED: llama-3.2-3b_general_task_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): llama-3.2-3b_general_task_none"
}

$current++
if ($completed -notcontains "llama-3.2-3b_general_task_anchoring") {
    Write-Host "[$current/$total] Running: llama-3.2-3b_general_task_anchoring"
    python run_experiment.py --config configs/generated/llama-3.2-3b_general_task_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "llama-3.2-3b_general_task_anchoring"
        Write-Host "  Completed: llama-3.2-3b_general_task_anchoring"
    } else {
        Write-Host "  FAILED: llama-3.2-3b_general_task_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): llama-3.2-3b_general_task_anchoring"
}

$current++
if ($completed -notcontains "llama-3.2-3b_general_task_store") {
    Write-Host "[$current/$total] Running: llama-3.2-3b_general_task_store"
    python run_experiment.py --config configs/generated/llama-3.2-3b_general_task_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "llama-3.2-3b_general_task_store"
        Write-Host "  Completed: llama-3.2-3b_general_task_store"
    } else {
        Write-Host "  FAILED: llama-3.2-3b_general_task_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): llama-3.2-3b_general_task_store"
}

$current++
if ($completed -notcontains "llama-3.2-3b_general_task_checksum") {
    Write-Host "[$current/$total] Running: llama-3.2-3b_general_task_checksum"
    python run_experiment.py --config configs/generated/llama-3.2-3b_general_task_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "llama-3.2-3b_general_task_checksum"
        Write-Host "  Completed: llama-3.2-3b_general_task_checksum"
    } else {
        Write-Host "  FAILED: llama-3.2-3b_general_task_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): llama-3.2-3b_general_task_checksum"
}

$current++
if ($completed -notcontains "llama-3.2-3b_general_task_breaker") {
    Write-Host "[$current/$total] Running: llama-3.2-3b_general_task_breaker"
    python run_experiment.py --config configs/generated/llama-3.2-3b_general_task_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "llama-3.2-3b_general_task_breaker"
        Write-Host "  Completed: llama-3.2-3b_general_task_breaker"
    } else {
        Write-Host "  FAILED: llama-3.2-3b_general_task_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): llama-3.2-3b_general_task_breaker"
}

$current++
if ($completed -notcontains "llama-3.2-3b_self_redesigning_none") {
    Write-Host "[$current/$total] Running: llama-3.2-3b_self_redesigning_none"
    python run_experiment.py --config configs/generated/llama-3.2-3b_self_redesigning_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "llama-3.2-3b_self_redesigning_none"
        Write-Host "  Completed: llama-3.2-3b_self_redesigning_none"
    } else {
        Write-Host "  FAILED: llama-3.2-3b_self_redesigning_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): llama-3.2-3b_self_redesigning_none"
}

$current++
if ($completed -notcontains "llama-3.2-3b_self_redesigning_anchoring") {
    Write-Host "[$current/$total] Running: llama-3.2-3b_self_redesigning_anchoring"
    python run_experiment.py --config configs/generated/llama-3.2-3b_self_redesigning_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "llama-3.2-3b_self_redesigning_anchoring"
        Write-Host "  Completed: llama-3.2-3b_self_redesigning_anchoring"
    } else {
        Write-Host "  FAILED: llama-3.2-3b_self_redesigning_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): llama-3.2-3b_self_redesigning_anchoring"
}

$current++
if ($completed -notcontains "llama-3.2-3b_self_redesigning_store") {
    Write-Host "[$current/$total] Running: llama-3.2-3b_self_redesigning_store"
    python run_experiment.py --config configs/generated/llama-3.2-3b_self_redesigning_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "llama-3.2-3b_self_redesigning_store"
        Write-Host "  Completed: llama-3.2-3b_self_redesigning_store"
    } else {
        Write-Host "  FAILED: llama-3.2-3b_self_redesigning_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): llama-3.2-3b_self_redesigning_store"
}

$current++
if ($completed -notcontains "llama-3.2-3b_self_redesigning_checksum") {
    Write-Host "[$current/$total] Running: llama-3.2-3b_self_redesigning_checksum"
    python run_experiment.py --config configs/generated/llama-3.2-3b_self_redesigning_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "llama-3.2-3b_self_redesigning_checksum"
        Write-Host "  Completed: llama-3.2-3b_self_redesigning_checksum"
    } else {
        Write-Host "  FAILED: llama-3.2-3b_self_redesigning_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): llama-3.2-3b_self_redesigning_checksum"
}

$current++
if ($completed -notcontains "llama-3.2-3b_self_redesigning_breaker") {
    Write-Host "[$current/$total] Running: llama-3.2-3b_self_redesigning_breaker"
    python run_experiment.py --config configs/generated/llama-3.2-3b_self_redesigning_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "llama-3.2-3b_self_redesigning_breaker"
        Write-Host "  Completed: llama-3.2-3b_self_redesigning_breaker"
    } else {
        Write-Host "  FAILED: llama-3.2-3b_self_redesigning_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): llama-3.2-3b_self_redesigning_breaker"
}

# --- Model: phi-3.5-mini ---
Write-Host ""
Write-Host "=== Load model: phi-3.5-mini ==="
Write-Host "Start llama.cpp server with:"
Write-Host "  .\llama-server.exe -m E:\data\code\claudecode\epistemic-edge\models\phi-3.5-mini\Phi-3.5-mini-instruct-Q4_K_M.gguf --port 8080 -ngl 99"
Write-Host "Press Enter when server is ready..."
Read-Host

$current++
if ($completed -notcontains "phi-3.5-mini_coding_none") {
    Write-Host "[$current/$total] Running: phi-3.5-mini_coding_none"
    python run_experiment.py --config configs/generated/phi-3.5-mini_coding_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "phi-3.5-mini_coding_none"
        Write-Host "  Completed: phi-3.5-mini_coding_none"
    } else {
        Write-Host "  FAILED: phi-3.5-mini_coding_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): phi-3.5-mini_coding_none"
}

$current++
if ($completed -notcontains "phi-3.5-mini_coding_anchoring") {
    Write-Host "[$current/$total] Running: phi-3.5-mini_coding_anchoring"
    python run_experiment.py --config configs/generated/phi-3.5-mini_coding_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "phi-3.5-mini_coding_anchoring"
        Write-Host "  Completed: phi-3.5-mini_coding_anchoring"
    } else {
        Write-Host "  FAILED: phi-3.5-mini_coding_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): phi-3.5-mini_coding_anchoring"
}

$current++
if ($completed -notcontains "phi-3.5-mini_coding_store") {
    Write-Host "[$current/$total] Running: phi-3.5-mini_coding_store"
    python run_experiment.py --config configs/generated/phi-3.5-mini_coding_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "phi-3.5-mini_coding_store"
        Write-Host "  Completed: phi-3.5-mini_coding_store"
    } else {
        Write-Host "  FAILED: phi-3.5-mini_coding_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): phi-3.5-mini_coding_store"
}

$current++
if ($completed -notcontains "phi-3.5-mini_coding_checksum") {
    Write-Host "[$current/$total] Running: phi-3.5-mini_coding_checksum"
    python run_experiment.py --config configs/generated/phi-3.5-mini_coding_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "phi-3.5-mini_coding_checksum"
        Write-Host "  Completed: phi-3.5-mini_coding_checksum"
    } else {
        Write-Host "  FAILED: phi-3.5-mini_coding_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): phi-3.5-mini_coding_checksum"
}

$current++
if ($completed -notcontains "phi-3.5-mini_coding_breaker") {
    Write-Host "[$current/$total] Running: phi-3.5-mini_coding_breaker"
    python run_experiment.py --config configs/generated/phi-3.5-mini_coding_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "phi-3.5-mini_coding_breaker"
        Write-Host "  Completed: phi-3.5-mini_coding_breaker"
    } else {
        Write-Host "  FAILED: phi-3.5-mini_coding_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): phi-3.5-mini_coding_breaker"
}

$current++
if ($completed -notcontains "phi-3.5-mini_general_task_none") {
    Write-Host "[$current/$total] Running: phi-3.5-mini_general_task_none"
    python run_experiment.py --config configs/generated/phi-3.5-mini_general_task_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "phi-3.5-mini_general_task_none"
        Write-Host "  Completed: phi-3.5-mini_general_task_none"
    } else {
        Write-Host "  FAILED: phi-3.5-mini_general_task_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): phi-3.5-mini_general_task_none"
}

$current++
if ($completed -notcontains "phi-3.5-mini_general_task_anchoring") {
    Write-Host "[$current/$total] Running: phi-3.5-mini_general_task_anchoring"
    python run_experiment.py --config configs/generated/phi-3.5-mini_general_task_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "phi-3.5-mini_general_task_anchoring"
        Write-Host "  Completed: phi-3.5-mini_general_task_anchoring"
    } else {
        Write-Host "  FAILED: phi-3.5-mini_general_task_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): phi-3.5-mini_general_task_anchoring"
}

$current++
if ($completed -notcontains "phi-3.5-mini_general_task_store") {
    Write-Host "[$current/$total] Running: phi-3.5-mini_general_task_store"
    python run_experiment.py --config configs/generated/phi-3.5-mini_general_task_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "phi-3.5-mini_general_task_store"
        Write-Host "  Completed: phi-3.5-mini_general_task_store"
    } else {
        Write-Host "  FAILED: phi-3.5-mini_general_task_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): phi-3.5-mini_general_task_store"
}

$current++
if ($completed -notcontains "phi-3.5-mini_general_task_checksum") {
    Write-Host "[$current/$total] Running: phi-3.5-mini_general_task_checksum"
    python run_experiment.py --config configs/generated/phi-3.5-mini_general_task_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "phi-3.5-mini_general_task_checksum"
        Write-Host "  Completed: phi-3.5-mini_general_task_checksum"
    } else {
        Write-Host "  FAILED: phi-3.5-mini_general_task_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): phi-3.5-mini_general_task_checksum"
}

$current++
if ($completed -notcontains "phi-3.5-mini_general_task_breaker") {
    Write-Host "[$current/$total] Running: phi-3.5-mini_general_task_breaker"
    python run_experiment.py --config configs/generated/phi-3.5-mini_general_task_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "phi-3.5-mini_general_task_breaker"
        Write-Host "  Completed: phi-3.5-mini_general_task_breaker"
    } else {
        Write-Host "  FAILED: phi-3.5-mini_general_task_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): phi-3.5-mini_general_task_breaker"
}

$current++
if ($completed -notcontains "phi-3.5-mini_self_redesigning_none") {
    Write-Host "[$current/$total] Running: phi-3.5-mini_self_redesigning_none"
    python run_experiment.py --config configs/generated/phi-3.5-mini_self_redesigning_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "phi-3.5-mini_self_redesigning_none"
        Write-Host "  Completed: phi-3.5-mini_self_redesigning_none"
    } else {
        Write-Host "  FAILED: phi-3.5-mini_self_redesigning_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): phi-3.5-mini_self_redesigning_none"
}

$current++
if ($completed -notcontains "phi-3.5-mini_self_redesigning_anchoring") {
    Write-Host "[$current/$total] Running: phi-3.5-mini_self_redesigning_anchoring"
    python run_experiment.py --config configs/generated/phi-3.5-mini_self_redesigning_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "phi-3.5-mini_self_redesigning_anchoring"
        Write-Host "  Completed: phi-3.5-mini_self_redesigning_anchoring"
    } else {
        Write-Host "  FAILED: phi-3.5-mini_self_redesigning_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): phi-3.5-mini_self_redesigning_anchoring"
}

$current++
if ($completed -notcontains "phi-3.5-mini_self_redesigning_store") {
    Write-Host "[$current/$total] Running: phi-3.5-mini_self_redesigning_store"
    python run_experiment.py --config configs/generated/phi-3.5-mini_self_redesigning_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "phi-3.5-mini_self_redesigning_store"
        Write-Host "  Completed: phi-3.5-mini_self_redesigning_store"
    } else {
        Write-Host "  FAILED: phi-3.5-mini_self_redesigning_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): phi-3.5-mini_self_redesigning_store"
}

$current++
if ($completed -notcontains "phi-3.5-mini_self_redesigning_checksum") {
    Write-Host "[$current/$total] Running: phi-3.5-mini_self_redesigning_checksum"
    python run_experiment.py --config configs/generated/phi-3.5-mini_self_redesigning_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "phi-3.5-mini_self_redesigning_checksum"
        Write-Host "  Completed: phi-3.5-mini_self_redesigning_checksum"
    } else {
        Write-Host "  FAILED: phi-3.5-mini_self_redesigning_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): phi-3.5-mini_self_redesigning_checksum"
}

$current++
if ($completed -notcontains "phi-3.5-mini_self_redesigning_breaker") {
    Write-Host "[$current/$total] Running: phi-3.5-mini_self_redesigning_breaker"
    python run_experiment.py --config configs/generated/phi-3.5-mini_self_redesigning_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "phi-3.5-mini_self_redesigning_breaker"
        Write-Host "  Completed: phi-3.5-mini_self_redesigning_breaker"
    } else {
        Write-Host "  FAILED: phi-3.5-mini_self_redesigning_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): phi-3.5-mini_self_redesigning_breaker"
}

# --- Model: qwen3-8b ---
Write-Host ""
Write-Host "=== Load model: qwen3-8b ==="
Write-Host "Start llama.cpp server with:"
Write-Host "  .\llama-server.exe -m E:\data\code\claudecode\epistemic-edge\models\qwen3-8b\Qwen3-8B-Q4_K_M.gguf --port 8080 -ngl 99"
Write-Host "Press Enter when server is ready..."
Read-Host

$current++
if ($completed -notcontains "qwen3-8b_coding_none") {
    Write-Host "[$current/$total] Running: qwen3-8b_coding_none"
    python run_experiment.py --config configs/generated/qwen3-8b_coding_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen3-8b_coding_none"
        Write-Host "  Completed: qwen3-8b_coding_none"
    } else {
        Write-Host "  FAILED: qwen3-8b_coding_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen3-8b_coding_none"
}

$current++
if ($completed -notcontains "qwen3-8b_coding_anchoring") {
    Write-Host "[$current/$total] Running: qwen3-8b_coding_anchoring"
    python run_experiment.py --config configs/generated/qwen3-8b_coding_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen3-8b_coding_anchoring"
        Write-Host "  Completed: qwen3-8b_coding_anchoring"
    } else {
        Write-Host "  FAILED: qwen3-8b_coding_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen3-8b_coding_anchoring"
}

$current++
if ($completed -notcontains "qwen3-8b_coding_store") {
    Write-Host "[$current/$total] Running: qwen3-8b_coding_store"
    python run_experiment.py --config configs/generated/qwen3-8b_coding_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen3-8b_coding_store"
        Write-Host "  Completed: qwen3-8b_coding_store"
    } else {
        Write-Host "  FAILED: qwen3-8b_coding_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen3-8b_coding_store"
}

$current++
if ($completed -notcontains "qwen3-8b_coding_checksum") {
    Write-Host "[$current/$total] Running: qwen3-8b_coding_checksum"
    python run_experiment.py --config configs/generated/qwen3-8b_coding_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen3-8b_coding_checksum"
        Write-Host "  Completed: qwen3-8b_coding_checksum"
    } else {
        Write-Host "  FAILED: qwen3-8b_coding_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen3-8b_coding_checksum"
}

$current++
if ($completed -notcontains "qwen3-8b_coding_breaker") {
    Write-Host "[$current/$total] Running: qwen3-8b_coding_breaker"
    python run_experiment.py --config configs/generated/qwen3-8b_coding_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen3-8b_coding_breaker"
        Write-Host "  Completed: qwen3-8b_coding_breaker"
    } else {
        Write-Host "  FAILED: qwen3-8b_coding_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen3-8b_coding_breaker"
}

$current++
if ($completed -notcontains "qwen3-8b_general_task_none") {
    Write-Host "[$current/$total] Running: qwen3-8b_general_task_none"
    python run_experiment.py --config configs/generated/qwen3-8b_general_task_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen3-8b_general_task_none"
        Write-Host "  Completed: qwen3-8b_general_task_none"
    } else {
        Write-Host "  FAILED: qwen3-8b_general_task_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen3-8b_general_task_none"
}

$current++
if ($completed -notcontains "qwen3-8b_general_task_anchoring") {
    Write-Host "[$current/$total] Running: qwen3-8b_general_task_anchoring"
    python run_experiment.py --config configs/generated/qwen3-8b_general_task_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen3-8b_general_task_anchoring"
        Write-Host "  Completed: qwen3-8b_general_task_anchoring"
    } else {
        Write-Host "  FAILED: qwen3-8b_general_task_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen3-8b_general_task_anchoring"
}

$current++
if ($completed -notcontains "qwen3-8b_general_task_store") {
    Write-Host "[$current/$total] Running: qwen3-8b_general_task_store"
    python run_experiment.py --config configs/generated/qwen3-8b_general_task_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen3-8b_general_task_store"
        Write-Host "  Completed: qwen3-8b_general_task_store"
    } else {
        Write-Host "  FAILED: qwen3-8b_general_task_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen3-8b_general_task_store"
}

$current++
if ($completed -notcontains "qwen3-8b_general_task_checksum") {
    Write-Host "[$current/$total] Running: qwen3-8b_general_task_checksum"
    python run_experiment.py --config configs/generated/qwen3-8b_general_task_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen3-8b_general_task_checksum"
        Write-Host "  Completed: qwen3-8b_general_task_checksum"
    } else {
        Write-Host "  FAILED: qwen3-8b_general_task_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen3-8b_general_task_checksum"
}

$current++
if ($completed -notcontains "qwen3-8b_general_task_breaker") {
    Write-Host "[$current/$total] Running: qwen3-8b_general_task_breaker"
    python run_experiment.py --config configs/generated/qwen3-8b_general_task_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen3-8b_general_task_breaker"
        Write-Host "  Completed: qwen3-8b_general_task_breaker"
    } else {
        Write-Host "  FAILED: qwen3-8b_general_task_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen3-8b_general_task_breaker"
}

$current++
if ($completed -notcontains "qwen3-8b_self_redesigning_none") {
    Write-Host "[$current/$total] Running: qwen3-8b_self_redesigning_none"
    python run_experiment.py --config configs/generated/qwen3-8b_self_redesigning_none.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen3-8b_self_redesigning_none"
        Write-Host "  Completed: qwen3-8b_self_redesigning_none"
    } else {
        Write-Host "  FAILED: qwen3-8b_self_redesigning_none" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen3-8b_self_redesigning_none"
}

$current++
if ($completed -notcontains "qwen3-8b_self_redesigning_anchoring") {
    Write-Host "[$current/$total] Running: qwen3-8b_self_redesigning_anchoring"
    python run_experiment.py --config configs/generated/qwen3-8b_self_redesigning_anchoring.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen3-8b_self_redesigning_anchoring"
        Write-Host "  Completed: qwen3-8b_self_redesigning_anchoring"
    } else {
        Write-Host "  FAILED: qwen3-8b_self_redesigning_anchoring" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen3-8b_self_redesigning_anchoring"
}

$current++
if ($completed -notcontains "qwen3-8b_self_redesigning_store") {
    Write-Host "[$current/$total] Running: qwen3-8b_self_redesigning_store"
    python run_experiment.py --config configs/generated/qwen3-8b_self_redesigning_store.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen3-8b_self_redesigning_store"
        Write-Host "  Completed: qwen3-8b_self_redesigning_store"
    } else {
        Write-Host "  FAILED: qwen3-8b_self_redesigning_store" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen3-8b_self_redesigning_store"
}

$current++
if ($completed -notcontains "qwen3-8b_self_redesigning_checksum") {
    Write-Host "[$current/$total] Running: qwen3-8b_self_redesigning_checksum"
    python run_experiment.py --config configs/generated/qwen3-8b_self_redesigning_checksum.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen3-8b_self_redesigning_checksum"
        Write-Host "  Completed: qwen3-8b_self_redesigning_checksum"
    } else {
        Write-Host "  FAILED: qwen3-8b_self_redesigning_checksum" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen3-8b_self_redesigning_checksum"
}

$current++
if ($completed -notcontains "qwen3-8b_self_redesigning_breaker") {
    Write-Host "[$current/$total] Running: qwen3-8b_self_redesigning_breaker"
    python run_experiment.py --config configs/generated/qwen3-8b_self_redesigning_breaker.yaml
    if ($LASTEXITCODE -eq 0) {
        Add-Content $checkpointFile "qwen3-8b_self_redesigning_breaker"
        Write-Host "  Completed: qwen3-8b_self_redesigning_breaker"
    } else {
        Write-Host "  FAILED: qwen3-8b_self_redesigning_breaker" -ForegroundColor Red
    }
} else {
    Write-Host "[$current/$total] Skipping (already done): qwen3-8b_self_redesigning_breaker"
}

Write-Host ""
Write-Host "All experiments complete."
Write-Host "Results in: results/"