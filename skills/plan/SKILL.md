---
name: plan
description: >
  Design a maintainable solution grounded in existing code and break it into
  ordered, verifiable tasks. Use for substantial features, architectural
  changes, or work spanning multiple implementation steps. Skip obvious,
  narrowly scoped changes that can be implemented directly.
---

# Plan

Produce the smallest understandable design that meets the requirements, then
decompose it into cohesive tasks. Prefer reuse and clear ownership over
speculative extensibility. Scale the detail to the work.

Bounded experiments are permitted to answer material planning questions. Do not
implement production code or execute implementation tasks during this workflow.
Respect host-mode restrictions, permissions, and user read-only constraints when
investigating or experimenting. Writing planning artifacts is allowed unless the
user requests discussion or read-only analysis only.

## 0. Establish the Goal

Before designing or decomposing work, establish the intended outcome:

1. **Goal:** What problem are we solving, and why?
2. **Success criteria:** What observable result would constitute success?
3. **Constraints:** What must remain true?
4. **Non-goals:** What is explicitly outside the scope?

Distinguish the desired outcome from a proposed implementation. Respect explicitly
chosen technical solutions as constraints. If it is materially unclear whether a
proposed solution is required or illustrative, clarify before considering alternatives.
Do not invent business objectives or numerical targets.

If the goal is unclear, investigate the available context and ask only questions
needed to resolve material ambiguity. Do not proceed with architectural design
until the goal is clear enough to evaluate competing solutions. Keep this section
concise; simple tasks may need only one sentence.

Use the success criteria to evaluate the proposed design and guide task acceptance
criteria and verification.

Read [plan selection and lifecycle](../../references/plan-lifecycle.md) in full
before selecting or creating a plan. It owns feature selection, artifact locations,
and lifecycle transitions for this workflow.

## 1. Establish Requirements and Context

Read [code quality](../../references/code-quality.md) and use its applicable
concerns to define acceptance criteria and verification for the current task.

- Identify required behavior, compatibility requirements, and important failure
  cases. Separate confirmed requirements from assumptions.
- Read repository instructions and relevant code, interfaces, callers, and tests.
  Identify existing components to reuse or extend, with paths and responsibilities.
- When existing evidence is insufficient, identify the material question a bounded
  experiment must answer before running it. Use an isolated temporary location for
  experimental code. Record the result, limitations, and resulting design decision
  in the plan. Experiments are optional when existing evidence suffices.
  Keep the plan **Not ready** while the material decision remains unresolved. If a
  needed experiment cannot be performed, report the blocker and what would resolve it.
- Ask only about unresolved choices that materially affect behavior, architecture,
  scope, security, or data integrity and cannot be answered from the repository.
  Honor decisions and authorization already provided; do not invent requirements.

## 2. Design and Review

Describe the proposed behavior and data flow, component ownership, interfaces,
and invariants. Explain new components and meaningful trade-offs; omit lengthy
alternatives analysis where the approach is straightforward.

Read [structural-review](../structural-review/SKILL.md) in full and apply its
**plan review** workflow before task breakdown. Supply the requirements, proposed
design, reuse candidates, and relevant repository evidence. That skill owns the
structural criteria; do not maintain a second checklist here.

Resolve High and Medium structural findings by revising the design or documenting
an evidence-backed reason to accept the trade-off. An unresolved High or Medium
finding remains a blocker. Low findings do not block readiness. Review again only
when a revision or new evidence warrants it. Require **Review status: Complete**
under structural-review's evidence rules. If the skill cannot be loaded or the
review is **Pending**, keep the plan **Not ready** and report what would unblock it.

## 3. Decompose and Order Tasks

- Prefer vertical slices that deliver verifiable behavior. Use separate contract,
  migration, or investigation tasks when they are real prerequisites.
- Size tasks for one focused implementation and verification session, based on
  cohesion and uncertainty rather than file counts.
- Establish dependencies and validate high-risk assumptions early. Keep the
  system working between steps where practical.
- Mark tasks parallelizable only when their responsibilities, file changes, and
  interfaces are independent. Establish shared contracts first; keep conflicting
  edits, shared mutable state, and ordered migrations sequential.

For each task, record:

```markdown
### Task N: Title
- Outcome: Observable behavior delivered.
- Changes: Specific changes, likely files, and existing code to reuse.
- Dependencies: Task IDs or none; unresolved decisions if any.
- Acceptance: Expected behavior and important invariants preserved.
- Verification: Relevant tests, checks, or runtime evidence.
```

Choose verification proportional to the change. Include structural-review in
**code review** mode at substantial implementation checkpoints, particularly when
ownership, interfaces, or abstractions change. Plan to resolve significant findings
before dependent work proceeds. Include independent correctness review according
to [implementation's review policy](../implementation/SKILL.md#independent-correctness-review),
with verification and repair time in the relevant tasks. Structural review does
not replace it. A completed plan is not evidence that these checks have run or
that implementation tasks are complete.

## 4. Review Verification Coverage

Review the proposed verification against every success criterion. Check that it
demonstrates the complete outcome, including integrated behavior where relevant.
Reuse task-level checks when they provide sufficient coverage; do not require
duplicate tests or a new test suite. Resolve gaps by revising the planned checks,
or keep the plan **Not ready** with the specific coverage blocker.

This review assesses planned verification; it does not mean implementation checks
have run.

## 5. Deliver the Plan

Mark the whole plan **Ready for implementation** only when requirements and success
criteria are clear, structural plan review is complete, material decisions and
findings are resolved, tasks have dependencies, acceptance criteria, and
verification defined, and the coverage review confirms that planned verification
demonstrates every success criterion.

Otherwise, mark it **Not ready** and list each blocker with the action or decision
needed to resolve it. Do not label the overall plan ready while any task remains
blocked by an unresolved decision. Normal ordering dependencies between
implementation tasks are not planning blockers.

Readiness describes the completeness of the plan. It does not authorize execution
or mean implementation checks have passed. Specified implementation tests do not
need to have run for the plan to be ready.

Save artifacts and record lifecycle according to the shared plan selection and
lifecycle contract.

Keep the plan organized around:

1. Goal, success criteria, constraints, and non-goals.
2. Existing components and proposed design, with relevant paths.
3. Meaningful decisions and structural-review outcomes.
4. Ordered tasks with acceptance criteria and verification.
5. Material risks, assumptions, and unresolved questions.

Omit empty sections. Keep the todo file as a short checklist linking to task
details in the plan. Leave implementation items unchecked. For discussion-only
requests, present the same information in chat without creating files.

Report the selected feature, lifecycle when known, readiness, artifact paths,
and any blockers or decisions needed before implementation. Respect existing
approval boundaries without adding an approval step after every task.
