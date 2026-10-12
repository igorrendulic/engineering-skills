---
name: structural-review
description: >
  Review proposed designs or existing code for duplicated functionality,
  unnecessary complexity, unjustified abstractions, and poor ownership or
  module boundaries. Use to assess a plan before implementation, review
  substantial changes, or investigate structural quality in a subsystem.
---

# Structural Review

Produce actionable findings supported by repository evidence. Assess whether the
design meets its requirements with appropriate complexity and clear ownership.
Passing tests alone does not establish structural quality.

This workflow is read-only: do not modify source code or planning artifacts.
Return findings to the caller; the planning or implementation workflow owns fixes.

## 1. Select the Target

Honor the explicit target before considering unrelated working-tree changes.
These modes describe review targets, not the host application's operating mode.

- **Plan review:** Review the supplied design or planning artifact against its
  requirements and existing repository architecture. Assess proposed components,
  responsibilities, interfaces, and reuse decisions. Do not require an
  implementation diff or invent implementation details that the plan leaves open.
- **Code review:** Review the specified diff, commit, PR, module, or subsystem.
  For a branch, compare against its merge base with the target branch. If no
  explicit target is given, use uncommitted changes against `HEAD`, including
  relevant untracked source files. In a repository without `HEAD`, inspect the
  relevant files directly. If no target can be inferred, ask for one.

Read applicable repository instructions and relevant architecture documentation.
Keep the investigation tied to the requested scope.

## 2. Gather Evidence

Inspect affected components and related callers, interfaces, tests, and existing
utilities. Trace ownership and dependencies beyond the immediate target where
needed. Reuse context already gathered, verifying claims against actual code.

Search by behavior and semantics, not just names. Before recommending reuse or
consolidation, compare contracts, edge cases, and lifecycle requirements. Similar
syntax does not establish equivalent behavior.

For a new project without existing code, use the stated requirements and proposed
contracts. Clearly distinguish design reasoning from verified repository facts.

## 3. Apply the Shared Criteria

Apply these criteria to either the proposed design or its implementation:

| Area | What to assess |
| --- | --- |
| Duplication and reuse | Repeated business logic, orchestration, helpers, or competing implementations of the same responsibility. Identify an appropriate existing owner when one exists. |
| Complexity | Unnecessary branching, transformations, wrappers, redundant state, configuration, defensive logic, or error handling. Distinguish required complexity from incidental machinery. |
| Abstractions | Whether classes, layers, factories, registries, frameworks, and dependencies serve a concrete requirement or established boundary. Challenge speculative extensibility and indirection. |
| Ownership and coupling | Clear responsibilities, consistent interfaces, a single authoritative owner for state, and appropriate dependency direction. Look for changes that spread unrelated responsibilities across modules. |
| Maintainability | Cohesive behavior, understandable data flow, and localized changes. Identify meaningful decomposition or consolidation rather than judging function length or file count. |

Consider simpler alternatives for significant additions. Prefer consistency with
existing architecture unless evidence shows that architecture is problematic.
Do not force unrelated responsibilities into one module merely to avoid new files,
or remove abstractions that enforce needed boundaries or isolate external systems.

## 4. Validate and Prioritize Findings

For each candidate finding, establish the location, supporting evidence, concrete
maintenance cost, and a smaller or clearer alternative. Check that the suggestion
preserves required behavior, compatibility, and important edge cases.

In plan review, cite the proposed decision and repository evidence that supports
the concern. An unspecified implementation detail is an open question only when
it materially affects feasibility or structure; it is not proof of a defect.

Investigate uncertain claims or omit them. Report material evidence gaps separately
and qualify the assessment when they prevent a conclusion. Never invent call sites,
constraints, or findings to fill a quota.

- **High:** Conflicting ownership, architectural duplication, unnecessary subsystems,
  or design choices likely to cause substantial rework.
- **Medium:** Significant avoidable complexity, redundant abstractions, or duplicated
  behavior that increases maintenance cost.
- **Low:** A concrete local structural improvement with modest benefit.

Favor a few high-confidence findings. Exclude cosmetic preferences, arbitrary
line-count reductions, speculative generalization, and large rewrites when a
targeted change is sufficient.

## 5. Report

Order findings by severity. For each, include:

- **Location:** Code path and line, or plan section/task; cite related code as needed.
- **Evidence and problem:** What exists or is proposed, and why it creates a
  structural cost.
- **Recommendation:** A concrete change and any behavior or trade-offs to preserve.

End with an overall assessment and an explicit review status:

- **Review status: Pending:** Missing evidence prevents assessment of a material
  structural decision within the requested scope. Identify the decision, the
  missing evidence, and what would resolve the gap. Report supported findings
  from the assessed portion, but do not give an overall favorable conclusion.
- **Review status: Complete:** Available evidence supports assessment of the
  material structural decisions in scope. State minor limitations; they do not
  block completion. Complete describes review coverage, not approval: High and
  Medium findings may still require resolution by the calling workflow.

If the review is Complete and no supported findings remain, say **No significant
structural issues identified**. A favorable plan review assesses the proposal;
it does not verify an implementation or authorize execution.
