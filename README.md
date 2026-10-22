# Reddit Neographical Unicode Registry (RNUR)

RNUR stores Private Use Area allocation records in two CSV sheets:

- `data/set1_master.csv` — Set 1 allocations and reserved/open ranges.
- `data/set2_sandbox.csv` — Set 2 isolated allocations and open sandbox
  ranges.

An allocation is identified by `(Set_Number, Start_Code_Point,
End_Code_Point)`. The CSV records also contain a script/project name, owner,
status, description, and (for Set 1) flags. These files are registry data,
not a Unicode font, encoder, shaping engine, or allocation service.

## Validate the local sheets

Requirements: Python 3; only the standard library is used.

```powershell
py tools/validator.py
```

With no arguments, the validator scans both CSV files, parses the set and
hexadecimal ranges, and reports malformed rows and overlapping ranges within
the same set. It skips rows marked `Waiting for Submissions`,
`Provisional Allocation / Open for Submission`, or
`Permanent Allocation / Open for Submission`. It then verifies the
Set 1 → Set 2 migration invariants: the nine SPUCE-supplied allocations
represented in RNUR Set 1 covering
`U+EE00–U+EFFF` exactly, the six RNUR relocations into Set 2 starting at
`U+E820`, the unchanged ConstantScript block at `U+E000–U+E81F`, the removal of
the former `???` provisional reservations, the relocation of the `Placeholder`
allocation from Set 1 `U+F5C0–U+F71F` to Set 2 `U+E9A0–U+EAFF` and the
three-range subdivision of the vacated Set 1 interval, and agreement between the
CSVs, `UNIDATA/*/Blocks.txt`, the roadmaps, and `core/SPECIFICATION.md`.

To check a proposed range against one local set (use a range you believe is
still open, such as the RNUR embassy space):

```powershell
py tools/validator.py 1 U+F9060 U+F908F
py tools/validator.py 2 U+EB00 U+EBFF
```

The command accepts set 1 or 2, start, and end; it reports overlap but does
not reserve or write an allocation. It does not query upstream registries,
build fonts, or perform an eviction/migration.

## Migration regression tests

The repository ships regression tests for the SPUCE-supplied allocations
represented in RNUR Set 1, the six Set 2
relocations, the permanent-space handling of the former `???` ranges, and the
`Placeholder` relocation into Set 2:

```powershell
py -m unittest discover -s tests -v
```

## Status and limits

The repository contains registry snapshots, specifications/roadmaps, issue
templates, and a validator. Allocation and eviction language in the data
describes policy; `tools/validator.py` only performs local range checks and
does not implement automatic relocation or rewrite font metrics. The GitHub
Actions workflow contains its own inline overlap check over the two CSV files;
it is separate from the Python validator and is not an upstream-collision
service.

Before proposing a range, inspect both CSVs and the relevant roadmap under
`S1/` or `S2/`. The validator only checks local overlaps; it cannot establish
that a PUA range is available under UCSUR, SPUCE, or another upstream
authority.

## Repository map

- `data/` — Set 1 and Set 2 CSV snapshots.
- `S1/`, `S2/` — set-specific roadmaps and supporting documents.
- `core/` — registry specifications.
- `UNIDATA/` — mirrored Unicode data and provenance.
- `tools/validator.py` — command-line collision, format, and migration check.
- `tests/test_migration.py` — regression tests for the Set 1 → Set 2 migration.
- `.github/workflows/registry_check.yml` — push/pull-request matrix check.

The authoritative review process and status definitions are documented in
`core/specification.md` and the set roadmaps.
