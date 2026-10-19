# Plane 15 Status Reconciliation — 2026-10-19

**Branch:** `plane15-status-reconciliation-2026-10-19`
**Scope:** RNUR Plane 15 (SPUA-A) records for Hacm, Liparxe, Shaleian, Visible Speech
Extended-I, Zbalermorna, Quikscript, Sitelen Pona Extended-A, and Sitelen Pona Extended-B,
reconciled against current evidence (UCSUR reserved ranges, UCSUR roadmap markers, Fairfax HD
coverage, SPUCE Plane 15 Roadmap, GS Unicode 3.0 Plane F map).

---

## 1. Files changed

| File | +/- | Summary |
| --- | --- | --- |
| `UNIDATA/S1/Blocks.txt` | +12 / −4 | Moved `Hacm`, `Liparxe`, `Shaleian` out of the UCSUR/unconfirmed sections into the SPUCE (🟥) section; renamed `Visible Speech Extended` → `Visible Speech Extended-I` in the SPUCE section; added a reconciliation provenance comment; `Zbalermorna` stays UCSUR-only (🟩); unconfirmed (⬛) section now contains only `¿Sitelen Pona Extended-A?`, `¿Sitelen Pona Extended-B?`, `¿Quikscript?`. |
| `S1/Roadmap/spua-a_roadmap.md` | +6 / −4 | F27xx cell → `🟥 Hacm (F2700–F27FF)` (was `⬛ ¿Hacm?`); F28xx cells → `🟥 Liparxe (F2800–F282F)` / `🟥 Shaleian (F2830–F289F)` (both were 🟩), `🟩 Zbalermorna (F28A0–F28DF)` unchanged; F29xx cell → `🟥 Visible Speech Extended-I (F2900–F295F)`; added a Plane 15 status reconciliation note. |
| `core/SPECIFICATION.md` | +5 / −1 | §3.2 SPUA-A Hints/Specials sector corrected from `U+FFF00–U+FFFFF` to `U+FFFF0–U+FFFFF` (separating the provisional `U+FFF00–U+FFFBF` slot and `U+FFFC0–U+FFFEF` Fragments allocation); added a Fragments provenance note and a detailed Plane 15 status reconciliation note documenting evidence and the `Visible Speech Extended` → `Visible Speech Extended-I` aliasing. |
| `data/set1_master.csv` | +4 / −0 | Added 4 `SPUCE Allocation` rows: Hacm `U+F2700–U+F27FF`, Liparxe `U+F2800–U+F282F`, Shaleian `U+F2830–U+F289F`, Visible Speech Extended-I `U+F2900–U+F295F` (each description records the UCSUR-reserved-but-not-named evidence and Fairfax HD coverage/planned status). |
| `tests/test_migration.py` | +73 / −12 | Rewrote `Plane15October2026Tests`: asserts reconciled block ranges/colors, section ownership (four in SPUCE section, Zbalermorna in 🟩, three in ⬛), roadmap cells, CSV rows (status `SPUCE Allocation`, flags `SPUCE`, no short-alias row), spec notes (§3.2 correction, provenance, reconciliation note), and Fragments/provisional sizes (48/192). |

---

## 2. Per-script reconciliation

| Script | Range | Status | Prior state |
| --- | --- | --- | --- |
| Hacm | `U+F2700–U+F27FF` (256) | 🟥 SPUCE allocation | ⬛ unconfirmed (`¿Hacm?`) → 🟥 |
| Liparxe | `U+F2800–U+F282F` (48) | 🟥 SPUCE allocation | 🟩 UCSUR-only → 🟥 |
| Shaleian | `U+F2830–U+F289F` (112) | 🟥 SPUCE allocation | 🟩 UCSUR-only → 🟥 |
| Visible Speech Extended-I | `U+F2900–U+F295F` (96) | 🟥 SPUCE allocation | 🟥 remains red; renamed from `Visible Speech Extended` (now recorded as alias) |
| Zbalermorna | `U+F28A0–U+F28DF` (64) | 🟩 UCSUR-only | unchanged (named UCSUR proposal) |
| Quikscript | `U+F2680–U+F26AF` (48) | ⬛ unconfirmed (`¿Quikscript?`) | unchanged |
| Sitelen Pona Extended-A | `U+F1A00–U+F1AFF` (256) | ⬛ unconfirmed (`¿Sitelen Pona Extended-A?`) | unchanged |
| Sitelen Pona Extended-B | `U+F1F00–U+F1FFF` (256) | ⬛ unconfirmed (`¿Sitelen Pona Extended-B?`) | unchanged |

