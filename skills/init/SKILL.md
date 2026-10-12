---
name: init
description: >
  Create or conservatively update a short root AGENTS.md for an existing
  repository or an empty project through inspection and focused questions.
  Use for project agent instructions, not application scaffolding or tooling setup.
---

# Initialize Project Instructions

Produce a concise, project-specific root `AGENTS.md` that helps agents work within
the project's structure, boundaries, and conventions. This workflow writes only
that file. Do not create component instruction files, architecture documents,
application scaffolding, configuration, or dependencies; do not install tools or
commit changes.

## 1. Inspect Before Asking

- Resolve the target from the user's path or current project context. Use the
  repository root by default in a Git checkout and the current directory for an
  empty project. Honor an explicitly selected project directory; clarify if
  multiple targets remain plausible. Do not initialize this skill's own directory
  merely because its instructions live there.
- Read applicable parent instructions, the target's existing `AGENTS.md`, and
  relevant nested agent instructions. Record existing custom rules and inspect
  the working tree so unrelated changes can be preserved. If the root file is a
  symlink, resolve its destination before writing; clarify an out-of-target
  destination rather than modifying another project or replacing the link.
- Inspect top-level structure, relevant component entry points, manifests,
  workspace configuration, task runners, lockfiles, CI, README/contributor guides,
  and architecture documentation. Keep inspection proportional to the project;
  avoid generated/vendor trees and secret values.
- Establish the project name and purpose, component responsibilities, boundaries,
  and configured test, lint, formatting, and typecheck entry points. Track the
  source and working directory for each command. A command found in configuration
  is configured, not evidence that it has run successfully.
- Collect plausible authoritative documentation candidates with their exact
  paths or supplied URLs and a brief description. Identify missing information
  and material disagreements between instructions, documentation, and code.

## 2. Resolve Missing Decisions

Ask small, adaptive batches of focused questions, usually one to three at a time.
Reuse answers already given and facts established by inspection; do not run a
fixed questionnaire or ask the user to restate repository facts.

- Establish only unresolved purpose, intended components/stack, responsibilities,
  architectural boundaries, and tooling preferences. For an empty project, ask
  about intended structure and label it as planned; do not imply directories,
  dependencies, or usable commands already exist.
- Present discovered documentation candidates for the user to select as
  authoritative, allowing none or another source. Reuse any prior selection. If
  no architecture docs exist, ask about the few boundaries that matter, such as
  dependency direction, API/data ownership, or separation of UI and business
  logic. Capture the answers briefly without inventing links or creating docs.
- Resolve material conflicts with existing rules through questions before
  changing those rules. Preserve custom rules and their meaning by default;
  silence is not permission to remove or weaken them. When documentation and
  implementation disagree, identify the discrepancy and ask only about decisions
  needed for initialization; do not redesign the application.
- Offer missing tooling only where relevant, preserving existing choices. For
  Python, consider Ruff for lint/format and pytest or a type checker if useful;
  for Go, consider gofmt, go test, go vet, or golangci-lint; for React/TypeScript,
  consider ESLint, Prettier, TypeScript checking, and the project's suitable test
  tools. These are options, not a required bundle. Record only accepted additions.
  Tools accepted but not configured are intended conventions, not working or
  verified commands. Do not install or configure them during initialization.

Wait for answers needed to establish the content. If interactive questions are
unavailable, state the unresolved decisions rather than inventing answers. Once
the content is established, write without an additional approval step unless the
user requested one or the host mode requires it. Honor read-only or plan mode by
presenting the proposed content without writing.

## 3. Write the Root File

Adapt the user's example when supplied; otherwise aim for a short, easily scanned
file of a few dozen lines, expanding only for useful project-specific guidance.
Use only applicable sections, with concrete paths and responsibilities rather
than exhaustive inventories or duplicated architecture details:

- **Project:** Name and a brief purpose statement.
- **Structure:** Main components and responsibilities; clearly distinguish planned
  layout from existing directories.
- **General rules:** Stay within requested scope, favor simple changes, reuse
  existing owners and patterns, preserve compatibility unless a change is
  authorized, keep secrets out of code and logs, and update relevant documentation
  when behavior, interfaces, or architecture materially change. Adapt these rules
  to existing conventions rather than overwriting custom policy.
- **Component boundaries:** Concise confirmed constraints and links to user-selected
  architecture docs. When docs and implementation materially disagree, instruct
  agents to surface the discrepancy before making an architectural change.
- **Checks:** Actual configured test, lint, formatting, and typecheck entry points
  with working directories where necessary. Preserve wrappers and package-manager
  conventions. Omit unavailable checks; keep accepted but unconfigured tooling
  separately labeled as intended. Never invent commands or claim tests passed.
- **Generated/vendor files and instruction scope:** Identify relevant existing
  generated/vendor paths and their source or regeneration entry point when known.
  Preserve nested files. Explain that conflicting nested `AGENTS.md` instructions
  take precedence within their scope, while other applicable parent instructions
  remain effective.

For an existing root file, make the smallest useful patch. Retain custom rules,
unrelated content, and managed markers; avoid wholesale replacement or formatting
churn. Brevity does not justify removing existing instructions. Do not add empty
sections, speculative architecture, nonexistent documentation links, or boilerplate
that gives agents no project-specific help.

## 4. Verify and Report

Re-read the result and compare it with the original and the evidence collected:

- Existing rules remain intact except for changes explicitly resolved with the user.
- Paths and documentation links exist or were supplied by the user; proposed
  directories are clearly planned. Commands match actual configuration and include
  necessary working directories. Verification claims match checks actually run.
- Accepted but unconfigured tools remain labeled as intended conventions.
- The result is concise, uses only applicable sections, and preserves instruction
  precedence without discarding nonconflicting parent rules.
- Only the intended root `AGENTS.md` changed during this workflow; nested files,
  application files, configuration, and pre-existing unrelated edits are untouched.

Do not run installers, auto-fixers, formatters, or application commands that would
modify other files merely to validate this instruction file. Inspection is enough
to identify configured commands; report execution separately if it was requested
and performed within scope. Summarize the file created or updated, the meaningful
conventions captured, and any remaining limitations without implying application
setup or successful tests.
