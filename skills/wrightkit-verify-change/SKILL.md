---
name: wrightkit-verify-change
description: >
  Independently falsify whether a material WrightKit change is actually correct
  and complete. Use before accepting or declaring complete semantic,
  compatibility, parser/compiler, source-edit, protocol, support-state, or
  real-project changes, and when replacing, migrating, or retiring a public or
  canonical API, model, IR, protocol, or boundary. Also use when the user asks
  to verify or prove a change, asks whether a fix is really complete or ready to
  merge, a regression fix needs independent re-checking after escaping coverage,
  tests were authored with the implementation, surviving contract continuity
  must be checked, or cross-repository evidence needs independent falsification.
  Do NOT use as a routine test runner, to diagnose why coverage missed a defect,
  for mechanical changes whose correctness is fully covered by normal gates, or
  to decide whether a test should exist. Return VERIFIED, NOT VERIFIED, or
  INCONCLUSIVE.
---

# WrightKit Verify Change

Use this skill when acceptance of a material semantic, compatibility, parser, compiler, source-edit, protocol, or similar change needs independent falsification rather than only rerunning tests authored with the implementation, or when verifying contract continuity across a public or canonical boundary migration, replacement, or retirement.

The authoritative testing and evidence-admission rules are in `.github/docs/testing-policy.md`, and the canonical contract continuity policy for boundary migrations is in `.github/docs/issue-readiness-and-pr-audit.md`. Repository-local guidance may add stricter constraints. This skill defines the verification procedure, not a second testing policy.

## Principle

Verification should try to distinguish a correct implementation from a plausible incorrect one.

Why: a green suite can confirm internal consistency while still agreeing with an incorrect expectation. When replacing a boundary, legacy or compatibility tests can remain green while the replacement boundary drops existing capabilities. Independent evidence is useful only when it constrains the implementation from outside the change being verified.

## Procedure

### 1. State a falsifiable claim

Describe the exact behavior that should be true after the change.

Prefer an observable statement such as "an OPY import cycle produces a structured diagnostic instead of a panic" over a broad statement such as "cycle handling is improved."

When replacing, hiding, or retiring a public or canonical boundary, derive surviving claims from the accepted pre-migration contract rather than only from the replacement implementation or its companion tests. Per `.github/docs/issue-readiness-and-pr-audit.md`, account for capabilities as preserved contracts, approved removals/changes, or ownership transfers, and formulate claims for representative capabilities on the replacement boundary.

If the claim cannot be made concrete, the verification is `INCONCLUSIVE` until the contract is clarified.

### 2. Identify independent authority

Find the source that defines correct behavior independently of the implementation under test, such as:

- reproducible Workshop runtime behavior;
- a pinned upstream oracle;
- an accepted semantic or public contract;
- the accepted pre-migration contract or baseline for surviving capabilities across boundary replacement;
- a provenance-linked real-project regression;
- an accepted invariant, Issue, ADR, or architecture decision.

If no independent authority exists, do not infer correctness from the implementation or its new tests. Report `INCONCLUSIVE` and name the missing contract.

### 3. Choose the smallest decisive falsification attempt

Use the narrowest observation that would fail if the claim were false. This may be an existing focused test, a targeted invocation with a minimal input, a provenance-linked corpus case, or a differential comparison.

For boundary migrations, require decisive evidence that exercises the replacement boundary directly for representative surviving capabilities. Exercising only a retired, private, hidden, or compatibility-only path is not decisive verification for the replacement contract.

Why: the purpose is to test the claim, not to maximize command coverage. Broader suites remain supporting gates.

### 4. Compare evidence

Where meaningful, compare pre-change and post-change behavior under equivalent conditions. More importantly, compare the resulting behavior with the independent authority.

Look for both the intended correction and unexpected differences. Ask whether a simple plausible wrong implementation would still pass the evidence you collected.

Evidence that exercises only a retired, private, hidden, or compatibility-only boundary cannot prove that a capability survives on the replacement canonical boundary. Compare replacement-boundary observations directly against the pre-migration accepted contract.

A missing historical baseline does not automatically invalidate verification if the current contract can still be tested decisively; record the limitation when it matters.

### 5. Return a verdict

Use exactly one:

- **`VERIFIED`** — decisive evidence matches the independent contract and would detect a plausible incorrect implementation. For boundary migrations, representative surviving capabilities must be verified through the replacement boundary; evidence resting solely on retired, private, hidden, or compatibility-only paths is explicitly insufficient for `VERIFIED`.
- **`NOT VERIFIED`** — observed behavior conflicts with the contract, introduces a material unexpected difference, or silently drops a surviving capability without an approved contract decision.
- **`INCONCLUSIVE`** — the available authority or evidence cannot distinguish correct from incorrect behavior, or surviving capability scope across a boundary replacement remains unclarified.

If the result is not `VERIFIED`, state what contract, evidence, or implementation change would resolve the uncertainty.

## Evidence lifecycle

Verification output is task evidence, not automatically repository state. Keep ad-hoc logs, reports, snapshots, minimized inputs, or other proof artifacts ephemeral unless `.github/docs/testing-policy.md` establishes a durable reason and canonical owner for them.

If verification reveals a reusable regression that deserves permanent coverage, report it as a candidate for integration into the owning repository's established test structure. Do not create a new evidence taxonomy or directory in this skill.

## Output

```text
Claim: <falsifiable behavior>
Authority: <independent contract or source>
Surface: <decisive verification>
Evidence: <relevant observation or comparison>
Verdict: VERIFIED | NOT VERIFIED | INCONCLUSIVE
Limitations: <material uncertainty, or none>
Repository evidence candidate: <only if durable admission should be considered>
```

Do not report `VERIFIED` solely because existing tests are green, or because a retired, private, or compatibility path passes while the replacement boundary was not verified.