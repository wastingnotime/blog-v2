# Implementation

## Scope Applied

This slice adds one shared site frame around generated pages:

- every rendered route now receives the same top-level navigation shell
- navigation state is projected deterministically from the route path
- representative routes highlight one active top-level section: home, sagas,
  library, studio, or about

## Boundary Notes

The chrome stays inside the static builder and does not depend on any runtime
framework. Active-state logic is isolated in a dedicated use case so the shared
layout does not rely on brittle page-specific conditionals spread through the
renderer.
