---
name: workspace-tidy
description: >
  Clean up the WrightKit workspace after a batch of work: find leftover
  worktrees, local branches whose PR was merged, scratch directories, and
  repositories that are not on `origin/main`, then remove what is safe and
  return each repository to `origin/main`.
  Use for "clean up the workspace", "scan for leftover worktrees or branches",
  "reset the repositories to origin/main", or after an orchestrator loop ends.
  Do NOT use to delete a branch or worktree that has unpushed or uncommitted
  work, or while another session still owns a worktree.
---

# Workspace tidy

Run the scan first. It is read-only and prints one JSON object per repository:

```sh
python3 -I .agents/skills/workspace-tidy/scan.py
```

## Decide per item

- **Worktree**: remove it when its branch has a merged PR (`merged_pr` is set), it is not `dirty`, and `unpushed` is empty. A `missing` worktree only needs `git worktree prune`.
- **Branch**: delete it when `merged_pr` is set. Squash merges leave the branch unmerged in Git's view, so trust the PR state, not `git branch --merged`.
- **Anything else** (dirty, unpushed, no PR, open PR): leave it and list it for the user. Why: a removed worktree with unsaved output once cost more than an hour of rework.
- **Checked-out branch**: when the repository is clean and its branch is merged or already on `main`, switch to `main` and fast-forward to `origin/main`.

## Remove

- Remove a worktree with `git worktree remove <path>`. Use `trash` for any leftover directory.
- Delete a merged branch with `git branch -D <branch>`. Do this only for a branch with a merged PR.
- Never use `rm`, `git clean`, or `find -delete`. The agent hook blocks them.
- Look for scratch directories (`.task-scratch/`, `/tmp` paths for this workspace) and `trash` those that no running session uses.

## Report

List what you removed, what you left and why, and each repository's final branch and distance from `origin/main`.
