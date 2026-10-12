# Plan Selection and Lifecycle

Shared contract for the planning and implementation workflows.

## Select the Feature and Plan

Honor an explicitly selected feature or plan, including a user-specified path.
Otherwise, infer the feature from the current conversation and use a matching
plan supplied there when available. Match repository artifacts by goal and scope,
following repository conventions and checking `tasks/<feature-slug>/plan.md` with
its `todo.md` checklist. Also inspect legacy `tasks/plan.md` and `tasks/todo.md`
when present. These paths are relative to the target repository root.

Paths identify candidates, not which plan is current. Never select solely by file
recency, unfinished tasks, or being the only Active plan. Multiple features may
be Active. Ask only if the feature or matching plan remains ambiguous after
inspection. Keep tasks attached to their feature and do not collect leftovers
from other plans or introduce a global current-plan pointer.

## Artifact Locations

Reuse the selected feature's existing paths, including legacy paths. For new
artifacts, use a user-specified destination or established repository convention;
otherwise use `tasks/<feature-slug>/plan.md` and `tasks/<feature-slug>/todo.md`.
Choose a short descriptive slug, inspect files before writing, and choose a
distinct slug if the directory belongs to other work. Create directories only
when writing artifacts is permitted by the calling workflow and host constraints.

## Lifecycle

Read the selected plan's lifecycle before continuing. For new plan artifacts,
record the feature name and **Lifecycle: Active** near the top, separately from
readiness. Lifecycle, readiness, and execution authorization are distinct.

- **Active:** Work is being planned or implemented, even if it is Not ready.
- **Paused:** The user has put the work on hold.
- **Completed:** The entire planned outcome has been implemented and verified.
- **Abandoned:** The user has decided not to pursue the plan.

Do not silently resume Paused work or reopen Completed or Abandoned work. Honor
an existing user request to resume or reopen it and return it to Active; otherwise
clarify intent. Change to Paused or Abandoned only when the user directs it.
Finishing planning or implementing only a requested subset does not mark the plan
Completed. Discarding an implementation attempt does not itself abandon the plan.
Update only the selected feature's lifecycle.

For legacy plans without a status, establish intent from their content and the
conversation. Do not assume they are Active or automatically migrate, relabel,
or clean them up.
