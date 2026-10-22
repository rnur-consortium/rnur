# Placeholder Relocation to Set 2 — 2026-10-22

**Baseline:** `09f0198` (state before this relocation) · **Scope:** the named RNUR `Placeholder`
allocation, relocated out of RNUR Set 1 (`U+F5C0–U+F71F`) into RNUR Set 2 (`U+E9A0–U+EAFF`)
under the SPUCE allocation update of 2026-10-22, together with the reclassification of the
vacated Set 1 interval into three contiguous ranges.

> **Summary.** The `Placeholder` allocation keeps its size (352 code points) and its repertoire;
> only its home layer changes. The Set 2 destination begins immediately after Foldian
> (`U+E960–U+E99F`), which is unchanged. The vacated Set 1 range is not left empty: it is
> subdivided into `U+F5C0–U+F5FF` (`???`), `U+F600–U+F6FF` (SPUCE allocation
> *Miscellaneous Symbols Extended-I*), and `U+F700–U+F71F` (`???`). The three ranges are
> contiguous, non-overlapping, and cover `U+F5C0–U+F71F` exactly.

---

## 1. The relocation

| Item | Set 1 (before) | Set 2 (after) | Size |
| --- | --- | --- | ---: |
| `Placeholder` | `U+F5C0–U+F71F` | `U+E9A0–U+EAFF` | 352 |

* The destination is contiguous with the six migration destinations and does not overlap any
  other Set 2 record: Set 2 BMP allocations now cover `U+E000–U+E81F` (ConstantScript),
  `U+E820–U+E99F` (the six relocated scripts) and `U+E9A0–U+EAFF` (Placeholder).
* Foldian (`U+E960–U+E99F`) is unchanged; the new allocation starts at `U+E9A0`, the very next
  address.
* The open Set 2 sandbox space resumes at `U+EB00–U+F8FF` (the address immediately after
  `U+EAFF`).

## 2. The vacated Set 1 interval

| Range | Size | Representation |
| --- | ---: | --- |
| `U+F5C0–U+F5FF` | 64 | `???` — `PROVISIONAL_RNUR_OPEN_SLOT`, status `Provisional Allocation / Open for Submission` |
| `U+F600–U+F6FF` | 256 | SPUCE allocation — *Miscellaneous Symbols Extended-I* (Author `SPUCE`, Status `SPUCE Allocation`, Flags `SPUCE`) |
| `U+F700–U+F71F` | 32 | `???` — `PROVISIONAL_RNUR_OPEN_SLOT`, status `Provisional Allocation / Open for Submission` |

* The two `???` ranges use RNUR's established provisional convention exactly. They carry no
  invented name, no `Placeholder` name/status, and no `Placeholder` description; the only
  provenance they record is that the range was vacated by the 2026-10-22 SPUCE allocation
  update.
* `Miscellaneous Symbols Extended-I` is recorded the way every other SPUCE allocation is
  recorded in this repository: Author `SPUCE`, Status `SPUCE Allocation`, Flags `SPUCE`, and a
  description prefixed `SPUCE Allocation:`. SPUCE supplies the definition; RNUR represents it
  inside its own Set 1 layer.
* Both `???` ranges are Tier B (provisional) under the §3.5.3.2 classification, and are
  rendered with the `???` marker in the Set 1 BMP roadmap grid.

## 3. Files changed