### Evidence per script

- **Hacm (F2700–F27FF):** UCSUR reserves the range, but the UCSUR allocation table does not
  list Hacm as a proposal or registration and the UCSUR roadmap still marks it `¿Hacm?`.
  Fairfax HD provides complete glyph coverage. The SPUCE Plane 15 Roadmap names and allocates
  `Hacm (F2700–F27FF)`. → SPUCE allocation (🟥), moved from the unconfirmed (⬛) section.
- **Liparxe (F2800–F282F):** UCSUR reserves the range but its allocation table does not name
  the script and its roadmap still marks it `¿Liparxe?`; Fairfax HD coverage is complete; the
  SPUCE Plane 15 Roadmap names `Liparxe (F2800–F282F)`. → SPUCE allocation (🟥), moved from
  UCSUR-only (🟩).
- **Shaleian (F2830–F289F):** Same evidence pattern as Liparxe — UCSUR reserves without
  naming (`¿Shaleian?` in the UCSUR roadmap), Fairfax HD complete, SPUCE Plane 15 Roadmap
  names `Shaleian (F2830–F289F)`. → SPUCE allocation (🟥), moved from UCSUR-only (🟩).
- **Visible Speech Extended-I (F2900–F295F):** UCSUR reserves the range but still marks it
  `¿Visible Speech Extended?`; Fairfax HD lists `Visible Speech Extended` as *planned* (not
  complete); the SPUCE Plane 15 Roadmap names the F2900–F295F allocation; the GS Unicode 3.0
  Plane F map uses the shorter alias `Visible Speech Extended`. RNUR preserves the exact name
  `Visible Speech Extended-I` per SPUCE/task. Remains a SPUCE allocation (🟥); renamed only.
- **Zbalermorna (F28A0–F28DF):** Named UCSUR proposal with a reserved range. Remains
  UCSUR-only (🟩); unchanged throughout.
- **Quikscript (F2680–F26AF):** Fairfax HD has complete coverage, but there is no UCSUR
  proposal/registration and no SPUCE Plane 15 Roadmap allocation; the UCSUR roadmap does not
  name it. Remains unconfirmed (⬛) with the question-marked name.
- **Sitelen Pona Extended-A (F1A00–F1AFF) / Sitelen Pona Extended-B (F1F00–F1FFF):** No UCSUR
  proposal, no SPUCE allocation, no Fairfax HD evidence changing their standing. Remain
  unconfirmed (⬛) with question-marked names, exactly as specified.

### Classification rationale

Observed font usage (Fairfax HD coverage) is treated as **evidence**, not as formal UCSUR
confirmation. UCSUR reserves the four ranges but does not list the scripts as proposals or
registrations, and its roadmap still marks them proposed (`¿...?`). The SPUCE Plane 15
Roadmap names and allocates all four ranges. Therefore Hacm, Liparxe, Shaleian, and Visible
Speech Extended-I are recorded as SPUCE allocations (🟥), not formal UCSUR confirmations (🟩).

---

## 3. Fragments and provisional slot

| Item | Range | Size |
| --- | --- | --- |
| Fragments (Zone 12, SPUCE reduction) | `U+FFFC0–U+FFFEF` | 48 code points |
| Provisional RNUR open slot (released range) | `U+FFF00–U+FFFBF` | 192 code points (`PROVISIONAL_RNUR_OPEN_SLOT`, charted `???`) |
| SPUA-A Hints/Specials empty-character sector (§3.2, corrected) | `U+FFFF0–U+FFFFF` | 16 code points |

---

## 4. Unresolved discrepancies

