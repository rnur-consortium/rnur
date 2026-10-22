#!/usr/bin/env python3
import csv
import sys
import os
import re

# ============================================================================
# Migration invariants (RNUR Set 1 -> Set 2 migration; SPUCE-supplied
# allocation map represented in RNUR Set 1)
# ============================================================================
# SPUCE supplies these allocation definitions; RNUR represents them within its
# own Set 1 BMP PUA interval U+EE00..U+EFFF. SPUCE does not use RNUR's Set 1 /
# Set 2 architecture. (Inclusive sizes are end - start + 1.)
SPUCE_ALLOCATIONS = [
    ("Vulcan",            0xEE00, 0xEE2F,  48),
    ("Gallifreyan",       0xEE30, 0xEE5F,  48),
    ("Atlantean",         0xEE60, 0xEE8F,  48),
    ("Valyrian",          0xEE90, 0xEEBF,  48),
    ("Dovahzul",          0xEEC0, 0xEEEF,  48),
    ("Utopian",           0xEEF0, 0xEF0F,  32),
    ("Global Alphabet",   0xEF10, 0xEF3F,  48),
    ("Ditema",            0xEF40, 0xEF6F,  48),
    ("Quốc âm tân tự", 0xEF70, 0xEFFF, 144),
]
SPUCE_INTERVAL = (0xEE00, 0xEFFF)

# The six named RNUR scripts evicted from Set 1, in original order, with their
# original Set 1 ranges (old_start, old_end) and required Set 2 destinations.
RELOCATED_SCRIPTS = [
    ("Benjamin Franklin's Phonetic Additions", 0xEE00, 0xEE0F, 0xE820, 0xE82F),
    ("Loopiform",                              0xEE10, 0xEE5F, 0xE830, 0xE87F),
    ("Sulat Hiligaynon",                       0xEE90, 0xEEDF, 0xE880, 0xE8CF),
    ("Western Script",                         0xEEE0, 0xEF2F, 0xE8D0, 0xE91F),
    ("Zurjon",                                 0xEF30, 0xEF6F, 0xE920, 0xE95F),
    ("Foldian",                                0xEF70, 0xEFAF, 0xE960, 0xE99F),
]
RELOCATION_DESTINATION = (0xE820, 0xE99F)

# Alternative names used for the displaced scripts in older records.
DISPLACED_NAME_ALIASES = {
    "Benjamin Franklin's Phonetic Additions": ["Franklin Phonetic Alphabet"],
}

# Former Set 1 ??? (PROVISIONAL_RNUR_OPEN_SLOT) reservations that must be
# dissolved into permanent space during the migration: removed from the active
# result, never migrated to Set 2, never recreated as slots/reservations.
FORMER_PROVISIONAL_RANGES = [
    (0xEE60, 0xEE8F),
    (0xEFB0, 0xEFFF),
]

# Unrelated allocations that must survive the migration untouched.
CONSTANTSCRIPT_RANGE = (0xE000, 0xE81F)

# The named 'Placeholder' allocation was relocated from Set 1 (U+F5C0-U+F71F)
# to Set 2 (U+E9A0-U+EAFF) under the SPUCE allocation update of 2026-10-22.
# Its inclusive size (352 code points) is preserved, and the Set 2 destination
# begins immediately after Foldian (U+E960-U+E99F).
PLACEHOLDER_SET2_RANGE = (0xE9A0, 0xEAFF)
PLACEHOLDER_SET1_RANGE = (0xF5C0, 0xF71F)
PLACEHOLDER_SIZE = 352
FOLDIAN_SET2_RANGE = (0xE960, 0xE99F)

# The three Set 1 ranges that replace the vacated Placeholder allocation.
# They are contiguous, non-overlapping, and cover U+F5C0-U+F71F exactly.
# The two '???' ranges carry no name and no allocation of their own.
FORMER_PLACEHOLDER_SUBDIVISION = [
    (0xF5C0, 0xF5FF, 'PROVISIONAL_RNUR_OPEN_SLOT'),
    (0xF600, 0xF6FF, 'Miscellaneous Symbols Extended-I'),
    (0xF700, 0xF71F, 'PROVISIONAL_RNUR_OPEN_SLOT'),
]

# BMP provisional open slots (PROVISIONAL_RNUR_OPEN_SLOT). These are defensive
# ??? territory eligible for clean Set 2 relocation routing, so they are Tier B
# by definition (Tier A is "Non-Provisional"). The specification must never
# re-list them under Tier A, or the classification contradiction returns.
TIER_B_BMP_PROVISIONAL_RANGES = [
    (0xF5C0, 0xF5FF),
    (0xF700, 0xF71F),
    (0xF720, 0xF7FF),
    (0xF820, 0xF87F),
]

