#!/usr/bin/env python3
"""
Find stale numbers that a correction left behind.

    python3 Code/pc/check_facts.py

Why this exists: on 2026-09-07 the ADC full scale was corrected from 4.096 V to
10.24 V and the preamp offset from 37 nA to 119 nA. Both had been written into
more than a dozen documents, and correcting the ones anybody thought of still
left stale copies in the rest. Nothing caught it. This does.

`docs/FACTS.md` holds the canonical value of every number that matters, and a
table of RETIRED values. This script reads that table and reports anywhere a
retired value still appears in a live document.

WHAT IT SKIPS, deliberately:
  * sessions/       -- history. Old logs SHOULD contain the old numbers
  * docs/FACTS.md   -- it lists the retired values on purpose
  * anything the harness generates, and non-prose files

WHAT IT DOES NOT DO: it cannot tell you a number is wrong. It only tells you a
number we already know is wrong is still sitting somewhere it will be believed.

Exit status 0 if clean, 1 if anything was found, so a hook can act on it.
"""

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FACTS = os.path.join(REPO, 'docs', 'FACTS.md')

SKIP_DIRS = {'.git', 'sessions', '__pycache__', 'node_modules'}
SKIP_FILES = {'FACTS.md', 'check_facts.py'}

# A line that is itself recording the correction is not stale. These are the
# words used when a document says "this used to say X, it is now Y".
EXCUSES = re.compile(
    r'~~|retired|superseded|corrected|was wrong|were wrong|no longer|'
    r'previously|used to|stale|not a bug|do not change|incorrect|'
    r'\bwrong\b|\bvoid\b|replaced by|instead of|rather than|\berror\b|not the input span|is not the|range option|REFBUF',
    re.I)


def retired_patterns():
    """Read the RETIRED table out of docs/FACTS.md.

    Each row looks like:  | `37 nA` as the preamp offset | **119 nA** | ... |
    The first backticked item on the row is the retired literal; the rest of the
    cell is context that narrows when it counts.
    """
    if not os.path.exists(FACTS):
        sys.stderr.write("cannot find docs/FACTS.md -- run from the repository\n")
        sys.exit(2)
    rows, in_table = [], False
    for line in open(FACTS, encoding='utf-8'):
        if line.startswith('## Retired values'):
            in_table = True
            continue
        if in_table and line.startswith('## '):
            break
        if not in_table or not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 2 or cells[0].startswith('---') or cells[0] == 'Retired':
            continue
        m = re.search(r'`([^`]+)`', cells[0])
        if not m:
            continue
        literal = m.group(1)
        # "as the ADC full scale" means only flag it near those words
        qual = re.search(r'as the \*\*?([^*|]+?)\*\*?\s*$', cells[0])
        rows.append((literal, qual.group(1).strip().lower() if qual else None,
                     re.sub(r'[*`]', '', cells[1])))
    return rows


# Two files inside sessions/ are NOT history and must be checked like any other
# live document. Found 2026-09-09: the whole directory was skipped, so a retired
# value in TEMPLATE.md would have been copied into every future log, and nothing
# checked the index at all.
SESSIONS_LIVE = {'README.md', 'TEMPLATE.md'}


def live_files():
    for root, dirs, names in os.walk(REPO):
        rel = os.path.relpath(root, REPO)
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in names:
            if n in SKIP_FILES:
                continue
            if n.endswith(('.md', '.py', '.hpp', '.cpp', '.txt')):
                yield os.path.join(root, n)
    sess = os.path.join(REPO, 'sessions')
    if os.path.isdir(sess):
        for n in sorted(SESSIONS_LIVE):
            fp = os.path.join(sess, n)
            if os.path.exists(fp):
                yield fp


