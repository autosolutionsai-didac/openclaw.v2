#!/usr/bin/env python3
"""Evaluate supporting files: BOOT, BOOTSTRAP, HEARTBEAT, MEMORY template, SOUL additions, USER additions, skill templates."""
from pathlib import Path
import sys

def check_file(path, checks):
    text = Path(path).read_text() if Path(path).exists() else ""
    lower = text.lower()
    issues = []
    for desc, test in checks:
        if not test(lower, text):
            issues.append(desc)
    return issues

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "."
    all_issues = 0
    
    files = {
        "BOOT.md": (f"{base}/docs/reference/templates/BOOT.md", [
            ("Missing skill index load step", lambda l,t: "skill_index" in l or "skill index" in l),
            ("Missing memory load step", lambda l,t: "memory.md" in l),
            ("Missing USER.md load step", lambda l,t: "user.md" in l),
            ("Missing 'silent' instruction", lambda l,t: "silent" in l or "do not narrate" in l),
            ("Missing graceful handling for missing files", lambda l,t: "doesn't exist" in l or "does not exist" in l or "if it" in l),
            ("No numbered/ordered steps", lambda l,t: "### 1" in t or "step 1" in l),
        ]),
        "BOOTSTRAP.md": (f"{base}/docs/reference/templates/BOOTSTRAP.md", [
            ("Missing identity phase", lambda l,t: "identity" in l and ("soul" in l or "who"  in l)),
            ("Missing work context phase", lambda l,t: "project" in l or "work context" in l or "working on" in l),
            ("Missing preferences phase", lambda l,t: "preference" in l or "timezone" in l),
            ("Missing learning loop orientation", lambda l,t: "learning" in l and ("loop" in l or "system" in l or "skill" in l)),
            ("Missing MEMORY.md seeding", lambda l,t: "memory.md" in l),
            ("Missing USER.md seeding", lambda l,t: "user.md" in l),
            ("Missing confirmation/summary phase", lambda l,t: "confirm" in l or "summary" in l or "complete" in l),
        ]),
        "HEARTBEAT.md": (f"{base}/docs/reference/templates/HEARTBEAT.md", [
            ("Missing skill index rebuild task", lambda l,t: "skill index" in l or "skill_index" in l),
            ("Missing memory compaction task", lambda l,t: "compaction" in l or "compact" in l or "archive" in l),
            ("Missing health report task", lambda l,t: "health report" in l or "report" in l),
            ("Missing frequency guidance (weekly/monthly)", lambda l,t: "weekly" in l or "sunday" in l),
            ("Missing USER.md review in maintenance", lambda l,t: "user.md" in l or "behavioral model" in l),
        ]),
        "MEMORY.structured.md": (f"{base}/docs/reference/templates/MEMORY.structured.md", [
            ("Missing Environment section", lambda l,t: "environment" in l or "infrastructure" in l),
            ("Missing Projects section", lambda l,t: "project" in l),
            ("Missing Learned Patterns section", lambda l,t: "learned pattern" in l or "lesson" in l),
            ("Missing Conventions section", lambda l,t: "convention" in l or "preference" in l),
            ("Missing Open Loops section", lambda l,t: "open loop" in l),
            ("Missing size guidance", lambda l,t: "short" in l or "200 line" in l or "under" in l),
        ]),
        "LEARNED_SKILL_TEMPLATE.md": (f"{base}/skills/templates/LEARNED_SKILL_TEMPLATE.md", [
            ("Missing required frontmatter fields", lambda l,t: all(f in l for f in ["name:", "description:", "category:", "version:", "times_used:", "success_rate:"])),
            ("Missing 'When to Use' section", lambda l,t: "when to use" in l),
            ("Missing 'Approach' section", lambda l,t: "approach" in l or "## approach" in l),
            ("Missing 'Pitfalls' section", lambda l,t: "pitfall" in l),
            ("Missing 'Verification' section", lambda l,t: "verification" in l or "verify" in l),
            ("Missing trigger_patterns in frontmatter", lambda l,t: "trigger_pattern" in l),
            ("Missing state field in frontmatter", lambda l,t: "state:" in l),
        ]),
        "SKILL_INDEX_TEMPLATE.md": (f"{base}/skills/templates/SKILL_INDEX_TEMPLATE.md", [
            ("Missing table format", lambda l,t: "|" in t and "skill" in l),
            ("Missing learned skills section", lambda l,t: "learned" in l),
            ("Missing manual skills section", lambda l,t: "manual" in l),
            ("Missing Level 0 reference", lambda l,t: "level 0" in l),
            ("Missing usage guide for agent", lambda l,t: "usage guide" in l or "session start" in l),
        ]),
        "SOUL.md additions": (f"{base}/docs/reference/templates/SOUL.md", [
            ("Missing learning identity section", lambda l,t: "learning" in l and "growth" in l),
            ("Missing learning boundaries", lambda l,t: "learning boundaries" in l or "never modify soul" in l),
            ("Missing transparency guidance", lambda l,t: "transparency" in l or "mention it" in l),
            ("Missing SOUL.md protection rule", lambda l,t: "soul.md" in l and ("never" in l or "must not" in l or "wins" in l)),
        ]),
        "USER.md additions": (f"{base}/docs/reference/templates/USER.md", [
            ("Missing Behavioral Model section", lambda l,t: "behavioral model" in l),
            ("Missing Communication Patterns subsection", lambda l,t: "communication pattern" in l),
            ("Missing Decision Patterns subsection", lambda l,t: "decision pattern" in l),
            ("Missing Work Rhythms subsection", lambda l,t: "work rhythm" in l),
            ("Missing Feedback Signals subsection", lambda l,t: "feedback signal" in l),
            ("Missing placeholder text for empty sections", lambda l,t: "no patterns observed" in l or "placeholder" in l),
        ]),
    }
    
    print(f"\n{'='*60}")
    print(f"SUPPORTING FILES EVALUATION — {len(files)} files")
    print(f"{'='*60}\n")
    
    total_checks = 0
    for name, (path, checks) in files.items():
        total_checks += len(checks)
        issues = check_file(path, checks)
        if issues:
            all_issues += len(issues)
            print(f"⚠️  {name} — {len(issues)} issues:")
            for i in issues:
                print(f"    → {i}")
        else:
            print(f"✅ {name} — clean ({len(checks)} checks passed)")
    
    score = ((total_checks - all_issues) / total_checks) * 100
    print(f"\n{'='*60}")
    print(f"SCORE: {score:.1f}% ({all_issues} issues across {total_checks} checks)")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
