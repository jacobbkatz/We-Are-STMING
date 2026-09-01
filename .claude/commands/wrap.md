---
description: End the work session - write the log, update STATUS.md, commit and push
---

End the work session. Do all four steps in order. Do not stop partway.

**1. Write the session log.** Copy `sessions/TEMPLATE.md` to `sessions/YYYY-MM-DD.md` with
today's real date. If a file for today already exists, add to it rather than overwriting.

Fill it in from what actually happened this session. Measurements with numbers and units.
What was observed, not what was expected. What was ruled out, not just what was found. If a
finding contradicts `STATUS.md`, an older session log, or `docs/PROJECT_HANDOFF_SUMMARY.md`,
record it explicitly in the "Corrections to earlier documents" section — that section is what
stops the other computer acting on a stale finding.

If nothing was measured this session because it was code-only, say so and keep the log short.

**2. Update `STATUS.md`.** Rewrite whatever changed: the stage table, open faults, next actions,
open questions, safety rules. Update the "Last updated" and "Updated by" lines at the top.

This is the first file the other person's Claude reads. It must describe reality, not intentions.
If a fault was fixed, remove it. If a rule no longer applies, remove it and say why in the log.

**3. Commit.**

```
git add -A
git commit -m "Session YYYY-MM-DD: <one line on what changed>"
```

**4. Push.**

```
git pull --rebase origin main && git push origin main
```

The rebase first is what stops the two computers clobbering each other. If there are conflicts,
resolve them and explain in plain language what conflicted and how you resolved it. Never force
push.

**Then confirm to the user, explicitly, that the push succeeded** and say what is now on GitHub.
They need to know their work is safe before they close the laptop. If the push failed, say so
clearly and do not let them walk away thinking it worked.
