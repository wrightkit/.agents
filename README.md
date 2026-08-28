# WrightKit agent skills

This repository is the canonical home for WrightKit-wide agent skills and procedural workflows.

It is intended to be checked out as `~/Repos/wrightkit/.agents` when agents are launched from the WrightKit workspace root. Codex and compatible tooling can then discover project-scoped skills from `.agents/skills` without installing WrightKit-specific skills into the user's global skill directory.

## Ownership boundary

- `.agents` owns reusable agent procedures and skill metadata.
- `wrightkit/.github` owns organization-wide engineering policy, CI/release standards, testing policy, and workspace agent routing.
- Individual WrightKit repositories own repository-specific architecture, contracts, source, tests, and local `AGENTS.md` guidance.

Skills should reference canonical policy in the sibling workspace checkout, for example `.github/docs/testing-policy.md`, rather than copying policy text into this repository.

## Skills

- `wrightkit-reclaim-entropy`: evidence-first simplification and entropy reclamation.
- `wrightkit-rust-engineering-review`: structural Rust engineering review beyond compiler and mechanical checks.
- `wrightkit-test-design-review`: test necessity, stability, duplication, fixture cost, and production-pollution review.
- `wrightkit-verify-change`: independent falsification and evidence-lifecycle verification.

Keep skills focused on procedures. Stable organization policy belongs in `wrightkit/.github`; dynamic project state belongs in the owning repository, Issue, PR, or generated evidence.