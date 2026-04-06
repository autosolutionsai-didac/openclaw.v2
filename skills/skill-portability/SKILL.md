---
name: skill-portability
description: >
  Export and import learned skills in agentskills.io-compatible format for portability
  across OpenClaw agents, Claude Code, Cursor, Hermes Agent, and other compatible tools.
  Use when the user asks to "export skills", "share skills between agents", "import a skill",
  "make skills portable", "transfer skills to another agent", "package skills", or
  "sync skills across my agents".
---

# Skill Portability — Export/Import

Learned skills are markdown files with YAML frontmatter — already portable by nature.
This skill standardizes the format for cross-agent and cross-framework compatibility
following the agentskills.io open standard.

## Export: Single Skill

### /skills export [skill-name]

Package a single learned skill for sharing:

1. Read the skill's SKILL.md and any files in references/, templates/, scripts/
2. Validate the skill passes security guard checks (no credentials, no identity mods)
3. Generate an export package:

```
[skill-name]/
├── SKILL.md          # Main instructions (agentskills.io format)
├── references/       # Additional docs (if any)
├── scripts/          # Helper scripts (if any)
└── MANIFEST.md       # Export metadata
```

4. MANIFEST.md contains:

```markdown
---
exported_from: openclaw
exported_date: YYYY-MM-DD
source_agent: <agent-id or "generic">
skill_version: <version>
skill_state: <DRAFT|VALIDATED|MATURE>
times_used: <count>
success_rate: <percentage>
compatible_with:
  - openclaw
  - claude-code
  - cursor
  - hermes-agent
  - codex
requires:
  - <any external tools or APIs the skill depends on>
---

# Export Notes

<Any context about where/how this skill was developed and tested>
```

5. Output the package path for the user to share (via git, zip, or direct copy)

## Export: Skill Pack (Multiple Skills)

### /skills export-pack [category] or /skills export-pack --all

Package multiple skills as a skill pack:

1. Collect all skills matching the category (or all learned skills if --all)
2. Validate each against security guard
3. Create a pack directory:

```
skill-pack-[name]/
├── README.md              # Pack description, contents, install instructions
├── SKILL_INDEX.md         # Index of all included skills
├── [category]/
│   ├── [skill-a]/
│   │   └── SKILL.md
│   └── [skill-b]/
│       └── SKILL.md
└── MANIFEST.md            # Pack-level metadata
```

4. README.md includes:
   - What problem domain the pack covers
   - List of included skills with descriptions
   - Prerequisites (tools, APIs, platforms needed)
   - Install instructions for each target platform

## Import: From File

### /skills import [path-or-url]

Import a skill or skill pack:

1. Read the SKILL.md (or MANIFEST.md for packs)
2. Run security guard validation on ALL content
3. If the skill has a MANIFEST.md, check `compatible_with` includes "openclaw"
4. Present the skill to the user for approval:

```
📦 Import: [skill-name]
Source: [path or URL]
Description: [from SKILL.md frontmatter]
State: IMPORTED (will start as DRAFT)
Security scan: ✅ Clean / ⚠️ [warnings]

Install this skill? [yes/no]
```

5. On approval:
   - Copy to `skills/learned/<category>/<skill-name>/`
   - Set state to DRAFT (regardless of original state — must earn trust locally)
   - Set `times_used: 0`, `success_rate: 0`
   - Add `imported_from` and `imported_date` to frontmatter
   - Update SKILL_INDEX.md
   - Log: "Imported skill: [name] from [source]"

## Import: From ClawHub

### /skills install [clawhub-id]

Install from the OpenClaw skill marketplace:

1. Search ClawHub for the skill ID
2. Download the skill package
3. Follow the same import flow as above (security scan → user approval → install as DRAFT)

## Import: From Hermes Agent

### /skills import-hermes [path-to-hermes-skills]

Import skills from a Hermes Agent installation:

1. Scan `~/.hermes/skills/` (or specified path)
2. Hermes skills use the same SKILL.md + YAML frontmatter format
3. Map Hermes-specific frontmatter fields to OpenClaw equivalents:
   - `disabled` → `state: DEPRECATED` if true
   - `platform_disabled` → note in skill body
   - `required_environment_variables` → add to "Context Requirements"
   - `required_credential_files` → add to "Context Requirements"
4. Import each skill through the standard import flow

## Cross-Agent Skill Sync

For users running multiple OpenClaw agents that should share skills:

### Option A: Shared Skill Directory

Point multiple agents at the same external skill directory:

```json
{
  "agents": {
    "defaults": {
      "skills": {
        "externalPaths": ["~/.shared-skills/learned/"]
      }
    }
  }
}
```

Skills created by any agent go to their local `skills/learned/`. Manually promote
good skills to the shared directory.

### Option B: Git-Based Sync

1. Initialize `skills/learned/` as a git repo (or subdirectory of the workspace repo)
2. After skill creation/refinement, commit and push
3. Other agents pull on session start (add to BOOT.md)
4. Conflict resolution: keep the version with higher `times_used`

### Option C: Export/Import Cycle

Periodically export mature skills from one agent and import into others.
Best for agents with different domains where only select skills should transfer.

## Format Compatibility Reference

| Field | OpenClaw | Hermes | Claude Code | agentskills.io |
|-------|----------|--------|-------------|----------------|
| Main file | SKILL.md | SKILL.md | SKILL.md | SKILL.md |
| Frontmatter | YAML | YAML | YAML | YAML |
| name | ✅ | ✅ | ✅ | ✅ |
| description | ✅ | ✅ | ✅ | ✅ |
| version | ✅ (custom) | ✅ (custom) | ❌ | ✅ |
| state/lifecycle | ✅ (custom) | ❌ | ❌ | ❌ |
| scripts/ | ✅ | ✅ | ❌ | ✅ |
| references/ | ✅ | ✅ | ❌ | ✅ |
| Body format | Markdown | Markdown | Markdown | Markdown |

The core SKILL.md + YAML frontmatter format is universally compatible.
OpenClaw-specific fields (state, times_used, success_rate) are ignored by
other tools — they don't break compatibility, they just aren't used.
