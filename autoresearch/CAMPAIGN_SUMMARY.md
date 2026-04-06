# Autoresearch Campaign: OpenClaw Learning Loop

## Campaign Results

| Round | Artifact(s) | Baseline | Final | Prompts | Improvements |
|-------|-------------|----------|-------|---------|-------------|
| R1 | AGENTS.md learning protocol | 85% (17/20) | 100% (20/20) | 20 | +inline security guardrails, +PARTIAL counting, +state regression rules |
| R2 | Full system (all files) | 100% (20/20) | — | 20 (harder) | System architecture already covered all edge cases |
| Skills | 6 learning loop skills | 95.8% (2 issues) | 100% (0 issues) | 48 checks | +error handling to skill-manager and skill-portability |
| Supporting | 8 supporting files | 100% (46 checks) | — | 46 checks | All clean on first pass |

## Total Eval Coverage

- **40 scenario prompts** across R1 + R2
- **48 structural checks** across 6 skills
- **46 completeness checks** across 8 supporting files
- **134 total evaluation points**

## Concrete Improvements Made

1. **Inline security guardrails** added to AGENTS.md learning protocol (credential safety, identity protection, exfiltration prevention, destructive command guardrails)
2. **PARTIAL outcome counting** formula: PARTIAL = 0.5 for success rate calculation
3. **State regression rules**: MATURE → VALIDATED at <70%, VALIDATED → DRAFT at <60%
4. **Error handling** added to skill-manager (6 edge cases) and skill-portability (6 edge cases)

## Files Modified During Campaign

- `docs/reference/templates/AGENTS.md` — security guardrails + state transitions
- `docs/reference/AGENTS.default.md` — same (synced)
- `docs/reference/workspace-template/AGENTS.md` — same (synced)
- `skills/skill-manager/SKILL.md` — error handling section
- `skills/skill-portability/SKILL.md` — error handling section

## Eval Infrastructure (Reusable)

- `autoresearch/eval_prompts.json` — 20 R1 scenario prompts
- `autoresearch/eval_prompts_r2.json` — 20 R2 harder scenario prompts
- `autoresearch/run_eval.py` — R1 evaluator (AGENTS.md focus)
- `autoresearch/run_eval_r2.py` — R2 evaluator (full system)
- `autoresearch/eval_skills.py` — 6-skill structural evaluator
- `autoresearch/eval_supporting.py` — 8-file completeness evaluator
- `autoresearch/results.tsv` — experiment log

All eval scripts can be re-run after future modifications to regression-test changes.
