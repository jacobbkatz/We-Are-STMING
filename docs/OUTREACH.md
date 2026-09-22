# Who we have asked for help, and what they said

**Created 2026-09-22.** **This file exists because a session drafted a reply to Dr. Zahl that
Jacob had already sent an hour earlier**, and nothing in this repository could have told it so.
Outreach lives in Jacob's and Nuh's email, which is exactly the failure mode `CLAUDE.md` §3d
describes: *"Anything that stays in the conversation is lost the moment the context is compacted."*

> **Rule.** Before drafting any letter to an outside expert, read this file. Before assuming a
> question is unasked, read this file. **When a reply arrives, add it here in the same session**,
> and put anything technical into `docs/OPEN_QUESTIONS.md` or `docs/FACTS.md` where it belongs.

> **What this file is NOT.** It is not a record of advice. **Technical content goes to its
> canonical home** — a candidate to `docs/OPEN_QUESTIONS.md`, a number to `docs/FACTS.md`, a bench
> step to `docs/NEXT_SESSION_PLAN.md`. This file records **who, when, and what is still pending**,
> so nobody asks twice and nobody waits on a reply that already came.

**Provenance:** all rows below `EMAIL` — read from Jacob's Gmail 2026-09-22 with his permission.

---

## Technical outreach

| Who | Where | Sent | State |
|---|---|---|---|
| **Dr. Percy Zahl** `pzahl@bnl.gov` | Brookhaven National Laboratory, CFN. **Had advised on vibration isolation and scan head design earlier in the build** — acknowledged in `README.md` | **2026-09-21 02:56 UTC**, cc Nuh | **REPLIED 2026-09-21 13:05.** Isolate systematically, eliminate the biggest contributor first; monitor temperature precisely, enclose, thermalize for hours; find mismatched expansion coefficients in the tip-sample loop; **look up piezo creep**; and joints and stressed points creep for a long time too. **Worked into the repository** — `STATUS.md` 2026-09-22 block, `docs/NEXT_SESSION_PLAN.md` STEP 1 and STEP 5b, `docs/OPEN_QUESTIONS.md`. **JACOB REPLIED 2026-09-22 16:52.** **SECOND REPLY 2026-09-22 ~14:31 ET, and it is the most consequential thing anyone outside this project has told us** — a materials ruling and a design principle, summarised in the section below. **NOT NAMED ON THE PUBLIC WEBSITE** — Jacob's instruction, 2026-09-22; the page calls him a physicist at Brookhaven and `check_site.py` enforces it |
| **Ming Lu** `mlu@bnl.gov` | Brookhaven, CFN. Jacob worked with him at CFN over the summer | **2026-09-21 02:44 UTC**, with Dr. Chang-Yong Nam, cc Carlos Colosqui and Nuh | **REPLIED 2026-09-21 14:09.** **Declined to advise and said why:** *"I myself never use STM (our research only needs AFM) and I am not a SPM expert who built SPM from ground before."* **Forwarded the problem to Dr. Xiao Tong.** Jacob acknowledged 2026-09-22 16:50 |
| **Dr. Xiao Tong** | Brookhaven, CFN. **Manages the CFN STMs** | **Not contacted directly** — reached via Ming Lu's forward, 2026-09-21 | **PENDING, AND NOT BEFORE 1 OCTOBER 2026.** Ming Lu: end of the government fiscal year, everyone is on year-end statistics and reports, *"he might not have time to look into the problem and give you feedback before Oct. 1st. Please be patient!"* **This is the most STM-specific expert the project has reached.** See `docs/OPEN_QUESTIONS.md` |
| **Dr. Chang-Yong Nam** `cynam@bnl.gov` | Brookhaven, CFN | **2026-09-21 02:44 UTC**, same letter as Ming Lu | **No reply as of 2026-09-22** |
| **Carlos Colosqui** `carlos.colosqui@stonybrook.edu` | Stony Brook | cc on the Lu/Nam letter, 2026-09-21 | **No reply as of 2026-09-22.** Also the PI on CFN proposal 317457, which Jacob is named on |

## Non-technical outreach

**Recorded so nobody re-contacts them, and because they may want follow-ups.** No advice sought.

