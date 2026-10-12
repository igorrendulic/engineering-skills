# Engineering Skills

A small set of AI coding-agent skills for taking work from an idea to a verified pull request. Plan around existing code, implement in manageable increments, and review both correctness and structure.

**Simple designs. Explicit scope. Evidence before completion.**

## Quick start

Install the full bundle into your user-level skills directory:

```sh
git clone https://github.com/igorrendulic/engineering-skills.git ~/.agents/skills/engineering-skills
```

Then invoke a workflow in your coding agent:

```text
$engineering-skills init
$engineering-skills plan Add password reset
$engineering-skills implementation Implement the password-reset plan
$engineering-skills pr-review Review the password-reset changes
$engineering-skills github-pr Create a PR for these changes
```

The install preserves shared references and sibling skills. The workflow examples above are agent prompts, not shell commands.

`plan` includes structural design review. `implementation` includes structural review at substantial checkpoints and independent `pr-review` when required, with repairs and re-review. The example makes `pr-review` explicit before PR creation; an existing review can be reused while its scope, snapshot, and evidence still apply.

## The SDLC

```mermaid
flowchart TD
    A["init: establish project instructions"] --> B

    subgraph Planning["plan workflow"]
        B["Define goal, scope, and design"] --> C["structural-review: assess the design"]
        C --> D["Resolve findings; define tasks and verification"]
        D --> P{"Plan ready?"}
        P -->|Revise within scope| B
        P -->|Blocked| Q["Report blockers; plan remains not ready"]
    end

    P -->|Yes, implementation authorized| E

    subgraph Implementation["implementation workflow"]
        E["Build or repair and verify increments"] --> F["structural-review: at substantial checkpoints"]
        F --> S{"Required structural review complete, with no unresolved High or Medium findings?"}
        S -->|Yes or not required| G["Verify the complete outcome"]
        S -->|No| R
        G --> H{"Independent review required?"}
        H -->|Yes| I["pr-review: fresh-context correctness review"]
        I --> J{"No blocking findings and required verification satisfied?"}
        H -->|No| J
        J -->|No| R{"Can resolve within scope and remaining repair limit?"}
        R -->|Yes| E
        R -->|No: limit, no progress, or blocked| X["Preserve work; report unresolved findings or evidence gaps"]
        J -->|Yes| V["Retain verified implementation; report results"]
    end

    V -->|PR delivery authorized| K["github-pr: create or update the PR"]
```

Start at the stage that fits the work; small, obvious changes can go straight to implementation. Review steps inside each workflow are invoked by that workflow. Independent review is required for substantial behavior changes, changes affecting security, data integrity, or shared/public contracts, and whenever the user or repository requires it. Explicit review waivers must be disclosed. The review-and-fix loop defaults to at most three repair rounds, each including a fresh follow-up review; it stops earlier when progress or authorization is blocked. Missing required evidence prevents completion. Publishing, merging, and deployment follow the user's authorization.

## Workflows

| Workflow | What it does |
| --- | --- |
| [init](skills/init/SKILL.md) | Create or conservatively update root `AGENTS.md` from repository evidence. |
| [plan](skills/plan/SKILL.md) | Define success criteria, review the design, and order verifiable tasks. |
| [implementation](skills/implementation/SKILL.md) | Implement, verify, and repair supported findings within scope. |
| [structural-review](skills/structural-review/SKILL.md) | Assess ownership, complexity, reuse, and maintainability in plans or code. |
| [pr-review](skills/pr-review/SKILL.md) | Independently review correctness and regressions in fresh context. |
| [github-pr](skills/github-pr/SKILL.md) | Prepare branches, commits, and PRs with clear rationale and validation evidence. |

Plans default to `tasks/<feature-slug>/plan.md` and `todo.md`, while respecting existing project conventions. See the shared [plan lifecycle](references/plan-lifecycle.md) and [code quality principles](references/code-quality.md).

## Contributing

Add workflows under `skills/<name>/SKILL.md` and register them in the root [dispatcher](SKILL.md). Keep instructions focused, reuse shared references, and include verification appropriate to the change.
