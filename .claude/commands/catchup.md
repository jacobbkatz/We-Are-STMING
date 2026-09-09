---
description: Get up to date with what the other person did last session
---

Bring the user up to date before work starts.

1. Make sure this computer is current: `git pull --ff-only origin main`. If that fails, follow
   the recovery guidance in `CLAUDE.md` section 2 — show the user what is uncommitted or
   diverged and ask before discarding anything.

2. Read `STATUS.md` and **every session log carrying the newest date** in `sessions/` — there is
   often more than one for a date, because both people log the same day. `sessions/README.md`
   indexes them all.

3. Read [`docs/NEXT_SESSION_PLAN.md`](../../docs/NEXT_SESSION_PLAN.md) — **the prioritised
   procedure for the next bench session**, written to be executed with no memory of any
   conversation. It is refreshed at the end of every session.

4. Check whether anything changed since this computer last saw the repo:
   `git log --oneline -10`

Then tell the user, in plain language and in a few sentences:

- Where the build stands right now
- What the other person did last session, if anything is new
- What the next action is, from the "Next actions" list in `STATUS.md`
- Any safety rule that applies to that next action

Do not start work yet. Wait for them to say what they want to do.
