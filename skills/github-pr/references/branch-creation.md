# Branch Creation From Default Branch

Use this reference when the full workflow starts from the repo's default branch and a feature branch must be created.

Before creating a branch from a dirty checkout, the main workflow must classify uncommitted changes, including mixed-ownership hunks within a path, and ask the user whether other local changes belong in this PR or a separate PR. Do not use checkout or stash commands to bypass that decision.

## Decision Flow

### 1. Fetch fresh remote base

```bash
git fetch --no-tags origin <base>
```

If fetch fails because of network, auth, or missing remote, create the branch from current local `HEAD` and note that base freshness was not verified. Do not run the unpushed-commit check without a fresh remote base.

### 2. Check for unpushed local commits

```bash
git log origin/<base>..HEAD --oneline
```

- Empty output: set `BASE_REF=origin/<base>` and continue.
- Non-empty output: show the commit list and ask:

```text
Local <base> has N unpushed commits not on origin/<base>. Carry them onto the new feature branch, or leave them on local <base>?
```

If the user chooses to carry them forward, set `BASE_REF=HEAD`.

If the user chooses to leave them on the default branch, set `BASE_REF=origin/<base>`.

Never default silently. Accidentally carrying unrelated local default-branch commits into a PR is worse than asking.

### 3. Create the feature branch

```bash
git checkout -b <branch-name> "$BASE_REF"
```

If checkout fails because uncommitted changes would be overwritten, follow the
main workflow's stash authorization rules before retrying. For paths containing
only current-PR changes, use the following recipe only when there are no staged
changes outside those paths. A path-scoped stash can record the whole index;
`apply --index` can fail by trying to reapply unrelated changes still staged.
When that condition is not met, use an isolated transfer of the selected changes
that preserves the original index and working tree, or resolve preservation
before switching branches. Do not unstage unrelated work to fit this recipe.

```bash
git stash push -u -m "github-pr: pre-branch <branch-name>" -- <current-pr-paths>
STASH_REF=$(git rev-parse refs/stash)
git checkout -b <branch-name> "$BASE_REF"
git stash apply --index "$STASH_REF"
```

Use explicit current-PR paths when stashing. Path-scoped stashing includes all
changes in those paths; it is not safe isolation for mixed-ownership hunks. If
mixed-ownership or separate-PR paths would be disturbed, resolve how to preserve
them before checkout. Never stash all dirty files after the user has routed some
of them to a separate PR unless the user explicitly asks for that.

If checkout or stash restoration fails, stop and report the state and recorded
stash ref. Do not apply the stash after a failed checkout. Verify restored
contents and the staged/unstaged split; do not auto-resolve stash conflicts or
drop the stash.

## Existing Linked Worktrees

If the current directory is already a linked worktree, do not run `git worktree add` from inside it. Create or switch the branch in the current directory so the harness remains in the visible workspace.