def parse_hex(hex_str):
    """Converts a Unicode code point string (e.g., 'U+EE00', 'EE00', '0xEE00') into an integer."""
    clean_str = hex_str.upper().replace('U+', '').replace('0X', '').strip()
    return int(clean_str, 16)

def check_overlap(start1, end1, start2, end2):
    """Returns True if two code point ranges overlap."""
    return max(start1, start2) <= min(end1, end2)

def inclusive_size(start, end):
    """Inclusive code point count of a range (end - start + 1)."""
    return end - start + 1

def load_registry_rows(base_dir):
    """Loads every row from both registry CSV sheets as parsed dictionaries."""
    rows = []
    for name in ('set1_master.csv', 'set2_sandbox.csv'):
        path = os.path.join(base_dir, 'data', name)
        with open(path, 'r', encoding='utf-8') as f:
            for line_num, row in enumerate(csv.DictReader(f), start=2):
                row['_file'] = name
                row['_line'] = line_num
                row['_set'] = int(row['Set_Number'])
                row['_start'] = parse_hex(row['Start_Code_Point'])
                row['_end'] = parse_hex(row['End_Code_Point'])
                row['_name'] = row.get('Script_Name') or row.get('Project_Name') or "UNKNOWN_ITEM"
                rows.append(row)
    return rows

def load_blocks(path):
    """Parses a Blocks.txt-style file into (start, end, name) tuples."""
    blocks = []
    pattern = re.compile(r'^([0-9A-Fa-f]+)\.\.([0-9A-Fa-f]+);\s*(.+?)\s*$')
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#'):
                continue
            m = pattern.match(line.rstrip('\n'))
            if m:
                blocks.append((int(m.group(1), 16), int(m.group(2), 16), m.group(3)))
    return blocks

def roadmap_has_range(text, name, start, end):
    """
    True when a roadmap grid charts `name` over the inclusive range start..end.
    A single label like 'Vulcan (EE00-EE2F)' matches directly; labels split
    across grid rows (e.g. 'Utopian (EEF0-EEFF)' + 'Utopian (EF00-EF0F)')
    match when consecutive lines starting at `start` chain to `end`.
    """
    if f"{name} ({start:04X}-{end:04X})" in text:
        return True
    candidates = [ln for ln in text.splitlines()
                  if name in ln and '(' in ln and '-' in ln]
    starts = f"({start:04X}-"
    ends = f"-{end:04X})"
    for i, ln in enumerate(candidates):
        if starts in ln:
            for j in range(i, min(i + 40, len(candidates))):
                if ends in candidates[j]:
                    return True
    return False

