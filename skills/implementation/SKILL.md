---
name: implementation
description: >
  Implement an authorized plan, task, or clear change request in cohesive
  increments, verifying each increment and the complete outcome. Use when
  executing planned work or making changes that benefit from staged
  implementation and verification, with independent correctness review for
  substantial or sensitive changes and re-review of PR repairs.
---

# Implementation

Deliver the requested outcome through small, verifiable increments. Prefer the
simplest implementation that meets the requirements and fits existing ownership.
Size increments by cohesion and uncertainty, not line counts or file counts.

Respect host-mode restrictions, permissions, and user read-only constraints. A
plan marked ready does not authorize execution. Honor existing authorization
without adding approval steps between increments.

## 1. Establish Scope

Read [code quality](../../references/code-quality.md) and apply its guidance
throughout implementation and verification, including changes without a plan.

Read [plan selection and lifecycle](../../references/plan-lifecycle.md) in full
before selecting the feature, its plan, and tasks. It owns feature selection,
artifact locations, and lifecycle transitions for this workflow.

Use the existing plan when available: read its goal, success criteria, constraints,
task dependencies, acceptance criteria, and verification. Honor the requested
task or subset; do not assume permission to execute the rest of the plan.

For a clear, small change request, establish the outcome and relevant checks
directly without requiring a separate planning artifact. If material behavior or
design decisions remain unresolved, investigate first and use
[plan](../plan/SKILL.md) when substantial design or decomposition is needed.
Resolve material blockers before implementing affected work.

For requested PR repair, establish the target, selected findings or autonomous
fix scope, and user constraints. Use the **Review and Fix** loop below without
repeating the original feature implementation or requiring a new plan for clear
fixes. Apply the independent correctness review policy below to ordinary
implementation as well; review does not depend on the user separately requesting
it or on a PR already existing.

## 2. Inspect the Current State

Read repository instructions and affected code, callers, interfaces, and tests.
Identify existing components to reuse and discover verification commands from
repository configuration and conventions. Check current state against the plan;
do not assume paths, contracts, or prior verification results remain current.

Inspect working-tree changes before editing. Preserve unrelated work and keep
fixes tied to the requested outcome. Note material out-of-scope issues without
turning them into additional work.

Before editing in a Git repository, identify whether a branch or worktree already
belongs to this exact task. Reuse it when it has the intended code baseline and
will not mix unrelated work. Otherwise, prefer a dedicated branch and worktree
for substantial implementation, following repository conventions and existing
user instructions. A separate worktree is optional for a small, isolated edit.
Record the branch, worktree path, and starting commit in existing task notes or
the progress report; if no commit exists yet, state that limitation.

A new worktree does not include uncommitted changes from the original checkout.
Account for any task prerequisites in those changes before proceeding; do not
silently omit them or copy unrelated work. Keep implementation changes and local
verification artifacts in the selected workspace where practical. Worktree
isolation does not isolate shared databases, services, or external side effects.

## 3. Implement and Verify Increments

Follow task dependencies. Prefer a thin vertical slice delivering observable
behavior; use contract, migration, or other prerequisite increments when needed.
Keep the system working between increments where practical.

For each increment:

1. Identify the behavior it delivers and the acceptance criteria it must satisfy.
2. Implement the smallest cohesive change using existing owners and conventions.
3. Run relevant tests, checks, or runtime verification. Add or update tests when
   needed to demonstrate changed behavior or prevent a meaningful regression;
   avoid tests that merely mirror the implementation.
4. Inspect the diff for scope, accidental changes, and compatibility. Resolve
   failures caused by the increment before dependent work proceeds. Distinguish
   pre-existing failures and unavailable checks from regressions, and report
   their effect on confidence.
5. Continue to the next authorized increment. Commit according to existing
   authorization and repository conventions; commits are not required by this
   workflow and must not include unrelated changes.

Choose verification proportional to the change. Run broader suites, builds,
type checks, and lint when required by repository rules or the affected behavior.
Reuse successful results while they remain applicable; repeat checks when later
changes, failures, or new evidence could invalidate them.

