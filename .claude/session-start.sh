#!/usr/bin/env bash
#
# Runs automatically when a Claude Code session starts in this repo.
#
# Purpose: this project is worked on from two computers. The other person's work
# lives on GitHub and this machine may be behind. This script checks, and pulls
# when it is safe to do so without touching anything you have in progress.
#
# It never merges, never rebases, never discards. If the situation is anything
# other than "clean tree, on main, simply behind", it reports and leaves it to
# Claude.
#
# AUDITED 2026-09-09 after Jacob reported sessions behaving worse. Four defects
# were found in this file, all of which fed a session wrong information in the
# first thing it ever reads. Each fix is commented at the site. See
# sessions/2026-09-09-jacob.md section 15.

set -uo pipefail

cd "$(dirname "$0")/.." || exit 0

MAIN="main"

# Install the tracked git hooks on this computer if they are not already active.
# .git/hooks is not version controlled, so a hook committed to the repository does
# nothing on the other person's machine until core.hooksPath points at it. Doing
# it here means neither Jacob nor Nuh has to run anything.
if [ -d .githooks ] && [ "$(git config --get core.hooksPath 2>/dev/null)" != ".githooks" ]; then
    git config core.hooksPath .githooks 2>/dev/null && \
        echo "Installed the repository's git hooks (commit is now blocked while check_facts fails)."
fi

echo "=== We-Are-STMING: sync check ==="

if ! git rev-parse --git-dir >/dev/null 2>&1; then
    echo "Not a git repository. Skipping sync check."
    exit 0
fi

# FIX 1 (2026-09-09). This was hardcoded to main. A session working on a branch
# got its distance from main reported as if it were its own, and the auto
# fast-forward below would have merged origin/main into that branch unasked.
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "$MAIN")
if [ "$BRANCH" != "$MAIN" ]; then
    echo "On branch '$BRANCH', not $MAIN. Nothing will be pulled or merged automatically."
fi

if ! git -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=15 \
        fetch --quiet origin "$MAIN" 2>/dev/null; then
    echo "Could not reach GitHub (offline, or credentials need attention)."
    echo "Working from the local copy. It may be out of date - do not push"
    echo "until a fetch succeeds."
    exit 0
fi

DIRTY=""
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    DIRTY="yes"
fi

BEHIND=$(git rev-list --count HEAD..origin/"$MAIN" 2>/dev/null || echo 0)
AHEAD=$(git rev-list --count origin/"$MAIN"..HEAD 2>/dev/null || echo 0)

if [ "$BRANCH" != "$MAIN" ]; then
    echo "Relative to origin/$MAIN: $AHEAD commit(s) ahead, $BEHIND behind."
    echo "ACTION FOR CLAUDE: work on this branch. Do not push to $MAIN without"
    echo "the user saying so explicitly."
elif [ "$BEHIND" -gt 0 ] && [ "$AHEAD" -gt 0 ]; then
    echo "DIVERGED: this computer has $AHEAD commit(s) GitHub does not have,"
    echo "and GitHub has $BEHIND this computer does not."
    echo "ACTION FOR CLAUDE: run 'git pull --rebase origin $MAIN', resolve any"
    echo "conflicts, and explain plainly to the user what conflicted. Do not force push."
elif [ "$BEHIND" -gt 0 ] && [ -n "$DIRTY" ]; then
    echo "BEHIND by $BEHIND commit(s), but there are uncommitted changes here."
    echo "Not pulling automatically."
    git status --short | head -20
    echo "ACTION FOR CLAUDE: show the user what is uncommitted and ask whether to"
    echo "keep it before pulling. Do not discard without asking."
elif [ "$BEHIND" -gt 0 ]; then
    echo "Behind by $BEHIND commit(s). Pulling..."
    if git merge --ff-only "origin/$MAIN" >/dev/null 2>&1; then
        echo "Up to date now. Changes pulled in:"
        git log --oneline -"$BEHIND" --no-decorate | sed 's/^/  /'
    else
        echo "Fast-forward failed unexpectedly. ACTION FOR CLAUDE: investigate before working."
    fi
elif [ "$AHEAD" -gt 0 ]; then
    echo "This computer has $AHEAD commit(s) not yet on GitHub."
    echo "ACTION FOR CLAUDE: these need pushing before the session ends."
else
    echo "Up to date with GitHub."
fi