def check_migration_invariants(base_dir):
    """
    Enforces the Set 1 -> Set 2 migration and SPUCE replacement invariants:

    1.  Overlapping allocations within a registry are rejected (also covered
        by run_full_database_scan).
    2.  Inclusive range sizes (end - start + 1) match the supplied mapping.
    3.  No missing or duplicated active allocations among the required sets.
    4.  The nine SPUCE allocations cover U+EE00..U+EFFF exactly.
    5.  No stale active Set 1 allocation for the six displaced scripts.
    6.  Set 2 destinations are exact, ordered, and contiguous.
    7.  The ??? reservations are not relocated into Set 2.
    8.  Former provisional RNUR reservation records are removed.
    9.  ConstantScript and other Set 2 allocations are not disturbed.
    10. Roadmaps, CSV files, block files, and the specification agree.
    11. The governance distinction is explicit: SPUCE supplies the incoming
        allocation definitions, while RNUR owns the Set 1 / Set 2 architecture
        (no artifact may describe SPUCE as using RNUR's sets).
    """
    errors = []

    def fail(msg):
        errors.append(msg)
        print(f"[-] MIGRATION INVARIANT VIOLATION: {msg}")

    try:
        rows = load_registry_rows(base_dir)
    except Exception as e:
        fail(f"could not load registry rows: {e}")
        return False

    s1 = [r for r in rows if r['_set'] == 1]
    s2 = [r for r in rows if r['_set'] == 2]

    # --- (2)(3) SPUCE rows: exact, sized, unique ---
    for name, exp_s, exp_e, exp_size in SPUCE_ALLOCATIONS:
        matches = [r for r in s1 if r['_name'] == name]
        if len(matches) != 1:
            fail(f"Set 1 must contain exactly one '{name}' allocation; found {len(matches)}")
            continue
        r = matches[0]
        if (r['_start'], r['_end']) != (exp_s, exp_e):
            fail(f"'{name}' range is {r['Start_Code_Point']}-{r['End_Code_Point']}, "
                 f"expected U+{exp_s:04X}-U+{exp_e:04X}")
        if inclusive_size(r['_start'], r['_end']) != exp_size:
            fail(f"'{name}' inclusive size is {inclusive_size(r['_start'], r['_end'])}, "
                 f"expected {exp_size}")

    # --- (4) exact coverage of U+EE00..U+EFFF ---
    lo, hi = SPUCE_INTERVAL
    covering = [r for r in s1 if check_overlap(r['_start'], r['_end'], lo, hi)]
    covered = sorted((r['_start'], r['_end']) for r in covering)
    expected = sorted((s, e) for _, s, e, _ in SPUCE_ALLOCATIONS)
    if covered != expected:
        fail(f"Set 1 rows covering U+{lo:04X}-U+{hi:04X} are {[(f'{a:04X}', f'{b:04X}') for a, b in covered]}, "
             f"expected the nine SPUCE ranges {[(f'{a:04X}', f'{b:04X}') for a, b in expected]}")
    else:
        cursor = lo
        for _, s, e, _ in sorted(SPUCE_ALLOCATIONS, key=lambda t: t[1]):
            if s != cursor:
                fail(f"SPUCE coverage gap/overlap at U+{cursor:04X} (next range starts U+{s:04X})")
                break
            cursor = e + 1
        if cursor - 1 != hi:
            fail(f"SPUCE coverage ends at U+{cursor - 1:04X}, expected U+{hi:04X}")

    # --- (5) no stale Set 1 record for the displaced scripts ---
    displaced = set()
    for name, old_s, old_e, _, _ in RELOCATED_SCRIPTS:
        displaced.add(name)
        displaced.update(DISPLACED_NAME_ALIASES.get(name, []))
    for r in s1:
        if r['_name'] in displaced:
            fail(f"stale Set 1 allocation for displaced script '{r['_name']}' "
                 f"({r['Start_Code_Point']}-{r['End_Code_Point']}, line {r['_line']})")

    # --- (8) former ??? reservation records removed ---
    for old_s, old_e in FORMER_PROVISIONAL_RANGES:
        for r in s1:
            looks_provisional = 'PROVISIONAL' in r['_name'].upper() or '???' in r['_name']
            if looks_provisional and check_overlap(r['_start'], r['_end'], old_s, old_e):
                fail(f"former ??? reservation U+{old_s:04X}-U+{old_e:04X} still present in "
                     f"{r['_file']} line {r['_line']} as '{r['_name']}'")

    # --- (7) ??? never migrated into Set 2 ---
    for r in s2:
        lname = r['_name'].upper()
        if '???' in r['_name'] or 'PROVISIONAL' in lname:
            fail(f"Set 2 contains a ??? / provisional reservation record: "
                 f"{r['_file']} line {r['_line']} ('{r['_name']}')")

    # --- (9) ConstantScript unchanged and unconflicted ---
    const = [r for r in s2 if r['_name'] == 'Constantscript']
    if len(const) != 1:
        fail(f"Set 2 must contain exactly one Constantscript allocation; found {len(const)}")
    else:
        c = const[0]
        if (c['_start'], c['_end']) != CONSTANTSCRIPT_RANGE:
            fail(f"Constantscript moved: {c['Start_Code_Point']}-{c['End_Code_Point']}, "
                 f"expected U+{CONSTANTSCRIPT_RANGE[0]:04X}-U+{CONSTANTSCRIPT_RANGE[1]:04X}")

    # --- (6) Set 2 relocations: exact, sized, ordered, contiguous ---
    for name, old_s, old_e, new_s, new_e in RELOCATED_SCRIPTS:
        matches = [r for r in s2 if r['_name'] == name]
        if len(matches) != 1:
            fail(f"Set 2 must contain exactly one '{name}' allocation; found {len(matches)}")
            continue
        r = matches[0]
        if (r['_start'], r['_end']) != (new_s, new_e):
            fail(f"Set 2 '{name}' range is {r['Start_Code_Point']}-{r['End_Code_Point']}, "
                 f"expected U+{new_s:04X}-U+{new_e:04X}")
            continue
        old_size = inclusive_size(old_s, old_e)
        if inclusive_size(new_s, new_e) != old_size:
            fail(f"Set 2 '{name}' inclusive size {inclusive_size(new_s, new_e)} != original {old_size}")
    relocated_rows = sorted(
        (r for r in s2 if r['_name'] in displaced),
        key=lambda r: r['_start'])
    expected_order = [name for name, *_ in RELOCATED_SCRIPTS]
    if [r['_name'] for r in relocated_rows] != expected_order:
        fail("Set 2 relocation order does not preserve the original Set 1 order: "
             f"got {[r['_name'] for r in relocated_rows]}")
    if relocated_rows:
        if relocated_rows[0]['_start'] != RELOCATION_DESTINATION[0]:
            fail(f"relocations must begin at U+{RELOCATION_DESTINATION[0]:04X}")
        prev_end = relocated_rows[0]['_end']
        for r in relocated_rows[1:]:
            if r['_start'] != prev_end + 1:
                fail(f"gap/overlap between relocations at U+{prev_end:04X}/U+{r['_start']:04X} "
                     f"('{r['_name']}')")
                break
            prev_end = r['_end']
        if prev_end != RELOCATION_DESTINATION[1]:
            fail(f"relocations must end at U+{RELOCATION_DESTINATION[1]:04X}, "
                 f"ended at U+{prev_end:04X}")
        if not all(CONSTANTSCRIPT_RANGE[1] < r['_start'] for r in relocated_rows):
            fail("a Set 2 relocation overlaps Constantscript")

    # --- named Placeholder allocation: relocated from Set 1 to Set 2 ---
    ph_s2 = [r for r in s2 if r['_name'] == 'Placeholder']
    if len(ph_s2) != 1:
        fail(f"Set 2 must contain exactly one 'Placeholder' allocation; found {len(ph_s2)}")
    else:
        r = ph_s2[0]
        if (r['_start'], r['_end']) != PLACEHOLDER_SET2_RANGE:
            fail(f"Set 2 'Placeholder' range is {r['Start_Code_Point']}-{r['End_Code_Point']}, "
                 f"expected U+{PLACEHOLDER_SET2_RANGE[0]:04X}-U+{PLACEHOLDER_SET2_RANGE[1]:04X}")
        if inclusive_size(r['_start'], r['_end']) != PLACEHOLDER_SIZE:
            fail(f"Set 2 'Placeholder' inclusive size is "
                 f"{inclusive_size(r['_start'], r['_end'])}, expected {PLACEHOLDER_SIZE}")
        if inclusive_size(*PLACEHOLDER_SET1_RANGE) != PLACEHOLDER_SIZE:
            fail(f"former Set 1 'Placeholder' range size is "
                 f"{inclusive_size(*PLACEHOLDER_SET1_RANGE)}, expected {PLACEHOLDER_SIZE}")
        if r['_start'] != FOLDIAN_SET2_RANGE[1] + 1:
            fail("Set 2 'Placeholder' must begin immediately after Foldian "
                 f"(U+{FOLDIAN_SET2_RANGE[1]:04X})")
        for other in s2:
            if other is r:
                continue
            if check_overlap(r['_start'], r['_end'], other['_start'], other['_end']):
                fail(f"Set 2 'Placeholder' overlaps '{other['_name']}' "
                     f"({other['Start_Code_Point']}-{other['End_Code_Point']})")
    if any(r['_name'] == 'Placeholder' for r in s1):
        fail("'Placeholder' must not remain a Set 1 allocation after the relocation")
    for r in s1:
        if (r['_start'], r['_end']) == PLACEHOLDER_SET1_RANGE:
            fail(f"Set 1 still records the vacated 'Placeholder' range "
                 f"U+{PLACEHOLDER_SET1_RANGE[0]:04X}-U+{PLACEHOLDER_SET1_RANGE[1]:04X}")

    # --- the vacated Set 1 range is subdivided into exactly three ranges ---
    cursor = PLACEHOLDER_SET1_RANGE[0]
    for sub_s, sub_e, sub_name in FORMER_PLACEHOLDER_SUBDIVISION:
        matches = [r for r in s1 if (r['_start'], r['_end']) == (sub_s, sub_e)]
        if len(matches) != 1:
            fail(f"Set 1 must contain exactly one '{sub_name}' allocation at "
                 f"U+{sub_s:04X}-U+{sub_e:04X}; found {len(matches)}")
        else:
            row = matches[0]
            if row['_name'] != sub_name:
                fail(f"Set 1 range U+{sub_s:04X}-U+{sub_e:04X} is named "
                     f"'{row['_name']}', expected '{sub_name}'")
            if sub_name == 'PROVISIONAL_RNUR_OPEN_SLOT':
                if row.get('Status') != 'Provisional Allocation / Open for Submission':
                    fail(f"Set 1 '???' range U+{sub_s:04X}-U+{sub_e:04X} has status "
                         f"'{row.get('Status')}', expected 'Provisional Allocation / Open for Submission'")
                if 'Placeholder' in (row.get('Description') or ''):
                    fail(f"Set 1 '???' range U+{sub_s:04X}-U+{sub_e:04X} still carries "
                         "the former Placeholder description")
            else:
                if row.get('Author') != 'SPUCE' or row.get('Status') != 'SPUCE Allocation' \
                        or row.get('Flags') != 'SPUCE':
                    fail(f"Set 1 range U+{sub_s:04X}-U+{sub_e:04X} ('{sub_name}') is not "
                         f"recorded as a SPUCE allocation (author/status/flags: "
                         f"{row.get('Author')!r}/{row.get('Status')!r}/{row.get('Flags')!r})")
        if sub_s != cursor:
            fail(f"Set 1 subdivision gap/overlap at U+{cursor:04X} "
                 f"(next range starts U+{sub_s:04X})")
        cursor = sub_e + 1
    if cursor - 1 != PLACEHOLDER_SET1_RANGE[1]:
        fail(f"Set 1 subdivision ends at U+{cursor - 1:04X}, expected "
             f"U+{PLACEHOLDER_SET1_RANGE[1]:04X}")

    # --- (10) block files consistent with the CSV registries ---
    s1_blocks_path = os.path.join(base_dir, 'UNIDATA', 'S1', 'Blocks.txt')
    s2_blocks_path = os.path.join(base_dir, 'UNIDATA', 'S2', 'Blocks.txt')
    try:
        s1_blocks = load_blocks(s1_blocks_path)
        s2_blocks = load_blocks(s2_blocks_path)
    except Exception as e:
        fail(f"could not parse block files: {e}")
        return False

    for name, exp_s, exp_e, _ in SPUCE_ALLOCATIONS:
        if (exp_s, exp_e, name) not in s1_blocks:
            fail(f"UNIDATA/S1/Blocks.txt missing block '{name}' "
                 f"({exp_s:04X}..{exp_e:04X})")
    for name, old_s, old_e, new_s, new_e in RELOCATED_SCRIPTS:
        if any(s <= old_e and old_s <= e and n == name for s, e, n in s1_blocks):
            fail(f"UNIDATA/S1/Blocks.txt still maps displaced '{name}' "
                 f"({old_s:04X}..{old_e:04X}) in Set 1")
        if (new_s, new_e, name) not in s2_blocks:
            fail(f"UNIDATA/S2/Blocks.txt missing block '{name}' "
                 f"({new_s:04X}..{new_e:04X})")
    for old_s, old_e in FORMER_PROVISIONAL_RANGES:
        for s, e, n in s1_blocks:
            if (s, e) == (old_s, old_e) and 'PROVISIONAL' in n.upper():
                fail(f"UNIDATA/S1/Blocks.txt still carries the former ??? reservation "
                     f"{old_s:04X}..{old_e:04X}")
        for s, e, n in s2_blocks:
            if 'PROVISIONAL' in n.upper() and check_overlap(s, e, old_s, old_e) \
                    and not check_overlap(s, e, lo, hi):
                fail(f"UNIDATA/S2/Blocks.txt carries a provisional record derived from "
                     f"the former ??? reservation {old_s:04X}..{old_e:04X}")
    if (CONSTANTSCRIPT_RANGE[0], CONSTANTSCRIPT_RANGE[1], 'Constantscript') not in s2_blocks:
        fail("UNIDATA/S2/Blocks.txt missing the Constantscript block")
    if any(n == 'OPEN_SLOT' and s == 0xE820 for s, e, n in s2_blocks):
        fail("UNIDATA/S2/Blocks.txt still reports U+E820.. as open space")
    if (0xEB00, 0xF8FF, 'OPEN_SLOT') not in s2_blocks:
        fail("UNIDATA/S2/Blocks.txt should keep U+EB00..U+F8FF as OPEN_SLOT")
    if (PLACEHOLDER_SET2_RANGE[0], PLACEHOLDER_SET2_RANGE[1], 'Placeholder') not in s2_blocks:
        fail("UNIDATA/S2/Blocks.txt missing the relocated 'Placeholder' block "
             f"({PLACEHOLDER_SET2_RANGE[0]:04X}..{PLACEHOLDER_SET2_RANGE[1]:04X})")
    for s, e, n in s1_blocks:
        if n == 'Placeholder' and check_overlap(s, e, *PLACEHOLDER_SET1_RANGE):
            fail("UNIDATA/S1/Blocks.txt still maps a named 'Placeholder' block over "
                 f"the vacated range ({s:04X}..{e:04X})")
    if any(s == PLACEHOLDER_SET1_RANGE[0] and e == PLACEHOLDER_SET1_RANGE[1]
           for s, e, n in s1_blocks):
        fail("UNIDATA/S1/Blocks.txt still maps the vacated Placeholder range "
             f"{PLACEHOLDER_SET1_RANGE[0]:04X}..{PLACEHOLDER_SET1_RANGE[1]:04X}")
    for sub_s, sub_e, sub_name in FORMER_PLACEHOLDER_SUBDIVISION:
        if (sub_s, sub_e, sub_name) not in s1_blocks:
            fail(f"UNIDATA/S1/Blocks.txt missing the subdivision block '{sub_name}' "
                 f"({sub_s:04X}..{sub_e:04X})")

    # --- (10) roadmaps and specification consistent with the registries ---
    def read_text(rel_path):
        with open(os.path.join(base_dir, rel_path), 'r', encoding='utf-8') as f:
            return f.read()

    try:
        s1_roadmap = read_text(os.path.join('S1', 'Roadmap', 'bmp_pua_roadmap.md'))
        s2_roadmap = read_text(os.path.join('S2', 'Roadmap', 'bmp_pua_roadmap.md'))
        spec = read_text(os.path.join('core', 'SPECIFICATION.md'))
    except Exception as e:
        fail(f"could not read roadmap/specification files: {e}")
        return False

    for name, exp_s, exp_e, _ in SPUCE_ALLOCATIONS:
        if not roadmap_has_range(s1_roadmap, name, exp_s, exp_e):
            fail(f"S1 roadmap missing SPUCE entry '{name} ({exp_s:04X}-{exp_e:04X})'")
        range_str = f"`U+{exp_s:04X}`–`U+{exp_e:04X}`"
        if range_str not in spec:
            fail(f"core/SPECIFICATION.md missing SPUCE range {range_str}")

    if f"??? (EE60-EE8F)" in s1_roadmap or f"??? (EFB0-EFFF)" in s1_roadmap:
        fail("S1 roadmap still charts a dissolved ??? reservation in U+EE00-U+EFFF")
    for name, old_s, old_e, _, _ in RELOCATED_SCRIPTS:
        stale = f"{name} ({old_s:04X}-{old_e:04X})"
        if stale in s1_roadmap:
            fail(f"S1 roadmap still charts displaced script '{stale}'")

    for name, _, _, new_s, new_e in RELOCATED_SCRIPTS:
        if not roadmap_has_range(s2_roadmap, name, new_s, new_e):
            fail(f"S2 roadmap missing relocation entry '{name} ({new_s:04X}-{new_e:04X})'")
        range_str = f"`U+{new_s:04X}`–`U+{new_e:04X}`"
        if range_str not in spec:
            fail(f"core/SPECIFICATION.md missing Set 2 range {range_str}")
    if '??? (' in s2_roadmap:
        fail("S2 roadmap charts a ??? entry; former reservations must not migrate to Set 2")
    if not roadmap_has_range(s2_roadmap, 'Constantscript',
                             CONSTANTSCRIPT_RANGE[0], CONSTANTSCRIPT_RANGE[1]):
        fail("S2 roadmap missing the Constantscript entry at U+E000-U+E81F")
    if '**U+EE60–U+EE8F**: PROVISIONAL_RNUR_OPEN_SLOT' in spec or \
       '**U+EFB0–U+EFFF**: PROVISIONAL_RNUR_OPEN_SLOT' in spec:
        fail("core/SPECIFICATION.md still lists the former ??? reservations as active")
    if 'dissolved into permanent space' not in spec:
        fail("core/SPECIFICATION.md does not document the permanent-space migration rule")

    # --- (10a) Placeholder relocation: roadmaps and specification agree ---
    # The named 'Placeholder' allocation now lives in Set 2; the Set 1 BMP grid
    # must chart the vacated range as two ??? cells and one SPUCE cell, and the
    # Set 2 grid must chart the relocated allocation.
    if 'Placeholder (F5C0-F71F)' in s1_roadmap:
        fail("S1 roadmap still charts the relocated 'Placeholder (F5C0-F71F)' cell")
    for sub_s, sub_e in ((0xF5C0, 0xF5FF), (0xF700, 0xF71F)):
        cell = f"??? ({sub_s:04X}-{sub_e:04X})"
        if cell not in s1_roadmap:
            fail(f"S1 roadmap is missing the ??? cell '{cell}'")
    if not roadmap_has_range(s1_roadmap, 'Miscellaneous Symbols Extended-I',
                             0xF600, 0xF6FF):
        fail("S1 roadmap missing SPUCE entry "
             "'Miscellaneous Symbols Extended-I (F600-F6FF)'")
    if not roadmap_has_range(s2_roadmap, 'Placeholder',
                             PLACEHOLDER_SET2_RANGE[0], PLACEHOLDER_SET2_RANGE[1]):
        fail("S2 roadmap missing the relocated entry "
             f"'Placeholder ({PLACEHOLDER_SET2_RANGE[0]:04X}-"
             f"{PLACEHOLDER_SET2_RANGE[1]:04X})'")
    if 'Placeholder (F5C0-F71F)' in s2_roadmap:
        fail("S2 roadmap still charts the former Set 1 'Placeholder (F5C0-F71F)' cell")
    for exp_s, exp_e in (PLACEHOLDER_SET2_RANGE, (0xF5C0, 0xF5FF),
                         (0xF600, 0xF6FF), (0xF700, 0xF71F)):
        range_str = f"`U+{exp_s:04X}`–`U+{exp_e:04X}`"
        if range_str not in spec:
            fail(f"core/SPECIFICATION.md missing range {range_str}")

    # --- (10b) Tier A/B classification of the BMP ??? gaps ---
    # Tier A covers non-provisional ranges only. The BMP PROVISIONAL_RNUR_OPEN_SLOT
    # gaps are provisional ??? territory (Tier B) and must never be claimed by
    # Tier A; otherwise the specification silently contradicts the CSV/Blocks data.
    if '##### 3.5.3.1' in spec and '##### 3.5.3.2' in spec:
        tier_a_sec = spec.split('##### 3.5.3.1', 1)[1].split('##### 3.5.3.2', 1)[0]
        tier_b_sec = spec.split('##### 3.5.3.2', 1)[1].split('##### 3.5.4', 1)[0]
    else:
        fail("core/SPECIFICATION.md is missing the §3.5.3.1/§3.5.3.2 tier sections")
        tier_a_sec = tier_b_sec = ''
    for prov_s, prov_e in TIER_B_BMP_PROVISIONAL_RANGES:
        if f"{prov_s:04X}" in tier_a_sec:
            fail(f"core/SPECIFICATION.md Tier A (§3.5.3.1) wrongly claims the "
                 f"Tier B provisional range U+{prov_s:04X}-U+{prov_e:04X}")
        if f"U+{prov_s:04X}" not in tier_b_sec:
            fail(f"core/SPECIFICATION.md Tier B (§3.5.3.2) does not name the "
                 f"provisional range U+{prov_s:04X}-U+{prov_e:04X}")

    # --- (10c) ??? markers on the provisional BMP roadmap cells ---
    # Each Tier B (provisional) BMP gap must be rendered as ??? territory in the
    # Set 1 BMP roadmap. A bare "(F820-F87F)" cell reads like a finalised gap and
    # hides the provisional status of the range.
    for (s, e) in TIER_B_BMP_PROVISIONAL_RANGES:
        bare = f"({s:04X}-{e:04X})"
        if f"??? {bare}" not in s1_roadmap and f"???{bare}" not in s1_roadmap:
            fail(f"S1 BMP roadmap cell for U+{s:04X}-U+{e:04X} is missing the ??? marker")

    # --- (11) governance distinction: SPUCE supplies definitions, RNUR owns sets ---
    if 'SPUCE does not use RNUR' not in spec:
        fail("core/SPECIFICATION.md does not state the SPUCE/RNUR governance distinction")
    governance_artifacts = {
        os.path.join('S1', 'Roadmap', 'bmp_pua_roadmap.md'): s1_roadmap,
        os.path.join('S2', 'Roadmap', 'bmp_pua_roadmap.md'): s2_roadmap,
        os.path.join('core', 'SPECIFICATION.md'): spec,
    }
    for rel in (os.path.join('data', 'set1_master.csv'),
                os.path.join('data', 'set2_sandbox.csv'),
                os.path.join('UNIDATA', 'S1', 'Blocks.txt'),
                os.path.join('UNIDATA', 'S2', 'Blocks.txt')):
        try:
            governance_artifacts[rel] = read_text(rel)
        except Exception as e:
            fail(f"could not read {rel} for governance check: {e}")
    for rel, text in governance_artifacts.items():
        for wrong in ('SPUCE Set 1', 'SPUCE Set 2'):
            if wrong in text:
                fail(f"{rel} wrongly describes SPUCE as using RNUR's set architecture ('{wrong}')")

    if errors:
        print(f"\n[-] MIGRATION VALIDATION FAILED: {len(errors)} violation(s).")
        return False
    print("[+] SUCCESS: Set 1 -> Set 2 migration invariants all hold.")
    return True

