---
name: wrightkit-reclaim-entropy
description: >
  WrightKit simplification: find or remove duplicate truth, dead
  or redundant abstractions, obsolete fallbacks or compatibility layers,
  post-migration leftovers, unused consumers, duplicated state/config, or
  replacement cleanup. Use for repo/codebase cleanup, entropy audits, migration
  cleanup, or focused "is this still load-bearing?" investigations. Also use
  when the user asks what can be deleted or simplified, to remove leftovers,
  find bloat or duplicate truth, or clean up after a replacement. Do NOT use for
  routine feature implementation, correctness-only PR review, or self-authorizing
  removal of public or compatibility contracts.
---

# WrightKit Reclaim Entropy

Use this skill to reduce maintenance obligations without treating line count as the objective.

The authoritative policies are `.github/docs/entropy-policy.md`, `.github/docs/engineering-quality.md`, and `.github/docs/testing-policy.md`. Repository-local contracts take precedence. This skill provides a reusable investigation workflow; it does not redefine public API, compatibility, licensing, or testing policy.

Core principle:

> Scanners create candidates; consumer inspection and contract checks justify a cut.

Why: unused-looking code can still encode an external contract, dynamic path, compatibility boundary, or lifecycle requirement. Conversely, code can be reachable and still be accidental duplication.

## Modes

Match the requested scope:

- **Audit** — identify and rank meaningful simplification candidates without editing.
- **Apply** — implement already-authorized simplifications and verify them.
- **Focused investigation** — determine whether one named abstraction, state representation, dependency, fallback, or layer is load-bearing.

Do not turn a review or audit request into implementation without authorization.

## Reasoning model

For each meaningful candidate, answer four questions.

### What maintenance obligation exists?

Name the concept being maintained: an API, state representation, wrapper layer, fallback, dependency, feature switch, lifecycle mechanism, fixture, generated surface, or duplicated semantic fact.

Why: deleting lines is not useful if the same obligation simply moves elsewhere.

### Who actually depends on it?

Trace callers and consumers far enough to understand whether the surface is production, test-only, generated, dynamic, cross-repository, or external. Search strings, protocol/config keys, build/codegen paths, registries, and known downstream WrightKit consumers when relevant.

Why: local reference counts are incomplete on their own in a multi-repository ecosystem.

### What makes it load-bearing?

Identify the contract, ownership decision, compatibility requirement, lifecycle need, historical reason, or current consumer that justifies the surface.

If the candidate touches a public or protocol contract, persisted data, declared OPY/DEL/OSTW/raw Workshop compatibility, security boundary, licensing boundary, or unresolved cross-repository ownership decision, do not self-authorize its removal. Route the decision to the appropriate owner.

Why: simplification is an implementation decision only while the behavior being removed is not itself a protected product or architecture decision.

### Does the cut reduce total complexity?

Compare the current obligation with the proposed result. Prefer consolidation onto one canonical owner, deletion of obsolete support paths, or removal of pass-through layers when doing so reduces concepts, synchronization, APIs, dependencies, or lifecycle states without introducing equivalent glue elsewhere.

Why: a change that removes one wrapper but adds another, or trades local code for a heavier dependency, is not necessarily a simplification.

## Common signals, not rules

Useful places to investigate include duplicate truth, pass-through layers, abandoned extension points, one-off generality, obsolete compatibility residue, overlapping lifecycle mechanisms, hand-rolled infrastructure, and support artifacts whose owning behavior no longer exists.

These are candidate generators, not findings. A trait with one implementation, a clone, a fallback, or a dependency can be entirely justified by a real contract.

## Apply mode

When a simplification is authorized:

- keep the change inside the relevant ownership boundary unless an approved migration requires coordination;
- remove the obsolete obligation end to end rather than leaving dead exports, docs, config, tests, or compatibility residue;
- prefer one canonical source of truth over synchronization glue;
- keep unrelated cleanup out of the change;
- preserve explicit compatibility or migration behavior when a real contract requires it.

Verify the smallest decisive property first, then run the broader repository gates appropriate to the affected boundary. Do not weaken diagnostics, expectations, validation, or tests to make a deletion pass.

## Output

Prefer a few well-supported candidates over a cleanup wishlist.

```text
Candidate: <maintenance obligation>
Consumers: <production callers, dynamic/external entrypoints, or cross-repository consumers>
Contract: <public or compatibility contract, ownership decision, or related history>
Current reality: <lifecycle state or observed behavior>
Change: <what can be removed or consolidated>
Net effect: <maintenance concepts removed and any replacement cost>
Tradeoff: <capability or flexibility lost, if any>
Authority: <implementation-level, or owner/decision required>
Verify: <smallest decisive check>
```

Finding no safe or worthwhile cut is a valid result.

When used during PR review, follow `.github/docs/issue-readiness-and-pr-audit.md`: do not expand the approved PR into an entropy cleanup unless the issue itself includes that work.