1. **UCSUR roadmap/allocation table:** still marks Hacm, Liparxe, Shaleian, and Visible Speech
   Extended as reserved/proposed (`¿...?`) rather than registered/named. RNUR records them as
   SPUCE allocations on the strength of the SPUCE Plane 15 Roadmap + Fairfax HD evidence.
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
5. **Quikscript:** complete coverage in Fairfax HD, but remains unconfirmed (⬛) because there
   is no UCSUR proposal and no SPUCE allocation.
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
test_blocks_sections_reflect_ownership (test_migration.Plane15October2026Tests.test_blocks_sections_reflect_ownership) ... ok
test_csv_tracks_reconciled_allocations (test_migration.Plane15October2026Tests.test_csv_tracks_reconciled_allocations) ... ok
test_csv_tracks_released_range (test_migration.Plane15October2026Tests.test_csv_tracks_released_range) ... ok
test_fragments_allocation_reduced (test_migration.Plane15October2026Tests.test_fragments_allocation_reduced) ... ok
test_released_range_is_provisional_open_slot (test_migration.Plane15October2026Tests.test_released_range_is_provisional_open_slot) ... ok
test_roadmap_cells_use_reconciled_colors (test_migration.Plane15October2026Tests.test_roadmap_cells_use_reconciled_colors) ... ok
test_spec_documents_reconciliation (test_migration.Plane15October2026Tests.test_spec_documents_reconciliation) ... ok
test_spuce_plane15_scripts_are_reconciled (test_migration.Plane15October2026Tests.test_spuce_plane15_scripts_are_reconciled) ... ok
test_constantscript_unchanged (test_migration.RegistryDataTests.test_constantscript_unchanged) ... ok
test_former_provisional_reservations_removed (test_migration.RegistryDataTests.test_former_provisional_reservations_removed) ... ok
test_named_placeholder_allocation_preserved (test_migration.RegistryDataTests.test_named_placeholder_allocation_preserved) ... ok
test_no_provisional_record_migrated_to_set2 (test_migration.RegistryDataTests.test_no_provisional_record_migrated_to_set2) ... ok
test_no_stale_set1_record_for_displaced_scripts (test_migration.RegistryDataTests.test_no_stale_set1_record_for_displaced_scripts) ... ok
test_set1_contains_the_nine_spuce_allocations (test_migration.RegistryDataTests.test_set1_contains_the_nine_spuce_allocations) ... ok
test_set2_open_sandbox_begins_after_relocations (test_migration.RegistryDataTests.test_set2_open_sandbox_begins_after_relocations) ... ok
test_set2_relocations_exact (test_migration.RegistryDataTests.test_set2_relocations_exact) ... ok

----------------------------------------------------------------------
Ran 40 tests in 2.062s

OK
```

---

## 6. Diff summary

`git diff --stat` (5 tracked files; this report is a new untracked file):

```
 S1/Roadmap/spua-a_roadmap.md | 10 +++---
 UNIDATA/S1/Blocks.txt        | 16 ++++++---
 core/SPECIFICATION.md        |  6 +++-
 data/set1_master.csv         |  4 +++
 tests/test_migration.py      | 85 +++++++++++++++++++++++++++++++++++++-------
 5 files changed, 100 insertions(+), 21 deletions(-)
```

Per-file insertions/deletions (`git diff --numstat`):

```
6	4	S1/Roadmap/spua-a_roadmap.md
12	4	UNIDATA/S1/Blocks.txt
5	1	core/SPECIFICATION.md
4	0	data/set1_master.csv
73	12	tests/test_migration.py
```

Concise per-file summary:

- **`UNIDATA/S1/Blocks.txt`** — section moves + rename + provenance comment; no range values
  changed for any script.
- **`S1/Roadmap/spua-a_roadmap.md`** — three cell color changes, one question-mark removal
  (Hacm), one rename (VSE-I), one added note.
- **`core/SPECIFICATION.md`** — one corrected range in §3.2 plus two added notes in §3.5.5.
- **`data/set1_master.csv`** — 4 appended rows, nothing else touched.
- **`tests/test_migration.py`** — `Plane15October2026Tests` rewritten (8 tests, up from 5) to
  lock in the reconciled state.
