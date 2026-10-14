---
name: engineering-skills
description: Route engineering-skills requests to bundled initialization, planning, implementation, review, PR, or usage-help workflows. Use when the user invokes the standalone engineering-skills dispatcher or asks which bundled workflow to use.
---

# Engineering Skills Dispatcher

Load the requested workflow before acting on its target. A bare invocation or
usage question selects help without executing another workflow.

## Available workflows

This table is the shared catalog for the dispatcher and help. Instruction paths
are relative to this file; example targets follow the selected command.

| Command | Instructions | Purpose | Example target |
| --- | --- | --- | --- |
| `init` | `skills/init/SKILL.md` | Create or update root project instructions. | Initialize this project's AGENTS.md |
| `plan` | `skills/plan/SKILL.md` | Define success, review the design, and order verifiable tasks. | Add password reset |
| `implementation` | `skills/implementation/SKILL.md` | Implement, verify, and repair changes within scope. | Implement the password-reset plan |
| `pr-review` | `skills/pr-review/SKILL.md` | Independently review correctness and regressions. | Review the password-reset changes |
| `structural-review` | `skills/structural-review/SKILL.md` | Assess complexity, reuse, and ownership in designs or code. | Assess the password-reset design |
| `github-pr` | `skills/github-pr/SKILL.md` | Prepare branches, commits, and pull requests. | Create a PR for these changes |
| `help` | `skills/help/SKILL.md` | Explain workflows and usage without executing them. | plan |

## Dispatch

1. Handle a bare `$engineering-skills` (or `/engineering-skills`), `help`,
   `help <workflow>`, and usage-only questions by reading `skills/help/SKILL.md`.
   Pass the topic, if any, and use standalone invocation examples. Do not run the
   workflow being explained. This takes precedence over action inference below.
2. Honor an explicitly selected workflow, whether named after `$engineering-skills`
   (or `/engineering-skills`) or in prose. Accept `structural review` as an alias
   for `structural-review` and `PR review` for `pr-review`. An explicitly requested
   unsupported command is an error: show available workflows without guessing a
   replacement or file path.
3. Without an explicit selection, infer the workflow from the requested action
   and current conversation when one workflow clearly fits. For example, "use
   engineering-skills to implement this plan" selects `implementation`, while
   "assess this plan for unnecessary abstractions" selects `structural-review`.
   "Review this implementation for correctness" or "review this PR" selects
   `pr-review`, including branch/worktree reviews before a PR exists. "Review and
   fix this PR" or "fix these review findings" selects `implementation` and its
   review-and-fix loop; an explicitly selected `pr-review` routes such requests
   there as well. Creating, publishing, or editing PR metadata selects `github-pr`.
   Creating or conservatively updating root `AGENTS.md` project instructions
   selects `init`. This initializes agent instructions, not an application:
   application scaffolding follows `plan` or `implementation` as appropriate.
   A bare "initialize this project" is ambiguous; clarify which outcome is wanted.
   Route by the requested action, not a keyword in its target.
4. If an action request is ambiguous, show the relevant workflows and ask which
   one to run before acting. A generic code review selects `pr-review`; a design or
   dedicated complexity/ownership review selects `structural-review`. If asked
   to recommend a workflow only, explain the choice without executing it.
5. Read the **entire** selected `SKILL.md` using the path relative to this file's
   directory. If it or a required reference cannot be read, explain the installation
   problem rather than substituting generic instructions.
6. Follow that workflow's instructions, using the user's remaining request as its
   target and scope. Preserve read-only constraints and existing authorization;
   selecting a workflow does not authorize additional actions.

## Adding workflows

Add a subdirectory under `skills/` containing a `SKILL.md`, then register its command and relative path in the table above. Keep this layout, including the root `references/` directory, when installing the dispatcher; `plan` and `implementation` depend on the shared plan lifecycle reference and the sibling `structural-review` skill. PR repair also depends on the sibling `pr-review` and `implementation` skills.
