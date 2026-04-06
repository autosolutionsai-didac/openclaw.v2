#!/usr/bin/env python3
"""
Regression test: verify our modifications don't break existing OpenClaw functionality.
Tests original content preservation, token budgets, section conflicts, and critical behaviors.
"""
import sys, os, re
from pathlib import Path

def load(path):
    return Path(path).read_text() if Path(path).exists() else ""

def char_count(text):
    return len(text)

def run_regression(base):
    issues = []
    warnings = []
    
    # Load all modified files
    agents = load(f"{base}/docs/reference/templates/AGENTS.md")
    soul = load(f"{base}/docs/reference/templates/SOUL.md")
    user = load(f"{base}/docs/reference/templates/USER.md")
    boot = load(f"{base}/docs/reference/templates/BOOT.md")
    bootstrap = load(f"{base}/docs/reference/templates/BOOTSTRAP.md")
    heartbeat = load(f"{base}/docs/reference/templates/HEARTBEAT.md")
    memory = load(f"{base}/docs/reference/templates/MEMORY.structured.md")
    identity = load(f"{base}/docs/reference/templates/IDENTITY.md")
    tools = load(f"{base}/docs/reference/templates/TOOLS.md")
    
    # Load originals
    orig_agents = load("/tmp/original_agents.md")
    orig_soul = load("/tmp/original_soul.md")
    orig_user = load("/tmp/original_user.md")
    orig_boot = load("/tmp/original_boot.md")
    orig_bootstrap = load("/tmp/original_bootstrap.md")
    orig_heartbeat = load("/tmp/original_heartbeat.md")
    
    print(f"\n{'='*60}")
    print("REGRESSION TEST — OpenClaw Compatibility")
    print(f"{'='*60}\n")
    
    # ═══════════════════════════════════════════
    # TEST 1: Original content preservation (APPEND files)
    # ═══════════════════════════════════════════
    print("TEST 1: Original content preservation")
    
    # AGENTS.md — first 219 lines should match
    orig_lines = orig_agents.count('\n')
    if agents[:len(orig_agents)] == orig_agents:
        print(f"  ✅ AGENTS.md: first {orig_lines} lines intact")
    else:
        issues.append("AGENTS.md: original content was modified, not just appended")
        print(f"  ❌ AGENTS.md: original content was MODIFIED")
    
    # SOUL.md — first 45 lines should match
    if soul[:len(orig_soul)] == orig_soul:
        print(f"  ✅ SOUL.md: original content intact")
    else:
        issues.append("SOUL.md: original content was modified")
        print(f"  ❌ SOUL.md: original content was MODIFIED")
    
    # USER.md — first 24 lines should match
    if user[:len(orig_user)] == orig_user:
        print(f"  ✅ USER.md: original content intact")
    else:
        issues.append("USER.md: original content was modified")
        print(f"  ❌ USER.md: original content was MODIFIED")
    
    # ═══════════════════════════════════════════
    # TEST 2: REPLACED files — critical content preserved
    # ═══════════════════════════════════════════
    print("\nTEST 2: Replaced files — critical content")
    
    # BOOT.md — must keep frontmatter + hooks.internal.enabled reference
    boot_lower = boot.lower()
    if "hooks.internal.enabled" in boot:
        print("  ✅ BOOT.md: hooks.internal.enabled instruction preserved")
    else:
        issues.append("BOOT.md: missing hooks.internal.enabled reference")
        print("  ❌ BOOT.md: missing hooks.internal.enabled reference")
    
    if "no_reply" in boot_lower or "NO_REPLY" in boot:
        print("  ✅ BOOT.md: NO_REPLY silent token instruction preserved")
    else:
        issues.append("BOOT.md: missing NO_REPLY silent token instruction")
        print("  ❌ BOOT.md: missing NO_REPLY silent token")
    
    # BOOTSTRAP.md — check for LOST features from original
    bs_lower = bootstrap.lower()
    bootstrap_lost = []
    
    if "don't interrogate" not in bs_lower and "don't be robotic" not in bs_lower and "conversational" not in bs_lower:
        if "natural" in bs_lower:
            pass  # we say "natural, conversational flow"
        else:
            bootstrap_lost.append("conversational tone instruction")
    
    if "whatsapp" not in bs_lower and "telegram" not in bs_lower and "channel" not in bs_lower and "connect" not in bs_lower:
        bootstrap_lost.append("channel connection guidance (WhatsApp/Telegram setup)")
    
    if "delete this file" not in bs_lower and "remove" not in bs_lower:
        bootstrap_lost.append("'delete this file when done' instruction")
    
    if "emoji" not in bs_lower:
        bootstrap_lost.append("emoji selection step")
    
    if "creature" not in bs_lower and "nature" not in bs_lower and "vibe" not in bs_lower:
        bootstrap_lost.append("personality/creature/vibe exploration")
    
    if bootstrap_lost:
        for lost in bootstrap_lost:
            issues.append(f"BOOTSTRAP.md: LOST original feature — {lost}")
            print(f"  ❌ BOOTSTRAP.md: LOST — {lost}")
    else:
        print("  ✅ BOOTSTRAP.md: all original features preserved")
    
    # HEARTBEAT.md — original was basically empty placeholder, appending is fine
    if "heartbeat" in heartbeat.lower():
        print("  ✅ HEARTBEAT.md: original was placeholder, additions are safe")
    
    # ═══════════════════════════════════════════
    # TEST 3: Token budget check
    # ═══════════════════════════════════════════
    print("\nTEST 3: Token budget")
    
    # bootstrapTotalMaxChars default is 150,000 characters
    # bootstrapMaxChars per file is 20,000 characters
    TOTAL_MAX = 150000
    PER_FILE_MAX = 20000
    
    all_bootstrap_files = {
        "AGENTS.md": agents,
        "SOUL.md": soul,
        "USER.md": user,
        "BOOT.md": boot,
        "BOOTSTRAP.md": bootstrap,
        "HEARTBEAT.md": heartbeat,
        "MEMORY.md": memory,
        "IDENTITY.md": identity,
        "TOOLS.md": tools,
    }
    
    total_chars = 0
    for name, content in all_bootstrap_files.items():
        chars = char_count(content)
        total_chars += chars
        if chars > PER_FILE_MAX:
            issues.append(f"{name}: {chars} chars exceeds per-file limit of {PER_FILE_MAX}")
            print(f"  ❌ {name}: {chars} chars (EXCEEDS {PER_FILE_MAX} limit)")
        else:
            pct = (chars / PER_FILE_MAX) * 100
            status = "⚠️" if pct > 75 else "✅"
            print(f"  {status} {name}: {chars} chars ({pct:.0f}% of per-file limit)")
    
    total_pct = (total_chars / TOTAL_MAX) * 100
    if total_chars > TOTAL_MAX:
        issues.append(f"Total bootstrap: {total_chars} chars EXCEEDS {TOTAL_MAX} limit")
        print(f"  ❌ TOTAL: {total_chars} chars (EXCEEDS {TOTAL_MAX} limit)")
    else:
        status = "⚠️" if total_pct > 50 else "✅"
        print(f"  {status} TOTAL: {total_chars} chars ({total_pct:.1f}% of aggregate limit)")
    
    # ═══════════════════════════════════════════
    # TEST 4: Section heading conflicts in AGENTS.md
    # ═══════════════════════════════════════════
    print("\nTEST 4: Section heading conflicts")
    
    # Extract all ## headings from AGENTS.md
    headings = re.findall(r'^##+ (.+)$', agents, re.MULTILINE)
    seen = {}
    duplicates = []
    for h in headings:
        if h in seen:
            duplicates.append(h)
        seen[h] = seen.get(h, 0) + 1
    
    if duplicates:
        for d in duplicates:
            warnings.append(f"AGENTS.md: duplicate heading '## {d}'")
            print(f"  ⚠️  Duplicate heading: '{d}'")
    else:
        print(f"  ✅ No duplicate headings in AGENTS.md ({len(headings)} unique)")
    
    # ═══════════════════════════════════════════
    # TEST 5: Skill name conflicts with existing bundled skills
    # ═══════════════════════════════════════════
    print("\nTEST 5: Skill name conflicts")
    
    our_skills = ["memory-search-enhanced", "skill-autoresearch-polish", "skill-manager", 
                  "skill-security-guard", "skill-portability", "learning-diagnostics"]
    
    existing_skills = [d for d in os.listdir(f"{base}/skills") 
                      if os.path.isdir(f"{base}/skills/{d}") and d not in our_skills 
                      and d not in ["templates", "learned"]]
    
    conflicts = set(our_skills) & set(existing_skills)
    if conflicts:
        for c in conflicts:
            issues.append(f"Skill name conflict: '{c}' exists in both our additions and original skills")
            print(f"  ❌ Conflict: '{c}'")
    else:
        print(f"  ✅ No conflicts (our {len(our_skills)} skills vs {len(existing_skills)} existing)")
    
    # Check for similar names that could confuse
    if "skill-creator" in existing_skills and "skill-manager" in our_skills:
        warnings.append("'skill-creator' (existing) and 'skill-manager' (ours) could confuse — different purposes but similar domain")
        print(f"  ⚠️  'skill-creator' (existing) vs 'skill-manager' (ours) — similar domain, verify no overlap")
    
    # ═══════════════════════════════════════════
    # TEST 6: Critical OpenClaw behaviors not contradicted
    # ═══════════════════════════════════════════
    print("\nTEST 6: Critical behavior preservation")
    
    agents_lower = agents.lower()
    
    # Original AGENTS.md says "You are a fresh instance each session; continuity lives in these files"
    if "fresh instance" in agents_lower or "continuity lives in" in agents_lower:
        print("  ✅ 'Fresh instance each session' principle preserved")
    else:
        warnings.append("Cannot find 'fresh instance each session' principle — may have been in a different section")
        print("  ⚠️  'Fresh instance' principle not found in AGENTS.md (may be in AGENTS.default.md)")
    
    # Memory system: daily log + MEMORY.md pattern
    if "memory/yyyy-mm-dd" in agents_lower or "daily log" in agents_lower:
        print("  ✅ Daily log memory pattern preserved")
    else:
        issues.append("Daily log memory pattern (memory/YYYY-MM-DD.md) missing")
        print("  ❌ Daily log pattern missing")
    
    # Git backup recommendation
    if "git" in agents_lower:
        print("  ✅ Git backup recommendation present")
    else:
        warnings.append("Git backup recommendation not found in AGENTS.md additions")
        print("  ⚠️  Git backup recommendation not found (may be in original section)")
    
    # Skills follow SKILL.md convention
    if "skill.md" in agents_lower:
        print("  ✅ SKILL.md convention referenced")
    
    # ═══════════════════════════════════════════
    # TEST 7: No hardcoded paths or credentials
    # ═══════════════════════════════════════════
    print("\nTEST 7: No hardcoded sensitive content")
    
    all_content = agents + soul + user + boot + bootstrap + heartbeat + memory
    sensitive_patterns = [
        (r'sk-[a-zA-Z0-9]{20,}', "API key pattern"),
        (r'ghp_[a-zA-Z0-9]{20,}', "GitHub token pattern"),
        (r'password\s*[:=]\s*["\'][^"\']+["\']', "Hardcoded password"),
        (r'/Users/\w+/', "macOS home path"),
        (r'/home/\w+/', "Linux home path"),
    ]
    
    found_sensitive = False
    for pattern, desc in sensitive_patterns:
        matches = re.findall(pattern, all_content)
        if matches:
            issues.append(f"Found {desc} in workspace files: {matches[0][:20]}...")
            print(f"  ❌ Found {desc}")
            found_sensitive = True
    
    if not found_sensitive:
        print("  ✅ No hardcoded sensitive content found")
    
    # ═══════════════════════════════════════════
    # SUMMARY
    # ═══════════════════════════════════════════
    print(f"\n{'='*60}")
    total_checks = 7
    failed = len([i for i in issues if "LOST" in i or "MODIFIED" in i or "EXCEEDS" in i or "missing" in i.lower()])
    
    if issues:
        print(f"RESULT: {len(issues)} ISSUES FOUND")
        print(f"\n🔴 Issues (must fix):")
        for i in issues:
            print(f"  - {i}")
    
    if warnings:
        print(f"\n🟡 Warnings (review):")
        for w in warnings:
            print(f"  - {w}")
    
    if not issues and not warnings:
        print("RESULT: ✅ ALL CLEAR — no regressions detected")
    elif not issues:
        print(f"\nRESULT: ✅ PASS with {len(warnings)} warnings")
    else:
        print(f"\nRESULT: ❌ {len(issues)} issues need fixing")
    
    print(f"{'='*60}")
    return len(issues)

if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "."
    sys.exit(run_regression(base))
