---
name: pr-review
description: >
  Review a PR or implemented branch/worktree changes using native Codex review
  in fresh context. Scale tests, runtime, and visual verification to impact;
  report supported findings, evidence gaps, confidence, and disposition.
  Route requested fixes to implementation for verified repair and re-review.
  A PR need not exist; review alone remains read-only.
---

# PR Review

Use native Codex review as the review mechanism after implementation or user
experimentation. Keep the existing PR, branch, or worktree workflow; review does
not require committing changes or opening a PR. Inspect and run checks within
existing authorization, but do not fix source, edit planning artifacts, change
Git state in the target checkout, or publish feedback automatically.

## Review or Repair

- **Review only:** "Review this PR" returns the assessment below without edits.
- **Guided repair:** "Fix findings 1 and 3; preserve the public API" hands the
  selected findings and constraints to implementation for repair and re-review.
- **Autonomous repair:** "Review and fix this PR" authorizes implementation to
  assess and fix supported defects within the agreed scope, then re-review.

For either repair request, read [implementation](../implementation/SKILL.md) in
full and hand control to its **Review and Fix** loop. Carry forward the target,
requirements, user constraints, selected findings, existing evidence and its
snapshot, and delivery authorization. Implementation owns the loop and edits;
each native reviewer remains read-only and independent. A review-only invocation
from that loop returns its report to implementation without starting another loop.
Review findings alone do not authorize repair, pushing, or merging.

## Scope

Read applicable repository instructions and establish the requested boundary:

- **GitHub PR URL:** Resolve that PR's actual repository, base, and head. Review
  its head against their merge base; exclude local edits unless requested.
- **Local branch/worktree:** Review the full feature diff against the intended
  base's merge base, including relevant staged, unstaged, and untracked changes.
  Exclude unrelated work; an upstream branch is not necessarily the intended base.
- **Explicit narrower scope:** Honor it and disclose its limits. Without Git
  history, review supplied files and state that no baseline is available.

Resolve material base ambiguity before reviewing. Record the target path, base
and head revisions, included local files, and exclusions. Fingerprint dirty and
untracked contents so evidence identifies the reviewed snapshot. Ensure checks
and services use that snapshot. Use an isolated checkout for a PR when needed;
do not switch or overwrite the user's checkout. A branch checkout alone does
not include its uncommitted work.

## Native review in fresh context

Start a separate Codex process/session with a self-contained custom review
prompt. Do not resume the implementation session or pass its conversation. Supply
only the boundary, requirements and accepted constraints, repository instructions,
and code/evidence locations, including commands and environments where known.
Treat supplied evidence as claims to assess, not a predetermined verdict.

For the CLI, check `codex review --help`, then run `codex review -` from the target
checkout with the custom prompt on stdin. Put the exact scope in that prompt;
do not combine custom prompts with `--base`, `--commit`, or `--uncommitted` when
the installed CLI treats them as exclusive. Explicitly request both the committed
feature diff and included local changes for a branch/worktree review.

Use this short adversarial prompt followed by the concrete handoff facts:

> Review the supplied target independently, with no loyalty to the implementation.
> Challenge important correctness claims, omitted requirements, broken consumers,
> and weakened tests against the requirements and available evidence. Report only
> supported findings using native review priorities; do not invent defects.
> Do not fix code, change the target's Git state, publish feedback, or delegate
> another review.

Do not run a second general-purpose review alongside native review. Record how
fresh context was obtained. If native review or context isolation is unavailable,
report the limitation and **Evidence missing**; do not substitute self-review.

## Verification effort and evidence

Choose effort by affected contracts, consumers, and consequences:

- **Leaf / focused:** Check the changed behavior and immediate integration.
- **Shared behavior / expanded:** Add contract and representative consumer checks.
- **Core infrastructure / deep:** Add cross-component integration, compatibility,
  and relevant failure/recovery checks.

Serious consequences or uncertain dependencies can increase effort. Assess tests,
actual runtime behavior through the normal entry point, and affected visible
output at that effort level. Reuse evidence applicable to the current snapshot;
perform missing checks where possible, including repository-required checks.
Native findings alone do not establish runtime or visual verification.
Distinguish supplied evidence from checks performed during review. Name commands,
results, environments, and inspected output/artifacts. Keep unavailable checks
explicit as gaps; use not applicable only when the area is genuinely unaffected.

## Blocking policy

Use the native review priorities without silently changing the reviewer's labels:

| Priority | Completion policy |
| --- | --- |
| P0 — Critical | Blocks completion; address immediately. |
| P1 — High | Blocks completion. |
| P2 — Normal | Blocks completion; a supported defect is not optional because it is less urgent. |
| P3 — Low | Does not block completion; disclose any remaining finding. |

A blocking finding is resolved when a fresh independent assessment confirms the
fix or accepts concrete evidence that the finding does not apply. Until then,
disagreement, deferral, or an implementer's rejection does not clear it. Keep the
original priority and resolution evidence in the report. An explicit user waiver
permits only the authorized exception; still disclose the defect and do not
report **No blocking findings** while it remains supported.

For a material finding without a priority, obtain clarification from the native
reviewer before declaring it non-blocking; if unavailable, report the gap.
Missing required review or verification evidence also prevents a readiness
conclusion, but belongs under **Evidence missing**, not an invented defect priority.

## Report and revisions

Return one concise report with the scope/snapshot and isolation, effort and reason,
native findings with their original priorities and supporting locations/evidence,
verification performed, remaining gaps and how to close them, and confidence
with its basis. Keep evidence gaps separate from defects. End with one disposition:

- **Changes needed:** Supported blocking defects remain, even if gaps also exist.
- **Evidence missing:** No blocking defect is established, but a material review
  or verification gap prevents a readiness conclusion.
- **No blocking findings:** Review and applicable evidence support the change
  within the stated scope; disclose residual limitations. This is not merge approval.

Implementation owns fixes. Before reporting, confirm the snapshot still matches.
After edits, rerun native review on affected changes and revisit prior findings,
contracts, and evidence against the current snapshot; reuse unaffected evidence.
If this cannot be completed, report the stale assessment as an evidence gap
rather than applying it to the new code.
