# Decisions Log

## Purpose

This document records relevant architectural and implementation decisions for the adopting repository.

Use it to preserve reasoning, avoid re-discussing settled trade-offs without context, and document deviations from `architecture.md` and `groundrules.md`.

---

## Entry Template

```md
## DEC-XXXX - Title

- Date: YYYY-MM-DD
- Status: proposed | accepted | superseded | rejected
- Owners: human | codex | both

### Context
What problem or tension led to this decision?

### Decision
What was decided?

### Consequences
What becomes easier, harder, or different because of this?

### Alternatives considered
What other options were considered and why were they not chosen?

### Notes
Any additional implementation guidance, migration note, or follow-up.
```

---

## Index

Add entries as the repository evolves.

## DEC-0009 - Keep The Pipeline On GitHub-Hosted Runners

- Date: 2026-05-14
- Status: accepted
- Owners: both

### Context
The repository has an open campaign issue requesting that the pipeline remain GitHub-hosted by default unless a specific non-cost reason justifies a different runner model.

### Decision
Keep all current GitHub Actions workflows on GitHub-hosted runners. The existing workflows already use `ubuntu-latest`, and no `self-hosted` runner is configured in the repository. Preserve this default unless a future change introduces a concrete non-cost requirement that cannot be satisfied on GitHub-hosted infrastructure.

### Consequences
The build, test, and publish pipeline stays portable and does not depend on private runtime adjacency. Future workflow changes should treat GitHub-hosted runners as the default and document any exception explicitly.

### Alternatives considered
Move selected jobs to self-hosted runners. This was rejected because the repository does not currently need private adjacency or other runner-specific capabilities.

### Notes
This decision is satisfied by the current workflow configuration in `.github/workflows/quality.yml`, `.github/workflows/gh-pages.yml`, `.github/workflows/notify-discord-on-issue-open.yml`, and `.github/workflows/notify-discord-on-issue-close.yml`.

## DEC-0008 - Scope Dependabot To GitHub Actions And Python Metadata

- Date: 2026-05-08
- Status: accepted
- Owners: both

### Context
The repository had no Dependabot configuration, so version updates for GitHub Actions and Python package metadata were not being tracked automatically. The project currently has no runtime Python dependencies, but it does have a GitHub Actions workflow and a `pyproject.toml` manifest that can grow over time.

### Decision
Enable Dependabot for two ecosystems only:

- `github-actions` at the repository root
- `pip` at the repository root, to cover the Python manifest and any future package pins

Schedule both updaters weekly.

### Consequences
GitHub Actions updates and Python dependency updates will surface through automated pull requests instead of relying on manual review. The `pip` updater is mostly dormant today because the manifest has no runtime dependencies, but it establishes the update path for future Python pins without expanding to unrelated ecosystems.

### Alternatives considered
Track only GitHub Actions. This was rejected because the Python manifest is part of the repository contract and should be ready for dependency updates if they are introduced later.

Add broader ecosystem coverage. This was rejected because the repository does not currently use those ecosystems, so extra updaters would add noise without value.

### Notes
If the repository adopts a lockfile or another Python dependency manager later, update Dependabot to match the chosen workflow instead of layering multiple overlapping Python updaters.

## DEC-0007 - Split Code And Content Licensing

- Date: 2026-04-26
- Status: accepted
- Owners: both

### Context
The repository contains both software used to transform and publish the site and authored blog material intended as publication content. A single MIT license for the whole repository would make the content easier to reuse commercially and without reciprocal content terms than intended.

### Decision
Use split licensing for `blog-v2`:

- code, build tooling, tests, and operating workflow documents are licensed under MPL-2.0
- blog content, publication assets, semantic artifacts, slice artifacts, and generated publication output derived from that content are licensed under CC BY-NC-SA 4.0

The root `LICENSE` file records the scope rules and points to full license texts under `LICENSES/`.

### Consequences
The site generator remains open source under a file-level copyleft license, while the published editorial material has attribution, non-commercial, and share-alike terms. Contributors and downstream users must pay attention to file scope instead of assuming one repository-wide license.

### Alternatives considered
Keep MIT for the whole repository. This was rejected because MIT is shaped for software reuse and does not express the intended terms for blog content.

Use CC BY 4.0 for content and MIT for code. This would maximize reuse, but it would allow commercial content reuse and would not require shared terms for adaptations.

### Notes
If future files need different terms, add explicit file-level notices and update the root `LICENSE` scope instead of relying on implicit exceptions.

## DEC-0006 - Commit After Each Completed Change

- Date: 2026-04-24
- Status: accepted
- Owners: both

### Context
The workflow benefits from treating git commits as the closure point for a completed slice or documentation change. Without that rule, finished work can remain uncommitted while attention moves to the next task, which weakens traceability and makes it harder to preserve a clean artifact trail.

### Decision
After each completed change, create the commit before starting the next task. The commit should stay scoped to the finished slice or documentation change whenever practical.

### Consequences
The repository gains a tighter record of completed work, fewer mixed-purpose working trees, and clearer checkpoints for review or rollback. The tradeoff is a slightly higher commit cadence, which is intentional.

### Alternatives considered
Batch several completed changes into a later commit. This was rejected because it delays closure and blurs the boundary between finished and unfinished work.

### Notes
This rule applies to ordinary repository work, not to an in-progress multi-file edit that is still part of one unfinished change.

## DEC-0001 - Separate MRL Core From Implementation Packs

- Date: 2026-03-29
- Status: accepted
- Owners: both

### Context
The starter was presenting Python plus a DDD-inspired modular monolith as if that were the default shape of MRL itself. That creates confusion when a repository needs another language, another architecture such as event sourcing, or more than one runtime.

