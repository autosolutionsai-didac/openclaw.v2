#!/usr/bin/env python3
"""
Evaluate all 6 learning loop skills for completeness, consistency, and quality.
Checks: frontmatter compliance, cross-references, actionability, edge case coverage.
"""
import yaml, sys, re
from pathlib import Path

SKILLS = [
    "skills/memory-search-enhanced/SKILL.md",
    "skills/skill-autoresearch-polish/SKILL.md",
    "skills/skill-manager/SKILL.md",
    "skills/skill-security-guard/SKILL.md",
    "skills/skill-portability/SKILL.md",
    "skills/learning-diagnostics/SKILL.md",
]

REQUIRED_FRONTMATTER = ["name", "description"]

def extract_frontmatter(text):
    match = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except:
            return None
    return None

def eval_skill(path):
    text = Path(path).read_text()
    lower = text.lower()
    name = Path(path).parent.name
    issues = []
    
    # 1. Frontmatter checks
    fm = extract_frontmatter(text)
    if not fm:
        issues.append("CRITICAL: No valid YAML frontmatter")
    else:
        for field in REQUIRED_FRONTMATTER:
            if field not in fm:
                issues.append(f"Missing required frontmatter field: {field}")
        if fm.get("description") and len(fm["description"]) < 20:
            issues.append("Description too short for reliable triggering (<20 chars)")
        if fm.get("description") and len(fm["description"]) > 500:
            issues.append("Description too long — may waste tokens on trigger matching (>500 chars)")
    
    # 2. Trigger patterns — does description contain trigger phrases?
    desc = fm.get("description", "") if fm else ""
    if "use when" not in desc.lower() and "trigger" not in desc.lower():
        issues.append("Description missing trigger phrases ('Use when...')")
    
    # 3. Actionability — does the skill have concrete steps/commands?
    has_steps = bool(re.search(r'\d+\..*\n', text))  # numbered steps
    has_commands = bool(re.search(r'/\w+', text))  # slash commands
    has_code = "```" in text  # code blocks
    if not has_steps and not has_commands:
        issues.append("No numbered steps or slash commands — may lack actionability")
    
    # 4. Cross-references to other learning loop files
    cross_refs = {
        "SKILL_INDEX.md": "skill_index" in lower or "skill index" in lower,
        "MEMORY.md": "memory.md" in lower,
        "AGENTS.md": "agents.md" in lower,
        "daily logs": "daily log" in lower or "memory/yyyy" in lower,
    }
    # Not all skills need all cross-refs, but check for obvious gaps
    if name == "memory-search-enhanced" and not cross_refs["SKILL_INDEX.md"]:
        issues.append("Memory search skill should reference SKILL_INDEX.md")
    if name == "learning-diagnostics" and not cross_refs["daily logs"]:
        issues.append("Diagnostics skill should reference daily logs")
    if name == "skill-manager" and not cross_refs["SKILL_INDEX.md"]:
        issues.append("Skill manager should reference SKILL_INDEX.md")
    
    # 5. Edge case coverage
    if "error" not in lower and "fail" not in lower and "edge" not in lower:
        issues.append("No error handling or edge case guidance")
    
    # 6. Security awareness (for relevant skills)
    if name == "skill-security-guard":
        security_checks = ["credential", "identity", "exfiltration", "injection", "destructive"]
        for check in security_checks:
            if check not in lower:
                issues.append(f"Security guard missing check category: {check}")
    
    if name == "skill-portability":
        if "security" not in lower and "scan" not in lower:
            issues.append("Portability skill should reference security scanning on import")
        if "draft" not in lower:
            issues.append("Portability skill should note imported skills start as DRAFT")
    
    # 7. Token efficiency — is the skill concise?
    line_count = len(text.split("\n"))
    if line_count > 250:
        issues.append(f"Skill is {line_count} lines — consider splitting or condensing for token efficiency")
    
    # 8. Consistency with AGENTS.md protocol
    if name == "skill-manager":
        states = ["draft", "validated", "mature", "deprecated"]
        for state in states:
            if state not in lower:
                issues.append(f"Skill manager missing lifecycle state: {state.upper()}")
    
    return {"name": name, "path": path, "issues": issues, "lines": line_count}


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "."
    
    total_issues = 0
    total_skills = 0
    
    print(f"\n{'='*60}")
    print(f"SKILL EVALUATION — {len(SKILLS)} skills")
    print(f"{'='*60}\n")
    
    for skill_path in SKILLS:
        full_path = f"{base}/{skill_path}"
        if not Path(full_path).exists():
            print(f"⚠️  MISSING: {skill_path}")
            continue
        
        result = eval_skill(full_path)
        total_skills += 1
        
        if result["issues"]:
            total_issues += len(result["issues"])
            print(f"⚠️  {result['name']} ({result['lines']} lines) — {len(result['issues'])} issues:")
            for issue in result["issues"]:
                print(f"    → {issue}")
        else:
            print(f"✅ {result['name']} ({result['lines']} lines) — clean")
    
    score = ((total_skills * 8 - total_issues) / (total_skills * 8)) * 100  # 8 checks per skill
    score = max(0, score)
    
    print(f"\n{'='*60}")
    print(f"SCORE: {score:.1f}% ({total_issues} issues across {total_skills} skills)")
    print(f"{'='*60}")
    
    return score

if __name__ == "__main__":
    main()
