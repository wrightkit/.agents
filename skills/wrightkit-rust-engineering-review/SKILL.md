---
name: wrightkit-rust-engineering-review
description: Use when WrightKit Rust changes add or alter public APIs, dependencies, ownership or borrowing, shared state, Arc/Mutex/interior mutability, async/concurrency/lifecycle/error behavior, or non-trivial abstractions. Review structural correctness and maintenance risk; do not use for routine mechanical Rust edits.
---

# WrightKit Rust Engineering Review

Use this skill when a Rust change has a real structural risk: ownership or shared state, a public API or dependency boundary, non-trivial error/lifecycle behavior, concurrency, or an abstraction whose cost may exceed the problem it solves.

Do not load it merely because Rust changed. Compiler, formatting, Clippy, and ordinary repository tests remain supporting gates, not reasons to perform an architectural review.

Read the nearest `AGENTS.md`, the linked issue, and relevant repository contracts first. Organization-wide engineering principles live in `.github/docs/engineering-quality.md`; do not duplicate or replace them here.

## Review principles

### Start from the domain and contract

Understand what state, identity, lifecycle, failure, or consumer relationship the code must represent before judging the Rust technique used to represent it.

Why: a sophisticated implementation may be justified by a difficult domain, while a familiar-looking implementation can still encode the wrong ownership or contract.

### Use Rust to make real invariants explicit

Prefer ownership, borrowing, enums, newtypes, `Result`/`Option`, and focused traits when they make a real distinction or invalid state harder to express. Do not reject useful Rust features simply because a less typed implementation would look more familiar.

Why: idiomatic Rust is valuable when the language removes a concrete class of mistakes or makes authority and lifetime easier to reason about.

### Prefer the least complicated correct ownership and state model

Look for complexity that exists mainly to avoid deciding who owns state or when it changes: unnecessary cloning, shared mutation, synchronization, indirection, task spawning, or lifecycle machinery.

Do not treat any of those mechanisms as smells by themselves. Ask what concrete concurrency, lifetime, performance, or ownership requirement they satisfy.

Why: ownership machinery is part of the design. Extra state-sharing mechanisms create additional transitions and failure modes that every future change must understand.

### Introduce abstractions for demonstrated boundaries

Traits, generics, adapters, managers, contexts, helpers, feature flags, and dependencies should correspond to a real stable boundary or repeated behavior whose common shape is understood.

Why: abstraction can reduce complexity, but speculative generality usually moves complexity into APIs and type relationships before there is evidence they are needed.

### Treat public surface and dependencies as obligations

A new public API, crate feature, dependency, protocol-facing type, or externally visible error shape creates maintenance work beyond the current implementation. Check that the current issue or existing architecture actually requires that obligation.

Why: local code can be changed cheaply; consumers and public contracts constrain future changes.

## Workflow

Trace only the parts needed to judge the material risk:

1. Establish the approved behavior and owning boundary.
2. Trace the relevant callers, state owner, lifecycle, and consumers.
3. Ask whether the Rust design makes those relationships clearer and safer, or adds machinery without a concrete need.
4. Compare against the simplest viable design that still satisfies the same contract.
5. Report only actionable problems in the current scope.

Do not turn this skill into a broad entropy audit or architecture redesign. Route substantial cleanup to `wrightkit-reclaim-entropy`; route unresolved architecture or public-contract decisions to the appropriate owner.

## Output

If this is being used as a PR review, follow `.github/docs/issue-readiness-and-pr-audit.md`: no actionable finding means `LGTM`; findings should stay concrete and local to the approved PR scope.

For a focused engineering investigation, state:

```text
Concern: <concrete ownership/API/state/abstraction problem>
Evidence: <contract, caller, consumer, lifecycle, or failure evidence>
Impact: <correctness or maintenance consequence>
Required change: <smallest correction, or owner/decision that must resolve it>
```

A different idiom or personal preference is not a finding without a concrete effect.