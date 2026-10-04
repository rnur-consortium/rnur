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
`Permanent Allocation / Open for Submission`.

To check a proposed range against one local set:

```powershell
py tools/validator.py 1 U+EE00 U+EE0F
py tools/validator.py 2 U+E820 U+E82F
```

The command accepts set 1 or 2, start, and end; it reports overlap but does
not reserve or write an allocation. It does not query upstream registries,
build fonts, or perform an eviction/migration.

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
- `tools/validator.py` — command-line collision and format check.
- `.github/workflows/registry_check.yml` — push/pull-request matrix check.

The authoritative review process and status definitions are documented in
`core/specification.md` and the set roadmaps.
