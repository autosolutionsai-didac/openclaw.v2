#!/usr/bin/env python3
"""
Autoresearch evaluator for the OpenClaw Learning Loop.
Scores the artifact (AGENTS.md learning loop additions) against eval prompts.
Checks whether the instructions provide clear, unambiguous guidance for each scenario.

Scoring: for each prompt, check if the artifact text contains sufficient guidance
to produce a passing response. Score = (passes / total) * 100
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime

def load_artifact(path):
    return Path(path).read_text()

def load_evals(path):
    return json.loads(Path(path).read_text())

def check_prompt(artifact, prompt_data):
    """Analyze whether the artifact provides clear guidance for this prompt's scenario."""
    pid = prompt_data["id"]
    category = prompt_data["category"]
    prompt = prompt_data["prompt"]
    criteria = prompt_data["pass_criteria"]
    ptype = prompt_data["type"]
    
    issues = []
    
    # Category-specific checks against the artifact text
    if category == "skill-creation-trigger":
        if ptype == "negative" and "P01" in pid:
            # Should NOT trigger for simple tasks
            if "5 or more tool calls" in artifact or "5+" in artifact:
                pass  # threshold is documented
            else:
                issues.append("Missing clear threshold for when skill extraction triggers")
            # Check if it explicitly says simple tasks should be skipped
            if "non-trivial" not in artifact.lower() and "routine" not in artifact.lower():
                issues.append("No guidance on skipping simple/routine tasks")
                
        elif ptype == "positive" and "P02" in pid:
            if "step 1" in artifact.lower() or "outcome evaluation" in artifact.lower():
                pass
            else:
                issues.append("Post-task learning steps not clearly numbered/structured")
            if "successful" in artifact.lower() or "success" in artifact.lower():
                pass
            else:
                issues.append("Success requirement not explicit")
                
        elif ptype == "negative" and "P03" in pid:
            # Failed task should not create skill
            if "successfully" in artifact.lower() or "success" in artifact.lower():
                # Check if it's conditional on success
                if "if all three are yes" in artifact.lower():
                    pass
                else:
                    issues.append("Success condition exists but gating logic unclear")
            else:
                issues.append("No explicit requirement for task success before skill extraction")
    
    elif category == "skill-refinement":
        if "refinement" in artifact.lower() or "refine" in artifact.lower():
            if "existing skill" in artifact.lower() or "matching skill" in artifact.lower():
                pass
            else:
                issues.append("Refinement mentioned but not clearly linked to matching existing skills")
        else:
            issues.append("No skill refinement guidance found")
        if "increment" in artifact.lower() and "version" in artifact.lower():
            pass
        else:
            issues.append("No guidance on incrementing version during refinement")
        if "pitfall" in artifact.lower():
            pass
        else:
            issues.append("No mention of updating pitfalls during refinement")
    
    elif category == "progressive-disclosure":
        if "level 0" in artifact.lower() or "index only" in artifact.lower():
            pass
        else:
            issues.append("Progressive disclosure levels not clearly defined")
        if "3,000 tokens" in artifact or "3k tokens" in artifact.lower() or "~3K" in artifact:
            pass
        else:
            issues.append("Token cost of index not specified")
        if "do not read individual" in artifact.lower() or "do not load" in artifact.lower():
            pass
        else:
            issues.append("No explicit prohibition on loading individual skills at session start")
        if "P06" in pid:
            if "level 1" in artifact.lower() or "full skill" in artifact.lower():
                pass
            else:
                issues.append("Level 1 (full skill load on match) not clearly defined")
    
    elif category == "daily-log-format":
        if "structured format" in artifact.lower() or "structured daily" in artifact.lower():
            pass
        else:
            issues.append("Structured daily log format not clearly defined")
        if "simple" in artifact.lower() and ("one-line" in artifact.lower() or "brief" in artifact.lower()):
            pass
        else:
            issues.append("No guidance on when to use brief vs full format")
    
    elif category == "user-model":
        if "P09" in pid:
            if "2+" in artifact or "confirmation across" in artifact.lower() or "multiple" in artifact.lower():
                pass  # mentions needing pattern confirmation
            else:
                issues.append("No clear threshold for when to update behavioral model")
        if "P10" in pid:
            if "single data point" in artifact.lower():
                pass
            else:
                issues.append("No explicit warning against updating on single observations")
    
    elif category == "security":
        if "P11" in pid:
            # Credentials in skills
            if "credential" in artifact.lower() or "api key" in artifact.lower() or "secret" in artifact.lower():
                pass
            else:
                issues.append("No credential safety guidance in the learning protocol itself")
        if "P12" in pid:
            if "soul.md" in artifact.lower() and ("never" in artifact.lower() or "must not" in artifact.lower()):
                pass
            else:
                issues.append("No explicit prohibition on modifying SOUL.md via skills in the learning protocol")
    
    elif category == "skill-lifecycle":
        if "draft" in artifact.lower() and "validated" in artifact.lower() and "mature" in artifact.lower():
            pass
        else:
            issues.append("Skill states not all defined")
        if "P13" in pid:
            if "partial" in artifact.lower():
                pass  # addresses PARTIAL outcomes
            else:
                issues.append("No guidance on how to count PARTIAL outcomes in success rate")
        if "P14" in pid:
            if "regression" in artifact.lower() or ("drops" in artifact.lower() and "below" in artifact.lower()):
                # Check if there's demotion guidance
                pass
            else:
                issues.append("No guidance on what happens when a MATURE skill's success rate drops")
    
    elif category == "memory-search":
        if "step 1" in artifact.lower() or "skill index" in artifact.lower():
            pass
        else:
            issues.append("Memory search protocol not structured as ordered steps")
    
    elif category == "boot-sequence":
        if "session start" in artifact.lower() or "startup" in artifact.lower():
            pass
        else:
            issues.append("No session startup sequence defined in the artifact")
        if "silent" in artifact.lower() or "do not narrate" in artifact.lower():
            pass
        else:
            issues.append("No instruction to perform startup silently")
    
    elif category == "adversarial":
        # The protocol should be respectful of user override
        if "user" in artifact.lower():
            pass  # mentions user context
        else:
            issues.append("No user override/opt-out guidance")
        # But this is an implicit check - the protocol doesn't need to explicitly handle "stop learning"
        # as long as it doesn't mandate learning over user wishes
    
    elif category == "skill-creation-quality":
        if "genuinely reusable" in artifact.lower() or "don't over-extract" in artifact.lower() or "routine" in artifact.lower():
            pass
        else:
            issues.append("No quality gate for skill creation (preventing trivial skills)")
    
    elif category == "index-maintenance":
        if "rebuild" in artifact.lower() or "regenerate" in artifact.lower() or "update" in artifact.lower():
            if "skill_index" in artifact.lower() or "index" in artifact.lower():
                pass
            else:
                issues.append("Index update mentioned but not linked to SKILL_INDEX.md")
        else:
            issues.append("No index maintenance guidance after skill operations")
    
    elif category == "end-to-end":
        # Check all major components are referenced
        components = {
            "boot/startup": any(w in artifact.lower() for w in ["session start", "startup", "boot"]),
            "pre-task search": any(w in artifact.lower() for w in ["before starting", "pre-task", "before any task"]),
            "skill loading": "level 1" in artifact.lower() or "full skill" in artifact.lower(),
            "post-task eval": "outcome evaluation" in artifact.lower() or "step 1" in artifact.lower(),
            "refinement": "refinement" in artifact.lower() or "refine" in artifact.lower(),
            "daily log": "daily log" in artifact.lower() or "memory/yyyy" in artifact.lower(),
            "index update": "skill_index" in artifact.lower(),
        }
        for component, found in components.items():
            if not found:
                issues.append(f"End-to-end: missing clear reference to {component}")
    
    # Score
    passed = len(issues) == 0
    return {
        "id": pid,
        "category": category,
        "type": ptype,
        "passed": passed,
        "issues": issues
    }


