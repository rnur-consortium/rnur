# Plane 15 Status Reconciliation — 2026-10-19

**Baseline:** `918af67` (state before this reconciliation) · **Supersedes:** PR #11
(`4681a79`, which charted the four as 🟥; see the revision note in §2)
**Scope:** RNUR Plane 15 (SPUA-A) records for Hacm, Liparxe, Shaleian, Visible Speech
Extended-I, Zbalermorna, Quikscript, Sitelen Pona Extended-A, and Sitelen Pona Extended-B,
reconciled against current evidence (UCSUR reserved ranges, UCSUR roadmap markers, Fairfax HD
coverage, SPUCE Plane 15 Roadmap, GS Unicode 3.0 Plane F map).

> **Revision 2 (2026-10-19, `¿...?` semantics correction):** The `¿Script Name?` marker was
> originally documented here as "unconfirmed by UCSUR". That reading was wrong: `¿Script
> Name?` denotes a **UCSUR-included script whose detailed proposal has not yet been
> written** — a proposal-completeness marker, not an inclusion statement. Accordingly
> `¿Sitelen Pona Extended-A?`, `¿Sitelen Pona Extended-B?`, and `¿Quikscript?` are charted in
> the UCSUR-Only (🟩) class and the black-square "Unconfirmed by UCSUR" class is retired. The
> `???` Provisional RNUR Open Slot keeps its separate meaning. No code-point range changed.
> §2, §4, and §5 below reflect the correction; §1 and §6 keep the original reconciliation-pass
> figures.

> **Revision 3 (2026-10-19):** `¿Hacm?`, `¿Liparxe?`, `¿Shaleian?`, and `¿Visible Speech
> Extended-I?` now also carry the `¿...?` proposal-completeness marker — they too are
> UCSUR-included with no detailed proposal yet. All seven Plane 15 scripts without a detailed
> proposal (those four plus `¿Sitelen Pona Extended-A?`, `¿Sitelen Pona Extended-B?`, and
> `¿Quikscript?`) are charted in the UCSUR-Only (🟩) class; `Zbalermorna`, a named UCSUR
> proposal, keeps the unmarked name. No code-point range changed.

---

## 1. Files changed

Diffs below are relative to the pre-reconciliation baseline `918af67` (the commit before this
reconciliation began).

| File | +/- | Summary |
| --- | --- | --- |
| `UNIDATA/S1/Blocks.txt` | +9 / −2 | `Hacm`, `Liparxe`, `Shaleian` moved into the UCSUR-Only (🟩) section (Hacm out of the former unconfirmed ⬛ section; Liparxe/Shaleian already green, now annotated); `Visible Speech Extended` → `Visible Speech Extended-I` moved from SPUCE (🟥) into UCSUR-Only (🟩); added the section-header comment defining "UCSUR-Only = allocated in UCSUR rather than CSUR"; `Zbalermorna` unchanged (🟩); `¿Sitelen Pona Extended-A?`, `¿Sitelen Pona Extended-B?`, and `¿Quikscript?` charted in the UCSUR-Only (🟩) class with the `¿...?` proposal-completeness marker (revision 2; the former ⬛ "Unconfirmed by UCSUR" class is retired). Revision 3 applies the same `¿...?` marker to `¿Hacm?`, `¿Liparxe?`, `¿Shaleian?`, and `¿Visible Speech Extended-I?`. |
| `S1/Roadmap/spua-a_roadmap.md` | +5 / −2 | F27xx/F28xx/F29xx cells → `🟩 ¿Hacm?` / `🟩 ¿Liparxe?` / `🟩 ¿Shaleian?` / `🟩 ¿Visible Speech Extended-I?` (revisions 2–3; VSE-I also renamed from the old red `Visible Speech Extended`); `🟩 Zbalermorna` untouched (no marker); legend defines the `¿...?` proposal-completeness marker and clarifies what "UCSUR-Only" means; added the Plane 15 status reconciliation note. |
| `core/SPECIFICATION.md` | +6 / −2 | §3.2 SPUA-A Hints/Specials sector corrected from `U+FFF00–U+FFFFF` to `U+FFFF0–U+FFFFF`; added the Fragments provenance note and the Plane 15 status reconciliation note (UCSUR origin, SPUCE naming recorded as provenance, `Visible Speech Extended` → `Visible Speech Extended-I` aliasing); §3.5.5 closing paragraph states why the four keep the UCSUR classification. |
| `data/set1_master.csv` | 0 / 0 | **Net unchanged vs baseline.** An intermediate pass briefly added 4 `SPUCE Allocation` rows; they were removed again because UCSUR-only allocations are not tracked in `set1_master.csv` (consistent with `Zbalermorna`, which has no row either). A test now asserts their absence. |
| `tests/test_migration.py` | +63 / −12 | Rewrote `Plane15October2026Tests` (5 → 8 tests): asserts the four ranges exist, question-mark markers are gone, section ownership (four + Zbalermorna + the three `¿...?` scripts in 🟩, none in the retired ⬛ class, none of the four in 🟥), green roadmap cells, **absence** of CSV rows for the UCSUR-only scripts, spec notes (§3.2 correction, UCSUR-origin wording), and Fragments/provisional sizes (48/192). Revision 2 adds regression tests for the corrected `¿...?` semantics. |
| `docs/PLANE15_RECONCILIATION_2026-10-19.md` | +221 | New: this report. |

