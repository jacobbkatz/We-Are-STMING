# The Drive copies, and how they are typeset

**The twenty documents on Google Drive are the same words as the Markdown in this
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
