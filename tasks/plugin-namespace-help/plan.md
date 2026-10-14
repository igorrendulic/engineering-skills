# Engineering Skills plugin namespace and help

Feature: `plugin-namespace-help`  
Lifecycle: **Active**  
Readiness: **Ready for implementation**  
Execution: Planning requested; implementation has not started.  
Date: 2026-10-14

## Goal and scope

Make Engineering Skills discoverable as one cohesive plugin with native names
such as `engineering-skills:plan`, plus concise, explanation-only help. Preserve
the existing standalone dispatcher installation for users who still need it.

### Success criteria

1. A plugin-only installation exposes exactly seven skills owned by this plugin:
   `engineering-skills:{init,plan,implementation,pr-review,structural-review,github-pr,help}`.
   It does not expose this bundle's workflows under unqualified names or register
   the root dispatcher as another plugin skill.
2. Installed skills retain working sibling and shared-reference paths. Their
   planning, implementation, review, and authorization rules remain intact.
3. General help lists workflows, purposes, and examples; topic help explains the
   selected workflow's inputs, outputs, and appropriate use. Help never starts
   that workflow or changes project files. Unknown topics produce a useful menu.
4. Existing `$engineering-skills <workflow>` prompts and `sh install.sh [destination]`
   remain supported. `$engineering-skills help [workflow]` also works. A bare
   dispatcher invocation displays help; ambiguous action requests still follow
   the dispatcher's existing clarification behavior.
5. README installation and invocation examples distinguish native plugin setup
   from legacy skill-bundle setup, including avoiding duplicate installations.
6. Local verification covers package loading, installed references, help routing,
   and installer preservation. Existing saved evaluations remain unchanged.

Constraints: Keep one copy of every workflow and the current relative layout.
Preserve short YAML skill names; the plugin supplies the namespace. Retain
implicit invocation behavior. Use standard-library checks and existing evaluation
infrastructure where useful. Do not change personal configuration or installed
skills as part of repository implementation.

Non-goals: Workflow redesign, command renaming, new orchestration, MCP servers,
hooks, automatic removal of old installations, public marketplace submission,
publishing, or expanding the full SDLC model evaluation runner.

## Evidence and current components

- `SKILL.md` owns command routing and the six-workflow table. It currently treats
  unsupported commands as errors and asks for selection on a bare invocation.
- `skills/*/SKILL.md` define six workflows with short names. For example,
  `skills/plan/SKILL.md` loads `../../references/plan-lifecycle.md` and the sibling
  structural-review skill. Moving these directories would create avoidable work.
- `references/` owns shared lifecycle and code-quality guidance.
- `install.sh` clones or fast-forwards the complete repository into
  `~/.agents/skills/engineering-skills` by default. `evals/test_install.py` covers
  preservation of dirty, conflicting, divergent, and symlink destinations.
- `evals/run.py` copies the root dispatcher, `skills/`, and `references/` into a
  temporary standalone skill installation. Its prompts use the dispatcher. Keep
  it as legacy regression coverage; it is not proof of plugin loading.
- No existing feature plan or root plugin manifest was present. The working tree
  was clean before planning. There is no Nx configuration or package manager
  setup in this repository; inherited Nx guidance has no applicable target here.

Official packaging guidance supports a portable root `plugin.json`, automatic
discovery from `skills/`, and repository marketplace entries:
https://developers.openai.com/plugins/build/plugins

A bounded, metadata-only experiment on Codex CLI **0.162.1** used a temporary
plugin and isolated Codex configuration under
`/private/tmp/engineering-plugin-probe-eqct2n3e`. It established:

- A portable `plugin.json` works without `.codex-plugin/plugin.json`.
- `.agents/plugins/marketplace.json` can reference the package root with `./`.
- `codex plugin marketplace add <local-root>` and `codex plugin add <plugin>@<marketplace>`
  successfully install that package.
- App-server `skills/list` returned `engineering-skills-probe:probe`, enabled,
  with the correct plugin ID and no discovery errors. The response is retained
  in the temporary `skills-list.json` for this session.

The probe used no model inference and changed no repository source or personal
plugin configuration. It validates the packaging approach, not the future full
bundle, help behavior, desktop picker, or older client versions. Durable findings
are recorded here; implementation must not depend on that temporary directory.

## Design and decisions

### Package and distribution

Add root `plugin.json` using the Agent Plugins 1.0.0 schema, package name
`engineering-skills`, initial version `0.1.0`, and a concise description. Omit
MCP, hook, compatibility-manifest, and UI configuration unless actual loading
requires it. Keep `skills/`, `references/`, and root `SKILL.md` where they are.

