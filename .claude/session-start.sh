#!/usr/bin/env bash
#
# Runs automatically when a Claude Code session starts in this repo.
#
# Purpose: this project is worked on from two computers. The other person's work
# lives on GitHub and this machine may be behind. This script checks, and pulls
# when it is safe to do so without touching anything you have in progress.
#
# It never merges, never rebases, never discards. If the situation is anything
# other than "clean tree, simply behind", it reports and leaves it to Claude.

set -uo pipefail

cd "$(dirname "$0")/.." || exit 0

BRANCH="main"

echo "=== We-Are-STMING: sync check ==="

if ! git rev-parse --git-dir >/dev/null 2>&1; then
    echo "Not a git repository. Skipping sync check."
    exit 0
fi

# Bound the fetch so a dead network cannot hang the session start.
if ! git -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=15 \
        fetch --quiet origin "$BRANCH" 2>/dev/null; then
    echo "Could not reach GitHub (offline, or credentials need attention)."
    echo "Working from the local copy. It may be out of date - do not push"
    echo "until a fetch succeeds."
    exit 0
fi

DIRTY=""
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    DIRTY="yes"
fi

BEHIND=$(git rev-list --count HEAD..origin/"$BRANCH" 2>/dev/null || echo 0)
AHEAD=$(git rev-list --count origin/"$BRANCH"..HEAD 2>/dev/null || echo 0)

if [ "$BEHIND" -gt 0 ] && [ "$AHEAD" -gt 0 ]; then
    echo "DIVERGED: this computer has $AHEAD commit(s) GitHub does not have,"
    echo "and GitHub has $BEHIND this computer does not."
    echo "ACTION FOR CLAUDE: run 'git pull --rebase origin $BRANCH', resolve any"
    echo "conflicts, and explain plainly to the user what conflicted. Do not force push."
elif [ "$BEHIND" -gt 0 ] && [ -n "$DIRTY" ]; then
    echo "BEHIND by $BEHIND commit(s), but there are uncommitted changes here."
    echo "Not pulling automatically."
    git status --short | head -20
    echo "ACTION FOR CLAUDE: show the user what is uncommitted and ask whether to"
    echo "keep it before pulling. Do not discard without asking."
elif [ "$BEHIND" -gt 0 ]; then
    echo "Behind by $BEHIND commit(s). Pulling..."
    if git merge --ff-only "origin/$BRANCH" >/dev/null 2>&1; then
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

# Surface the two lines that matter most, so state is in context immediately.
if [ -f STATUS.md ]; then
    echo ""
    sed -n '3,4p' STATUS.md
    LATEST=$(ls -1 sessions/2*.md 2>/dev/null | sort | tail -1)
    if [ -n "$LATEST" ]; then
        echo "Latest session log: $LATEST"
        # A session log newer than STATUS.md means someone wrote up their work
        # but never updated the live-state file the other computer reads first.
        LOG_DATE=$(basename "$LATEST" .md | cut -c1-10)
        STATUS_DATE=$(sed -n 's/^\*\*Last updated:\*\* \([0-9-]\{10\}\).*/\1/p' STATUS.md | head -1)
        if [ -n "$STATUS_DATE" ] && [ "$LOG_DATE" \> "$STATUS_DATE" ]; then
            echo ""
            echo "WARNING: STATUS.md says $STATUS_DATE but there is a session log from $LOG_DATE."
            echo "STATUS.md was probably not updated at the end of that session, so it may not"
            echo "describe reality. ACTION FOR CLAUDE: read $LATEST, tell the user what is"
            echo "missing from STATUS.md, and offer to bring it up to date before starting work."
        fi
    fi
fi

echo "=== Read STATUS.md before starting work. See CLAUDE.md for the full protocol. ==="
exit 0
