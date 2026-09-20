# The Drive copies, and how they are typeset

**The twenty-two documents on Google Drive are the same words as the Markdown in this
repository.** They were first uploaded as raw Markdown, so Google converted them with
its defaults: Arial 11 point, black, one size for the body and one for every heading.
They read as a working file rather than as a document, which is not the standard the
rest of the project is held to.

`md_to_doc.py` writes the same words out as HTML with the website's typography attached
to every element, and Drive's importer keeps that. **Nothing about the words changes.**

## Running it

```bash
python3 deliverables/2026-09-19-pause/drive/md_to_doc.py <source.md> <out.html>
```

Then the HTML replaces the existing document's content **in place**, through the Drive
API's update-with-media call. **The file keeps its ID, so every link already sent out
still works, and no document is ever deleted and recreated.**

## Which document is which

| Drive document | Source in this repository |
|---|---|
| What held us back | `deliverables/2026-09-19-pause/WHAT_HELD_US_BACK.md` |
| Findings report | `deliverables/2026-09-19-pause/report/FINDINGS_REPORT.md` |
| Every junction we made | `deliverables/2026-09-19-pause/JUNCTIONS.md` |
| Pause-point handoff | `deliverables/2026-09-19-pause/report/PAUSE_POINT_HANDOFF.md` |
| Lead verification log | `deliverables/2026-09-19-pause/LEAD_VERIFICATION.md` |
| Analysis findings | `deliverables/2026-09-19-pause/analysis/FINDINGS.md` |
| Candidate images: the verdict | `deliverables/2026-09-19-pause/candidates/VERDICT.md` |
| Candidate images: the gallery | `deliverables/2026-09-19-pause/candidates/GALLERY.md` |
| Comparison tables | `deliverables/2026-09-19-pause/analysis/COMPARISON_TABLES.md` |
| Data inventory | `deliverables/2026-09-19-pause/analysis/DATA_INVENTORY.md` |
| The manual | `deliverables/2026-09-19-pause/manual/MANUAL.md` |
| Manual changelog | `deliverables/2026-09-19-pause/manual/CHANGELOG.md` |
| Inconsistencies found in the sources | `deliverables/2026-09-19-pause/manual/INCONSISTENCIES.md` |
| Photograph inventory | `deliverables/2026-09-19-pause/photos/IMAGE_INVENTORY.md` |
| Mechanical observations | `deliverables/2026-09-19-pause/photos/MECHANICAL_OBSERVATIONS.md` |
| Prepared photographs | `deliverables/2026-09-19-pause/photos/prepared/MANIFEST.md` |
| The second instrument | `deliverables/2026-09-19-pause/AI_WORKFLOW_SECTION.md` |
| Framing | `deliverables/2026-09-19-pause/FRAMING.md` |
| Brief | `deliverables/2026-09-19-pause/BRIEF.md` |
| Source inventory | `deliverables/2026-09-19-pause/SOURCE_INVENTORY.md` |
| Poster speaker script | `deliverables/2026-09-19-pause/poster/SPEAKER_SCRIPT.md` |
| Poster questions and answers | `deliverables/2026-09-19-pause/poster/QUESTIONS_AND_ANSWERS.md` |

**The repository is the source of truth.** If a Drive document and its Markdown ever
disagree, the Markdown is right and the document should be regenerated.

---

## The document IDs, as the website links them

**Generated from `deliverables/2026-09-19-pause/site/index.html`, which is where these
IDs actually live.** They were nowhere else in the repository until 2026-09-20, so losing
that one file would have lost the link between every Drive document and its source. The
label is the one the website shows, which is written for a reader and does not always
match the document's own title in the table above.

| As the website labels it | Document ID |
|---|---|
| the speaker script | `1g7_9QSFmusXeYeFyfknpLyufYXengNEakGYpBflJYvU` |
| the questions people ask | `1RADFrvVwFRQhFxcq_QQwnunfPm4atYvDhER1L1WYR7I` |
| What held us back | `1F3eXgBQKr8mJWtThS5IoH4OlmaV9LGfvfSy5-M1vVe4` |
| Findings report | `1qhrhRTaiNG-ipN6KWmezRR0UpEnaSAgLl3umcreMntY` |
| Every junction we made | `17KdMFAEhQCOTMV48eSpyMQ5LGIGPwc1W20qr5lQx1b8` |
| Pause-point handoff | `1T4ND1r1AkhXNMTvWW0bGt4zpKmnDQLfelMxemoR_TKc` |
| Lead verification log | `1GUbiFGpMq6g_YXMyLzhdd32Z2ChWT5cxgH7X5rLwoFY` |
| Analysis findings | `1eDJqCq0xhErAtEXaP2sG0OPCLrrWgSGBpjPMeJdPF2k` |
| Candidate images: the verdict | `17e0XA07-JeSk42g4fEUKsSGThZGOhl2tP1XtTXSKPpM` |
| Candidate images: the gallery | `1PkK78eOPSs_p_QygSRqEcen648Mmbe6Irc1xHYbzLEk` |
| Comparison tables | `1EkLAORGx9ZNXIkVWhGOHiXAekBDHSyF3Q_SF1KsWzj8` |
| Data inventory | `143R8hr2mNDje94m6sEdpjWSc5ktEX_AVm99MK8me7dA` |
| The manual | `1gJDZQkIY1xSPuSHiAUP6WTUM_ELa_q2jJmkEc3dC7TU` |
| Manual changelog | `15hb8lbpqc87pWFhQA1sbkQnFMMkXW0KRrwwrhzWwevo` |
| Inconsistencies found in the sources | `14gKoQ2yQzVE9nVQTXkHe0KQR6nb_ijgG7d7nyJIwJVs` |
| Photograph inventory | `1e4nE7qrfxwUjMA4U1tedhIdnaDkwzsXRw1hMU3RcPeg` |
| Mechanical observations | `1TodlSzgqcvWdyIZyoNRBUuEZu7SOJNXVNmdmnHqffjU` |
| Prepared photographs | `1cTbNY6D2x_6u3xeoS1mPLRXQadgViYu3MDUDRbF3TPw` |
| The second instrument | `1je7xGS1Vnq1Zu8Z2vpbrX3-bAvGDopqaqqu41v6bKTc` |
| Framing | `1ZMKwWzdkKEcTh1nt1xEvFGgnXMTAW1Ld-5ybiZwCR7k` |
| Brief | `1sHkbQacs51TlU30P7pdWzIytpzeXmSATgOCioTBFYpk` |
| Source inventory | `1IImuZzscD-5Yqxi4yhTb1wg1C3Q4tTq2T8s81HPOxPc` |
