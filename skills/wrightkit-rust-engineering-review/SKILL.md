---
name: wrightkit-rust-engineering-review
description: >
  Structural review for substantive WrightKit Rust design or implementation.
  Use when Rust changes add or alter public/canonical APIs, models, IRs,
  protocols, dependencies, ownership/borrowing, Arc/Mutex/interior mutability,
  async/concurrency/lifecycle/error behavior, non-trivial abstractions, semantic
  placement, feature locality, mixed module responsibilities,
  parser/lowerer/compiler/checker growth, or behavior-driving metadata and
  registries. Also use when the user asks for a Rust engineering/design review,
  whether a Rust change is over-engineered or idiomatic, or whether code lives
  in the right owner/module. Do NOT use for fmt/Clippy/compiler-only fixes,
  routine mechanical edits, or broad repo cleanup outside the changed
  responsibility.
---

# WrightKit Rust Engineering Review

Use this skill when a Rust change has a real structural risk: ownership or shared state, a public API or dependency boundary, a public or canonical boundary migration, non-trivial error/lifecycle behavior, concurrency, an abstraction whose cost may exceed the problem it solves, or a placement decision that can make domain behavior harder to find and maintain.

Relevant placement signals include adding semantic policy to an already mixed parser/lowerer/compiler/checker, spreading one feature across unrelated phases, growing generic registries or metadata into behavior interpreters, or extending a large implementation unit simply because adjacent code already lives there.

Do not load it merely because Rust changed. Compiler, formatting, Clippy, ordinary repository tests, small mechanical edits, and file size by themselves are not reasons to perform a structural review.

Read the nearest `AGENTS.md`, the linked issue, and relevant current repository contracts first. Establish current implementation reality separately; an ADR is decision history, not proof that the repository still matches it. Organization-wide engineering principles live in `.github/docs/engineering-quality.md`, and boundary contract continuity rules live in `.github/docs/issue-readiness-and-pr-audit.md`; do not duplicate or replace them here.

## Review principles

### Start from the domain and contract

Understand what behavior, state, identity, lifecycle, failure, or consumer relationship the code must represent before judging the Rust technique or file in which it is implemented.

Ask where a maintainer looking for this domain behavior would reasonably expect to find it. Existing placement describes current code, but does not prove that it is the correct owning responsibility for new behavior.

Why: a sophisticated implementation may be justified by a difficult domain, while a familiar-looking implementation can still encode the wrong ownership or bury a feature inside infrastructure that does not conceptually own it.

### Preserve feature locality and coherent responsibility

Prefer a primary implementation home that corresponds to the domain responsibility being changed. Phase-oriented modules such as parsers, lowerers, emitters, compilers, checkers, registries, and catalogs should not become default homes for unrelated semantic policy merely because they already contain nearby cases.

A bounded extraction is justified when it is needed to keep the changed behavior cohesive and discoverable. Do not expand that into unrelated cleanup or a repository-wide reorganization.

Why: repeated smallest-diff additions can make every PR individually easy to review while steadily increasing navigation distance and mixed responsibility across the codebase.

### Keep behavior in code and facts in data

Prefer typed Rust for semantic transformations, context-sensitive behavior, invariants, control flow, receiver/member rules, validation policy, and lowering decisions. Validated or generated data is appropriate for genuinely declarative bulk facts such as names, aliases, localization, enum membership, and large inventories.

When a new metadata or registry field causes generic code to decide program behavior, review it as a semantic abstraction: identify the stable data contract it represents and why that indirection is clearer and cheaper than explicit typed behavior.

Why: data-driven representation is useful for mechanical facts, but a growing semantic metadata language can hide behavior behind schemas and generic interpreters even when the underlying domain is already known.

### Use Rust to make real invariants explicit

Prefer ownership, borrowing, enums, newtypes, `Result`/`Option`, and focused traits when they make a real distinction or invalid state harder to express. Do not reject useful Rust features simply because a less typed implementation would look more familiar.

Why: idiomatic Rust is valuable when the language removes a concrete class of mistakes or makes authority and lifetime easier to reason about.

### Prefer the least complicated correct ownership and state model

Look for complexity that exists mainly to avoid deciding who owns state or when it changes: unnecessary cloning, shared mutation, synchronization, indirection, task spawning, or lifecycle machinery.

Do not treat any of those mechanisms as smells by themselves. Ask what concrete concurrency, lifetime, performance, or ownership requirement they satisfy.

Why: ownership machinery is part of the design. Extra state-sharing mechanisms create additional transitions and failure modes that every future change must understand.

### Introduce abstractions for demonstrated boundaries

Traits, generics, adapters, managers, contexts, helpers, feature flags, and dependencies should correspond to a real stable boundary or repeated behavior whose common shape is understood.

Why: abstraction can reduce complexity, but speculative generality usually moves complexity into APIs and type relationships before a demonstrated need exists.

### Treat public surface and dependencies as obligations

A new public API, crate feature, dependency, protocol-facing type, or externally visible error shape creates maintenance work beyond the current implementation. Check that the current issue or existing architecture actually requires that obligation.

When replacing, hiding, or retiring a public or canonical boundary (such as an API, model, IR, or protocol), verify contract continuity per `.github/docs/issue-readiness-and-pr-audit.md`: surviving accepted capabilities must be accounted for on the replacement boundary rather than orphaned in compatibility or internal paths, and removals or ownership transfers must have approved contract backing.

Why: local code can be changed cheaply; consumers and public contracts constrain future changes. Boundary migrations carry the special risk that a replacement boundary looks complete while silently shedding surviving capabilities.

## Workflow

Trace only the parts needed to judge the material risk:

1. Establish the approved behavior, current contract, and owning domain.
2. Inspect the current implementation location and the minimum callers/consumers needed to understand its responsibility.
3. Ask whether the proposed placement makes the domain behavior easier to locate and reason about, or deepens an already mixed responsibility.
4. If metadata/registry/schema changes drive behavior, identify whether they represent declarative facts or a new semantic interpreter layer.
5. Trace ownership, state, lifecycle, API, dependency, and abstraction costs when those are material to the change. For boundary migrations, confirm that surviving accepted capabilities are represented on the replacement boundary instead of lingering only in compatibility adapters.
6. Compare against the simplest viable design that satisfies the same contract while keeping the changed behavior coherent.
7. Report only actionable problems in the current scope.

Do not turn this skill into a broad entropy audit or architecture redesign. Route accumulated cleanup outside the changed responsibility to `wrightkit-reclaim-entropy`; route unresolved architecture or public-contract decisions to the appropriate owner.

## Output

If this is being used as a PR review, follow `.github/docs/issue-readiness-and-pr-audit.md`: no actionable finding means `LGTM`; findings should stay concrete and local to the approved PR scope.

For a focused engineering investigation, state:

```text
Concern: <concrete placement/ownership/API/boundary-contract/state/abstraction problem>
Contract: <domain contract, public boundary, or owner decision>
Consumers: <current implementation, caller, consumer, lifecycle, or observed failure>
Impact: <correctness, discoverability, or maintenance consequence>
Required change: <smallest correction, bounded extraction, or owner/decision that must resolve it>
```

A different idiom, preferred file layout, or file size alone is not a finding without a concrete effect on the changed responsibility.
