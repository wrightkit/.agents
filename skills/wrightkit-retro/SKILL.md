---
name: wrightkit-retro
description: >
  Look back over already-merged WrightKit PRs to spot recurring defect patterns
  and decide what should prevent them: the nightly retrospective (including dry
  runs and catching up after missed nights), a backfill of the last N days, or a
  "since Monday / since the last release" sweep across one or more wrightkit
  repos.
  Use when maintaining a repo's docs/LESSONS.md (add, dedupe against existing
  entries, prune entries already promoted to a test or policy), or when checking
  whether the same defect class landed in two separate merged PRs within three
  days.
  Also use for "which bugs do we keep hitting", "was this fix reverted or
  reopened", "did the same class of bug land in two PRs this week", or "does this
  deserve a policy Issue".
  Do NOT use for reviewing or verifying a single PR or fix, debugging a failing
  CI job, writing release notes, cleaning up code (use
  wrightkit-reclaim-entropy), or editing policy docs such as pr-review.md.
---

# WrightKit Retro

Turn evidence from merged work into a short list of prevention rules, and escalate fast when one failure class recurs. The skill produces a reviewable PR or an Issue update; it never edits policy, `AGENTS.md`, or a default branch directly.

Authority: the recurring-findings rule in `.github/docs/pr-review.md` stays the slow route (three separate PRs). This skill adds a faster signal and a small lessons file. It does not replace that rule or create a second policy authority. Promotion targets are owned by `.github/docs/testing-policy.md`, `.github/docs/engineering-quality.md`, and each repository's own tests and `AGENTS.md`.

Why this exists: a lesson written after one incident is cheap, but a lesson inferred from commit titles is noise. The bar below keeps the file short enough to be read.

## Inputs and modes

- **Backfill** — one-time, explicit window (for example the preceding 10 days).
- **Nightly** — default window is the trailing 4 days: three for the recurrence rule plus a day of slack for a skipped or delayed run. If the last run is known to be older, the caller passes an explicit start. Do not keep a watermark file; it would be a second state store.

Select PRs by **GitHub merge timestamp** (`mergedAt`), never author or commit time, and only PRs, not bare commits.

```bash
for r in $(gh repo list wrightkit --no-archived --json name --jq '.[].name'); do
  gh pr list --repo wrightkit/$r --state merged --limit 200 \
    --search "merged:>=$SINCE" --json number,title,url,mergedAt,mergeCommit
done
```

`gh search prs` has no `mergedAt` field; use the per-repository listing. Keep `--json` fields small on the list call; request `reviews`, `commits`, and `closingIssuesReferences` per PR, because bundling them in one wide query exceeds the GraphQL node limit. Private repositories need the caller's token to see them; if a repository cannot be read, record it as not inspected.

If any PR, review, or CI data cannot be fetched, say which and continue without it. Never fill the gap by guessing from the title.

## Procedure

### 1. Collect candidate signals per merged PR

Look at evidence of a real defect, in this order of strength:

1. Review threads or findings that a later commit in the same PR fixed, with the policy rule or contract they cite.
2. A later PR that fixes, reverts, or reopens this one (linked issue, `Fixes`, `Revert`, or an Issue reopened after merge).
3. A CI failure that required a code change, not a retry or infrastructure flake.

A merge, a test edit, or a "fix" title alone is not evidence. Two commits inside one PR are one incident.

### 2. Name the failure class

Write the class as the underlying mistake, not the symptom: "tolerated residual hides sibling errors", not "wrong output in opy-rs". Strip repository-specific nouns so a second incident elsewhere can match it. If you cannot state the class and its prevention without the incident text, the candidate is not reusable; drop it.

### 3. Check independence and recurrence

Two incidents are independent only when they sit in **distinct merged PRs** and have separate root causes (different code, different author action). Several comments on one PR, or one bug fixed across a PR stack, count once.

- **Fast escalation:** the same class in at least two independent merged PRs whose merge times fall in a rolling three-day window.
- **Slow route:** three separate PRs outside that window follow `.github/docs/pr-review.md#recurring-findings` unchanged.

### 4. Deduplicate before writing

Before adding or escalating, search the `docs/LESSONS.md` of each repository involved and the open escalation Issues for the class and for each PR URL. An incident already cited is not new. A repeat of a known class updates the existing entry (add the link and date) instead of adding another.

### 5. Choose the smallest effective prevention

For each lesson pick one, in this order of preference:

1. an executable regression test or CI check, owned by the repository that owns the behavior;
2. the owner repository's contract or `AGENTS.md`, or a repository-local principle in its `docs/principles/` when prevention is a judgment made while authoring that no test or check can choose;
3. an existing organization policy gaining or sharpening one rule, after confirming no rule already covers it.

Open no new policy document or registry. Route language semantics, tests, and domain corrections to the owning repository.

## Output

### Lessons file

Write each entry to `docs/LESSONS.md` in the repository that owns the behavior or the prevention home, not in `wrightkit/.github`. Create the file in a repository only for its first supported lesson. A class seen in several repositories gets an entry in each owner repository, citing its own incidents; the cross-repository link lives in the escalation Issue. Why: lessons are read by the people changing that repository's code, and the organization repository holds policy, not per-repository history. Each entry:

```markdown
### <Failure class, as a prevention rule>
- **Rule:** <what to do or check>
- **Why:** <the harm, in one or two sentences>
- **Prevention home:** <test/CI | owner contract | existing policy link>
- **Incidents:** <PR/review/fix links> — observed <YYYY-MM-DD>, <YYYY-MM-DD>
```

Combine repeated instances into one entry per repository. Never append commit summaries. Remove an entry when its rule has been promoted into the prevention home or the class is obsolete, and leave the link in the promotion Issue or PR. Do not exceed what a maintainer reads in a minute; if the file grows past that, prune rather than extend.

### Escalation

For a confirmed fast recurrence, open or update one Issue in the owning repository (or `wrightkit/.github` for cross-repository classes) that links the affected PRs, names the class, and asks the owner to choose among the prevention homes in step 5. Update an existing Issue rather than opening a second. Use `Refs`, not a closing keyword.

### Delivery

Put lessons changes in one PR per affected repository, from a task branch, using the identity rules in `AGENTS.md`. A night with no supported lesson and no escalation produces no commit and no PR. Escalation Issues are metadata operations and need no commit.

### Report

End with what a reviewer needs: PR count inspected and window, lessons added or updated, escalations opened or updated, candidates dropped and why (one line each), and anything not inspected with where you looked. If nothing met the bar, say that plainly; that is a valid result.

## Limits

- Do not run this inside GitHub Actions with an LLM unless an authorized execution and authentication path already exists; the on-demand agent run is the supported path.
- Do not promote a lesson into binding policy without owner review.
- Do not treat repeated wording as recurrence; compare root causes.