### Decision
The repository now distinguishes between:

- MRL core, which stays artifact-driven and architecture-agnostic
- implementation packs, which define language, architecture, structure, and testing defaults

The current repository keeps `python_ddd_monolith` as the example selected pack.

### Consequences
It becomes easier to reuse the same refinement workflow across Python, JavaScript, Go, event-sourced, and polyglot client/server repositories. It also becomes necessary to make the selected pack explicit in architecture docs and slice docs.

### Alternatives considered
Keep one universal Python starter and treat every other shape as an undocumented deviation. This was rejected because it would keep conflating MRL with one implementation style.

### Notes
Future pack additions should live under `docs/packs/` and should be referenced by slice documents when the runtime topology matters.

## DEC-0002 - Treat Skill Model Guidance As Advisory

- Date: 2026-04-02
- Status: accepted
- Owners: both

### Context
The repository skills now include model guidance for tasks such as `build`, `refine`, and `extract`. That creates a potential ambiguity: a reader could assume that naming a preferred model in a skill will automatically switch the active Codex model or force sub-agent routing during execution.

### Decision
Model guidance inside repository skills is advisory only. It documents which model shape is usually a good fit for the task, but it does not by itself require automatic model switching, worker spawning, or hard routing behavior.

### Consequences
The skills remain durable even if model names, availability, or routing capabilities change. The repository gains clearer guidance for future operators and tooling, but predictable model selection still requires explicit runtime policy or orchestration outside the skill text.

### Alternatives considered
Encode specific model names in skills as if they were enforced execution rules. This was rejected because skill text alone does not guarantee runtime behavior and would overstate what the repository can currently control.

### Notes
If the repository later wants deterministic skill-to-model routing, document that as a separate operational decision and implement it in the calling workflow or agent orchestration layer.

## DEC-0003 - Avoid `.codex` Repository Artifacts For Now

- Date: 2026-04-02
- Status: accepted
- Owners: both

### Context
The repository has used `.codex`-specific artifacts while shaping the workflow. That creates a risk that the MRL process starts to look tool-defined rather than process-defined before it is clear whether MRL can stay tool-agnostic in practice.

### Decision
For now, the repository should avoid relying on `.codex` as part of the committed process shape. The workflow should stay centered on MRL artifacts and repository documents rather than tool-specific folders. This decision is explicitly reversible while the team validates whether MRL can remain tool-agnostic or whether a specific AI tool will prove operationally necessary.

### Consequences
The repository stays cleaner and more focused on portable process artifacts. It may require some extra translation when using Codex or another tool because fewer tool-native conventions are captured directly in versioned files. The decision also preserves room to adopt tool-specific support later if real usage shows that generic artifacts are not enough.

### Alternatives considered
Keep `.codex` as a first-class part of the repository workflow immediately. This was rejected for now because it would prematurely optimize for one tool before validating whether that coupling is necessary for MRL.

### Notes
If future evidence shows that MRL depends on stable capabilities from a specific AI tool, record a follow-up decision describing the required coupling, why generic artifacts were insufficient, and which tool-specific assets should become part of the repository.

## DEC-0004 - Target Static GitHub Pages Deployment For `blog-v2`

- Date: 2026-04-16
- Status: accepted
- Owners: both

### Context
The predecessor `../blog` repository currently deploys through AWS-backed
container infrastructure and includes a first-party `/api` path for analytics
ingestion. The intended direction for `blog-v2` is to simplify the runtime back
to static hosting and remove the dependency on that first-party backend path.

### Decision
`blog-v2` will treat GitHub Pages as the primary deployment target for the
site's initial slices. The generated site must remain valid when served as
static files only. Analytics, if enabled, must use direct third-party endpoints
or stay disabled; the blog must not require its own same-origin `/api`.

### Consequences
The early implementation can optimize for deterministic static output and a
simple deployment workflow. AWS infrastructure material from `../infrastructure`
is retained only as migration context and reference, not as the target runtime
for the site itself.

### Alternatives considered
Continue the AWS container plus API ingestion path as the default for `v2`.
This was rejected because it carries runtime complexity that is not required to
publish the blog and conflicts with the desired GitHub Pages deployment shape.

### Notes
If a future slice reintroduces server-side capabilities, that should be
documented as a new decision rather than silently undoing the static-site
assumption.

## DEC-0005 - Keep The Static Site Generator In Python

- Date: 2026-04-19
- Status: accepted
- Owners: both

### Context
The predecessor repository used Go for static generation, but `blog-v2` already
has its content model, build logic, CLI, tests, and dev tooling in Python. The
generator is part of an active refinement loop, so iteration speed and low
ceremony matter more than packaging the build tool as a standalone binary.

### Decision
`blog-v2` will keep the static site generator in Python. The build pipeline,
local dev server, and supporting tests should continue to use the existing
Python implementation rather than being rewritten in Go or Node.js.

### Consequences
The repository keeps one language across the build loop, which reduces friction
for slice-level changes, testing, and local development. The generator remains
easy to inspect and evolve, and the dev-server reload path can reuse the same
Python code path as the production build.

### Alternatives considered
Rewrite the generator in Go. That would improve standalone binary packaging,
but it would add ceremony without solving a current problem in the repository.

Rewrite the generator in Node.js. That would align more closely with browser
tooling, but it would introduce a second runtime and dependency model without a
clear benefit for the current Python-shaped codebase.

### Notes
If the generator later becomes a distributed tool or build performance becomes a
measured bottleneck, revisit this decision as a separate entry rather than
implicit drift.
