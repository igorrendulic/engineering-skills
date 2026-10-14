# Local checks and skill improvement eval

## Package and installer checks

Run the standard-library regression suite without model calls:

```sh
python3 -m unittest discover -s evals -v
```

With Codex CLI installed, separately check the actual local package installation
and discovery (tested with 0.162.1):

```sh
python3 evals/plugin_smoke.py
```

The smoke check copies the package into a temporary local marketplace, installs
it into a disposable home, and queries app-server `skills/list`. It requires all
seven enabled, namespaced skills with the correct plugin ownership and installed
paths, and checks internal instruction references. It uses no credentials or model
inference and does not change the personal plugin installation. Each subprocess
or metadata request has a timeout; temporary files are removed after the check.
An alternate checkout can be checked with `--package /absolute/path/to/checkout`.

These checks validate packaging, not help's decisions. For behavioral verification,
use separate disposable plugin and standalone sessions. Exercise general help,
`help plan`, `help PR review`, an unknown topic, bare standalone invocation, and
help containing a quoted implementation request. Inspect the answers and loaded
skill paths, and compare project files and Git state before and after help. Check
that both native and standalone plan invocations select their intended workflow.
Keep transcripts and installed-package fingerprints with local run evidence.

## Full SDLC evaluation

Run a small development task through this repository's `init`, `plan`,
`implementation` (including structural/native review), and description-only
`github-pr` workflows. No GitHub access, publication, or CI is involved.

Requires macOS or Linux, Python 3.11+, Git, and Codex CLI (tested with 0.162.1).
Sign in with `codex login`, or provide `CODEX_API_KEY`. The default
model is `gpt-6.1-sol`; account availability varies. Model inference uses the
configured provider, while execution and artifacts stay on your machine.

```sh
python3 -m unittest discover -s evals -v
python3 evals/run.py --model gpt-6.1-sol
python3 evals/run.py --model gpt-6.1-sol --variant sparse-ids
```

The runner tests the standalone dispatcher. It uses a disposable Git repository
and isolated agent home, copies only this skill bundle, and temporarily copies
local authentication when using login.
Credentials are removed with the temporary home and never intentionally included
in run artifacts. Agent shell networking is enabled for native review's model
connection. Use this runner with the trusted local fixture and skills only.

Each run retains its project, skill snapshot/fingerprint, prompts, JSONL events,
stderr, final messages, checks, and report in ignored `evals/runs/`. Runs time out
after 30 minutes (`--timeout SECONDS` overrides this). Exit codes: 0 automated
checks pass, 1 task checks fail, 2 infrastructure/configuration failure. A
successful process exit is not sufficient: the CLI must emit `turn.completed`.

Acceptance tests run outside the agent workspace after development. This is
separation for ordinary evaluation, not a hardened adversarial sandbox. Outer
session token usage is recorded; nested review usage may be additional. The PR
stage drafts text only and its evidence must be checked against transcripts.

## Improvement loop

Inspect the report and transcripts before changing a skill. Assess plan quality,
appropriate reuse, unnecessary work, truthful verification, review scope and
independence, and final-snapshot applicability. Record findings with evidence in
the run directory. The grader requires a completed native-review session and saves
its verdict for inspection. Review quality, resolution of findings, and whether
its scope and snapshot are correct require transcript assessment. Missing
or incompatible native review records fail the check rather than silently passing.

Distinguish runner/fixture defects from model mistakes and unclear skill rules.
Prefer a small general clarification or simplification, then rerun the same
scenario/model from a clean fixture. Keep before/after evidence. Allow at most
three skill-revision rounds; after improvement, run a fresh confirmation and the
sparse-ID variation. Do not weaken acceptance checks to obtain a pass.

The fixture follows Python's standard-library argparse approach:
https://docs.python.org/3/howto/argparse.html
It is a focused smoke test, not a statistical comparison against no-skills agents.
