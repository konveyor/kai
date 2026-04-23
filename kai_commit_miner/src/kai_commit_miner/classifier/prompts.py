"""Prompt templates for LLM classification."""

from kai_commit_miner.attribution.models import AttributedFix, UnattributedChange
from kai_mcp_solution_server.db.python_objects import ViolationID

_MAX_SAMPLE_INCIDENTS = 5


def build_hint_prompt(
    migration_description: str,
    violation_key: ViolationID,
    violation_description: str,
    attributed_fixes: list[AttributedFix],
    commit_before: str,
    commit_after: str,
    existing_hint: str | None = None,
) -> str:
    """Build a prompt for generating a hint that adds value beyond the rule itself."""
    ranked = sorted(
        attributed_fixes,
        key=lambda f: (
            len(f.relevant_hunks) > 0,
            len(f.context_hunks) > 0,
            not f.indirect,
        ),
        reverse=True,
    )
    sample = ranked[:_MAX_SAMPLE_INCIDENTS]
    total = len(attributed_fixes)

    # Collect a sample incident message for the "what agent knows" section
    sample_message = ""
    for f in sample:
        if f.incident.message:
            sample_message = f.incident.message
            break

    prompt = (
        f"You are building a knowledge base for AI coding agents that perform "
        f"code migrations.\n\n"
        f"**Migration:** {migration_description}\n\n"
        f"## What the agent ALREADY sees (DO NOT repeat any of this)\n"
        f"When the agent encounters this violation, it has:\n"
        f"- **Rule ID:** {violation_key.violation_name}\n"
        f"- **Rule description:** {violation_description}\n"
        f"- **Incident message** (example): {sample_message}\n"
        f"- **Code snippet:** the exact flagged line of code\n"
        f"- **File path and line number**\n\n"
        f"The agent can already read the rule description and incident message. "
        f"DO NOT restate what the violation is or what the basic fix looks like "
        f"-- the agent already knows that.\n\n"
    )

    if existing_hint:
        prompt += (
            f"## Previously generated hint\n"
            f"```\n{existing_hint}\n```\n\n"
            f"If this hint already covers the patterns below, respond with: "
            f"`SKIP: <reason>`\n\n"
        )

    prompt += (
        f"## How a developer actually fixed {total} instance(s) of this violation\n"
    )

    for i, fix in enumerate(sample, 1):
        prompt += f"\n### Example {i}: `{fix.file_path}`\n"

        if fix.relevant_hunks:
            prompt += "**The fix:**\n"
            for hunk in fix.relevant_hunks[:2]:
                prompt += f"```diff\n{hunk.content}\n```\n"

        if fix.context_hunks:
            prompt += (
                f"**Other changes in the same file** "
                f"({len(fix.context_hunks)} hunks):\n"
            )
            for hunk in fix.context_hunks[:3]:
                prompt += f"```diff\n{hunk.content}\n```\n"

        if fix.indirect:
            prompt += (
                "*Resolved indirectly (dependency/config change, not a code edit).*\n"
            )

    if total > len(sample):
        prompt += f"\n*({total - len(sample)} more similar incidents omitted)*\n"

    prompt += (
        "\n## What your hint should ADD\n"
        "Your hint teaches the agent things it CANNOT learn from the rule alone:\n"
        "- **Gotchas:** what breaks if you do the obvious fix wrong?\n"
        "- **Ordering:** does this need to happen before/after other migration steps?\n"
        "- **Accompanying changes:** what else must change in the same file or project "
        "that the rule doesn't mention? (new imports, config entries, dependency changes)\n"
        "- **Variations:** are there non-obvious variants of this pattern the rule misses?\n\n"
        "If the rule description + incident message already tell the agent everything "
        "it needs, respond with: `SKIP: rule description is sufficient`\n\n"
        "Format (only if NOT skipping):\n"
        "```\n"
        "GOTCHAS: [what can go wrong, if anything]\n\n"
        "ACCOMPANYING CHANGES:\n"
        "- [change 1 the rule doesn't mention]\n"
        "- [change 2]\n\n"
        "ORDERING: [what needs to happen first/last, if relevant]\n"
        "```\n"
        "Omit any section that doesn't apply. Be terse.\n"
    )

    return prompt


