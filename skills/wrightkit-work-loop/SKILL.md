---
name: wrightkit-work-loop
description: >
  Run one iteration of the WrightKit unattended work loop: move in-flight loop
  PRs forward, review and merge eligible PRs from other agents, claim and
  implement a ready Issue, or discover new Issues, then stop. Use when invoked
  by a repeating runner such as a /loop, a schedule, or an overnight session,
  or when asked to continue the loop, work the ready queue, or run an
  autonomous or long-running pass. Do NOT use for a single named task such as
  "implement #123" or "review this PR", which follow normal Issue and review
  routing, and not for releasing, which is the owner's.
---

# WrightKit Work Loop

One iteration does one unit of work and ends. A repeating runner calls it again. State lives in GitHub, not in the session, so any agent of any kind can pick up where another stopped.

The authoritative rules are `.github/docs/agent-loop.md`, `.github/AGENTS.md`, `.github/docs/issue-readiness.md`, and `.github/docs/pr-review.md`. This skill is the order of work; it does not widen what the policy delegates, and the policy wins on any difference.

## Before acting

- Read the current roadmap Issue for a pause or paused repositories. Stop for that scope if one applies.
- Do not merge in a repository whose default branch is currently red.
- Identify your agent kind (the tool you are, such as `claude`, `codex`, or `swe`). Record it on every PR you open as a line `Agent: <kind>` in the body. Another agent uses it to review as a different kind.

## Pick one unit of work, in this order

Finish in-flight work before starting new work.

1. **Your own loop PRs.** A draft or open PR you opened with failing CI or unaddressed review findings: fix it in place under `AGENTS.md` and `docs/pr-review.md`. Do not weaken checks to turn CI green.
2. **Review and merge.** An open, non-draft PR from the loop whose CI is green and that no independent reviewer has reviewed. If its `Agent:` kind differs from yours, review it under `docs/pr-review.md` against its Issue. If it is your own kind, do not review it in the session that wrote it; start a fresh non-interactive session of your own tool (for example `devin -p`, `codex exec`, or `claude -p`) that is given only the PR number and `docs/pr-review.md`, and use its verdict. If you find nothing actionable, comment `LGTM (reviewed by <kind>)`; all agents share one GitHub identity, so a formal approval is not available. Then merge only if every condition in "Delegated merge" in `agent-loop.md` holds. Verify the required checks yourself; do not assume branch rules enforce them. Add the `loop-delegated` label, squash-merge, and comment how to revert (`git revert` of the squash commit). If it is not eligible, leave a comment saying why for the owner and do not merge.
3. **Implement.** Take one `ready-for-implementation` Issue not already claimed by an open PR or branch, in a repository where none of your own PRs has failing CI or unaddressed review findings. Claim it with a draft PR as `agent-loop.md` describes, then follow `AGENTS.md` and the repository's `AGENTS.md`, and deliver. Do not wait for a review: once delivered, end the iteration. If it turns out to need a decision, stop and route it with `needs-*`; do not decide it.
4. **Discover.** If none of the above applies, run `wrightkit-discover-issues` on one evidence source.
5. **Nothing to do.** Say so in one line and end.

## End of iteration

End with a short note: what you did, the PR or Issue, anything that needs the owner. If you stopped on a decision, a red default branch, or a conflict, say that first. Do not start a second unit of work in the same iteration.

## Do not

- Merge a Release PR, publish, push to a default branch, or close an Issue other than through its merged PR.
- Promote an Issue outside the delegated class, or decide a contract, compatibility exception, or architecture question.
- Review or verify a PR in the session that wrote it; a fresh session or another agent kind does that.
