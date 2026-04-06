#!/usr/bin/env python3
"""
Round 2 evaluator — harder prompts testing gaps, edge cases, and cross-file interactions.
Also tests ALL skills and supporting files, not just AGENTS.md additions.
"""
import json, sys, os
from pathlib import Path

def load(path):
    return Path(path).read_text() if Path(path).exists() else ""

def run_eval(base_dir):
    # Load all artifacts that make up the learning loop system
    agents = load(f"{base_dir}/docs/reference/templates/AGENTS.md")
    soul = load(f"{base_dir}/docs/reference/templates/SOUL.md")
    user = load(f"{base_dir}/docs/reference/templates/USER.md")
    boot = load(f"{base_dir}/docs/reference/templates/BOOT.md")
    bootstrap = load(f"{base_dir}/docs/reference/templates/BOOTSTRAP.md")
    heartbeat = load(f"{base_dir}/docs/reference/templates/HEARTBEAT.md")
    memory_tmpl = load(f"{base_dir}/docs/reference/templates/MEMORY.structured.md")
    skill_template = load(f"{base_dir}/skills/templates/LEARNED_SKILL_TEMPLATE.md")
    skill_index_tmpl = load(f"{base_dir}/skills/templates/SKILL_INDEX_TEMPLATE.md")
    skill_manager = load(f"{base_dir}/skills/skill-manager/SKILL.md")
    skill_security = load(f"{base_dir}/skills/skill-security-guard/SKILL.md")
    skill_portability = load(f"{base_dir}/skills/skill-portability/SKILL.md")
    skill_diagnostics = load(f"{base_dir}/skills/learning-diagnostics/SKILL.md")
    skill_memory_search = load(f"{base_dir}/skills/memory-search-enhanced/SKILL.md")
    skill_autoresearch = load(f"{base_dir}/skills/skill-autoresearch-polish/SKILL.md")
    
    ALL = agents + soul + user + boot + bootstrap + heartbeat + memory_tmpl + skill_template + skill_index_tmpl + skill_manager + skill_security + skill_portability + skill_diagnostics + skill_memory_search + skill_autoresearch
    all_lower = ALL.lower()
    
    evals = json.loads(load(f"{base_dir}/autoresearch/eval_prompts_r2.json"))
    results = []
    
    for p in evals:
        pid, cat = p["id"], p["category"]
        issues = []
        
        if cat == "context-window-pressure":
            if not any(w in all_lower for w in ["context window", "context limit", "bootstraptotalmaxchars", "compaction", "truncat"]):
                issues.append("No guidance on context window pressure or what to do when approaching limits")
            if not any(w in all_lower for w in ["prioritiz", "skip", "truncat"]):
                issues.append("No guidance on prioritizing what to load under pressure")
                
        elif cat == "skill-conflict":
            if not any(w in all_lower for w in ["conflict", "contradict", "overlapping"]):
                issues.append("No guidance on handling conflicting skills")
            if "at most 2 skills" not in all_lower and "max 2" not in all_lower and "load at most" not in all_lower:
                # Check variations
                if not any(w in all_lower for w in ["most 2 skill", "max 2 full", "limit to 2", "load at most 2"]):
                    issues.append("No limit on how many full skills to load per task")
                    
        elif cat == "multi-agent-skill-sync":
            if not any(w in all_lower for w in ["shared skill directory", "git-based sync", "export/import", "cross-agent", "multiple agent"]):
                issues.append("No multi-agent skill sharing guidance")
            if "draft" not in all_lower or "imported" not in all_lower:
                if "import" in all_lower and "draft" in all_lower:
                    pass
                else:
                    issues.append("No mention that imported skills start as DRAFT")
                    
        elif cat == "learning-loop-overhead":
            if "5 or more tool calls" in all_lower or "5+" in all_lower or "5 or more" in all_lower:
                pass
            else:
                issues.append("Tool call threshold for learning loop not clearly stated")
                
        elif cat == "skill-sprawl":
            if not any(w in all_lower for w in ["sprawl", "too many", "curati", "aggressive"]):
                if "hygiene" in all_lower and "deprecat" in all_lower:
                    pass  # hygiene cycle covers this
                else:
                    issues.append("No guidance on handling skill sprawl (too many skills)")
            if "3,000" not in ALL and "3k" not in all_lower and "~3k" not in all_lower:
                issues.append("No target token budget for skill index")
                
        elif cat == "partial-outcome-chain":
            if "partial" in all_lower and "0.5" in ALL:
                pass
            else:
                issues.append("PARTIAL outcome counting formula not specified")
                
        elif cat == "bootstrap-cold-start":
            if "doesn't exist" in all_lower or "does not exist" in all_lower or "if it doesn't" in all_lower:
                pass
            else:
                if "create" in all_lower and "index" in all_lower:
                    pass  # mentions creating index if needed
                else:
                    issues.append("No graceful handling for missing files on cold start")
            if "bootstrap" in all_lower:
                pass
            else:
                issues.append("BOOTSTRAP.md not referenced for initial setup")
                
        elif cat == "security-evasion":
            if "~/.ssh" in ALL or ".ssh" in all_lower:
                pass
            else:
                if "credential" in all_lower and ("store" in all_lower or "path" in all_lower):
                    pass
                else:
                    issues.append("No mention of blocking references to credential store paths like ~/.ssh/")
                    
        elif cat == "skill-over-extraction":
            if any(w in all_lower for w in ["genuinely reusable", "don't over-extract", "routine task"]):
                pass
            else:
                issues.append("No quality gate against over-extraction of trivial patterns")
                
        elif cat == "concurrent-skill-creation":
            if not any(w in all_lower for w in ["user's message", "user's needs", "priority", "urgent"]):
                issues.append("No guidance on prioritizing user messages over learning loop operations")
                
        elif cat == "cross-skill-learning":
            if any(w in all_lower for w in ["cross-skill", "meta-pattern", "category-level readme", "shared pattern"]):
                pass
            else:
                issues.append("No cross-skill learning guidance (extracting patterns shared across skills in same category)")
                
        elif cat == "stale-index":
            if any(w in all_lower for w in ["after creating", "after refining", "regenerate the relevant row", "rebuild"]):
                if "skill_index" in all_lower:
                    pass
                else:
                    issues.append("Index rebuild mentioned but not linked to SKILL_INDEX.md")
            else:
                issues.append("No instruction to update index immediately after skill operations")
                
        elif cat == "token-efficiency":
            if "3+ steps" in ALL or "non-trivial" in all_lower:
                pass  # pre-task search scoped to non-trivial
            else:
                issues.append("Pre-task skill search not scoped to non-trivial tasks — could waste tokens on simple queries")
                
        elif cat == "user-override":
            if not any(w in all_lower for w in ["user override", "don't follow blindly", "not blindly", "user's request"]):
                if "guidance" in all_lower or "inform your approach" in all_lower:
                    pass  # framed as guidance not mandate
                else:
                    issues.append("Skills not explicitly framed as guidance that user can override")
                    
        elif cat == "memory-bloat":
            if any(w in all_lower for w in ["200 lines", "under 200", "keep this file short", "keep memory.md short"]):
                pass
            else:
                if "short" in all_lower and "memory" in all_lower:
                    pass
                else:
                    issues.append("No explicit size limit or target for MEMORY.md")
            if "archive" in all_lower and ("30 day" in all_lower or "older than" in all_lower):
                pass
            else:
                issues.append("No archival guidance for old daily logs")
                
        elif cat == "skill-template-compliance":
            if "pitfall" in all_lower:
                # Check if template allows empty pitfalls
                if "no pitfall" in all_lower or "none" in all_lower:
                    pass
                else:
                    issues.append("Template doesn't explicitly allow empty Pitfalls section with placeholder text")
            else:
                issues.append("Pitfalls section not mentioned in template context")
                
        elif cat == "adversarial-injection":
            if "exfiltration" in all_lower or "data exfil" in all_lower:
                if "block" in all_lower or "reject" in all_lower or "prevent" in all_lower:
                    pass
                else:
                    issues.append("Data exfiltration mentioned but no clear BLOCK action")
            else:
                issues.append("No data exfiltration scanning for imported skills")
                
        elif cat == "diagnostics":
            if "diagnos" in all_lower or "/learning status" in all_lower or "/learning diagnose" in all_lower:
                pass
            else:
                issues.append("No diagnostic capability for debugging the learning loop itself")
                
        elif cat == "heartbeat-conflict":
            if not any(w in all_lower for w in ["in-progress", "mid-write", "conflict", "concurrent", "skip"]):
                issues.append("No guidance on handling concurrent access to skill files during heartbeat rebuild")
                
        elif cat == "end-to-end-failure":
            components = {
                "post-task eval triggers": "outcome evaluation" in all_lower or "step 1" in all_lower,
                "finds existing skill": "matching skill" in all_lower or "existing skill" in all_lower,
                "refines not creates": "refinement" in all_lower,
                "adds pitfall": "pitfall" in all_lower,
                "increments version": "increment" in all_lower and "version" in all_lower,
                "updates index": "skill_index" in all_lower,
                "structured daily log": "structured format" in all_lower or "structured daily" in all_lower,
            }
            for comp, found in components.items():
                if not found:
                    issues.append(f"End-to-end: missing {comp}")
        
        results.append({
            "id": pid, "category": cat, "type": p["type"],
            "passed": len(issues) == 0, "issues": issues
        })
    
    passes = sum(1 for r in results if r["passed"])
    total = len(results)
    score = (passes / total) * 100
    
    print(f"\n{'='*60}")
    print(f"ROUND 2 EVAL — Score: {score:.1f}% ({passes}/{total})")
    print(f"{'='*60}\n")
    
    failures = [r for r in results if not r["passed"]]
    passes_list = [r for r in results if r["passed"]]
    
    print(f"✅ PASSED ({len(passes_list)}):")
    for r in passes_list:
        print(f"  {r['id']} [{r['category']}]")
    
    print(f"\n❌ FAILED ({len(failures)}):")
    for r in failures:
        print(f"  {r['id']} [{r['category']}]")
        for issue in r["issues"]:
            print(f"    → {issue}")
    
    return score, results

if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "."
    run_eval(base)
