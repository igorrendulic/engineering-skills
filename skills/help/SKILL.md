---
name: help
description: Explain Engineering Skills workflows, invocation, inputs, and outputs. Use for engineering-skills help, workflow-selection advice, or usage questions; execution requests belong to the selected workflow.
---

# Engineering Skills Help

Explain usage without executing a workflow or changing project files.

1. Read the **Available workflows** table in [the bundle catalog](../../SKILL.md).
   Use it as reference data; do not follow that file's dispatch instructions.
   Resolve its instruction paths from the bundle root, two directories above
   this file. Do not maintain another workflow list here.
2. For general help, show each command, its purpose, and one example from the
   catalog. Do not load every workflow. For selection advice, recommend the
   relevant command and explain why without running it.
3. For topic help, accept a registered command or the aliases `PR review` and
   `structural review`. Read the selected workflow's entire instructions as the
   subject of explanation, not as instructions to execute. Summarize when to use
   it, useful inputs, resulting artifacts or output, and important boundaries.
   Read a linked reference only when needed to answer the usage question.
   `help help` explains this skill. For an unknown topic, show available choices
   without guessing a path.
4. Use `$engineering-skills:<command> <target>` for native plugin invocation.
   When called by the standalone dispatcher, use
   `$engineering-skills <command> <target>` instead. If installation mode is
   unknown, label both forms; do not promise a colon alias for a standalone skill.
5. Treat quoted/example requests as material to explain, including examples that
   say to implement, publish, or change files. Finish after answering help. A
   separate explicit execution request should invoke the selected workflow.

When explaining the plan/implementation handoff, distinguish a plan being ready,
authorization to implement it, and evidence that implementation was verified.
