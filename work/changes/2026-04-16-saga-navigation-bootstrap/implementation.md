# Implementation

## Scope Applied

This slice restores the minimum navigable hierarchy for saga content:

- arc records are loaded explicitly from repository markdown
- saga pages project arc summaries and a timeline
- arc pages project ordered episode links
- episode pages expose parent and adjacent navigation

## Boundary Notes

Navigation projection is implemented as an explicit application use case rather
than buried inside the builder so ordering and adjacency rules remain
inspectable and testable.

The committed content set now includes a second episode in the HireFlow arc so
adjacent navigation can be verified deterministically in both unit and
integration tests.