Use feature flags only when incomplete behavior needs to remain hidden during
delivery. Choose rollback or recovery measures appropriate to the actual change,
especially for data migrations; do not mandate destructive reverse migrations or
split a coherent replacement solely to separate additions from deletions.

If implementation exposes a material flaw in the plan, resolve it before
dependent work proceeds. Update this work's existing planning artifacts when
appropriate. Make routine implementation choices autonomously within the agreed
scope; ask only when an unresolved decision changes requirements, scope, or
authorization and cannot be settled from available evidence.

#### Investigate Failures Before Fixing

For bug reports, failing checks, or unexpected behavior, establish the cause before
changing code. Scale the investigation to the problem; an obvious defect needs
only a short evidence-backed explanation.

1. **Establish the failure.** Identify expected versus actual behavior. Reproduce
   through the relevant entry point when practical, recording the triggering
   input, environment, and error. If reproduction is unavailable, use available
   logs, traces, or other evidence and state the limitation.
2. **Localize the cause.** Trace the failing behavior through relevant code,
   callers, and state. Distinguish the underlying cause from its symptoms and
   separate pre-existing failures from regressions introduced by current work.
3. **Test a hypothesis.** State the likely cause and use the smallest targeted
   check or experiment that can support or reject it. Reuse decisive evidence
   already available. Avoid stacking speculative fixes; if a hypothesis fails,
   reassess before making another change.
4. **Fix and verify.** Apply the smallest change that addresses the supported
   cause. Add or update a regression test when practical and meaningful,
   preferably demonstrating the failure before the fix. Verify the original
   failing case and relevant neighboring behavior through the normal
   implementation checks. Do not weaken tests or hide errors to obtain a pass.

If the cause remains uncertain, report what is known, which hypotheses were
tested, and the next evidence needed. Do not present a speculative change as a
verified fix.

## 4. Review Structure

At substantial checkpoints, particularly when ownership, interfaces, or
abstractions change, read [structural-review](../structural-review/SKILL.md) in
full and apply its **code review** workflow to this work. Honor review checkpoints
already specified in the plan. That skill owns the structural criteria; do not
maintain a duplicate checklist here.

Resolve High and Medium findings by fixing the implementation or documenting an
evidence-backed reason to accept the trade-off before dependent work proceeds.
Unresolved High or Medium findings block completion; Low findings do not. Repeat
review only when revisions or new evidence warrant it. Require **Review status:
Complete** under structural-review's evidence rules. If the skill cannot be loaded
or a required review is **Pending**, report what would unblock it, pause work
dependent on the unresolved assessment, and do not claim completion.

## 5. Verify the Complete Outcome

Check the actual results against every success criterion in the authorized scope,
including integrated behavior where relevant. Reuse increment-level evidence
when it demonstrates the complete outcome; add checks only to close material
coverage gaps. Complete repository-required final checks.

Planned checks are not executed checks. If verification is unavailable or
inconclusive, report what remains unverified, why, and what would resolve it.
Do not claim the outcome is verified while required checks or material findings
remain unresolved.

### Independent Correctness Review

Require [pr-review](../pr-review/SKILL.md) before declaring completion for
substantial behavior changes, changes to security or authorization, data integrity,
or shared/public contracts, and whenever the user or repository requires it.
Assess impact and affected consumers, not file count; a one-line authorization
change still requires review. A small, isolated change without those impacts may
use local verification alone; state why independent review was not needed.
Honor an explicit user instruction to skip review and disclose that limitation.

Identify required review during scope assessment and check that native review
and fresh context are available early. If unavailable, report **Evidence missing**;
continue authorized work that does not depend on the assessment, but do not mark
the work complete while its required review is missing. Structural review and
self-review do not substitute for independent correctness review.

Use the **Review and Fix** loop below on the completed authorized scope. An
implementation request authorizes repair of supported defects within that scope;
it does not authorize unrelated fixes. Reuse a completed independent review only
while its scope, snapshot, and evidence still apply. Required review must end with
**No blocking findings**, and required verification must pass, before claiming
completion. Disclose any explicit user waiver separately from a clean review.

