---
name: github-pr
description: Create or update GitHub pull requests from the current repository using git and the GitHub CLI. Use when asked to open, create, ship, draft, describe, rewrite, or update a PR; turn uncommitted or committed changes into a branch-backed pull request; generate a high-quality PR title/body; or handle branch, commit, push, and gh pr create/edit workflows safely.
---

# GitHub Pull Request

Turn the current repo state into a reviewable GitHub pull request. Prefer the full workflow unless the user explicitly asks only for a PR description or only to update an existing PR body.

When this skill says to ask the user, use the available blocking question tool if the harness provides one. If no blocking question tool exists, ask plainly in chat and wait. Do not silently choose when the skill says a decision must be user-owned.

## Modes

- **Full workflow**: inspect context, resolve branch state, commit changes if needed, push, compose the PR title/body, and create or report the PR.
- **Description-only**: draft a title/body for the current branch or a supplied PR ref. Print the result and stop unless the user asks to apply it.
- **Description update**: rewrite an existing open PR title/body. Preview the new title and body summary, ask for confirmation, then apply with `gh pr edit`.

## Step 1: Gather Context

Run focused read-only commands before deciding what to do:

```bash
git status --short --branch
git diff --stat HEAD
git diff HEAD
git diff --cached
git diff
git branch --show-current
git log --oneline -10
git remote -v
git rev-parse --abbrev-ref origin/HEAD 2>/dev/null || echo DEFAULT_BRANCH_UNRESOLVED
```

For an existing PR, honor the supplied URL or reference before considering the
current branch. Resolve a bare number or branch in the intended repository; ask
only if that repository is ambiguous. Without an explicit reference, discover
the current branch's PR. Read its URL, title, body, state, base, and head with
`gh pr view`, and retain the returned canonical URL as `PR_URL` for all subsequent
PR reads and edits. A failed lookup is a blocker to resolve, not permission to
fall back to another PR or create one. Description-only and description-update
requests do not authorize checkout changes, commits, or pushes.

Also check whether the current checkout is a linked worktree:

```bash
git rev-parse --absolute-git-dir
git rev-parse --git-common-dir
git rev-parse --show-superproject-working-tree
```

Resolve the common git dir to an absolute path before comparing it with `--absolute-git-dir`. If they differ and `--show-superproject-working-tree` is empty, this is already a linked worktree. Reuse it when it belongs to the target; do not create a nested worktree.

## Step 2: Resolve Branch State

For an existing PR in the full workflow, resolve its head repository, head branch,
and head commit from `PR_URL` before staging, committing, or pushing. Verify that
the selected checkout belongs to that PR and that the remote's push URL targets
the head repository, including when the head is in a fork. A matching branch name
alone is insufficient. If the checkout does not match, locate a matching checkout
or use an isolated worktree based on the PR's actual head, preserving unrelated
local work. Transfer intended local changes only under Step 3's ownership rules.
If the target cannot be established, report the blocker without pushing. A
supplied PR URL never makes the current branch its head. Description-only and
description-update modes continue using `PR_URL` without checkout changes or pushes.

Resolve the default branch in this order:

1. `git rev-parse --abbrev-ref origin/HEAD`, stripping `origin/`.
2. `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`.
3. Existing remote branches named `main`, `master`, or `develop`.
4. Ask the user if no base can be resolved.

Branch routing:

- Detached `HEAD`: create a feature branch from current `HEAD` before committing or pushing.
- On default branch with no uncommitted changes and no unpushed commits: report that there is no feature-branch work to PR and stop.
- On default branch with work: resolve uncommitted change ownership using Step 3 before creating a feature branch. Then create the branch for the current-PR changes. Read `references/branch-creation.md` before creating it.
- On a feature branch: continue in place after any existing-PR target check above.
- Existing open PR for the branch: push new commits using Step 4's verified destination, report the PR URL, then ask before rewriting the description.

Derive branch names from the change intent using lowercase hyphenated words, for example `fix-pr-description-body-file`. If the name exists, add a short numeric suffix.

## Step 3: Resolve Uncommitted Change Ownership

Before staging, committing, or creating a feature branch from a dirty checkout,
inspect staged and unstaged diffs separately and read relevant untracked files.
Classify changes from that evidence, including individual hunks when a path
contains more than one concern:

- **Current PR changes**: changes that clearly belong to the user's requested PR intent.
- **Other local changes**: changes that appear unrelated, ambiguous, generated outside the current intent, or part of a different logical change.

A path can contain both groups. Record the existing staged/unstaged split before
modifying the index; whole-file inclusion is not implied by owning one hunk.

If there are any other local changes, do not ignore them and do not silently leave them behind. Show the user the grouped paths with a concise reason for the classification, then ask:

```text
I found other uncommitted changes that do not clearly belong to this PR. Include them in this PR, or keep them for a separate PR?
```

The user owns this decision. If they choose:

- **Include in this PR**: treat the selected paths as current PR changes and include them in the commit plan.
- **Separate PR**: keep the selected paths out of this PR, report that they remain for a separate PR, and include the exact path list in the final report. If branch creation or checkout would disturb current-PR or separate-PR paths, ask before stashing. Stash only the paths the user authorizes for that purpose, use a descriptive message, restore the stash as soon as it is safe, and report the stash result. Do not drop the stash.
- **Split selection**: include only the selected paths in this PR and keep the rest for a separate PR.