if [ -n "$DIRTY" ]; then
    echo "Note: there are uncommitted changes in the working tree."
fi

# Surface the state lines that matter most, so they are in context immediately.
if [ -f STATUS.md ]; then
    echo ""
    # FIX 2 (2026-09-09). This was `sed -n '3,4p' STATUS.md` -- a positional slice
    # of a file that CLAUDE.md section 5 requires rewriting at the end of EVERY
    # session. It had already drifted: it printed a sentence cut off mid-clause
    # ("...nothing was powered or measured. C2's"). Match the labels instead, so
    # rewording the header cannot break it.
    grep -m1 '^\*\*Last updated:\*\*' STATUS.md || echo "STATUS.md has no 'Last updated' line."
    grep -m1 '^\*\*Updated by:\*\*'   STATUS.md | cut -c1-160

    # FIX 3 (2026-09-09). This was `ls sessions/2*.md | sort | tail -1`, which is
    # a LEXICAL sort: '-' (0x2D) sorts before '.' (0x2E), so "2026-09-09-jacob.md"
    # sorts BEFORE "2026-09-09.md" and a second log written later the same day was
    # never surfaced. CLAUDE.md section 2 tells every session to read "the newest
    # file in sessions/", and this named the older one. Take the newest DATE, then
    # list every log carrying it.
    NEWEST_DATE=$(ls -1 sessions/ 2>/dev/null \
        | grep -o '^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}' | sort -u | tail -1)
    if [ -n "$NEWEST_DATE" ]; then
        COUNT=$(ls -1 sessions/"$NEWEST_DATE"*.md 2>/dev/null | wc -l)
        if [ "$COUNT" -gt 1 ]; then
            echo "Latest session logs ($NEWEST_DATE) - THERE ARE $COUNT, READ THEM ALL:"
            ls -1 sessions/"$NEWEST_DATE"*.md | sed 's/^/  /'
        else
            echo "Latest session log: $(ls -1 sessions/"$NEWEST_DATE"*.md 2>/dev/null)"
        fi

        STATUS_DATE=$(sed -n 's/^\*\*Last updated:\*\* \([0-9-]\{10\}\).*/\1/p' STATUS.md | head -1)
        if [ -n "$STATUS_DATE" ] && [ "$NEWEST_DATE" \> "$STATUS_DATE" ]; then
            echo ""
            echo "WARNING: STATUS.md says $STATUS_DATE but there is a session log from $NEWEST_DATE."
            echo "STATUS.md was probably not updated at the end of that session, so it may not"
            echo "describe reality. ACTION FOR CLAUDE: read that log, tell the user what is"
            echo "missing from STATUS.md, and offer to bring it up to date before starting work."
        fi
    fi
fi

# FIX 4 (2026-09-09). This block used to discard stderr and then print ONE fixed
# diagnosis -- "a value docs/FACTS.md lists as RETIRED is still in a live
# document" -- whatever the checker had actually found. check_facts.py reports
# four distinct problems, so three times in four it named the wrong cause and
# sent the session hunting the wrong thing. Worse, a crashed checker produced an
# empty message plus that same confident wrong diagnosis. Show what it said.
if [ -f Code/pc/check_facts.py ]; then
    FACTS_OUT=$(python3 Code/pc/check_facts.py 2>&1)
    FACTS_RC=$?
    if [ "$FACTS_RC" -ne 0 ]; then
        echo ""
        if printf '%s' "$FACTS_OUT" | grep -q '^check_facts:'; then
            printf '%s\n' "$FACTS_OUT" | head -40
            echo ""
            echo "ACTION FOR CLAUDE: fix what check_facts.py named above, not what you expect"
            echo "it to have found. It reports four different kinds of problem: a retired value"
            echo "still in a live document, a broken file reference, an archived document cited"
            echo "as current, and a 'safety rule N' citation pointing at the wrong rule."
        else
            echo "check_facts.py FAILED TO RUN (exit $FACTS_RC)."
            echo "This is a BROKEN CHECKER, not a documentation problem:"
            printf '%s\n' "$FACTS_OUT" | head -20
            echo ""
            echo "ACTION FOR CLAUDE: repair the script first. While it is broken, nothing is"
            echo "checking the numbers in this repository."
        fi
    fi
fi

echo "=== Read STATUS.md before starting work. See CLAUDE.md for the full protocol. ==="
exit 0
