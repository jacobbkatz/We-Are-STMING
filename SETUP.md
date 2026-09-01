# Setting up a computer to work on this project

Follow this once per computer. After that, the day-to-day routine is section 5, which is two
sentences long.

Written for people who don't code. Every command is meant to be copied and pasted exactly.

---

## 1. Install the three things you need

| | What | Where |
|---|---|---|
| 1 | **Git** | https://git-scm.com/downloads |
| 2 | **Claude Code** | https://claude.com/claude-code |
| 3 | **Python 3** | https://python.org/downloads — tick "Add Python to PATH" on Windows |

You only need **PlatformIO** if you are going to flash firmware to the Teensy. It installs as an
extension inside VS Code: install VS Code, then search the extensions panel for "PlatformIO IDE".

---

## 2. Get the project onto this computer

Open a terminal — Terminal on Mac, Git Bash on Windows — and run:

```bash
git clone https://github.com/jacobbkatz/We-Are-STMING.git
cd We-Are-STMING
```

That downloads roughly 35 MB and creates a `We-Are-STMING` folder. Everything from now on happens
inside that folder.

The first time you push, Git will ask who you are. Answer once:

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

GitHub will also ask you to sign in the first time you push. Use the browser sign-in it offers,
or a personal access token if it asks for a password — **your GitHub account password will not
work**, GitHub stopped accepting those.

---

## 3. Install the Python tools

From inside the `We-Are-STMING` folder:

```bash
pip install pyserial numpy matplotlib
```

`tkinter` comes with Python on Windows and Mac. On Linux, install it separately with
`sudo apt install python3-tk`.

Check it worked by listing the serial ports with the Teensy plugged in:

```bash
python Code/pc/stm_console.py GSTS
```

If it finds the board it prints a line of ten comma-separated numbers. If it says no Teensy found,
the usual cause is a **charge-only USB cable** — see `docs/START_HERE_gotchas.md`.

---

## 4. Start Claude

From inside the `We-Are-STMING` folder:

```bash
claude
```

It must be started **from inside that folder**. Claude reads `CLAUDE.md` automatically on startup
and gets the whole project protocol, the safety rules, and where everything lives. You do not
need to explain the project to it.

When it starts you should see a sync check that ends with either "Up to date with GitHub" or a
note about pulling changes. **That message is how you know the two computers are talking.**

---

## 5. The routine, every session from now on

**At the start:** open a terminal, `cd` into the `We-Are-STMING` folder, run `claude`. The sync
happens automatically.

**At the end:** tell Claude *"wrap up the session"*. It will write the session log, update
`STATUS.md`, commit, and push to GitHub. Wait until it confirms the push succeeded before you
close the laptop.

That is the whole thing.

---

## 6. Do we have to stay in one chat forever?

**No. Start a new chat whenever you like** — that is the whole point of keeping everything in
GitHub rather than in a conversation.

Every new Claude Code session automatically pulls from GitHub and reads `CLAUDE.md`, so a fresh
chat already knows the safety rules, which documents supersede which, and where the build stands.
You do not need to explain anything or ask it to pull.

Fresh chats are usually better — long ones get slow, and a new one starts from the repository,
which is the accurate picture.

**The rule that makes this safe: the repository is the memory, the chat is not.** Anything worked
out in a conversation that never made it into a file is gone when that conversation ends. So type
`/wrap` before closing a chat.

The only reason to stay in one chat is if you are mid-task and the reasoning so far only exists in
the conversation. Either finish it, or `/wrap` first.

---

## 7. When something goes wrong

**"I forgot to push last time."** Nothing is lost. Say to Claude: *"I have unpushed work from
last session, please push it."* It will handle the ordering.

**"We both worked at the same time."** Also fine. Git will notice, and Claude is instructed to
run `git pull --rebase` and sort it out. The only thing that would genuinely lose work is a
**force push**, which Claude is instructed never to do.

**"It says my changes would be overwritten."** There is unfinished work on this computer. Ask
Claude what is uncommitted before doing anything else — do not let anything be discarded until
you have seen what it is.

**"The sync check says it can't reach GitHub."** You are offline or your sign-in expired. You can
still work; just don't assume your copy is current, and push once you're back online.

---

## 8. What not to do

- **Do not edit files on the GitHub website** while someone is working locally. It creates the
  one situation that needs manual untangling.
- **Do not both work at the same time** on the same files if you can avoid it. It's recoverable,
  it's just avoidable.
- **Do not force push.** Ever. It is the only operation here that can actually destroy the other
  person's work.