Add `.agents/plugins/marketplace.json` with marketplace name `engineering-skills`
and one plugin entry of the same name, source `{ "source": "local", "path": "./" }`,
installation policy `AVAILABLE`, authentication policy `ON_INSTALL`, and category
`Productivity`. No authentication integration is required for this skills-only
package. Include the marketplace display name `Engineering Skills`.

The primary documented installation uses the native marketplace and plugin CLI:

```sh
codex plugin marketplace add igorrendulic/engineering-skills --ref master
codex plugin add engineering-skills@engineering-skills
```

These remote commands become usable after the changes are published to `master`;
test the local checkout before that. Do not claim a remote release during local
implementation. Document the tested client version rather than asserting an
unverified minimum version or universal support across coding agents.

Keep `install.sh` semantics unchanged and label its README instructions as the
legacy/standalone option. Recommend choosing one installation mode. Explain that
retaining a separately discovered legacy checkout can also expose generic skills;
native packaging cannot suppress an independent installation. Switching users
can disable or relocate their legacy installation through their host's supported
mechanism after checking local changes. Do not delete or rewrite it automatically.

### Help and compatibility

Add only `skills/help/SKILL.md` for help. Its description targets usage questions,
workflow selection advice, and explicit help requests, not execution requests.

Keep the root dispatcher's workflow table as the authoritative catalog; enrich
it with concise purposes and example targets, and register help there. The help
skill reads that table via `../../SKILL.md` as reference data, without executing
the dispatch instructions. It formats examples for the selected installation
mode: native `$engineering-skills:plan ...` or legacy `$engineering-skills plan ...`.

General help displays the catalog. Topic help resolves an exact registered name
or existing supported alias and reads only that workflow's instructions for
explanation. Treat those instructions as the subject of help, not authorization
to execute them. Unknown topics show available choices without guessing paths.
Do not load all workflows for a general menu or create planning artifacts during
help. Keep the distinction between readiness, execution, and verification visible
when explaining the plan/implementation handoff.

The root dispatcher handles `help`, `help <workflow>`, and bare invocation before
normal action inference. Existing explicit commands, prose routing, aliases,
unsupported-command handling, and authorization boundaries remain intact.
There is no text parser or synthetic colon-name wrapper: native discovery owns
namespacing, and the standalone dispatcher owns compatibility.

### Structural plan review

Applied `skills/structural-review/SKILL.md` in plan-review mode against the files
and runtime evidence above. **Review status: Complete. No significant structural
issues identified.** The design has one implementation of each workflow, one
catalog, one native manifest, and an unchanged legacy installer. Root catalog
reuse avoids a second registry; an additional compatibility manifest, copied
plugin tree, installer migration engine, and full evaluation-runner rewrite are
unnecessary. The root dispatcher is deliberately packaged as help reference data
without being registered as a plugin skill.

## Ordered implementation tasks

### Task 1: Package and discover the existing workflows

- Outcome: The current six workflows install and load with native namespacing.
- Changes: Add `plugin.json` and `.agents/plugins/marketplace.json` as specified;
  preserve workflow files and references. Start from isolated task-owned Git state.
- Dependencies: None.
- Acceptance: Local marketplace installation succeeds; all six existing skills
  have namespaced names and correct plugin ownership; root dispatcher is not
  registered; installed shared and sibling references resolve inside the package.
- Verification: Repeat the temporary metadata probe using the actual package in
  an isolated configuration and fresh project. Inspect `skills/list` and cached
  files, not just manifest syntax. Check both source and installed relative links.
  Apply structural code review before dependent work if packaging changes the
  proposed ownership or layout. No personal install or model call is needed.

### Task 2: Add help and preserve dispatcher behavior

- Outcome: Native and legacy help provide usage without running workflows.
- Changes: Add `skills/help/SKILL.md`; update the root catalog and early help
  routing in `SKILL.md`. Reuse existing command names and aliases.
- Dependencies: Task 1.
- Acceptance: Seven plugin-owned skills load. General help is concise; topic help
  explains actual instructions; unknown topics are handled; bare legacy invocation
  shows help. Explicit legacy execution requests still select their workflow.
- Verification: Validate changed skill frontmatter with skill-creator's
  `quick_validate.py`. Exercise general help, `help plan`, `help PR review`, an
  unknown topic, and bare dispatcher invocation. Include a topic prompt containing
  an implementation request as example text and verify it is explained rather
  than executed. Compare project files and Git state before/after help. Verify
  routing for `$engineering-skills plan ...` and native plan selection in a
  disposable fixture. Assess outputs semantically, not by exact prose matching.

