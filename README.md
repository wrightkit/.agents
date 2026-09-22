# WrightKit agent skills

This repository is the canonical home for WrightKit-wide agent skills and procedural workflows.

It is intended to be checked out as `~/Repos/wrightkit/.agents` when agents are launched from the WrightKit workspace root. Codex and compatible tooling can then discover project-scoped skills from `.agents/skills` without installing WrightKit-specific skills into the user's global skill directory.

## Ownership boundary

- `.agents` owns reusable agent procedures and skill metadata.
- `wrightkit/.github` owns organization-wide engineering policy, CI/release standards, testing policy, and workspace agent routing.
- Individual WrightKit repositories own repository-specific architecture, contracts, source, tests, and local `AGENTS.md` guidance.

Skills should reference canonical policy in the sibling workspace checkout, for example `.github/docs/testing-policy.md`, rather than copying policy text into this repository.

## Skill activation

Skill descriptions are discovery metadata, not short summaries of the body. Treat each `description` as the activation contract an agent sees before the full `SKILL.md` is available.

A strong description normally answers four things in this order:

1. **What** — the job or outcome the skill provides.
2. **Use when** — semantic task surfaces, changed artifacts, risks, or failure signals that should activate it.
3. **Also use when** — representative user wording or indirect situations that should still route here.
4. **Do NOT use** — adjacent tasks that look similar but belong to another skill, normal repository workflow, or no skill at all.

Representative phrases are examples, not an exhaustive keyword router. Front-load semantic triggers, then add a few natural-language aliases when users are likely to describe the same need differently. State mode or scope boundaries when they materially affect activation, such as diff review versus whole-repository audit, read-only investigation versus apply mode, or test design versus independent verification.

Cover important indirect contexts as well as explicit requests: for example, a dependency bump that changes test expectations belongs in the test-design activation surface even when the task was not described as test work. Avoid descriptions made mostly of internal architecture vocabulary when a normal user prompt would use simpler language.

Before merging a new or materially changed skill, exercise its description against representative natural trigger prompts, indirect trigger prompts, and neighboring non-trigger prompts. If two skills activate on the same ordinary prompt for different reasons, clarify their scope boundary instead of relying on ordering or hidden precedence. Keep procedure and authoritative policy in their owning documents rather than duplicating them in the description.

A useful shape is:

```yaml
description: >
  <job or outcome>.
  Use when <semantic task/risk/artifact triggers>.
  Also use when <representative user wording or indirect signals>.
  Do NOT use for <adjacent non-triggers or another skill's scope>.
```

## Skills

- `wrightkit-reclaim-entropy`: post-hoc behavioral simplification and entropy reclamation.
- `wrightkit-rust-engineering-review`: structural Rust engineering review, challenging proposed mechanisms against direct alternatives before evaluating Rust shape.
- `wrightkit-test-design-review`: test necessity, stability, duplication, fixture cost, and production-pollution review.
- `wrightkit-verify-change`: post-implementation independent falsification, contract continuity, and verification of tests, reference comparisons, and runtime behavior.

Keep skills focused on procedures. Stable organization policy belongs in `wrightkit/.github`; dynamic project state belongs in the owning repository, Issue, PR, CI run, release, or generated output.
