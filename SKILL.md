---
name: engineering-skills
description: Route project-instruction initialization, planning, implementation, independent PR review, structural review, and GitHub PR creation requests to the matching bundled workflow. Use when the user invokes engineering-skills or asks to choose an engineering workflow.
---

# Engineering Skills Dispatcher

Load the requested workflow before acting on its target.

## Available workflows

| Command | Instructions |
| --- | --- |
| `init` | `skills/init/SKILL.md` |
| `plan` | `skills/plan/SKILL.md` |
| `implementation` | `skills/implementation/SKILL.md` |
| `pr-review` | `skills/pr-review/SKILL.md` |
| `structural-review` | `skills/structural-review/SKILL.md` |
| `github-pr` | `skills/github-pr/SKILL.md` |

## Dispatch

1. Honor an explicitly selected workflow, whether named after `$engineering-skills`
   (or `/engineering-skills`) or in prose. Accept `structural review` as an alias
   for `structural-review` and `PR review` for `pr-review`. An explicitly requested
   unsupported command is an error: show available workflows without guessing a
   replacement or file path.
2. Without an explicit selection, infer the workflow from the requested action
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
3. If the request is bare or ambiguous, show the relevant workflows and ask which
   one to run before acting. A generic code review selects `pr-review`; a design or
   dedicated complexity/ownership review selects `structural-review`. If asked
   to recommend a workflow only, explain the choice without executing it.
4. Read the **entire** selected `SKILL.md` using the path relative to this file's
   directory. If it or a required reference cannot be read, explain the installation
   problem rather than substituting generic instructions.
5. Follow that workflow's instructions, using the user's remaining request as its
   target and scope. Preserve read-only constraints and existing authorization;
   selecting a workflow does not authorize additional actions.

## Adding workflows

Add a subdirectory under `skills/` containing a `SKILL.md`, then register its command and relative path in the table above. Keep this layout, including the root `references/` directory, when installing the dispatcher; `plan` and `implementation` depend on the shared plan lifecycle reference and the sibling `structural-review` skill. PR repair also depends on the sibling `pr-review` and `implementation` skills.
