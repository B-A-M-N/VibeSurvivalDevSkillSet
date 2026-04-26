#!/usr/bin/env python3
"""Generate SKILL-IMPLEMENTATIONS.md for all skill folders."""
import os
import re

SKILLS_DIR = "skills"

SYSTEMS = {
    "specforge": "SpecForge System",
    "researchforge": "ResearchForge System",
    "skill-forge": "SkillForge System",
    "vibe-continuity": "Continuity & Overlord System",
    "overlord": "Continuity & Overlord System",
    "mistral-vibe-compaction-skill": "Continuity & Overlord System",
}

def read_skill_md(path):
    with open(path, 'r') as f:
        content = f.read()
    m = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not m:
        return {}, ""
    frontmatter_text, body = m.groups()
    fm = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            k, _, v = line.partition(':')
            fm[k.strip()] = v.strip().strip('"').strip('|').strip()
    return fm, body.strip()

def get_system(name):
    for key, system in SYSTEMS.items():
        if key in name:
            return system
    return None

def generate_implementation_md(skill_path, skill_name):
    skill_md_path = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md_path):
        return None

    fm, body = read_skill_md(skill_md_path)
    description = fm.get('description', '')
    tools = fm.get('allowed-tools', [])

    system = get_system(skill_name)

    lines = []
    lines.append("# {} -- Implementation Guide".format(skill_name))
    lines.append("=" * (len(skill_name) + 25))
    lines.append("")
    lines.append("## Skill Description")
    lines.append("")
    lines.append(description or "No description provided.")
    lines.append("")

    # Standalone use
    lines.append("## Standalone Use")
    lines.append("")
    lines.append("**Invoke:** `/{}` (if user-invocable) or via skill manager".format(skill_name))
    lines.append("")
    lines.append("**What it does on its own:**")
    lines.append("- " + (description or "See SKILL.md for details"))
    lines.append("")

    # Tools
    if tools:
        if isinstance(tools, list):
            tool_str = ", ".join(tools)
        else:
            tool_str = str(tools)
        lines.append("**Tools used:** " + tool_str)
        lines.append("")

    # Combine with other systems
    lines.append("## Combine With Other Systems")
    lines.append("")

    if system == "SpecForge System":
        lines.append("**Part of:** SpecForge System (Phase skill)")
        lines.append("")
        lines.append("**Combine with:**")
        lines.append("- **ResearchForge** -- use research findings to inform spec writing")
        lines.append("- **SkillForge** -- package this spec skill as a reusable component")
        lines.append("- **Continuity System** -- ensure spec work survives compaction")
        lines.append("")
    elif system == "ResearchForge System":
        lines.append("**Part of:** ResearchForge System (Phase skill)")
        lines.append("")
        lines.append("**Combine with:**")
        lines.append("- **SpecForge** -- feed research into spec generation")
        lines.append("- **SkillForge** -- package this research skill as a reusable component")
        lines.append("- **Continuity System** -- ensure research work survives compaction")
        lines.append("")
    elif system == "SkillForge System":
        lines.append("**Part of:** SkillForge System (Runtime-activated skill)")
        lines.append("")
        lines.append("**Combine with:**")
        lines.append("- **SpecForge** -- use SkillForge to create new spec skills")
        lines.append("- **ResearchForge** -- use SkillForge to create new research skills")
        lines.append("- **Continuity System** -- SkillForge uses state snapshots for recovery")
        lines.append("")
    elif system == "Continuity & Overlord System":
        lines.append("**Part of:** Continuity & Overlord System")
        lines.append("")
        lines.append("**Combine with:**")
        lines.append("- **SpecForge** -- maintain continuity during long spec runs")
        lines.append("- **ResearchForge** -- maintain continuity during long research runs")
        lines.append("- **SkillForge** -- same runtime activation pattern (state snapshot + restore)")
        lines.append("")
    else:
        lines.append("**Standalone skill** -- not part of a specific system.")
        lines.append("")
        lines.append("**Combine with:**")
        lines.append("- **SpecForge** -- use as a quality gate during spec construction")
        lines.append("- **ResearchForge** -- use during evidence collection or validation")
        lines.append("- **SkillForge** -- use SkillForge to create variations of this skill")
        lines.append("- **Continuity System** -- pair with vibe-continuity for long sessions")
        lines.append("- **Overlord** -- let overlord delegate this skill to a sub-agent")
        lines.append("")

    # Integration examples
    lines.append("## Integration Examples")
    lines.append("")
    lines.append("### Example 1: Standalone Invocation")
    lines.append("```bash")
    lines.append("/{}".format(skill_name))
    lines.append("```")
    lines.append("")
    lines.append("### Example 2: Part of a Larger Workflow")
    lines.append("```")
    lines.append("1. Run /{}".format(skill_name))
    lines.append("2. Review output")
    lines.append("3. Continue with next step in your workflow")
    lines.append("```")
    lines.append("")

    # Tips
    lines.append("## Tips")
    lines.append("")
    lines.append("- Read the SKILL.md in this folder for full instructions")
    lines.append("- Check allowed-tools to understand what this skill can access")
    lines.append("- Combine with team agents (team-dev, team-ops, team-verify) for complex workflows")
    lines.append("")

    return "\n".join(lines)

def main():
    count = 0
    for root, dirs, files in os.walk(SKILLS_DIR):
        if "SKILL.md" in files:
            skill_name = os.path.basename(root)
            impl_path = os.path.join(root, "SKILL-IMPLEMENTATIONS.md")
            if os.path.exists(impl_path):
                print("  Skipping (exists): {}".format(impl_path))
                continue
            content = generate_implementation_md(root, skill_name)
            if content:
                with open(impl_path, 'w') as f:
                    f.write(content)
                count += 1
                print("  Created: {}".format(impl_path))
    print("\nDone. Created {} SKILL-IMPLEMENTATIONS.md files.".format(count))

if __name__ == "__main__":
    main()
