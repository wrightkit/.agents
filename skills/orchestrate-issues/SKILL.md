---
name: orchestrate-issues
description: >
  Drive ready Issues through implementation, independent review, and merge as
  the orchestrator: pick the next Issue, dispatch an implementer session in its
  own worktree, dispatch a separate reviewer session, decide whether the PR may
  merge, squash-merge it, and clean up.
  Use when running an issue loop or backlog sweep across one or more
  repositories, when dispatching implementer or reviewer sessions or agents for
  Issues, or when applying the merge gate to an agent-authored PR that already
  has a review verdict.
  Also use for "clear the ready-for-implementation queue", "start the loop",
  "keep implementing the next issue", "stop the loop after #N", or "merge the
  PRs that passed review".
  Do NOT use for implementing one Issue yourself (follow AGENTS.md), reviewing
  or verifying one PR as the reviewer, including judging whether a change is
  correct (use the review policy or verify-change), release or tag work, or
  triaging which Issues are ready (that is PM work).
---

# Orchestrate Issues

The orchestrator schedules work, integrates results, and owns the merge decision. It does not implement or review the Issues it dispatches. The loop prompt states only the scope and the stop condition; everything else comes from this skill and the routing in the nearest `AGENTS.md`.

Selection order, readiness, concurrency, and escalation labels are defined in the project's issue readiness policy. Implementation follows `AGENTS.md` and the policies it routes to. Review follows the project's PR review policy. This skill adds the procedure that connects them and the merge gate.

## Inputs

- **Scope**: the repositories to sweep. Exclude repositories the project guidance or the user marks as frozen.
- **Stop condition**: run until the queue is empty, after named Issues, or until the user says stop.

## Cycle

### 1. Pick

Take the next Issue in the readiness policy's order, within its concurrency limit. Before dispatch, re-read the Issue with its comments, and check for an open or merged PR that already covers it. An Issue that is already done or no longer matches the code is reported, not reimplemented.

An Issue too broad to verify as one outcome, or one that needs an owner choice, gets a comment with the exact question and the `needs-decision` or `needs-design` label, and the loop moves on. Why: the orchestrator has no authority to split scope or choose product behavior.

### 2. Implement

Create one worktree per Issue from a fresh `origin/main`, and dispatch one implementer session into it. The implementer opens the PR with the implementation identity named in `AGENTS.md`.

- Never touch the shared checkout or a worktree that another session owns.
- Push with an explicit refspec (`git push origin <branch>`), never relying on the checked-out branch. Why: a force-push once went to a branch the user had switched to mid-task.
- Check the worktree for file changes shortly after launch. A session with no progress is stopped and restarted, not waited on.

### 3. Review

Dispatch a reviewer in a session separate from the implementer. It checks out the PR head, runs the Issue's acceptance checks and the relevant gates, and tries to falsify each requirement. The reviewer does not trust the implementer's tests or claims. Findings reach the implementer as review threads or one PR comment, and the fix-and-handoff rules of the review policy apply.

Allow at most two review rounds. If round two still has findings, close the PR and redo the Issue from scratch with the findings as input. Exception: if round two leaves one narrow finding, fix only that finding and run round three. Why: a third round of patches on a design that failed twice rarely converges; a fresh attempt does.

### 4. Merge

Merge only when all of these hold on the current head commit:

- the independent reviewer's latest verdict is LGTM;
- every required check is green;
- the PR changes no path that CODEOWNERS assigns to a human owner, or that owner has approved;
- the PR is not a release PR, unless the owner authorized that specific PR in the conversation.

Before merging, re-read the Issue and compare the PR against its acceptance criteria. Squash-merge with the implementation identity and pass the subject and body explicitly. The body carries `Fixes #N` only when the whole Issue scope is delivered, otherwise `Refs #N`. Why: the default squash body concatenates every commit message, so a stale `Fixes` from an early commit closes an Issue whose scope is still open.

After the merge, confirm the Issue state matches the reference used. Do not tag, publish, or approve with the personal identity.

### 5. Clean up

Remove an Issue's worktree and branch only after its PR shows `merged_at`. Never remove a worktree that has uncommitted or unpushed work. Why: a removed worktree with unsaved output once cost more than an hour of rework.

## Stop

When the stop condition is met or the user says stop, bring each in-flight Issue to a safe state: committed and pushed, or left in its worktree untouched. Do not start new Issues. Do not delete worktrees on the way out.

Stop and ask before any action this skill does not authorize, such as force-pushing a branch the orchestrator did not create, merging outside the gate above, or editing Issues beyond labels and comments.

## Report

For each Issue touched: the PR, review rounds, merge commit or current state, and the Issue state. Then list the decisions queued for the owner, PRs waiting on a code owner, and any session that stalled or was redone.
