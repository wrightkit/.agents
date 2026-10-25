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
computer use. Request access to Overwatch first. Do not enter credentials, and do not sign
in on the user's behalf; if the client needs a sign-in, stop and ask.

Follow "Agent 执行" in `docs/procedure.zh-CN.md`:

1. Put `probes/<id>/probe.zh-CN.ow` on the clipboard (`write_clipboard` with the file
   content). Never edit it.
2. In a new Custom Game in Workshop mode, clear existing rules, paste the probe, turn on
   the Workshop Inspector and Inspector recording, and confirm Slow Motion is off.
3. Apply the probe-specific set-up from the procedure doc (P5 and P7 need the host to
   pick a hero and spawn; every other probe needs no input and the character must not be
   touched).
4. Start the game and watch the Inspector until the probe's `end` line appears.
5. Get the log text out (step 4). Leave the client in a state the next run can start from.

If a screen does not match the procedure (a dialog, a different language, a missing
button), stop and report with a screenshot. Do not guess a click.

## 4. Get the log as a file

One run per file, with a different file name each time (`sources` de-duplicates by name).
Save into `.wright/runs/` (ignored by Git), for example
`.wright/runs/<id>-<n>.log`.

- Preferred: the Inspector log file the client writes. The procedure doc names where it
  is once known. If you find it, report the path in the final report.
- Fallback: select all in the Inspector, copy, read the clipboard, and save the text
  unchanged. P6 also needs the variable block (see its entry in the procedure doc).

Check before ingesting: the `end` line is present once, and the line count matches. If the
text is cut short, mixed with another probe, or starts before the probe's first line,
discard the run and redo it. Never repair, reformat, or complete the text.

## 5. Ingest

```bash
cargo run -p athena-capture -- ingest probes/<id> .wright/runs/<id>-<n>.log
```

`ingest` prints the verdict of the run and updates `capture.json` (`runs`, `result`,
`notes`, `sources`) and the saved `capture*.txt`. If it rejects the log (no or several end
lines, stale `probe_sha256`, `runs` out of step with the saved files, another probe's
lines), nothing is written. Fix the cause or discard the run; do not edit
`capture.json` to get past it.

To feed several runs, `cargo run -p athena-capture -- watch .wright/runs` ingests each
finished log as it lands. Use `ingest` when you need the exact verdict of one run.

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
