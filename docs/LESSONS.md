# Lessons

Short review queue of reusable failure classes from merged .agents work. Each entry names a prevention action and the evidence behind it. Promote an entry into a regression test, an owner contract, or an existing engineering standard, then remove it here. The procedure is the `wrightkit-retro` skill in this repository.

### A terminology cleanup must preserve the concept, not only replace the word

- **Rule:** Lexical renames in guidance keep the referent concrete — destinations and output fields stay named by the information they carry, not by a generic replacement term.
- **Why:** Removing generic verification terms still blurred the concrete concepts the work required — current-state destinations went abstract and output fields stopped describing their content; a second commit restored the semantics after review blocked.
- **Prevention home:** review judgment — cleanup reviews check that semantics survived, not only that the word is gone.
- **Incidents:** [#12](https://github.com/wrightkit/.agents/pull/12) — observed 2026-09-20

### A shared skill demonstrates distinct value before it merges

- **Rule:** A new shared skill is admitted only with a concrete task where it adds procedural or executable value over `AGENTS.md` routing and the existing skills — demonstrated before merge, not after.
- **Why:** wrightkit-discover-issues and wrightkit-work-loop merged, needed a same-day correction, and were removed within hours; the open admission concern (#19) asks the same question.
- **Prevention home:** the skill admission bar tracked in #19.
- **Incidents:** [#21](https://github.com/wrightkit/.agents/pull/21), [#23](https://github.com/wrightkit/.agents/pull/23), [#24](https://github.com/wrightkit/.agents/pull/24), [#25](https://github.com/wrightkit/.agents/pull/25) — observed 2026-10-07
