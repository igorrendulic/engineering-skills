---
name: plan
description: >
  Design a maintainable solution grounded in existing code and break it into
  ordered, verifiable tasks. Use for substantial features, architectural
  changes, or work spanning multiple implementation steps. Skip obvious,
  narrowly scoped changes that can be implemented directly.
---

# Plan

Design the smallest understandable solution, then break it into verifiable tasks.
Prefer reuse and clear ownership over speculative extensibility.

Do not implement production code or execute implementation tasks. Bounded planning
experiments and artifact writes must respect host mode, permissions, and user
constraints. For discussion-only or read-only requests, deliver the plan in chat.

## 0. Establish the Goal

Establish **Goal**, observable **Success criteria**, **Constraints**, and
**Non-goals** before designing. Distinguish outcomes from implementation choices;
honor explicitly chosen solutions. Clarify whether a solution is required or
illustrative when that materially affects the design. Do not invent objectives
or numerical targets.

Investigate context and resolve material ambiguity before architecture. Ask only
questions the repository and conversation cannot answer; honor existing decisions
and authorization. Scale detail to the task. Use success criteria to judge the
design, task acceptance, and verification.

Before selecting or creating a plan, read
[plan selection and lifecycle](../../references/plan-lifecycle.md) in full. It owns
feature selection, artifact paths, and lifecycle transitions.

## 1. Establish Requirements and Context

Read repository instructions, relevant code, interfaces, callers, and tests.
Record required behavior, compatibility, important failure cases, and reuse
candidates with paths and responsibilities. Separate requirements from assumptions.
Apply [code quality](../../references/code-quality.md) to acceptance and verification.

When evidence cannot resolve a material decision, define the question before
running a bounded experiment. Isolate experimental code in a temporary location;
record results, limitations, and the resulting decision. Experiments are optional
when evidence suffices. Unresolved decisions or unavailable necessary experiments
keep the plan **Not ready**; state what would unblock them.

## 2. Design and Review

Describe behavior, data flow, ownership, interfaces, invariants, new components,
and meaningful trade-offs. Omit unnecessary alternatives analysis.

Read [structural-review](../structural-review/SKILL.md) in full and perform its
**plan review** before task breakdown. Supply requirements, design, reuse
candidates, and repository evidence; that skill owns the structural criteria.
Resolve High and Medium findings through revisions or evidence-backed acceptance
of trade-offs. Low findings do not block. Repeat review only when changes warrant.
Require **Review status: Complete**; unresolved High/Medium findings, a **Pending**
review, or an unavailable review skill keep the plan **Not ready**.

## 3. Decompose and Order Tasks

- Prefer vertical slices sized for one focused implementation and verification
  session. Separate contracts, migrations, or investigations when prerequisites.
- Record dependencies, validate risky assumptions early, and keep the system
  working between steps where practical.
- Parallelize only independent responsibilities, edits, and interfaces. Establish
  shared contracts first; sequence conflicting edits, mutable state, and migrations.

For each task use:

```markdown
### Task N: Title
- Outcome: Observable behavior delivered.
- Changes: Specific changes, likely files, and existing code to reuse.
- Dependencies: Task IDs or none; unresolved decisions if any.
- Acceptance: Expected behavior and important invariants preserved.
- Verification: Relevant tests, checks, or runtime evidence.
```

Scale verification to the change. Include structural **code review** at substantial
checkpoints, especially ownership, interface, or abstraction changes; resolve
significant findings before dependent work. Also include independent correctness
review under [implementation's review policy](../implementation/SKILL.md#independent-correctness-review).
Allow verification and repair time; structural review does not replace correctness
review.

## 4. Review Verification Coverage

Check that planned verification demonstrates every success criterion and the
complete outcome, including integrated behavior where relevant. Reuse sufficient
task checks without duplicate tests or a new suite. Revise checks to close gaps
or keep the plan **Not ready** with specific coverage blockers.

## 5. Deliver the Plan

Mark the whole plan **Ready for implementation** only when requirements and success
criteria are clear, structural review is Complete, material decisions and blocking
findings are resolved, every task defines dependencies, acceptance and verification,
and coverage review confirms every success criterion is demonstrated by planned
checks. Otherwise mark **Not ready** and give each blocker's resolution action.
Any task blocked by an unresolved decision blocks readiness; normal ordering
dependencies do not.

Readiness means plan completeness, not execution authorization, completed tasks,
or passed implementation checks. Planned tests need not have run. Respect existing
approval boundaries without adding per-task approvals.

Save artifacts and lifecycle under the shared contract. Organize the plan around
goal and success criteria, constraints and non-goals, existing components and
design with paths, decisions and review outcomes, ordered tasks, and material
risks, assumptions, and questions. Omit empty sections. Keep todo as a short
checklist linking to task details; leave implementation items unchecked.

Report selected feature, lifecycle when known, readiness, artifact paths, and
remaining blockers or decisions.
