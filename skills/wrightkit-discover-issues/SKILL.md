---
name: wrightkit-discover-issues
description: >
  WrightKit issue discovery: find real problems from evidence and propose them
  as readiness-labelled Issues, without implementing. Use for scheduled or
  on-demand sweeps of agent-benchmark failures, differential or corpus
  failures, recurring CI failures, real-project regressions, entropy audit
  findings, or contract-versus-code drift; also to triage or file Issues from a
  failure. Do NOT use to implement an Issue, to promote an Issue outside the
  owner-delegated class, to review a PR, to answer what to work on next (read
  the roadmap and ready Issues), or to file Issues from `docs/goal.md`
  alone without a reproducible failure or evidenced gap.
---

# WrightKit Discover Issues

Read-only discovery. The output is proposed Issues and a short digest for the owner; no code, no readiness promotion, no PR.

The authoritative rules are `.github/docs/agent-loop.md`, `.github/docs/issue-readiness.md`, and `.github/docs/goal.md`. This skill is the procedure; it does not widen what an agent may decide.

## Workflow

1. Pick one evidence source per run: benchmark results, differential/corpus failures, recurring CI failures, entropy audit, or contract-versus-code drift. Query current reality from the source (Issues, PRs, CI, the repository); do not rely on earlier summaries.
2. For each candidate, reproduce it or open the evidence. A candidate you cannot reproduce is not a finding.
3. Search existing Issues and PRs across WrightKit repositories. If one covers it, add the evidence there and stop; otherwise continue.
4. Identify the owning repository from `.github/AGENTS.md` routing. A gap in language semantics belongs to the language engine, not Wright.
5. Draft the Issue as `needs-design` or `needs-decision`, with the open question and a recommendation. Include the evidence, the goal principle and decision-priority rank it serves, and acceptance criteria that could fail; if you cannot write such criteria, say what decision is missing.
6. Report a digest: proposed Issues with evidence and recommendation, and candidates dropped with the reason.

## Boundaries

- Label an Issue `ready-for-implementation` only when it meets the owner-delegated class in `.github/docs/agent-loop.md`: acceptance fully defined by an external authority you name, no design or contract decision, one repository, no `needs-*` or `blocked` state. Otherwise the owner does.
- File no Issue the owner has already decided against, and respect repositories the owner has paused (read the current roadmap Issue).
- Do not reference repositories outside WrightKit as linked Issues or PRs, per `.github/AGENTS.md` global invariants.
- Do not propose a deviation from upstream compiler output; route it as a recorded-exception decision for the owner.
- At most a handful of Issues per run; a long list of weak candidates costs the owner more than it finds.

## Stop

If the evidence source is unavailable or the candidate depends on an unresolved owner decision, report that and stop rather than filing a guess.