def check_links():
    """Every `path/to/file.md` mentioned in prose should exist.

    Added 2026-09-08 after files were archived into docs/archive/. A reference
    that silently rots is worse than no reference: it sends a future session
    looking for something and it comes back with nothing.
    """
    ref = re.compile(r'`((?:docs|sessions|Code|CAD|PCB|gerbers)/[A-Za-z0-9_./-]+\.(?:md|py|hpp|cpp|json|txt))`')
    bad = []
    for path in live_files():
        if not path.endswith('.md'):
            continue
        rel = os.path.relpath(path, REPO)
        hist = False
        for i, line in enumerate(open(path, encoding='utf-8', errors='replace'), 1):
            # The handoff's Appendix A is a dated change log. The paths in it were
            # correct when written and several files have moved since. Rewriting
            # them would falsify history, so stop checking from there on.
            if rel.endswith('PROJECT_HANDOFF_SUMMARY.md') and re.match(r'#+ +A\b|#+ +Appendix', line):
                hist = True
            if hist:
                continue
            for target in ref.findall(line):
                if 'YYYY' in target or 'MM-DD' in target:
                    continue          # a filename template, not a reference
                if not os.path.exists(os.path.join(REPO, target)):
                    bad.append((rel, i, target))
    return bad


def check_archive_refs():
    """An archived document must not be cited as if it were current.

    docs/archive/ holds superseded procedures. Anything pointing at one should
    say so, or a future session will follow instructions that no longer apply.
    """
    archive = os.path.join(REPO, 'docs', 'archive')
    if not os.path.isdir(archive):
        return []
    names = [n for n in os.listdir(archive) if n.endswith('.md')]
    ok = re.compile(r'archive|supersed|archiv|preserved|no longer|历史|was written|resolved', re.I)
    bad = []
    for path in live_files():
        if not path.endswith('.md') or '/archive/' in path:
            continue
        rel = os.path.relpath(path, REPO)
        if rel.startswith('sessions'):
            continue
        hist = False
        for i, line in enumerate(open(path, encoding='utf-8', errors='replace'), 1):
            if rel.endswith('PROJECT_HANDOFF_SUMMARY.md') and re.match(r'#+ +A\b|#+ +Appendix', line):
                hist = True
            if hist:
                continue
            for n in names:
                if n in line and not ok.search(line):
                    bad.append((rel, i, n))
    return bad


STOPWORDS = set("""
about above after again against because before being below between both cannot could does
doing during each every from have having here into itself just more most only other over
same should some such than that their them then there these they this those through under
until very were what when where which while will with would your rule rules safety status
""".split())


# Words that mean "this sentence is discussing a citation" rather than making
# one. Kept tight on purpose -- see check_safety_rule_refs.
CITATION_TALK = re.compile(
    r'miscit|citation|\bcited\b|renumber|meant rule|now rule|became rule|'
    r'points at|pointing at|should (?:be|cite)|read as',
    re.I)


def status_rules():
    """STATUS.md's numbered safety rules, as {number: body text}.

    Written as "0.", "0b.", "0c.", "1." ... at the start of a line inside the
    standing-safety-rules section. A rule runs on until the next one starts.
    """
    path = os.path.join(REPO, 'STATUS.md')
    if not os.path.exists(path):
        return {}
    rules, inside, cur = {}, False, None
    for line in open(path, encoding='utf-8', errors='replace'):
        if re.match(r'#+ +Standing safety rules', line):
            inside = True
            continue
        if inside and re.match(r'#+ ', line):
            break
        if not inside:
            continue
        m = re.match(r'(\d+[a-z]?)\. +(\S.*)', line)
        if m:
            cur = m.group(1)
            rules[cur] = m.group(2)
        elif cur and line.strip():
            rules[cur] += ' ' + line.strip()
    return rules


def _words(text):
    text = re.sub(r'`[^`]*`', ' ', text)
    return {w for w in re.findall(r"[a-z]{5,}", text.lower()) if w not in STOPWORDS}