| Who | Sent | State |
|---|---|---|
| **Mr. Buckley** `pbuckley@sharonschools.net` and **Mrs. Bhalekar** `ubhalekar@sharonschools.net` | Jacob, **2026-09-21 02:49 UTC**, cc Nuh | **Both replied warmly, 2026-09-22.** **Jacob has said they may share it with their classes** (2026-09-22 16:55) |
| **Ms. Das** `ndas@sharonschools.net` and **Mr. Tessier** `atessier@sharonschools.net` | **Nuh**, 2026-09-22 16:14 UTC, cc Jacob | No reply yet |

---

## What was sent that this repository should know about

**All four technical letters lead with the corrected central claim** — we detected tunnelling, we
could not hold the range — and all four link the public page. **That is consistent with
`deliverables/2026-09-19-pause/FRAMING.md`**, and it was checked rather than assumed.

**One figure in the Lu/Nam letter is now superseded**: it says *"about seven possible
explanations for the drift"*. **Zahl's reply made it eight**, hours after it was sent. **Not worth
a correction email** — it was true when written and the number was never the point — but **do not
copy "seven" out of that letter into anything new.**


---

## The 2026-09-22 materials ruling, and why it outranks a test

**Second reply from the Brookhaven adviser, 2026-09-22.** Recorded here because it is advice rather
than a measurement; **the consequences are in `docs/NEXT_SESSION_PLAN.md` and
`docs/OPEN_QUESTIONS.md`.** Paraphrased, not quoted.

**He was not ranking our candidates. He was ruling out materials.**

| | |
|---|---|
| **What he will not have in the mechanical loop** | **No plastics of any kind** — he named PTFE and PLA. **No rubber of any kind. No paper**, which he said will *go crazy* with changing humidity. **Squishy materials flow under pressure essentially forever** and keep changing dimensions at this scale |
| **What he will have** | **Metals** — steel, stainless, aluminium, copper, brass (brass fine outside vacuum). **Aluminium has a fairly high expansion coefficient**, so keep that in mind. For insulation: **ceramics, alumina, glass, sapphire, rock such as granite; quartz or mica sheets** |
| **On the coarse drive** | A steel micrometer drive is fine **provided every thread and screw in the path is steel or brass**, and **provided it is spring pre-loaded to eliminate backlash**. **Use steel balls for any pivot point** |
| **THE DESIGN PRINCIPLE, and it is the part we could actually act on cheaply** | **Make the loop SYMMETRIC and thermal expansion cancels.** In XY this is easy, and with the tip and sample dead centre a symmetric frame has **zero XY thermal drift**. In Z what remains is only the *difference* between the frame material, the piezo ceramic, the effective tip-wire length and the sample thickness |
| **Scope** | **All of this applies only to the mechanical loop** — everything supporting the tip-wire mounting point through to the sample. Outside that loop he did not care |
| **His sketch, in words** | A rigid low-expansion frame (**Inconel, steel, ceramic or glass**) standing on a solid base, sample **clipped or screwed down onto a rigid flat surface**, the scan piezo above it, the whole head with **decent mass**, then soft vibration isolation, then a very heavy table, floor or rock base |

### Why this is not just another candidate

**Three of our loop's materials are on his no list, and they are the three we were planning to
TEST rather than remove:** the **printed PETG-CF plates**, the **rubber bands** that retain the
sample plate, and the **backing paper** under the gold. **`STATUS.md` carries the first two as
drift candidates 2 and 3 and the paper as candidate 1.**

**He is saying the test is not worth running, because the answer is known.** That is a genuine
disagreement with our plan, and it is worth stating plainly rather than quietly adopting:

- **For the plan, it changes the order, not the physics.** The box test and the three-amplitude
  sweep still cost nothing and still run — **they are how we learn how much each one contributed**,
  which he has no way to know for our build.
- **But it promotes a rebuild of the sample mounting from "maybe" to "the known fix"**, and it
  makes the paper the cheapest thing to remove rather than the third thing to test.
- **And the humidity mechanism is new to this project.** Nothing here had considered that paper
  tracks room humidity. It is slow, it reverses, and it would not show up in a box test that only
  controls temperature — which means **a box test that comes back clean does not clear the paper.**
