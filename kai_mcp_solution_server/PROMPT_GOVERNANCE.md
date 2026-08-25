# Prompt Template Governance

This document defines the change-management lifecycle for the LLM **prompt templates** the Kai
solution server uses to generate migration hints. It satisfies ISO/IEC 42001 Control **A.5.2
(Governance and lifecycle of AI systems)**: the hint prompt is the instruction set defining the
server's hint-generation behavior, so it is treated as governed source code — version-controlled,
peer-reviewed, and validated by CI before distribution.

## Scope — what is governed

All model-bound prompt templates live as individual Jinja2 assets under
[`src/kai_mcp_solution_server/prompts/templates/`](src/kai_mcp_solution_server/prompts/templates/) and
are enumerated in
[`src/kai_mcp_solution_server/prompts/manifest.yaml`](src/kai_mcp_solution_server/prompts/manifest.yaml).
Today this is the live hint prompt, `generate_hint_v3`. Prompts are rendered by
[Jinja2](https://jinja.palletsprojects.com/) via `render_prompt(prompt_id, **context)` from
`kai_mcp_solution_server.prompts`; loops and structure live in the template, not in `server.py`. The
prompt-set is semantically versioned by `version:` in the manifest, kept in lockstep with the package
version in `pyproject.toml`.

The `ast_diff_str` value (computed from `associate_files` + `extract_ast_info`) is data marshalling
and stays in Python; the template receives it as a variable.

## Roles

- **Prompt Engineer / Product Architect** (`@konveyor/kai-prompt-reviewers`) — required approver for any
  change under `prompts/`. Owns prompt wording, the threat-model review, and the regression baseline.
- **Solution-server maintainers** — co-reviewers for the code that calls `render_prompt`.

The prompts directory is assigned to the reviewers in [`.github/CODEOWNERS`](../.github/CODEOWNERS).

## Lifecycle of a prompt change

1. **Branch & edit** the template asset(s). Do not reintroduce prompt strings inline in `server.py`.
2. **Refresh checksums.** Run `python scripts/prompts_version.py update`. Bump `version:` in the
   manifest (and `pyproject.toml`) if the change ships in a new release.
3. **Update parity expectations.** The byte-exact oracle (`tests/prompts/oracle.py`) is the historical
   baseline. For an _intentional_ wording change, update the oracle and call it out in the PR.
4. **Complete the prompt-injection threat-model checklist** (below) in the PR.
5. **Open a PR** with DCO sign-off (`git commit -s`). CODEOWNERS routes it to a Prompt Engineer; the
   [`prompt-validation`](../.github/workflows/prompt-validation.yml) workflow runs automatically.
6. **Merge** only after required review + green CI.

## CI gates

The `prompt-validation` workflow (triggered on `prompts/**`) runs `scripts/prompts_version.py check`
and `pytest tests/prompts`:

- **Syntactic verification** — every template parses as Jinja2; declared variables exactly match the
  template's referenced variables; no leftover `{var}` f-string interpolation.
- **Manifest/version governance** — every asset is declared (and vice-versa); content checksums match.
- **Byte-exact parity** — the template reproduces the pre-extraction prompt string exactly across the
  incident / AST-diff matrix.
- **Semantic regression (deterministic, mock model)** — renders the prompt against a baseline of
  migration scenarios and asserts the required scaffolding (output-format contract, each incident's
  fields, the `AST Diff:` anchor) survives.

## Prompt-injection threat-model checklist

Complete for every template change that adds or alters an interpolation point:

- [ ] **Untrusted interpolation** — `incident.message`, `incident.code_snip`, and `ast_diff_str` are
      derived from analyzed user code. Confirm they remain data-only and cannot be read by the model
      as instructions overriding the output-format contract.
- [ ] **Output-contract integrity** — do the `SUMMARY:` / `HINT:` anchors remain unambiguous so a
      malicious code snippet can't spoof the expected response shape?
- [ ] **Rendering** — output is non-escaped by design (these are plain-text prompts); confirm no new
      context (JSON, code fence) where unescaped interpolation enables injection.
- [ ] **Regression** — the semantic-regression baseline still passes.

## Branch protection (repo admin action — not in code)

A repository admin must, for `main` and `release-*`:

1. **Require the status check** `Validate prompt templates`.
2. **Require review from Code Owners** so `prompts/**` edits need `@konveyor/kai-prompt-reviewers`.
3. **Create the `@konveyor/kai-prompt-reviewers` team** with the designated Prompt Engineers /
   Product Architects.
