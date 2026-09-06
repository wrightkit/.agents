---
name: wrightkit-verify-change
description: Use when a material WrightKit semantic, compatibility, parser/compiler, source-edit, protocol, support-state, or real-project change is being accepted or declared complete. Especially relevant when expected behavior changed, tests were authored with the implementation, a regression escaped coverage, or cross-repository evidence needs independent falsification. Return VERIFIED, NOT VERIFIED, or INCONCLUSIVE.
---

# WrightKit Verify Change

Use this skill when acceptance of a material semantic, compatibility, parser, compiler, source-edit, protocol, or similar change needs independent falsification rather than only rerunning tests authored with the implementation.

The authoritative testing and evidence-admission rules are in `.github/docs/testing-policy.md`. Repository-local guidance may add stricter constraints. This skill defines the verification procedure, not a second testing policy.

## Principle

Verification should try to distinguish a correct implementation from a plausible incorrect one.

Why: a green suite can confirm internal consistency while still agreeing with an incorrect expectation. Independent evidence is useful only when it constrains the implementation from outside the change being verified.

## Procedure

### 1. State a falsifiable claim

Describe the exact behavior that should be true after the change.

Prefer an observable statement such as "an OPY import cycle produces a structured diagnostic instead of a panic" over a broad statement such as "cycle handling is improved."

If the claim cannot be made concrete, the verification is `INCONCLUSIVE` until the contract is clarified.

### 2. Identify independent authority

Find the source that defines correct behavior independently of the implementation under test, such as:

- reproducible Workshop runtime behavior;
- a pinned upstream oracle;
- an accepted semantic or public contract;
- a provenance-linked real-project regression;
- an accepted invariant, Issue, ADR, or architecture decision.

If no independent authority exists, do not infer correctness from the implementation or its new tests. Report `INCONCLUSIVE` and name the missing contract.

### 3. Choose the smallest decisive falsification attempt

Use the narrowest observation that would fail if the claim were false. This may be an existing focused test, a targeted invocation with a minimal input, a provenance-linked corpus case, or a differential comparison.

Why: the purpose is to test the claim, not to maximize command coverage. Broader suites remain supporting gates.

### 4. Compare evidence

Where meaningful, compare pre-change and post-change behavior under equivalent conditions. More importantly, compare the resulting behavior with the independent authority.

Look for both the intended correction and unexpected differences. Ask whether a simple plausible wrong implementation would still pass the evidence you collected.

A missing historical baseline does not automatically invalidate verification if the current contract can still be tested decisively; record the limitation when it matters.

### 5. Return a verdict

Use exactly one:

- **`VERIFIED`** — decisive evidence matches the independent contract and would detect a plausible incorrect implementation.
- **`NOT VERIFIED`** — observed behavior conflicts with the contract or introduces a material unexpected difference.
- **`INCONCLUSIVE`** — the available authority or evidence cannot distinguish correct from incorrect behavior.

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

Do not report `VERIFIED` solely because existing tests are green.