---

## 2. Per-script reconciliation

| Script | Range | Status | Prior state |
| --- | --- | --- | --- |
| Hacm | `U+F2700–U+F27FF` (256) | 🟩 UCSUR-only; detailed proposal not yet written (`¿Hacm?`) | ⬛ unconfirmed → 🟩; `¿...?` marker added (revision 3) |
| Liparxe | `U+F2800–U+F282F` (48) | 🟩 UCSUR-only; detailed proposal not yet written (`¿Liparxe?`) | 🟩 UCSUR-only (kept); `¿...?` marker added (revision 3) |
| Shaleian | `U+F2830–U+F289F` (112) | 🟩 UCSUR-only; detailed proposal not yet written (`¿Shaleian?`) | 🟩 UCSUR-only (kept); `¿...?` marker added (revision 3) |
| Visible Speech Extended-I | `U+F2900–U+F295F` (96) | 🟩 UCSUR-only; detailed proposal not yet written (`¿Visible Speech Extended-I?`) | 🟥 `Visible Speech Extended` (red, old name) → 🟩 `Visible Speech Extended-I`; `¿...?` marker added (revision 3) |
| Zbalermorna | `U+F28A0–U+F28DF` (64) | 🟩 UCSUR-only | unchanged (named UCSUR proposal) |
| Quikscript | `U+F2680–U+F26AF` (48) | 🟩 UCSUR-only; detailed proposal not yet written (`¿Quikscript?`) | range unchanged; reclassified, ⬛ unconfirmed → 🟩 |
| Sitelen Pona Extended-A | `U+F1A00–U+F1AFF` (256) | 🟩 UCSUR-only; detailed proposal not yet written (`¿Sitelen Pona Extended-A?`) | range unchanged; reclassified, ⬛ unconfirmed → 🟩 |
| Sitelen Pona Extended-B | `U+F1F00–U+F1FFF` (256) | 🟩 UCSUR-only; detailed proposal not yet written (`¿Sitelen Pona Extended-B?`) | range unchanged; reclassified, ⬛ unconfirmed → 🟩 |

### Evidence per script

- **Hacm (F2700–F27FF):** UCSUR reserves the range, and the range originates in UCSUR, but
  the UCSUR allocation table does not list Hacm as a registration and the UCSUR roadmap still
  marks it `¿Hacm?`. Fairfax HD provides complete glyph coverage. The SPUCE Plane 15 Roadmap
  also names `Hacm (F2700–F27FF)` — recorded as provenance, not SPUCE ownership. → UCSUR-only
  (🟩), moved out of the former unconfirmed (⬛) section and written `¿Hacm?` (UCSUR-included;
  no detailed proposal yet).