def run_full_database_scan(base_dir):
    """
    Scans the entire existing repository data files (master and sandbox) 
    to ensure internal consistency within each parallel set layer.
    """
    paths = [
        os.path.join(base_dir, 'data', 'set1_master.csv'),
        os.path.join(base_dir, 'data', 'set2_sandbox.csv')
    ]
    allocated = []
    has_errors = False
    
    print("\nExecuting comprehensive RNUR matrix validation scan...")
    
    for path in paths:
        if not os.path.exists(path):
            print(f"[-] CRITICAL ERROR: {path} does not exist.")
            return False
            
        print(f"Analyzing {os.path.basename(path)} for integrity...")
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for line_num, row in enumerate(reader, start=2):
                # Skip checking against open/empty sandbox slots
                if row.get('Status') in ['Waiting for Submissions', 'Provisional Allocation / Open for Submission', 'Permanent Allocation / Open for Submission']:
                    continue
                try:
                    s_set = int(row['Set_Number'])
                    start = parse_hex(row['Start_Code_Point'])
                    end = parse_hex(row['End_Code_Point'])

                    # Inclusive range integrity (end - start + 1)
                    if start > end:
                        print(f"[-] INVALID RANGE in {os.path.basename(path)}, Line {line_num}: "
                              f"{row['Start_Code_Point']} > {row['End_Code_Point']}")
                        has_errors = True
                        continue

                    # Dynamically key the project/script name due to differing headers
                    script_name = row.get('Script_Name') or row.get('Project_Name') or "UNKNOWN_ITEM"
                    
                    # Parallel Isolation Collision Check
                    for c_file, c_set, c_start, c_end, c_name, c_line in allocated:
                        if s_set == c_set and check_overlap(start, end, c_start, c_end):
                            print(f"[-] CRITICAL COLLISION DETECTED IN SET {s_set}!")
                            print(f"    -> Current:  {os.path.basename(path)}, Line {line_num} ({script_name}) [{hex(start)}-{hex(end)}]")
                            print(f"    -> Existing: {os.path.basename(c_file)}, Line {c_line} ({c_name}) [{hex(c_start)}-{hex(c_end)}]")
                            has_errors = True
                            
                    allocated.append((path, s_set, start, end, script_name, line_num))
                except Exception as e:
                    print(f"[-] Malformed data in {os.path.basename(path)} on line {line_num}: {e}")
                    has_errors = True
                    
        print(f"[+] {os.path.basename(path)} internal verification complete.")
        
    if has_errors:
        print("\n[-] SCAN FAILED: Matrix conflicts or malformed entries detected.")
        return False
        
    print("\n[+] SUCCESS: Entire RNUR matrix verified cleanly with zero internal overlaps.")
    return True