def check_dead_qualifiers():
    """A qualified RETIRED row whose qualifier matches nothing is an inert check.

    Added 2026-09-09, generalising a finding Nuh recorded the same day
    (sessions/2026-09-09.md section 9). The `5.93 mm` row was qualified as "the
    preamp mounting-hole spacing" -- wording that appears in no document -- so the
    qualifier never matched and THE CHECKER REPORTED CLEAN WHILE THREE LIVE FILES
    CARRIED THE WRONG NUMBER. Broadening it to "the mounting holes" caught all
    three at once.

    Nuh's own words: "A silent checker is worse than no checker, because it is
    believed. When adding a RETIRED row, phrase the qualifier in the words the
    documents actually use, then confirm it fires before trusting it."

    That confirmation was a manual step, so this does it automatically. It does not
    test whether the row finds stale values -- it tests whether the row is CAPABLE
    of finding them. A qualifier matching nothing anywhere is dead wording.
    """
    dead = []
    for literal, qual, replacement in retired_patterns():
        if not qual:
            continue                      # unqualified rows always fire
        words = [w for w in qual.split() if len(w) > 3]
        if not words:
            continue
        seen = False
        for path in live_files():
            if not path.endswith('.md') or seen:
                continue
            lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
            for i in range(len(lines)):
                window = ' '.join(lines[max(0, i - 2):i + 2]).lower()
                if all(w in window for w in words):
                    seen = True
                    break
        if not seen:
            dead.append((literal, qual))
    return dead


def check_plan_freshness():
    """docs/NEXT_SESSION_PLAN.md must not be older than the newest session log.

    Added 2026-09-09, at Jacob's request. The file existed from 2026-09-07 and was
    the canonical home for "what to do next at the bench" (CLAUDE.md section 6),
    but NOTHING kept it current -- neither /wrap nor /catchup mentioned it. It sat
    unmaintained for two days while three sessions happened, and by then neither
    Jacob nor Nuh knew it existed.

    Its content had gone stale in ways that cost real work: it still scheduled the
    board rebuild for "Sunday", still asked for callipers on a piezo that is now
    built, and its H1 told you to print the ORIGINAL box while describing the
    expected result as the v2 geometry it forbids two lines earlier.

    A plan older than the last session is a plan that does not know what happened.
    """
    plan = os.path.join(REPO, 'docs', 'NEXT_SESSION_PLAN.md')
    sess = os.path.join(REPO, 'sessions')
    if not os.path.exists(plan) or not os.path.isdir(sess):
        return None
    m = re.search(r'^\*\*Last updated:\*\* +(\d{4}-\d{2}-\d{2})',
                  open(plan, encoding='utf-8', errors='replace').read(), re.M)
    if not m:
        return ('MISSING', 'add a "**Last updated:** YYYY-MM-DD" line')
    plan_date = m.group(1)
    dates = sorted(m2.group(1) for m2 in
                   (re.match(r'(\d{4}-\d{2}-\d{2})', n) for n in os.listdir(sess))
                   if m2)
    if not dates:
        return None
    newest = dates[-1]
    return (plan_date, newest) if newest > plan_date else None


def check_session_index():
    """Every session log on disk must be linked from sessions/README.md.

    Added 2026-09-09. sessions/2026-09-09.md -- a whole day's work -- was missing
    from the index, and was simultaneously invisible to the start-up hook, whose
    lexical sort put the same day's "-jacob" log first. Two independent
    mechanisms, the same blind spot, the same file: a log nobody would find.

    The root cause is that the naming convention was never agreed. README.md said
    "one file per work session, named YYYY-MM-DD.md" while four logs on disk have
    always carried a suffix. Everything that consumes logs assumed the singular
    form. So this checks the index against reality rather than against the rule.
    """
    sess = os.path.join(REPO, 'sessions')
    readme = os.path.join(sess, 'README.md')
    if not os.path.isdir(sess) or not os.path.exists(readme):
        return []
    text = open(readme, encoding='utf-8', errors='replace').read()
    linked = set(re.findall(r'\]\((\d{4}-\d{2}-\d{2}[^)]*\.md)\)', text))
    on_disk = {n for n in os.listdir(sess)
               if re.match(r'\d{4}-\d{2}-\d{2}.*\.md$', n)}
    return sorted(on_disk - linked)


