---
name: wrightkit-test-design-review
description: Review whether a proposed or newly added WrightKit test protects a durable contract or distinct failure mode without unnecessary duplication, instability, fixture cost, or production coupling. Return keep, consolidate, rewrite, or delete.
---

# WrightKit Test Design Review

Use this skill to decide whether a test is worth keeping and whether it protects the right surface. A code change does not automatically require a new test, and fewer tests can be the correct result.

The authoritative rules are `.github/docs/testing-policy.md` and `.github/docs/engineering-quality.md`. Repository-local guidance may add stricter requirements. Do not restate those policies here.

## Review principles

### A durable test needs a durable claim

Identify the observable behavior, regression, public contract, or stable invariant the test is meant to protect.

Why: without an independent claim, a test usually records the current implementation rather than constraining correctness.

### Existing coverage changes the value of a new test

Look for the nearest focused, integration, property, corpus, oracle, or end-to-end coverage and ask whether the proposed test would detect a distinct plausible failure.

Why: duplicated tests increase maintenance without necessarily increasing confidence.

### Protect contracts, not implementation shape

Prefer assertions about observable semantics, diagnostics, invariants, and externally meaningful results. Treat private structure, helper calls, incidental formatting, mutable inventories, and current counts as unstable unless a contract explicitly makes them observable.

Why: a good regression test should survive a correct internal rewrite.

### Use the smallest useful test surface

Choose the layer that exposes the failure clearly without duplicating broader coverage. A lower-level test is useful when it isolates a failure that higher-level coverage would make hard to diagnose; a higher-level test is useful when the contract itself is user-facing or cross-component.

Why: test value comes from the failure mode it protects, not from maximizing the number of layers that repeat the same behavior.

### Tests belong to features, not work items

Before accepting a test, identify the stable feature that owns it, then identify the contract, invariant, regression, or failure mode it protects within that feature. Organize the test under that feature and behavior. Issue, pull-request, and task identifiers may be retained as provenance, but they must not define the test file, module, suite, case name, or directory.

Why: issues are planning containers whose scope can be narrow or aggregate multiple capabilities; using them as test taxonomy makes coverage reflect project bookkeeping instead of the product contract.

### Include maintenance cost in the design

Fixtures, snapshots, generated expectations, test-only APIs, and visibility changes all create obligations. Prefer small representative inputs and existing public or internal boundaries when they are sufficient.

Why: a test that distorts production design or requires constant bookkeeping can cost more than the regression risk it protects.

## Workflow

Reason through these questions rather than treating them as a mandatory checklist:

- Which stable feature owns this test?
- What contract, invariant, regression, or failure mode does it protect within that feature?
- Is any Issue/PR/task identifier being used as taxonomy rather than provenance?
- What existing coverage already protects that claim?
- What distinct incorrect implementation would this test catch?
- Is the assertion stable across a correct internal rewrite?
- Is this the smallest useful layer and input?
- Does the test introduce disproportionate fixture or production-surface cost?

If repository admission of a fixture, corpus case, snapshot, or verification artifact is part of the decision, route that question to `.github/docs/testing-policy.md` instead of inventing a local evidence policy.

## Decision

Return exactly one primary recommendation:

- `keep` — protects a durable claim or distinct failure mode at an appropriate cost.
- `consolidate` — valuable coverage exists, but equivalent tests can be combined or moved to a better surface.
- `rewrite` — the intended claim is valuable, but the assertions, input, fixture, or test boundary targets unstable or incidental behavior.
- `delete` — there is no durable claim, no distinct failure mode, or the test exists mainly to mirror the implementation.

Use a concise rationale:

```text
Recommendation: keep | consolidate | rewrite | delete
Feature: <stable owning feature>
Claim: <observable behavior, regression, or invariant within that feature>
Rationale: <why this test does or does not add durable protection>
Existing coverage: <relevant overlap or distinct failure mode>
Cost/coupling: <material fixture, stability, or production-surface concern, if any>
```

Do not manufacture a test merely because code changed.