---
description: End the work session - write the log, update STATUS.md, commit and push
---

End the work session. Do all five steps in order. Do not stop partway.

**1. Write the session log.** Copy `sessions/TEMPLATE.md` to `sessions/YYYY-MM-DD.md` with
today's real date.

**If a log for today already exists, check whose session it is first.** If it belongs to the other
person, **do not append to it** — create `sessions/YYYY-MM-DD-<your name>.md` instead. Only add to
a log that is your own session's. **Then add a row to `sessions/README.md`** — `check_facts.py`
fails if a log is not indexed.

Fill it in from what actually happened this session. Measurements with numbers and units.
What was observed, not what was expected. What was ruled out, not just what was found. If a
finding contradicts `STATUS.md`, an older session log, or `docs/PROJECT_HANDOFF_SUMMARY.md`,
record it explicitly in the "Corrections to earlier documents" section — that section is what
stops the other computer acting on a stale finding.

If nothing was measured this session because it was code-only, say so and keep the log short.

**2. Update `STATUS.md`.** Rewrite whatever changed: the stage table, open faults, next actions,
open questions, safety rules. Update the "Last updated" and "Updated by" lines at the top.

This is the first file the other person's Claude reads. It must describe reality, not intentions.

**When a fault is fixed or a rule stops applying, strike it through and say what replaced it — do
not delete it.** This project has twice found that a retraction was itself wrong, and a deleted
rule leaves nothing to check that against. Deleting is only right for something that was never
true. Say what changed in the log either way.

**3. Update `docs/NEXT_SESSION_PLAN.md`.**

That file is the **only** place that says what to do next at the bench, and it is written to be
executed with no memory of any conversation. Rewrite whatever this session changed: steps that are
now done or moot, new gates, anything bought or arriving, any measurement that changes a procedure.
**Update its `**Last updated:**` line** — `check_facts.py` fails if a session log is newer than it,
which will block the commit in step 4.

**Struck-through, not deleted**, same as `STATUS.md`: a step that is no longer needed says so and
says why.

> **Added 2026-09-09.** The file had existed since 2026-09-07 and **nothing ever updated it**.
> Neither this command nor `/catchup` mentioned it, so it went stale for two days across three
> sessions and neither Jacob nor Nuh knew it was there.

**4. Commit.**

```
git add -A
git commit -m "Session YYYY-MM-DD: <one line on what changed>"
```

**5. Push.**

```
git pull --rebase origin main && git push origin main
```

The rebase first is what stops the two computers clobbering each other. If there are conflicts,
resolve them and explain in plain language what conflicted and how you resolved it. Never force
push.

**Then confirm to the user, explicitly, that the push succeeded** and say what is now on GitHub.
They need to know their work is safe before they close the laptop. If the push failed, say so
clearly and do not let them walk away thinking it worked.