def run_eval(artifact_path, eval_path):
    artifact = load_artifact(artifact_path)
    evals = load_evals(eval_path)
    
    results = []
    for prompt_data in evals:
        result = check_prompt(artifact, prompt_data)
        results.append(result)
    
    passes = sum(1 for r in results if r["passed"])
    total = len(results)
    score = (passes / total) * 100
    
    print(f"\n{'='*60}")
    print(f"EVAL RESULTS — Score: {score:.1f}% ({passes}/{total})")
    print(f"{'='*60}\n")
    
    # Group by pass/fail
    failures = [r for r in results if not r["passed"]]
    passes_list = [r for r in results if r["passed"]]
    
    print(f"✅ PASSED ({len(passes_list)}):")
    for r in passes_list:
        print(f"  {r['id']} [{r['category']}] ({r['type']})")
    
    print(f"\n❌ FAILED ({len(failures)}):")
    for r in failures:
        print(f"  {r['id']} [{r['category']}] ({r['type']})")
        for issue in r["issues"]:
            print(f"    → {issue}")
    
    # Category breakdown
    print(f"\n{'='*60}")
    print("CATEGORY BREAKDOWN:")
    categories = {}
    for r in results:
        cat = r["category"]
        if cat not in categories:
            categories[cat] = {"pass": 0, "fail": 0}
        if r["passed"]:
            categories[cat]["pass"] += 1
        else:
            categories[cat]["fail"] += 1
    
    for cat, counts in sorted(categories.items()):
        total_cat = counts["pass"] + counts["fail"]
        pct = (counts["pass"] / total_cat) * 100
        status = "✅" if pct == 100 else "⚠️" if pct >= 50 else "❌"
        print(f"  {status} {cat}: {counts['pass']}/{total_cat} ({pct:.0f}%)")
    
    return score, results


if __name__ == "__main__":
    artifact_path = sys.argv[1] if len(sys.argv) > 1 else "autoresearch/artifact.md"
    eval_path = sys.argv[2] if len(sys.argv) > 2 else "autoresearch/eval_prompts.json"
    score, results = run_eval(artifact_path, eval_path)