def check_safety_rule_refs():
    """Every "safety rule N" citation must resolve, AND point at the right rule.

    Added 2026-09-09 after this went wrong in both ways it can. STATUS.md cited
    "safety rule 10" twice meaning the DAC modulo-wrap hazard, which had become
    rule 13 when rules were inserted above it -- while rule 10 had become "do not
    glue the spare board". The citation still resolved, so a dangling-reference
    check passes it. A session following it reads a different rule, and the one it
    misses is a tip hazard.

    So this checks two things: that rule N exists, and that the citing sentence
    shares at least one content word with rule N's own text. No overlap at all
    means the citation is almost certainly pointing at the wrong number.

    Prose *about* a miscitation necessarily quotes the bad number, so a passage
    matching CITATION_TALK within +/-2 lines is skipped. That regex is deliberately
    narrow. The retired-value EXCUSES regex was tried first and is far too broad
    here: it matches "wrong" and "error", both of which sit within two lines of the
    two real miscitations, so it excused exactly the bug this exists to catch.

    STATUS.md's numbered list is the only citable one. Session logs are history
    and keep whatever numbering was current when they were written.
    """
    rules = status_rules()
    if not rules:
        return [], []
    ref = re.compile(r'safety rules? (\d+[a-z]?)(?: and (\d+[a-z]?))?', re.I)
    missing, mismatched = [], []
    for path in live_files():
        if not path.endswith('.md') or '/archive/' in path:
            continue
        rel = os.path.relpath(path, REPO)
        if rel.startswith('sessions'):
            continue
        lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
        for i, line in enumerate(lines, 1):
            for m in ref.finditer(line):
                for n in m.groups():
                    if not n:
                        continue
                    if n not in rules:
                        missing.append((rel, i, n))
                        continue
                    # A passage describing a past miscitation is not making one.
                    # This needs its OWN narrow excuse, not the retired-value
                    # EXCUSES: that regex matches "wrong" and "error", which occur
                    # naturally in this repository's technical prose and silently
                    # excused both real miscitations when it was tried.
                    if CITATION_TALK.search(' '.join(lines[max(0, i - 3):i + 2])):
                        continue
                    # Compare against THIS LINE ONLY. Widening to a +/-1 line
                    # window was tried on 2026-09-09 to clear a false positive and
                    # was reverted: it silently lost one of the two known
                    # miscitations and introduced a different false positive.
                    # A citation belongs next to the claim it supports; if it does
                    # not overlap, move the citation, do not widen the check.
                    cite = _words(line)
                    if len(cite) < 3:
                        continue          # "see safety rule 10" and nothing else
                    if not (cite & _words(rules[n])):
                        mismatched.append((rel, i, n, line.strip()[:80]))
    return missing, mismatched


