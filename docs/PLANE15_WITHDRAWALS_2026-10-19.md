# Plane 15 Withdrawals — 2026-10-19

**Scope:** Withdrawal of the `L8` allocation, plus the `FE7xx` `Gerudo` /
`Gerudo Presentation Forms` entries, from RNUR Plane 15 (SPUA-A), following the current
public SPUCE Plane 15 Roadmap.

---

## 1. Background

The RNUR Set 1 yellow zone (`FE000–FEFFF`, *SPUCE Project Allocations — Reserved for
@erictom333 & SPUCE Admin*) charted four named allocations in the `FE7xx` row:

| Script | Range | Size |
| --- | --- | --- |
| Hylian | `U+FE700–U+FE77F` | 128 |
| Gerudo | `U+FE780–U+FE79F` | 32 |
| Gerudo Presentation Forms | `U+FE7A0–U+FE7DF` | 64 |
| L8 | `U+FE7E0–U+FE7FF` | 32 |

The current public SPUCE Plane 15 Roadmap renders the `0xFE7xx` row as `Hylian`
(`colspan=8`) followed by eight blank yellow columns — i.e. `U+FE780–U+FE7FF` is unnamed
erictom333-reserved space. `L8` was withdrawn by its creator and is no longer part of
Plane 15; the `FE7xx` `Gerudo` / `Gerudo Presentation Forms` entries no longer appear in
that row either.

The unrelated `0xFEDxx` entries *Script Gerudo* (`FED80–FEDAF`) and *Script Gerudo
Presentation Forms* (`FEDB0–FEDFF`) are a different set and are **kept**.

---

## 2. Change

| File | Change |
| --- | --- |
| `UNIDATA/S1/Blocks.txt` | Removed `FE780..FE79F; Gerudo`, `FE7A0..FE7DF; Gerudo Presentation Forms`, and `FE7E0..FE7FF; L8`; added `FE780..FE7FF; Layout Sandbox Space (erictom333 Reserved)`. |
| `S1/Roadmap/spua-a_roadmap.md` | `FE7xx` row is now `🟨 Hylian (FE700–FE77F)` + `🟨 Layout Sandbox Space (FE780–FE7FF)` (8 + 8 columns). |
| `tests/test_migration.py` | Added `test_withdrawn_plane15_allocations_removed` to lock the withdrawal in. |

Nothing changed for `Hylian` (`U+FE700–U+FE77F`) or the `FEDxx` Gerudo entries. The freed
range reverts to the zone default, `Layout Sandbox Space (erictom333 Reserved)`, matching
how the repository already renders unnamed erictom333-reserved space elsewhere
(`FE000–FE3FF`, `FE800–FECFF`, `FEF90–FEFFF`).

---

## 3. Validation results

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

### `py -m unittest discover -s tests`

```
Ran 41 tests in 1.967s

OK
```