If the user says the other changes should be a separate PR and asks you to create it too, finish or safely pause the current PR flow first, then start a new full workflow for those paths. Never stage separate-PR paths into the current PR.

## Step 4: Commit and Push

Skip commit creation when the working tree is clean and all intended commits already exist on the branch.

When committing:

- Match repo commit style from recent commits and project instructions.
- Prefer one commit. Use 2-3 commits only when changed files clearly represent separate logical concerns.
- Stage explicit paths only when all their changes belong to this PR; otherwise
  select only the intended hunks. Do not use `git add .`, `git add -A`, or
  `git commit -a`.
- Existing staged changes are part of a normal commit even if this workflow did
  not stage them. If unrelated changes are staged, prepare the commit in an
  isolated temporary index or task checkout containing only current-PR changes.
  Preserve unrelated working-tree contents and their staged/unstaged split;
  after committing, reconcile only the committed changes against the new HEAD.
  Do not bulk reset, unstage, or stash unrelated work to simplify committing.
- Before each commit, inspect the **entire prospective commit diff** against its
  parent, including pre-existing staged changes, additions, deletions, and renames.
  Verify it contains exactly the selected changes. A path-limited commit can still
  include unrelated hunks in that path. If changes cannot be separated safely,
  report the specific ambiguity before committing.
- If commit hooks fail, inspect the failure and fix only issues caused by the intended change.

Before pushing, inspect the resulting commit and confirm unrelated work and its
staging state are preserved. A commit containing unexpected changes must be
resolved within existing authorization before publication.

For an existing PR, recheck the verified head repository and branch before pushing.
Set `PR_HEAD_REMOTE` to the remote whose push URL matches that repository and
`PR_HEAD_BRANCH` to the PR's head branch. Push explicitly:

```bash
git push "$PR_HEAD_REMOTE" "HEAD:refs/heads/$PR_HEAD_BRANCH"
```

Record the intended local commit before pushing. After success, read that same PR
with `gh pr view "$PR_URL" --json url,headRefOid` and verify its head commit matches
the recorded commit before reporting success. Report a mismatch or failed readback
as unverified; do not force-push to make it match.

For a new PR, push with:

```bash
git push -u origin HEAD
```

If push fails because auth, network, or permissions are unavailable, stop and report the exact blocker and the branch/commit state.

## Step 5: Compose Title and Body

Always read `references/pr-description-writing.md` in full before composing or rewriting a title/body.

For PR creation, description-only drafts, and description updates, require exactly these three sections in order: `# Why`, `# What changed`, and `# Validation and Proof`. Use the reference's checklist even when the repository has another PR template; preserve its required information and existing evidence within these sections. Checklist items report evidence, not new execution or approval gates.

Inputs to use:

- User request and conversation context.
- Branch name and commits.
- Full diff against the base branch.
- Existing PR body when rewriting.
- PR template if present.
- Validation commands actually run and their outcomes.
- Supplied evidence links, screenshots, recordings, or artifact paths.

Do not invent validation, issue-closing references, screenshots, or product behavior. If a required related-work decision is ambiguous, ask; otherwise use neutral `Related:` references or omit the reference.

## Step 6: Apply With `gh`

Resolve the PR-body file before creating or updating the PR:

- When the active session context clearly identifies a `plan_name`, create `.agent/<plan_name>/` if needed and write the body to `.agent/<plan_name>/pr_body.md`.
- Infer `plan_name` only from the active session or plan context. Do not scan `.agent/` and guess from unrelated plan directories.
- If no single plan name can be determined from that context, fall back to a unique real temporary file, for example `mktemp "${TMPDIR:-/private/tmp}/github-pr-body.XXXXXX.md"`.
- Keep a plan-scoped `pr_body.md` after the GitHub command so it remains with the plan context. A fallback temp file remains temporary.

For a new PR, write the body to the resolved file and call:

```bash
gh pr create --title "<TITLE>" --body-file "$BODY_FILE"
```

For an existing PR update, preview first:

- New title.
- First two sentences of the new body.
- Total body line count.

Ask for confirmation, then call:

```bash
gh pr edit "$PR_URL" --title "<TITLE>" --body-file "$BODY_FILE"
```

Read back that same PR with `gh pr view "$PR_URL" --json url,title,body` and confirm
the target and persisted title/body match the intended update before reporting
success. Never replace the resolved target with the current branch's PR.

Never pass a multi-line body through inline command substitution, stdin, or `--body "$(cat ...)"`. Use `--body-file` with the resolved real file so wrappers cannot silently create an empty PR body.

## Step 7: Report

Report:

- PR URL, or the exact reason PR creation/update could not be completed.
- Branch name and pushed state.
- Commits created, if any.
- Validation performed, including commands not run and why.
- Other local changes that were routed to a separate PR, including exact paths and whether they are restored, still unstaged, or in a named stash.
- Any user action still required, such as resolving stash conflicts, authenticating `gh`, or creating the separate PR for routed local changes.