- **Liparxe (F2800–F282F):** UCSUR reserves the range (UCSUR origin) but its allocation table
  does not name the script and its roadmap still marks it `¿Liparxe?`; Fairfax HD coverage is
  complete; the SPUCE Plane 15 Roadmap names `Liparxe (F2800–F282F)` as provenance. Stays
  UCSUR-only (🟩) and is written `¿Liparxe?` (UCSUR-included; no detailed proposal yet).
- **Shaleian (F2830–F289F):** Same evidence pattern as Liparxe — UCSUR reserves without
  naming (`¿Shaleian?` in the UCSUR roadmap), Fairfax HD complete, SPUCE Plane 15 Roadmap
  names `Shaleian (F2830–F289F)` as provenance. Stays UCSUR-only (🟩) and is written
  `¿Shaleian?` (UCSUR-included; no detailed proposal yet).
- **Visible Speech Extended-I (F2900–F295F):** UCSUR reserves the range (UCSUR origin) but
  still marks it `¿Visible Speech Extended?`; Fairfax HD lists `Visible Speech Extended` as
  *planned* (not complete); the SPUCE Plane 15 Roadmap names the F2900–F295F allocation as
  provenance; the GS Unicode 3.0 Plane F map uses the shorter alias `Visible Speech Extended`.
  RNUR preserves the exact name `Visible Speech Extended-I` per SPUCE/task. → UCSUR-only
  (🟩) with the `-I` rename and the `¿...?` marker (`¿Visible Speech Extended-I?`;
  UCSUR-included, no detailed proposal yet); this is the one classification change among the
  four besides Hacm (it was charted red under the short name).
- **Zbalermorna (F28A0–F28DF):** Named UCSUR proposal with a reserved range. Remains
  UCSUR-only (🟩); unchanged throughout.
- **Quikscript (F2680–F26AF):** Fairfax HD has complete coverage. The range is UCSUR-included,
  but no detailed proposal has yet been written for it and there is no SPUCE Plane 15 Roadmap
  allocation; it therefore carries the `¿Quikscript?` proposal-completeness marker and stays
  in the UCSUR-Only (🟩) class.
- **Sitelen Pona Extended-A (F1A00–F1AFF) / Sitelen Pona Extended-B (F1F00–F1FFF):** Both ranges
  are UCSUR-included, but no detailed proposal has yet been written for either, there is no
  SPUCE allocation, and no Fairfax HD evidence changes their standing. They carry the `¿...?`
  proposal-completeness marker and stay in the UCSUR-Only (🟩) class.

### Classification rationale

UCSUR reserves all four ranges and they **originate in UCSUR** — the ranges predate the SPUCE
Plane 15 Roadmap naming. In this repository the 🟩 bucket is labeled *UCSUR-Only Allocations*,
which means *allocated in UCSUR rather than CSUR*, not *never touched by SPUCE*: a range may be
named by SPUCE without leaving the UCSUR classification. Therefore `¿Hacm?`, `¿Liparxe?`,
`¿Shaleian?`, and `¿Visible Speech Extended-I?` are UCSUR-only allocations (🟩), while the SPUCE
Plane 15 Roadmap's
naming of the same four ranges is recorded as provenance (in `Blocks.txt`, the roadmap note,
and `core/SPECIFICATION.md` §3.5.5), not as SPUCE ownership. Observed font usage (Fairfax HD
coverage) is additionally treated as **evidence**, not as a formal UCSUR registration — the
green classification asserts allocation-level UCSUR origin, not a published UCSUR character
chart (see §4, items 1 and 6).

