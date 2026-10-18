---
name: wrightkit-run-workshop-probe
description: >
  Run one Workshop runtime-behavior probe from the `runtime` repository and record
  the result: validate the probe, hand the paste file to the user for the Overwatch
  client, save the returned Inspector text as a verbatim capture, judge it against
  the verdict table, and write `capture.json`.
  Use when the task is to run, re-run, repeat, or record a probe, to
  judge a pasted Inspector log, or to find which probe still needs runs.
  Also use when the user pastes an Inspector log with probe lines such as `P0 ...`, or
  asks to measure tick, Wait, rule-order, or value-refresh behavior in the real client.
  Do NOT use to design or edit a probe (follow `runtime/AGENTS.md`), to change
  Workshop semantics or catalog data, or to claim a probe was run without a capture.
---

# Run a Workshop probe

One probe, one session. The agent prepares the file and judges the result. Pasting into
the client and copying the Inspector back is done by the user. Do not attempt to drive
the game client yourself, and never state or imply a probe ran unless a capture exists.

All paths below are relative to the `runtime` repository;
work from that directory. The expected values and the `match` / `mismatch` /
`inconclusive` conditions are in `docs/procedure.zh-CN.md` under "操作与判定". Read that
table for the chosen probe. Do not restate or invent expected values in this skill or in
the reply. The capture layout, `capture.json` shape, and result rules are in
`docs/capture-convention.md`; `AGENTS.md` routes to both.

## 1. Choose the probe

If the user named one, use it. Otherwise list `probes/*/capture.json` and pick the
probe with the fewest `runs` (fewer than 3), or one whose `probe_sha256` no longer
matches. Report which one and why.

## 2. Prepare and validate

```bash
wright check --kind workshop probes/<id>/probe.workshop
wright check --kind workshop probes/<id>/probe.zh-CN.ow
wright inspect cost --kind workshop -f json probes/<id>/probe.workshop | jq .result.elementCount.total
wright inspect cost --kind workshop --locale zh-CN -f json probes/<id>/probe.zh-CN.ow | jq .result.elementCount.total
shasum -a 256 probes/<id>/probe.zh-CN.ow
```

Both checks must pass and the element counts must be equal. If not, stop and report.
Note the SHA-256: it goes into `probe_sha256`.

## 3. Hand over to the user

Tell the user, briefly:

1. Which file to paste: `probes/<id>/probe.zh-CN.ow` (the file path, not its content
   unless they ask).
2. The general steps from "通用步骤" in `docs/procedure.zh-CN.md` (Workshop mode, Inspector and
   recording on, no Slow Motion, only this probe pasted, start the game, do not touch the
   character).
3. The probe's last log line to wait for, and any probe-specific setup (such as
   spawning a hero), from the procedure table.
4. To paste back the **whole** Inspector text, variable block included.

Then wait. Do not continue until the user sends the text.

## 4. Save the capture verbatim

Check the pasted text before saving:

- the variable block is present;
- the probe's last log line is present, and the line count matches the procedure table;
- any validity line the procedure table requires for this probe is present and valid.

If a check fails, say which one and ask for the text again, or mark the run invalid
when the table says the run is void. Never repair, reformat, or complete
the text.

Save it unchanged: `capture.txt` for run 1, `capture-2.txt` for run 2, `capture-3.txt`
for run 3. Do not overwrite an earlier run.

## 5. Judge

Compare the log with the expected values for this probe in `docs/procedure.zh-CN.md` and
decide `match`, `mismatch`, or `inconclusive` by its conditions only. Quote the observed
numbers next to the expected ones. Cross-check with the variable block (for example `i`,
`runs`, `t0`) and report any disagreement instead of smoothing it over.

With several runs: the result is final only when at least three runs agree. Fewer
than three agreeing runs, or runs that disagree, keep the result provisional and say so.
If runs disagree, do not pick one; report `inconclusive` with the differences.

## 6. Write `capture.json`

Update or create `probes/<id>/capture.json` with the existing shape:

```json
{
  "probe": "<id>",
  "client": { "version": "", "date": "YYYY-MM-DD", "locale": "zh-CN" },
  "runs": 1,
  "probe_sha256": "<from step 2>",
  "hypothesis": "...",
  "observed": [],
  "result": "match | mismatch | inconclusive",
  "notes": ""
}
```

- Ask the user for the client version once if it is empty. Do not guess it.
- `runs` is the number of saved captures that are valid for this `probe_sha256`.
- `notes` states whether the result is provisional, anything the procedure table says the
  probe cannot test, and
  invalid runs.
- Keep `observed` to what the capture shows, in milliseconds.

## 7. Report

Lead with the verdict and whether it is provisional. Then the observed values beside
the expected ones, anything that disagreed, and what is still owed (remaining runs,
client version). Do not commit unless the user asks.
