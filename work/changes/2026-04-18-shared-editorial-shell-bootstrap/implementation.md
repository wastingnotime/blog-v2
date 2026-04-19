# Implementation Notes

## Summary

Implemented the shared shell recovery by aligning the document renderer with
the original blog's dark, mono editorial style.

## Changes

- updated the shared document renderer in
  `src/app/application/use_cases/build_site.py` to use a black background,
  monospace typography, muted zinc-style links, and slash-separated navigation
- restored the original blog's dark shell cues for headings, metadata,
  prose, code, and topic chips
- updated unit and integration assertions to verify the dark shell contract
  instead of the earlier light serif shell

## Validation

- `python3 -m pytest tests/unit/test_build_site.py tests/integration/test_run_scenario.py`
