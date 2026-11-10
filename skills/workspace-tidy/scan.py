#!/usr/bin/env python3
"""List what a workspace tidy-up may remove. Read-only; it changes nothing.

Usage: scan.py [WORKSPACE_ROOT]   (default: two levels above this file)

For each Git repository directly under the root, print as JSON:
- the checked-out branch and how far it is from origin/main;
- each linked worktree, with its dirty and unpushed state;
- each local branch with the merged PR that covers it. `git branch --merged`
  cannot see squash merges, so the PR state comes from GitHub.
"""
import json
import os
import subprocess
import sys


def run(cwd, *args):
    out = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else None


def worktrees(repo):
    entries, cur = [], {}
    for line in (run(repo, "git", "worktree", "list", "--porcelain") or "").splitlines() + [""]:
        if not line:
            if cur:
                entries.append(cur)
            cur = {}
        else:
            key, _, value = line.partition(" ")
            cur[key] = value
    return entries[1:]  # the first entry is the main checkout


def scan_repo(repo):
    slug = (run(repo, "gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner") or "")
    merged = {}
    if slug:
        listing = run(repo, "gh", "pr", "list", "--state", "merged", "--limit", "200", "--json", "headRefName,number,mergedAt")
        merged = {p["headRefName"]: p for p in json.loads(listing or "[]")}
    branches = []
    for name in (run(repo, "git", "for-each-ref", "--format=%(refname:short)", "refs/heads") or "").splitlines():
        pr = merged.get(name)
        branches.append({"branch": name, "merged_pr": pr["number"] if pr else None})
    trees = []
    for wt in worktrees(repo):
        path = wt["worktree"]
        if not os.path.isdir(path):
            trees.append({"path": path, "branch": wt.get("branch", "").removeprefix("refs/heads/"), "missing": True})
            continue
        trees.append({
            "path": path, "branch": wt.get("branch", "").removeprefix("refs/heads/"),
            "dirty": bool(run(path, "git", "status", "--porcelain")),
            "unpushed": (run(path, "git", "log", "--oneline", "@{upstream}..HEAD") or "unknown"),
        })
    return {
        "repo": os.path.basename(repo),
        "checked_out": run(repo, "git", "branch", "--show-current"),
        "behind_ahead_origin_main": run(repo, "git", "rev-list", "--left-right", "--count", "origin/main...HEAD"),
        "dirty": bool(run(repo, "git", "status", "--porcelain")),
        "worktrees": trees,
        "branches": branches,
    }


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    repos = [os.path.join(root, d) for d in sorted(os.listdir(root)) if os.path.isdir(os.path.join(root, d, ".git"))]
    print(json.dumps([scan_repo(r) for r in repos], indent=1))


if __name__ == "__main__":
    main()