def main():
    pats = retired_patterns()
    if not pats:
        print("no retired values listed in docs/FACTS.md -- nothing to check")
        return 0

    hits = []
    for path in sorted(live_files()):
        rel = os.path.relpath(path, REPO)
        try:
            lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            if EXCUSES.search(line):
                continue
            for literal, qual, replacement in pats:
                if literal.lower() not in line.lower():
                    continue
                # If the corrected value is on the same line, the line is a
                # correction table or a sentence saying "X, not Y". Not stale.
                num = re.search(r'[\d.]+', replacement)
                if num and num.group(0) in line:
                    continue
                # A qualified entry ("`4.096` as the ADC full scale") only counts
                # when its qualifying words are nearby -- so 4.096 as REFBUF, and
                # +/-5 V as a DAC range option, do not trip it.
                if qual:
                    window = ' '.join(lines[max(0, i - 2):i + 2]).lower()
                    if not all(w in window for w in qual.split() if len(w) > 3):
                        continue
                hits.append((rel, i, literal, replacement, line.strip()[:88]))

    links = check_links()
    arch = check_archive_refs()
    rule_missing, rule_wrong = check_safety_rule_refs()
    unindexed = check_session_index()
    dead_quals = check_dead_qualifiers()
    stale_plan = check_plan_freshness()

    if not hits and not links and not arch and not rule_missing and not rule_wrong and not unindexed and not dead_quals and not stale_plan:
        print("check_facts: clean.")
        print("  - no retired value in a live document")
        print("  - no broken file reference")
        print("  - no archived document cited as current")
        print("  - every 'safety rule N' citation resolves, and matches its rule")
        print("  - every session log is listed in sessions/README.md")
        print("  - every RETIRED qualifier still matches real wording")
        print("  - docs/NEXT_SESSION_PLAN.md is no older than the newest session log")
        return 0

    if links:
        print("check_facts: %d reference(s) to a file that does not exist:\n" % len(links))
        for rel, ln, target in links:
            print("    %s:%d  ->  %s" % (rel, ln, target))
        print()

    if arch:
        print("check_facts: %d reference(s) to an ARCHIVED document that do not say so:\n"
              % len(arch))
        for rel, ln, name in arch:
            print("    %s:%d  mentions %s" % (rel, ln, name))
        print("  Say 'archived' or 'superseded' on the line, or point somewhere current.\n")

    if stale_plan:
        print("check_facts: docs/NEXT_SESSION_PLAN.md is out of date.\n")
        print("    plan says 'Last updated: %s', newest session log is %s"
              % stale_plan)
        print("  That file is the ONLY place that says what to do next at the bench, and")
        print("  it is written to be executed with no memory of any conversation. A plan")
        print("  older than the last session does not know what happened in it.")
        print("  Update it and its 'Last updated' line -- /wrap step 3.\n")

    if dead_quals:
        print("check_facts: %d RETIRED row(s) whose qualifier matches NOTHING:\n"
              % len(dead_quals))
        for literal, qual in dead_quals:
            print("    '%s' qualified as '%s'" % (literal, qual))
        print("  This row can never fire, so the checker is BLIND to that value while")
        print("  reporting clean. Reword the qualifier in docs/FACTS.md using the words")
        print("  the documents actually use. See sessions/2026-09-09.md section 9.\n")

    if unindexed:
        print("check_facts: %d session log(s) missing from sessions/README.md:\n"
              % len(unindexed))
        for n in unindexed:
            print("    sessions/%s" % n)
        print("  An unindexed log is one nobody finds. Add a row to sessions/README.md.\n")

    if rule_missing:
        print("check_facts: %d 'safety rule N' citation(s) that STATUS.md does not have:\n"
              % len(rule_missing))
        for rel, ln, n in rule_missing:
            print("    %s:%d  cites safety rule %s" % (rel, ln, n))
        print()

    if rule_wrong:
        print("check_facts: %d 'safety rule N' citation(s) pointing at the WRONG rule:\n"
              % len(rule_wrong))
        for rel, ln, n, text in rule_wrong:
            print("    %s:%d  cites safety rule %s, which is about something else"
                  % (rel, ln, n))
            print("          %s" % text)
        print("  The rule exists, but shares no wording with the sentence citing it.")
        print("  STATUS.md renumbers when a rule is inserted -- find the rule that")
        print("  actually holds this content and cite that number instead.\n")

    if not hits:
        return 1

    print("check_facts: %d possible stale value(s).\n" % len(hits))
    print("Each line below still contains a number docs/FACTS.md lists as RETIRED.")
    print("If the line is deliberately quoting the old value, add a word like")
    print("'was', 'corrected' or 'superseded' to it and this will stop flagging it.\n")
    last = None
    for rel, ln, literal, repl, text in hits:
        if rel != last:
            print("  %s" % rel)
            last = rel
        print("    %4d  '%s'  ->  should be %s" % (ln, literal, repl))
        print("          %s" % text)
    print("\n%d to review. This script cannot tell you a number is wrong --" % len(hits))
    print("only that one we already know is wrong is still where it will be believed.")
    return 1


if __name__ == '__main__':
    sys.exit(main())
