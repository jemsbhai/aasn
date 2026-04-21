# Context Propagation Experiment Findings

**Paper:** "Context Propagation and Context Rot in Multi-Generation Agent Systems"
**Target:** NeurIPS 2026
**Last updated:** 2026-04-21

---

## Experiment Matrix

| Dimension | Values |
|-----------|--------|
| Agent types | coding, general_task, self_redesigning |
| Models | Bonsai-1.7B, Bonsai-4B, Bonsai-8B, Llama-3.2-3B, Phi-3.5-mini, Qwen3-8B, Qwen2.5-Coder-7B |
| Mitigations | none, context_anchoring, structured_store, checksumming, circuit_breaker |
| Coding benchmarks | HumanEval, MBPP, CRUXEval |
| General benchmarks | GSM8K, ARC-Challenge, MMLU |
| Generations | 20 per chain |
| Independent runs | 5 per configuration |

Total configurations: 7 models x 3 agent types x 5 mitigations = 105

---

## Log of Findings

### 2026-04-21: Smoke Test (Qwen2.5-Coder-7B, coding, baseline)

- **Setup:** 2 generations, 1 run, 5 custom coding tasks (placeholder)
- **Result:** Fidelity dropped from 1.0 to 0.6 in 2 generations
- **Rot rate:** 0.4 per generation
- **Semantic drift:** 0.080 (low after only 2 generations)
- **Note:** Placeholder tasks, not canonical benchmarks. Will re-run with HumanEval/MBPP.

---

*Findings below this line will be added as experiments complete.*

---