def build_rule_discovery_prompt(
    migration_description: str,
    known_rulesets: list[str],
    known_violation_names: list[str],
    unattributed_changes: list[UnattributedChange],
    commit_before: str,
    commit_after: str,
) -> str:
    """Build a prompt that produces analyzer-lsp rules detecting PRE-migration patterns."""
    prompt = (
        f"You are analyzing a completed code migration: {migration_description}\n\n"
        f"Below are code diffs from this migration. Your job is to write static "
        f"analysis rules that would detect the **BEFORE-state** (pre-migration) "
        f"patterns in codebases that HAVEN'T been migrated yet.\n\n"
        f"## CRITICAL: Rule direction\n"
        f"Rules must detect the OLD code pattern (the `-` lines in the diff), NOT "
        f"the new code (the `+` lines).\n\n"
        f"Example: if the diff shows:\n"
        f"```diff\n"
        f"-import javax.ejb.Stateless;\n"
        f"+import jakarta.enterprise.context.ApplicationScoped;\n"
        f"```\n"
        f"The rule MUST detect `javax.ejb.Stateless` (what un-migrated code has).\n"
        f"The message should explain to replace it with `@ApplicationScoped`.\n\n"
        f"## Existing rules (DO NOT rediscover)\n"
    )

    for vn in sorted(set(known_violation_names)):
        prompt += f"- {vn}\n"

    prompt += f"\n## Known rulesets: {', '.join(known_rulesets)}\n"

    prompt += "\n## Migration diffs:\n"
    for change in unattributed_changes:
        prompt += f"\n**`{change.file_path}`**\n"
        for hunk in change.hunks[:5]:
            prompt += f"```diff\n{hunk.content}\n```\n"
        if len(change.hunks) > 5:
            prompt += f"*({len(change.hunks) - 5} more hunks)*\n"

    # Detect if this chunk is build files and add specific instructions
    is_build = any(
        "pom.xml" in c.file_path.lower() or "build.gradle" in c.file_path.lower()
        for c in unattributed_changes
    )
    if is_build:
        prompt += (
            "\n## BUILD FILE INSTRUCTIONS\n"
            "For build files (pom.xml, build.gradle):\n"
            "- Focus on REMOVED dependencies and configuration (the `-` lines)\n"
            "- Do NOT create rules that detect the NEW dependencies being added — "
            "those are the TARGET framework, not what pre-migration code has\n"
            "- Generate ONE rule per significant dependency that was removed or replaced\n"
            "- Use `java.dependency` conditions with the OLD groupId:artifactId\n"
            "- For Maven plugin changes, generate separate rules for each plugin\n\n"
        )

    prompt += (
        "\n## Instructions\n"
        "For each migration pattern in the diffs, generate an analyzer-lsp rule.\n\n"
        "Remember:\n"
        "- The `when` condition detects the OLD (pre-migration) pattern\n"
        "- The `message` explains what to REPLACE it with (the new pattern)\n"
        "- `java.referenced` pattern must be a fully qualified class FROM THE OLD CODE\n"
        "- `builtin.filecontent` pattern must match OLD file content\n"
        "- `java.dependency` name must be the OLD dependency, not the new one\n\n"
        "Assess `migration_relevance`:\n"
        "- `high` -- clearly migration-related (old API usage, old config format)\n"
        "- `medium` -- probably migration-related, needs human review\n"
        "- `low` -- probably unrelated (bug fix, feature, cosmetic)\n"
        "- `very_low` -- almost certainly not a migration pattern\n\n"
        "Include `relevance_reasoning` explaining your assessment.\n\n"
        "```yaml\n"
        "- ruleID: mined-<descriptive-id>\n"
        "  description: <what OLD pattern this detects>\n"
        "  category: mandatory  # or optional, potential\n"
        "  effort: 1  # 1-10\n"
        "  migration_relevance: high\n"
        "  relevance_reasoning: <why>\n"
        "  when:\n"
        "    java.referenced:\n"
        "      pattern: <old.fully.qualified.ClassName>\n"
        "      location: IMPORT  # or ANNOTATION, TYPE, METHOD_CALL\n"
        "  message: |\n"
        "    <what to replace it with and why>\n"
        "  labels:\n"
        "    - konveyor.io/source=<source>\n"
        "    - konveyor.io/target=<target>\n"
        "```\n\n"
        "Output a YAML array wrapped in ```yaml ... ``` markers.\n"
        "Output `[]` if no migration patterns are found.\n\n"
        "IMPORTANT:\n"
        "- Do NOT create rules that detect the NEW/target code\n"
        "- Do NOT rediscover patterns covered by existing rules above\n"
    )

    return prompt