| File | +/- | Summary |
| --- | --- | --- |
| `data/set1_master.csv` | +3 / −1 | The `Placeholder` row is replaced by three rows: `U+F5C0–U+F5FF` and `U+F700–U+F71F` (`PROVISIONAL_RNUR_OPEN_SLOT` / `Provisional Allocation / Open for Submission`) and `U+F600–U+F6FF` (`Miscellaneous Symbols Extended-I` / `SPUCE` / `SPUCE Allocation` / flags `SPUCE`). |
| `data/set2_sandbox.csv` | +2 / −1 | New `Placeholder` row at `U+E9A0–U+EAFF`; the `OPEN_SANDBOX` row is split so that open space runs `U+EB00–U+F8FF` (it previously covered `U+E9A0–U+F8FF`). |
| `UNIDATA/S1/Blocks.txt` | +13 / −2 | `F5C0..F71F; Placeholder` removed (with an explanatory note); `F600..F6FF; Miscellaneous Symbols Extended-I` added to the SPUCE (🟥) section after `F4F0..F5BF`; `F5C0..F5FF` and `F700..F71F` added as `PROVISIONAL_RNUR_OPEN_SLOT` in the provisional section. |
| `UNIDATA/S2/Blocks.txt` | +9 / −2 | `E9A0..EAFF; Placeholder` added; `E9A0..F8FF; OPEN_SLOT` re-anchored to `EB00..F8FF; OPEN_SLOT`. |
| `UNIDATA/S1/UnicodeData.txt` | +2 / −359 | The 352 BMP `Placeholder` character entries (`U+F5C0–U+F71F`) removed; the separate SPUCE Plane 15 `Placeholder` allocation (`U+F92C0–U+F941F`) is untouched. |
| `UNIDATA/S1/NamesList.txt` | +5 / −356 | As above, for the character names. |
| `UNIDATA/S1/CaseFolding.txt` | +1 / −30 | The 26 BMP `Placeholder` case-folding pairs removed. |
| `UNIDATA/S2/UnicodeData.txt` | +361 / −2 | The 352 `Placeholder` character entries (`U+E9A0–U+EAFF`, `Lo`) added. |
| `UNIDATA/S2/NamesList.txt` | +361 / −2 | The 352 `PLACEHOLDER-Exxx` names added. |
| `UNIDATA/S2/CaseFolding.txt` | +29 / −4 | The 26 case-folding pairs added, shifted with the repertoire (see §4). |
| `S1/Roadmap/bmp_pua_roadmap.md` | +28 / −7 | The `F5xx`/`F6xx`/`F7xx` grid cells re-rendered as `??? (F5C0-F5FF)`, `🟥 Miscellaneous Symbols Extended-I (F600-F6FF)`, `??? (F700-F71F)`; the `F700–F71F` cell's `colspan` corrected from 3 to 2 (and the following cell from 13 to 14) so the grid geometry matches the labelled ranges; legend note, appendix §2/§3.1 updated; new §3.2 documenting the update. |
| `S2/Roadmap/bmp_pua_roadmap.md` | +15 / −3 | The `E9xx`/`EAxx` cells re-rendered as `🟧 Placeholder (E9A0-E9FF)` and `🟧 Placeholder (EA00-EAFF)`; notes updated and a new "SPUCE Allocation Update Notes — 2026-10-22" section added. |
| `core/SPECIFICATION.md` | +36 / −10 | New §3.1.3 *Placeholder Relocated to Set 2 (SPUCE Allocation Update, 2026-10-22)*; the former §3.1.3/§3.1.4 renumbered to §3.1.4/§3.1.5 with all cross-references updated; §3.4 and §3.5.3.2 Tier B updated; §3.5.4 cross-reference updated. |
| `tools/validator.py` | +127 / −13 | New constants (`PLACEHOLDER_SET2_RANGE`, `PLACEHOLDER_SET1_RANGE`, `PLACEHOLDER_SIZE`, `FOLDIAN_SET2_RANGE`, `FORMER_PLACEHOLDER_SUBDIVISION`); `TIER_B_BMP_PROVISIONAL_RANGES` extended with `(0xF5C0,0xF5FF)` and `(0xF700,0xF71F)`; the former "Placeholder must remain Set 1" check replaced by relocation, subdivision, block-map, roadmap and specification checks. |
| `tests/test_migration.py` | +233 / −11 | Relocation regression tests (see §6). |
| `README.md` | +7 / −4 | Validator description updated; the Set 2 example range changed from the now-occupied `U+E9A0–U+E9BF` to the open `U+EB00–U+EBFF`. |
| `.github/CONTRIBUTING.md` | +1 / −1 | The CI invariant list now names the relocation and the three-range subdivision. |
| `.github/ISSUE_TEMPLATE/bug_report.yml` | +1 / −1 | Example range changed from the now-occupied `U+E9A0` to `U+EB00`. |
| `docs/PLACEHOLDER_RELOCATION_2026-10-22.md` | new | This report. |

---

## 4. The repertoire moved with the allocation

The 352-character `Placeholder` repertoire moved intact from `U+F5C0–U+F71F` to `U+E9A0–U+EAFF`.
The shift is a constant `-0xC20` (`U+F5C0` = 62912 → `U+E9A0` = 59808), so the internal
structure is preserved exactly:

* All 352 entries are `Lo` and named `PLACEHOLDER-Exxx`.
* The case-folding block keeps its original shape: 26 uppercase letters at `U+E9A0–U+E9B9`
  folding to the 26 lowercase letters at `U+E9BA–U+E9D3` — a constant `+0x1A` offset, exactly
  as the original `U+F5C0–U+F5D9` → `U+F5DA–U+F5F3` pair.

