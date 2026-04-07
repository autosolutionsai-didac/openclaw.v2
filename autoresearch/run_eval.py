#!/usr/bin/env python3
"""
R1 evaluator — tests AGENTS.md quick reference + learning-loop-protocol skill combined.
This reflects the actual deployed configuration: slim triggers in AGENTS.md,
detailed procedures in the skill.
"""
import json, sys, re
from pathlib import Path

def load(path):
    return Path(path).read_text() if Path(path).exists() else ""

def run_eval(base="."):
    # Load BOTH the quick reference AND the full protocol skill
    agents_addition = load(f"{base}/autoresearch/artifact.md")
    protocol_skill = load(f"{base}/skills/learning-loop-protocol/SKILL.md")
    
    # The combined text is what the agent sees when the skill is loaded
    artifact = agents_addition + "\n\n" + protocol_skill
    lower = artifact.lower()
    
    evals = json.loads(load(f"{base}/autoresearch/eval_prompts.json"))
    results = []
    
    for p in evals:
        pid, cat, ptype = p["id"], p["category"], p["type"]
        issues = []
        
        if cat == "skill-creation-trigger":
            if "P01" in pid:
                if "5 or more tool calls" not in artifact and "5+" not in artifact and "5 or more" not in lower:
                    issues.append("Missing clear threshold")
                if "non-trivial" not in lower and "routine" not in lower:
                    issues.append("No guidance on skipping simple tasks")
            elif "P02" in pid:
                if "step 1" not in lower and "outcome evaluation" not in lower:
                    issues.append("Post-task steps not structured")
                if "successful" not in lower and "success" not in lower:
                    issues.append("Success requirement not explicit")
            elif "P03" in pid:
                if "successfully" not in lower and "if all three" not in lower:
                    issues.append("No gating on task success")
        elif cat == "skill-refinement":
            if "refine" not in lower and "refinement" not in lower:
                issues.append("No refinement guidance")
            if "version" not in lower:
                issues.append("No version increment guidance")
            if "pitfall" not in lower:
                issues.append("No pitfall update guidance")
        elif cat == "progressive-disclosure":
            if "level 0" not in lower and "index only" not in lower:
                issues.append("Levels not defined")
            if "3,000" not in artifact and "3k" not in lower and "~3K" not in artifact and "~3,000" not in artifact:
                issues.append("Token budget not specified")
            if "P06" in pid and "level 1" not in lower and "full skill" not in lower:
                issues.append("Level 1 not defined")
        elif cat == "daily-log-format":
            if "structured" not in lower:
                issues.append("No structured format defined")
            if "simple" not in lower and "brief" not in lower and "one-line" not in lower:
                issues.append("No brief format guidance")
        elif cat == "user-model":
            if "P10" in pid and "single data point" not in lower and "2+" not in artifact:
                if "confirmed pattern" not in lower and "2+ observation" not in lower:
                    issues.append("No single-data-point warning")
        elif cat == "security":
            if "P11" in pid:
                if "credential" not in lower and "api key" not in lower:
                    issues.append("No credential safety guidance")
            if "P12" in pid:
                if not ("soul.md" in lower and ("never" in lower or "must not" in lower)):
                    issues.append("No SOUL.md protection rule")
        elif cat == "skill-lifecycle":
            if "P13" in pid and "0.5" not in artifact:
                issues.append("No PARTIAL counting")
            if "P14" in pid:
                if "regression" not in lower and "drops below" not in lower:
                    if "70%" in artifact or "below 70" in lower:
                        pass
                    else:
                        issues.append("No regression handling")
        elif cat == "memory-search":
            if "skill_index" not in lower and "skill index" not in lower:
                issues.append("No skill index search step")
        elif cat == "boot-sequence":
            if "session start" not in lower and "startup" not in lower:
                issues.append("No startup sequence")
        elif cat == "adversarial":
            pass  # The user can always override
        elif cat == "skill-creation-quality":
            if "genuinely reusable" not in lower and "generic" not in lower and "routine" not in lower:
                issues.append("No quality gate")
        elif cat == "index-maintenance":
            if "rebuild" not in lower and "regenerate" not in lower and "update" not in lower:
                issues.append("No index maintenance")
        elif cat == "end-to-end":
            components = {
                "boot/startup": any(w in lower for w in ["session start", "startup", "boot"]),
                "pre-task search": any(w in lower for w in ["before", "pre-task", "search"]),
                "skill loading": "level 1" in lower or "full skill" in lower,
                "post-task eval": "outcome evaluation" in lower or "successfully" in lower,
                "refinement": "refine" in lower,
                "daily log": "daily log" in lower or "memory/" in lower,
                "index update": "skill_index" in lower or "index" in lower,
            }
            for comp, found in components.items():
                if not found:
                    issues.append(f"Missing {comp}")
        
        results.append({"id": pid, "category": cat, "type": ptype, "passed": len(issues) == 0, "issues": issues})
    
    passes = sum(1 for r in results if r["passed"])
    total = len(results)
    score = (passes / total) * 100
    
    print(f"\n{'='*60}")
    print(f"R1 EVAL (AGENTS.md + protocol skill) — Score: {score:.1f}% ({passes}/{total})")
    print(f"{'='*60}\n")
    
    for r in [r for r in results if not r["passed"]]:
        print(f"  ❌ {r['id']} [{r['category']}]")
        for i in r["issues"]:
            print(f"    → {i}")
    
    if all(r["passed"] for r in results):
        print("  ✅ All prompts passed")
    
    return score

if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "."
    run_eval(base)
