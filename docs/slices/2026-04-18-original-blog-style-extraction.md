# Slice: 2026-04-18 Original Blog Style Extraction

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- documentation artifacts
- semantic model updates
- shared editorial shell follow-on

## Architecture Mode

Extraction of the predecessor's visual language into explicit repository
artifacts:

- capture the dark editorial signals already observed in `../blog`
- keep the extracted style evidence separate from implementation mechanics
- feed the resulting signals into the shared editorial shell model

## Discovery Scope

The request asks for the predecessor's visual language to be made explicit so
`blog-v2` does not drift into a generic starter appearance.

Current repository evidence already identifies the relevant signals:

- dark, text-first, editorial shell
- subdued links and metadata
- compact uppercase section labels
- understated breadcrumb and prose treatments
- outlined topic chips or pills

This slice does not attempt a new runtime implementation. It records the style
signals that justify the already-built shared editorial shell and keeps the
migration evidence explicit.

## Use-Case Contract

### `ExtractEditorialStyleSignals`

Given the predecessor blog and the current repository state, capture the
portable style signals such that:

- the extracted signals are explicit in repository artifacts
- the style evidence can justify bounded shell recovery work
- the extraction does not recreate old templates wholesale

## Main Business Rules

- The extracted insight is the visual language, not the old implementation.
- Shared-style recovery should remain bounded and deterministic.
- The extraction should support the shared editorial shell without expanding
  into a broader redesign.
- Static-hosting compatibility remains a hard constraint.

## Required Ports

- `docs/semantics/model_hypothesis.md`
- `docs/semantics/domain_background_knowledge.md`
- `work/changes/2026-04-18-original-blog-style-extraction/request.md`

## Initial Test Plan

- review semantic docs for explicit predecessor style signals
- verify the shared editorial shell slice already reflects those signals

## Done Criteria

- the predecessor style signals are explicit in repository artifacts
- the request is connected to the existing shared editorial shell recovery
- no production code changes are required for this extraction artifact