> **Revision note:** an earlier pass of this reconciliation (PR #11) charted the four as SPUCE
> allocations (🟥) on the reading that the current naming authority sets the color. That was
> superseded: because UCSUR had the ranges first and "UCSUR-Only" is defined against CSUR, the
> four are UCSUR-only (🟩) and the SPUCE naming is provenance. This report and the artifacts
> reflect the corrected classification.

---

## 3. Fragments and provisional slot

| Item | Range | Size |
| --- | --- | --- |
| Fragments (Zone 12, SPUCE reduction) | `U+FFFC0–U+FFFEF` | 48 code points |
| Provisional RNUR open slot (released range) | `U+FFF00–U+FFFBF` | 192 code points (`PROVISIONAL_RNUR_OPEN_SLOT`, charted `???`) |
| SPUA-A Hints/Specials empty-character sector (§3.2, corrected) | `U+FFFF0–U+FFFFF` | 16 code points |

---

## 4. Unresolved discrepancies

1. **UCSUR roadmap/allocation table:** marks Hacm, Liparxe, Shaleian, and Visible Speech
   Extended as reserved/proposed (`¿...?`), i.e. included but without a written detailed
   proposal. RNUR mirrors this by writing `¿Hacm?`, `¿Liparxe?`, `¿Shaleian?`, and
   `¿Visible Speech Extended-I?` and keeping them in the UCSUR-Only class, while the SPUCE
   Plane 15 Roadmap's matching names are recorded only as provenance.
2. **Fairfax HD name:** lists `Visible Speech Extended` as *planned* — no `-I` suffix and no
   complete coverage.
3. **GS Unicode 3.0 Plane F map:** uses `Visible Speech Extended` (no `-I`). RNUR preserves
   the exact name `Visible Speech Extended-I` per SPUCE/task; the shorter form is documented
   as an alias.
4. **Public SPUCE Plane 15 Roadmap / GS Unicode FFFxx:** the public SPUCE roadmap still showed
   the pre-reduction `FFF00–FFFEF Fragments` line, and the GS Unicode Plane F map listed
   `FFFxx` as unassigned, when this record was reconciled. The repo follows the
   maintainer-confirmed reduction to `FFFC0–FFFEF`; `FFF00–FFFBF` remains provisional RNUR
   space.
5. **Quikscript:** complete coverage in Fairfax HD; the range is UCSUR-included, but its
   detailed proposal has not yet been written (hence `¿Quikscript?`) and there is no SPUCE
   allocation.
6. **No formal UCSUR character charts/repertoires** were found for the four scripts — only
   allocation-level evidence (reserved ranges + roadmap markers) exists.
7. **§3.2 correction:** the SPUA-A Hints/Specials sector was previously written as
   `U+FFF00–U+FFFFF`; it is now `U+FFFF0–U+FFFFF`, separating the provisional slot
   (`U+FFF00–U+FFFBF`) and the Fragments allocation (`U+FFFC0–U+FFFEF`).

---

## 5. Validation results

### `py tools/validator.py`

```
=== RNUR Allocation Validator ===
No input coordinates provided. Shifting to global repository integrity check...

Executing comprehensive RNUR matrix validation scan...
Analyzing set1_master.csv for integrity...
[+] set1_master.csv internal verification complete.
Analyzing set2_sandbox.csv for integrity...
[+] set2_sandbox.csv internal verification complete.

[+] SUCCESS: Entire RNUR matrix verified cleanly with zero internal overlaps.
[+] SUCCESS: Set 1 -> Set 2 migration invariants all hold.
```

### `py -m unittest discover -s tests -v`

```
test_set2_destinations_contiguous_sized_and_ordered (test_migration.ArithmeticTests.test_set2_destinations_contiguous_sized_and_ordered) ... ok
test_spuce_ranges_cover_ee00_efff_exactly (test_migration.ArithmeticTests.test_spuce_ranges_cover_ee00_efff_exactly) ... ok
test_spuce_sizes_match_supplied_map (test_migration.ArithmeticTests.test_spuce_sizes_match_supplied_map) ... ok
test_full_invariant_check_passes_on_repository (test_migration.ArtifactConsistencyTests.test_full_invariant_check_passes_on_repository) ... ok
test_governance_distinction_is_explicit (test_migration.ArtifactConsistencyTests.test_governance_distinction_is_explicit)
SPUCE supplies the definitions; RNUR owns Set 1 / Set 2. ... ok
test_provisional_bmp_cells_carry_question_marks (test_migration.ArtifactConsistencyTests.test_provisional_bmp_cells_carry_question_marks)
Tier B BMP gaps must render as ??? cells, never bare ranges. ... ok
test_roadmaps_and_spec_match (test_migration.ArtifactConsistencyTests.test_roadmaps_and_spec_match) ... ok
test_set1_blocks_contains_the_spuce_map (test_migration.ArtifactConsistencyTests.test_set1_blocks_contains_the_spuce_map) ... ok
test_set2_blocks_contains_relocations (test_migration.ArtifactConsistencyTests.test_set2_blocks_contains_relocations) ... ok
test_tier_classification_of_bmp_provisional_gaps (test_migration.ArtifactConsistencyTests.test_tier_classification_of_bmp_provisional_gaps)
The BMP ??? gaps are Tier B (provisional), never Tier A. ... ok
test_check_overlap_boundaries (test_migration.HelperTests.test_check_overlap_boundaries) ... ok
test_inclusive_size (test_migration.HelperTests.test_inclusive_size) ... ok
test_detects_governance_violation (test_migration.NegativeDetectionTests.test_detects_governance_violation) ... ok
test_detects_moved_constantscript (test_migration.NegativeDetectionTests.test_detects_moved_constantscript) ... ok
test_detects_overlap_within_set (test_migration.NegativeDetectionTests.test_detects_overlap_within_set) ... ok
test_detects_provisional_cell_missing_question_marks (test_migration.NegativeDetectionTests.test_detects_provisional_cell_missing_question_marks) ... ok
test_detects_provisional_migrated_into_set2 (test_migration.NegativeDetectionTests.test_detects_provisional_migrated_into_set2) ... ok
test_detects_reintroduced_displaced_script (test_migration.NegativeDetectionTests.test_detects_reintroduced_displaced_script) ... ok
test_detects_reintroduced_provisional_reservation (test_migration.NegativeDetectionTests.test_detects_reintroduced_provisional_reservation) ... ok
test_detects_removed_placeholder (test_migration.NegativeDetectionTests.test_detects_removed_placeholder) ... ok
test_detects_spuce_gap (test_migration.NegativeDetectionTests.test_detects_spuce_gap) ... ok
test_detects_tier_a_claiming_provisional_gap (test_migration.NegativeDetectionTests.test_detects_tier_a_claiming_provisional_gap) ... ok
test_detects_wrong_relocation_destination (test_migration.NegativeDetectionTests.test_detects_wrong_relocation_destination) ... ok
test_invalid_inclusive_range_detected (test_migration.NegativeDetectionTests.test_invalid_inclusive_range_detected) ... ok
test_affected_scripts_are_not_marked_unconfirmed (test_migration.Plane15October2026Tests.test_affected_scripts_are_not_marked_unconfirmed) ... ok
test_blocks_sections_reflect_ownership (test_migration.Plane15October2026Tests.test_blocks_sections_reflect_ownership) ... ok
test_csv_does_not_track_ucsur_allocations (test_migration.Plane15October2026Tests.test_csv_does_not_track_ucsur_allocations) ... ok
test_csv_tracks_released_range (test_migration.Plane15October2026Tests.test_csv_tracks_released_range) ... ok
test_fragments_allocation_reduced (test_migration.Plane15October2026Tests.test_fragments_allocation_reduced) ... ok
test_provisional_slot_notation_stays_distinct (test_migration.Plane15October2026Tests.test_provisional_slot_notation_stays_distinct) ... ok
test_question_mark_allocations_unchanged (test_migration.Plane15October2026Tests.test_question_mark_allocations_unchanged) ... ok
test_question_mark_notation_means_missing_detailed_proposal (test_migration.Plane15October2026Tests.test_question_mark_notation_means_missing_detailed_proposal) ... ok
test_released_range_is_provisional_open_slot (test_migration.Plane15October2026Tests.test_released_range_is_provisional_open_slot) ... ok
test_roadmap_cells_use_reconciled_colors (test_migration.Plane15October2026Tests.test_roadmap_cells_use_reconciled_colors) ... ok
test_spec_documents_reconciliation (test_migration.Plane15October2026Tests.test_spec_documents_reconciliation) ... ok
test_ucsur_origin_scripts_are_reconciled (test_migration.Plane15October2026Tests.test_ucsur_origin_scripts_are_reconciled) ... ok
test_constantscript_unchanged (test_migration.RegistryDataTests.test_constantscript_unchanged) ... ok
test_former_provisional_reservations_removed (test_migration.RegistryDataTests.test_former_provisional_reservations_removed) ... ok
test_named_placeholder_allocation_preserved (test_migration.RegistryDataTests.test_named_placeholder_allocation_preserved) ... ok
test_no_provisional_record_migrated_to_set2 (test_migration.RegistryDataTests.test_no_provisional_record_migrated_to_set2) ... ok
test_no_stale_set1_record_for_displaced_scripts (test_migration.RegistryDataTests.test_no_stale_set1_record_for_displaced_scripts) ... ok
test_set1_contains_the_nine_spuce_allocations (test_migration.RegistryDataTests.test_set1_contains_the_nine_spuce_allocations) ... ok
test_set2_open_sandbox_begins_after_relocations (test_migration.RegistryDataTests.test_set2_open_sandbox_begins_after_relocations) ... ok
test_set2_relocations_exact (test_migration.RegistryDataTests.test_set2_relocations_exact) ... ok

----------------------------------------------------------------------
Ran 45 tests in 1.941s

OK
```

---

## 6. Diff summary

`git diff 918af67 --stat` at the time of the original reconciliation pass (this report
included; `data/set1_master.csv` does not appear because it is back to its baseline content).
The figures below predate revision 2 and the separate L8-withdrawal pass
(`docs/PLANE15_WITHDRAWALS_2026-10-19.md`):

```
 S1/Roadmap/spua-a_roadmap.md              |   7 +-
 UNIDATA/S1/Blocks.txt                     |  11 +-
 core/SPECIFICATION.md                     |   8 +-
 docs/PLANE15_RECONCILIATION_2026-10-19.md | 232 ++++++++++++++++++++++++++++++
 tests/test_migration.py                   |  75 ++++++++--
 5 files changed, 315 insertions(+), 18 deletions(-)
```

Per-file insertions/deletions (`git diff 918af67 --numstat`):

```
5	2	S1/Roadmap/spua-a_roadmap.md
9	2	UNIDATA/S1/Blocks.txt
6	2	core/SPECIFICATION.md
232	0	docs/PLANE15_RECONCILIATION_2026-10-19.md
63	12	tests/test_migration.py
```

Working tree vs `HEAD` (`4681a79`, the PR #11 state) additionally shows
`data/set1_master.csv | 4 ---` — the removal of the four `SPUCE Allocation` rows added by
PR #11, restoring the file to its baseline content.

Concise per-file summary (vs baseline):

- **`UNIDATA/S1/Blocks.txt`** — Hacm/Liparxe/Shaleian annotated and grouped in the UCSUR-Only
  section, VSE renamed to `-I` and moved from 🟥 to 🟩, section-header comment added; all four
  written with the `¿...?` proposal-completeness marker (revision 3); no range value changed
  for any script.
- **`S1/Roadmap/spua-a_roadmap.md`** — Hacm cell black→green; all four Plane 15 UCSUR cells
  written `🟩 ¿...?`; VSE-I cell red→green + rename; legend clarified (defines `¿...?`, retires
  ⬛); notes added.
- **`core/SPECIFICATION.md`** — §3.2 corrected range plus two added notes in §3.5.5.
- **`data/set1_master.csv`** — no net change (4 rows added and removed in the interim).
- **`tests/test_migration.py`** — `Plane15October2026Tests` rewritten (8 tests, up from 5) to
  lock in the UCSUR-only classification; a withdrawal test and four revision-2 regression tests
  bring the suite to 45 tests.
