Add `done <id>` to Task CLI so I can complete a task and see its completed status
in subsequent listings. Use `tasks/done/` for the feature plan.

Requirements:
- Persist completion across processes without changing task order, IDs, titles,
  extra fields, or other tasks.
- Completing an already-completed task succeeds without writing the data file.
- Unknown IDs and invalid IDs (non-integer, zero, or negative) exit nonzero and
  leave storage unchanged, including when the file does not exist.
- Preserve existing add/list behavior and storage format. Do not add dependencies.
- Preserve the unrelated local edit to NOTES.txt, including its unstaged state.

Use README.md as the authoritative project document. Keep the current component
boundaries and standard-library tooling; do not add optional tools. No other
product decisions or external services are needed. There is no issue/PR URL.
Do not commit, push, create a remote PR, or merge. This is a local development task.