### Review and Fix

Implementation is the sole owner of this loop. Read
[pr-review](../pr-review/SKILL.md) in full; invoke it in review-only mode for each
independent assessment. Preserve its scope, snapshot, isolation, and evidence
rules. Start from a supplied review when it still applies to the current code;
otherwise obtain a current review before selecting fixes.
For a PR URL, start from its actual head; subsequent reviews must explicitly
include the repair workspace's uncommitted fixes until they are committed or
pushed. Do not repeatedly review the unchanged remote head while editing locally.

1. Assess findings against code and requirements before editing. For each, fix a
   supported defect, reject it with concrete evidence, or identify an unresolved
   decision. Apply pr-review's **Blocking policy**, preserve original priorities,
   and report disagreements; do not treat reviewer suggestions as new requirements
   or silently dismiss blocking issues. Submit the evidence for a rejected finding
   to the independent reviewer; rejection alone does not clear the blocker.
2. In guided repair, fix only the selected findings and their necessary
   consequences. In autonomous repair, fix supported defects within the agreed
   scope without asking about routine implementation choices. Ask only when an
   unresolved decision changes requirements, scope, or authorization. Report
   unrelated issues and cosmetic suggestions without expanding the work.
3. Apply this skill's implementation, structural review, and verification steps
   to the fixes. Preserve required behavior and contracts; do not weaken checks
   or tests merely to make findings disappear. Close material evidence gaps with
   applicable checks where possible; missing evidence is not itself a code defect.
4. After each repair round, obtain a fresh independent review of the revised
   snapshot, revisiting prior findings and affected contracts. Supply current
   requirements, constraints, and evidence, including evidence behind disputed
   findings, without prescribing the verdict. Reuse unaffected verification.
   Report new findings outside guided repair scope rather than fixing them
   automatically.
5. Stop when the current review disposition is **No blocking findings** and required
   verification is satisfied, or when guided repairs are verified and re-reviewed
   with remaining out-of-scope findings disclosed. Default to at most three repair rounds, each
   including its follow-up review; honor an explicit user limit. Stop earlier on repeated
   disagreement without new evidence, lack of progress, or a material blocker
   that cannot be resolved within authorization. Do not reset the limit by
   handing control between skills. Preserve the work and report what remains.

Report findings fixed, rejected with evidence, or unresolved; the rounds used;
verification; and the final review disposition for the actual final snapshot.
Exhausting the limit, missing review evidence, or completing only selected fixes
does not establish readiness of the whole PR. Follow existing authorization for
committing or pushing; repair does not itself authorize merging or deployment.

## 6. Retain or Discard the Implementation

After verification, retain the implementation for review or integration under
existing authorization. Do not merge or delete its branch or worktree merely
because checks passed, and do not discard work automatically because checks fail.

When the user requests discarding an implementation, inspect the task's diff,
commits, worktree contents, and branch usage before removal. Remove only the
task-owned worktree and branch covered by that request, preserving unrelated
changes, untracked or ignored user data, and work used elsewhere. Do not delete
a reused workspace or branch containing other work; discard only this task's
changes when they can be separated safely. If ownership or the deletion scope
is unclear, clarify before destructive action. Use Git's worktree management
commands for worktree removal and verify the resulting repository state.

Removing a branch or worktree does not undo changes already integrated elsewhere,
database migrations, deployments, or other external effects. Identify those
separately and follow their recovery procedures and existing authorization;
report any effects that remain after local cleanup.

## 7. Report Results

Summarize what changed, the verification performed and its results, and any
remaining blockers or limitations. Update existing task checklists belonging to
this work only when their acceptance and required verification are satisfied.
Update lifecycle according to the shared plan selection and lifecycle contract;
report the selected feature, plan location, and lifecycle when known.
Do not create additional reporting artifacts unless requested or required by
repository conventions.

Distinguish implementation, verification, and delivery status. A clean working
tree is not a completion requirement. Completion does not itself authorize
pushing, opening a PR, merging, or deploying; follow the user's existing
instructions and approval boundaries for those actions.
