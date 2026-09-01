---
description: Get up to date with what the other person did last session
---

Bring the user up to date before work starts.

1. Make sure this computer is current: `git pull --ff-only origin main`. If that fails, follow
   the recovery guidance in `CLAUDE.md` section 2 — show the user what is uncommitted or
   diverged and ask before discarding anything.

2. Read `STATUS.md` and the newest file in `sessions/`.

3. Check whether anything changed since this computer last saw the repo:
   `git log --oneline -10`

Then tell the user, in plain language and in a few sentences:

- Where the build stands right now
- What the other person did last session, if anything is new
- What the next action is, from the "Next actions" list in `STATUS.md`
- Any safety rule that applies to that next action

Do not start work yet. Wait for them to say what they want to do.
