---
name: wrightkit-run-workshop-probe
description: >
  Run one Workshop runtime-behavior probe from the `athena` repository in the real
  Overwatch client and record the result: validate the probe, run it in the client
  (by computer use, or by the user), ingest the Inspector log with `athena ingest`,
  and report the verdict.
  Use when the task is to run, re-run, repeat, or record a probe, to
  judge a pasted Inspector log, or to find which probe still needs runs.
  Also use when the user pastes an Inspector log with probe lines such as `P0 ...`, or
  asks to measure tick, Wait, rule-order, or value-refresh behavior in the real client.
  Do NOT use to design or edit a probe (follow `athena/AGENTS.md`), to change
  Workshop semantics or catalog data, or to claim a probe was run without a capture.
---

# Run a Workshop probe

One probe, one session. Never state or imply a probe ran unless a capture exists.
The agent that drives the client returns raw Inspector text. `athena ingest` judges it
and writes the capture; the agent does not judge by eye and does not hand-write
`capture.json`.

All paths are relative to the `athena` repository; work from that directory. Expected
values live only in `probes/<id>/expect.json`. The client set-up, per-probe set-up, and
invalid-run rules are in `docs/procedure.zh-CN.md` under "Agent 执行". The capture layout and
result rules are in `docs/capture-convention.md`. Do not restate or invent expected values.

## 1. Choose the probe

If the user named one, use it. Otherwise list `probes/*/capture.json`. Pick, in order:
a probe whose `probe_sha256` no longer matches (stale), then the probe with the fewest
`runs`. Skip a probe that already has `runs: 3` and a final result. Do not re-run a
`mismatch` to look for a different answer. Report which probe and why.

Run one probe at a time. Probes share global variable names, and only one agent may write
to a probe's directory.

## 2. Validate

```bash
wright check --kind workshop probes/<id>/probe.workshop
wright check --kind workshop probes/<id>/probe.zh-CN.ow
wright inspect cost --kind workshop -f json probes/<id>/probe.workshop | jq .result.elementCount.total
wright inspect cost --kind workshop --locale zh-CN -f json probes/<id>/probe.zh-CN.ow | jq .result.elementCount.total
shasum -a 256 probes/<id>/probe.zh-CN.ow
```

Both checks must pass and the element counts must be equal. If not, stop and report.
Read `probes/<id>/expect.json` for the `end` line and the expected line count.

## 3. Run in the client

If the user pastes the log themselves, go to step 4. Otherwise drive the client by
computer use. The client runs on a remote Windows machine; reach it through the remote
desktop window on this Mac. Request access to the remote desktop app first. Do not enter
credentials, and do not sign in on the user's behalf; if a sign-in is needed, stop and ask.
Install nothing on the Windows machine.

Follow "Agent 执行" in `docs/procedure.zh-CN.md`:

1. Get `probes/<id>/probe.zh-CN.ow` into the client unchanged. Use whatever the remote
   desktop offers: clipboard sync, file transfer, or typing into Notepad. Check the pasted
   rule count against the file. Never edit the probe.
2. In a new Custom Game in Workshop mode, clear existing rules, paste the probe, turn on
   the Workshop Inspector and Inspector recording, and make sure no rule calls `Set Slow Motion` (it is an action, not a toggle; the probes do not use it).
3. Apply the probe-specific set-up from the procedure doc (P5 and P7 need the host to
   pick a hero and spawn; every other probe needs no input and the character must not be
   touched).
4. Start the game and watch the Inspector until the probe's `end` line appears.
5. Get the log text out (step 4). Leave the client in a state the next run can start from.

If a screen does not match the procedure (a dialog, a different language, a missing
button), stop and report with a screenshot. Do not guess a click.

## 4. Get the log as a file on this Mac

The client writes its log on the Windows machine
(`文档\Overwatch\Workshop\Log-<date>.txt`). Bring the text back by any means the remote
desktop allows: file transfer, clipboard sync, or copy from the Inspector. Choose the means
that works. Do not set up anything on the Windows machine.

Save one run per file in `.wright/runs/` (ignored by Git), with a different file name each
time (`sources` de-duplicates by name). Keep the client's log file name when you copy the
file, for example `.wright/runs/Log-2026-10-19-12-45-59.txt`. Otherwise use
`.wright/runs/<id>-<n>.log`. Save the text unchanged. P6 also needs the variable block (see
its entry in the procedure doc).

Check before ingesting: the `end` line is present once, and the line count matches. If the
text is cut short, mixed with another probe, garbled (encoding, line endings), or starts
before the probe's first line, discard the run and redo it. Never repair, reformat, or
complete the text. Report which means worked and the log file's encoding, so the procedure
doc can record them.

## 5. Ingest

```bash
cargo run -p athena-capture -- ingest probes/<id> .wright/runs/<id>-<n>.log
```

`ingest` prints the verdict of the run and updates `capture.json` (`runs`, `result`,
`notes`, `sources`) and the saved `capture*.txt`. If it rejects the log (no or several end
lines, stale `probe_sha256`, `runs` out of step with the saved files, another probe's
lines), nothing is written. Fix the cause or discard the run; do not edit
`capture.json` to get past it.

Repeat steps 3 to 5 until `runs` is 3, or stop earlier if a run is a `mismatch` you must
report. Fewer than three agreeing runs keep the result provisional.

## 6. Fill the human fields

`ingest` does not set `client`, `hypothesis`, or `observed`. Fill them:

- `client.version`: read it from the client options menu. Do not guess it. `date` is the
  run date.
- `observed`: only what the capture shows, in milliseconds.
- `notes`: human text for what the probe cannot test, and invalid runs. Keep the
  trailing `[ingest: …]` marker that `ingest` owns.
- P6: confirm `endAbort` is `0` in the variable export, and say so in `notes`.

Check with `cargo test -p athena-sim --test probe_hashes`.

## 7. Report

Lead with the verdict and whether it is provisional. Then the observed values beside the
expected ones, anything that disagreed, and what is still owed (remaining runs, client
version, where the Inspector log lives if it was unknown). Do not commit unless the user
asks.