def validate_single_submission(set_number, start_hex, end_hex, base_dir):
    """Checks a single new script proposal against the appropriate target layer sheet."""
    # Dynamic Routing Protocol based on Target Environment Layer
    if int(set_number) == 1:
        target_csv_path = os.path.join(base_dir, 'data', 'set1_master.csv')
    elif int(set_number) == 2:
        target_csv_path = os.path.join(base_dir, 'data', 'set2_sandbox.csv')
    else:
        print(f"[-] Error: Set {set_number} configuration file does not exist locally.")
        return False

    if not os.path.exists(target_csv_path):
        print(f"[-] Error: Target registry file not found at {target_csv_path}")
        return False

    try:
        new_start = parse_hex(start_hex)
        new_end = parse_hex(end_hex)
    except ValueError:
        print("[-] Error: Invalid hexadecimal format provided.")
        return False

    if new_start > new_end:
        print("[-] Error: Start code point cannot be greater than the end code point.")
        return False

    collisions = []

    with open(target_csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Status'] in ['Waiting for Submissions', 'Provisional Allocation / Open for Submission', 'Permanent Allocation / Open for Submission']:
                continue            
            try:
                current_set = int(row['Set_Number'])
                if current_set == int(set_number):
                    curr_start = parse_hex(row['Start_Code_Point'])
                    curr_end = parse_hex(row['End_Code_Point'])
                    
                    if check_overlap(new_start, new_end, curr_start, curr_end):
                        collisions.append(row)
            except (ValueError, KeyError):
                continue

    if collisions:
        print(f"\n[!] COLLISION DETECTED in Set {set_number}!")
        for item in collisions:
            name = item.get('Script_Name') or item.get('Project_Name') or "Unknown"
            author = item.get('Author') or item.get('Owner') or "Unknown"
            print(f"  - Script: {name} ({item['Start_Code_Point']} to {item['End_Code_Point']}) by {author}")
        return False

    print(f"\n[+] SUCCESS: Range {start_hex} to {end_hex} in Set {set_number} is valid for entry!")
    return True

if __name__ == "__main__":
    print("=== RNUR Allocation Validator ===")
    
    # Calculate base repository directories
    tools_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(tools_dir)
    
    # If passed explicit parameters, perform a precision check for a single input
    if len(sys.argv) == 4:
        target_set = sys.argv[1]
        start_pt = sys.argv[2]
        end_pt = sys.argv[3]
        success = validate_single_submission(target_set, start_pt, end_pt, base_dir)
        sys.exit(0 if success else 1)
        
    # Default behavior: run the complete automated sweep across all registry
    # sheets, then verify the Set 1 -> Set 2 migration invariants.
    else:
        print("No input coordinates provided. Shifting to global repository integrity check...")
        matrix_ok = run_full_database_scan(base_dir)
        migration_ok = check_migration_invariants(base_dir)
        sys.exit(0 if (matrix_ok and migration_ok) else 1)
