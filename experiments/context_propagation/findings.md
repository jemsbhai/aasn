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

### 2026-04-21: Full Benchmark Run (Bonsai-1.7B, coding, baseline)

- **Setup:** 3 generations, 1 run, 669 tasks (164 HumanEval + 500 MBPP + 5 custom)
- **Timing:** Gen 0 = 361s, Gen 1 = 686s, Gen 2 = ~850s (est). ~524s avg/gen.
- **Scores:** Gen 0 = 0.1151, Gen 1 = 0.1101, Gen 2 = 0.1193
- **Critical finding: prompt did NOT evolve.** Bonsai-1.7B echoed the spawning prompt back identically across all 3 generations. The model is too small (1.7B, 1-bit quant) to follow meta-instructions for prompt redesign.
- **Implication:** Context rot requires a minimum model capability threshold. Below it, the spawning mechanism fails silently (prompt unchanged = no rot, but also no adaptation). This is a paper-worthy finding: rot rate as a function of model capability.
- **Metric gap:** metrics.json not generated - sentence-transformers likely failed. Fix pending.
- **Timing extrapolation:** Full benchmarks at ~0.78s/call. 669 tasks x 20 gens x 5 runs = ~14.6 hrs per config. Full matrix needs A100 cluster.

---

### 2026-04-21: Qwen2.5-Coder-7B, coding, baseline (5 generations, 1 run)

- **Setup:** 5 generations, 1 run, 669 tasks (HumanEval + MBPP + custom), score-only feedback
- **Score trajectory:** 0.2292 -> 0.1938 -> 0.2103 -> 0.2013 -> 0.2152
- **Final fidelity:** 0.939, avg rot rate: 0.0152
- **Semantic drift:** cosine similarity to P_0 drops to 0.56-0.65 by gen 1 and oscillates
- **Prompt length instability:** 194 -> 1391 -> 433 -> 1037 -> 714 tokens (wild swings)
- **Key finding: STOCHASTIC REGIME.** Not monotonic rot, not improvement. Rot rate alternates sign. This places Qwen-7B + score-only feedback near the phase transition boundary.
- **Prompt evolution:** P_0 was terse (194 chars). Model rewrites it each generation into varying structures (numbered lists, paragraphs). Core intent preserved but surface form unstable.
- **Contrast with Bonsai-1.7B:** Bonsai couldn't modify the prompt at all (fidelity=1.0, drift=0.0). Qwen-7B modifies aggressively (drift=0.41) but maintains performance. Two failure modes: (1) can't redesign at all, (2) redesigns chaotically.
- **Phase diagram placement:** Qwen-7B with score-only feedback sits at the transition boundary. Predicts: richer feedback should push into improvement regime; weaker models should push into degradation regime.
- **LLM stats:** 3351 calls, 1.28M tokens, ~90 minutes runtime

---

### 2026-04-21: Rich vs Score-Only Feedback Comparison (Qwen2.5-Coder-7B, coding)

**PHASE TRANSITION SIGNAL DETECTED.**

**Rich feedback** (10 gens, 50 tasks, per-task error analysis + cumulative memory):
- Trajectory: 0.28 -> 0.20 -> 0.26 -> 0.20 -> 0.28 -> 0.28 -> 0.24 -> 0.26 -> 0.24 -> 0.30
- Net change: +0.02 (IMPROVEMENT, 7.1% relative)
- Final fidelity: 1.0 (at or above gen 0 performance)
- Prompt length: monotonically grows 194 -> 2238 (accumulates knowledge)
- Gen 9 prompt explicitly references error categories (wrong_logic, import_error) from feedback

**Score-only** (5 gens, 669 tasks, aggregate scores only):
- Trajectory: 0.229 -> 0.194 -> 0.210 -> 0.201 -> 0.215
- Net change: -0.014 (DEGRADATION, 6.2% relative)
- Final fidelity: 0.939 (below gen 0)
- Prompt length: oscillates wildly 194 -> 1391 -> 433 -> 1037 -> 714

**Key differences:**
1. Direction: rich feedback trends upward, score-only trends downward
2. Prompt stability: rich accumulates monotonically, score-only oscillates chaotically
3. Knowledge transfer: rich prompt incorporates specific error patterns, score-only rewrites generically
4. This supports the channel capacity theory: richer feedback crosses the phase transition threshold

**Caveats for the paper:**
- Different task counts (50 vs 669) between runs. Need matched control.
- Single run each, no statistical significance yet. Need 5 runs per condition.
- Improvement is small (0.02 absolute). Need more generations to see if trend continues.
- Running matched score-only control next.

---