> **Correction made during this pass.** An intermediate revision of the relocation regenerated
> the case-folding block as 58 mappings with a `+0x3A` offset (`U+E9A0–U+E9D9` →
> `U+E9DA–U+EA13`), which both enlarged the case-pair portion of the repertoire (52 → 116 code
> points) and contradicted its own header comment. A relocation must move the repertoire, not
> restructure it, so the block was regenerated as the faithful `+0x1A` translation and a
> regression test (`test_case_folding_shifts_with_the_repertoire`) now pins the shape.

---

## 5. Governance

SPUCE does not use RNUR's Set 1 / Set 2 architecture. SPUCE supplied the allocation definition
that now occupies `U+F600–U+F6FF`; RNUR defines how that definition is represented within its
own Set 1 layer, and how the displaced RNUR allocation was relocated into RNUR Set 2. No
artifact describes SPUCE as using RNUR's sets.

The `Placeholder` relocation is a named-allocation move, **not** a dissolution of a `???`
reservation: the two `???` ranges it leaves behind (`U+F5C0–U+F5FF` and `U+F700–U+F71F`) remain
provisional RNUR territory in Set 1, subject to the Tier B relocation routing described in
§3.5.3.2.

---

## 6. Validation results

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

62 tests, all passing (45 before this change; 17 added).

New coverage added by this pass:

* `RegistryDataTests.test_named_placeholder_allocation_relocated_to_set2` — the allocation is in
  Set 2 at `U+E9A0–U+EAFF` and no longer in Set 1.
* `RegistryDataTests.test_set1_vacated_range_is_subdivided_into_three_ranges` — the three
  ranges exist, cover `U+F5C0–U+F71F` exactly, and are contiguous.
* `RegistryDataTests.test_set1_provisional_subdivision_uses_established_convention` — the two
  `???` ranges use the established name/status and carry no `Placeholder` residue.
* `RegistryDataTests.test_set1_spuce_subdivision_uses_spuce_representation` — the middle range
  uses Author `SPUCE` / Status `SPUCE Allocation` / Flags `SPUCE`.
* `RegistryDataTests.test_placeholder_relocation_preserves_size_and_contiguity` — 352 code
  points, destination immediately after Foldian, Foldian itself unchanged.
* `RegistryDataTests.test_placeholder_relocation_does_not_overwrite_set2` — no Set 2 record
  overlaps the new allocation.
* `ArtifactConsistencyTests.test_roadmaps_and_spec_track_the_placeholder_relocation` — the grid
  cells and specification ranges agree.
* `UnidataMirrorTests.*` — the S2 mirrors hold exactly 352 contiguous entries, the S1 mirrors
  hold no BMP `Placeholder` entry (the Plane 15 SPUCE one survives), and the case-folding block
  keeps its original shape.
* `RoadmapGridGeometryTests.test_bmp_grid_cells_match_their_spans` — every cell in both BMP
  grids spans exactly the range it is labelled with, and every row totals the full 16 columns.
* `NegativeDetectionTests.*` — six new mutants, each confirmed to fail the validator for the
  intended reason: removing the Set 2 `Placeholder` row, re-adding it to Set 1, renaming it,
  resizing it, dropping one subdivision range, leaving `Placeholder` text in a `???`
  description, and un-marking the SPUCE subdivision range.

---

## 7. Assumptions and notes

1. **The subdivision boundaries are as specified** by the SPUCE allocation update: `U+F5C0–U+F5FF`
   and `U+F700–U+F71F` are `???`, `U+F600–U+F6FF` is *Miscellaneous Symbols Extended-I*. Only
   the three ranges and their order were given; the sizes (64 / 256 / 32) follow from them.
2. **The Set 2 destination was derived** from the requirement that it begin immediately after
   Foldian (`U+E960–U+E99F`), giving `U+E9A0–U+EAFF` for 352 code points.
3. **The open Set 2 sandbox split point is `U+EB00`,** the first address after `U+EAFF`. An
   intermediate revision used `U+EAB0`, which is *before* `U+EAFF` and therefore overlapped the
   new allocation by 80 code points; that was caught by the validator's overlap check and
   corrected everywhere (CSV, `Blocks.txt`, roadmaps, specification, validator, tests).
4. **The Set 1 Plane 15 `Placeholder` allocation (`U+F92C0–U+F941F`) is a different allocation**
   and was left untouched. It is the SPUCE-staked mirror of the same cipher repertoire.
5. **`???` ranges carry no provenance metadata beyond the standard provisional description.**
   The two `???` rows record only that the range was vacated by the 2026-10-22 allocation
   update; they do not carry the `Placeholder` name, status, or description.