### Task 3: Document installation, invocation, and migration

- Outcome: Users can install the plugin and understand the standalone alternative.
- Changes: Update the existing README quick start and workflow examples; retain
  legacy installer instructions in a clearly labeled section. Explain help,
  restart/new-session requirements where observed, and duplicate-install handling.
  Retain existing workflow and lifecycle explanations.
- Dependencies: Tasks 1 and 2.
- Acceptance: Primary examples use native names; standalone examples use the
  dispatcher; installation commands match the tested CLI; local verification and
  remote availability are distinguished. No promise of automatic migration.
- Verification: Walk through local-checkout instructions in the isolated setup.
  Resolve every referenced path. Check the remote recipe against CLI help and
  marketplace configuration without claiming unpublished changes are available.

### Task 4: Add focused package regression coverage

- Outcome: Future changes detect broken distribution and discovery contracts.
- Changes: Extend installer fixture coverage to preserve new package/help files.
  Add focused package checks under `evals/` using standard-library unittest:
  manifest/catalog consistency, real relative references, and a bounded opt-in
  CLI discovery smoke check for the installed package. Keep CLI-dependent checks
  separate from ordinary unit discovery so the base suite does not gain a CLI or
  network dependency. Document exact smoke commands in `evals/README.md`.
- Dependencies: Tasks 1–3.
- Acceptance: Checks detect missing packaged resources and unqualified/missing
  plugin skills. CLI smoke uses local sources, a temporary configuration, explicit
  timeouts, and no credentials or inference. Legacy dirty/conflicting/symlink
  preservation remains covered. Existing full SDLC runner and saved runs remain
  usable and unchanged.
- Verification: `python3 -m unittest discover -s evals -v`, the new metadata smoke,
  and `git diff --check`. Use an intentionally omitted reference or wrong manifest
  name in a temporary fixture to verify the smoke/checks fail meaningfully.

### Task 5: Verify the integrated result and review

- Outcome: Evidence covers the complete installed user experience and compatibility.
- Changes: Fix supported in-scope findings; record results alongside this plan.
- Dependencies: Tasks 1–4.
- Acceptance: Every success criterion has current evidence. Structural code review
  is Complete with no unresolved High/Medium findings. Independent correctness
  review under `skills/pr-review/SKILL.md` has no blocking findings, because this
  change affects public installation and invocation contracts.
- Verification: Reuse passing task checks. Run the Task 2 behavioral cases on the
  final installed snapshot in a bounded isolated agent/session; inspect actual
  outputs, loaded paths, and before/after state. Keep native-plugin and standalone
  cases separate so one cannot mask failure of the other. Do not automatically
  run the paid full `evals/run.py` SDLC benchmark; it is unnecessary for this scope.
  If an additional paid runner is proposed, provide its exact command for approval.
  Apply the implementation skill's bounded repair/re-review loop as needed. Report
  missing runtime evidence instead of substituting static wording checks or
  declaring completion. Desktop picker behavior remains explicitly unverified
  unless exercised in that host.

Tasks are sequential because they share the catalog, packaging, and acceptance
evidence. No parallel agent work is necessary for implementation scheduling.

## Coverage, risks, and readiness

| Criterion | Planned evidence |
| --- | --- |
| 1. Native discovery | Tasks 1, 2, 4: real CLI install and app-server inventory |
| 2. Reference and workflow integrity | Tasks 1, 4, 5: installed links, diff review, final runtime cases |
| 3. Explanation-only help | Tasks 2, 5: outputs, loaded paths, file/Git state comparisons |
| 4. Legacy compatibility | Tasks 2, 4, 5: routing cases and existing installer tests |
| 5. Usable setup and migration | Task 3: local installation walkthrough and README review |
| 6. Verification and preserved history | Tasks 4, 5: regression results and final scope review |

Primary risks are accidentally testing the legacy installation instead of the
plugin, cache staleness at a reused version, and help executing a workflow it was
asked to explain. Use separate temporary installations, fresh configuration for
each smoke, correct plugin ownership/path assertions, and behavioral help cases.
Keep version updates consistent for later releases; do not rely on a stale cache.

The repository's `.agents` path is read-only under the current session permission
profile. Creating its marketplace file during implementation requires the normal
filesystem approval mechanism. This is an execution permission boundary, not an
unresolved design choice; planning does not modify it or request installation.

Requirements, material design choices, structural review, task acceptance, and
verification coverage are complete. **Ready for implementation.** No unresolved
planning decisions. This status does not mean implementation or its checks ran.
