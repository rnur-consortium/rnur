#!/usr/bin/env python3
"""Regression tests for the RNUR Set 1 -> Set 2 migration and the SPUCE-supplied
allocation map represented in RNUR Set 1.

Run from the repository root:

    python -m unittest discover -s tests -v
"""
import csv
import contextlib
import io
import os
import re
import shutil
import sys
import tempfile
import unittest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(TESTS_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'tools'))

import validator  # noqa: E402


def read(rel_path):
    with open(os.path.join(BASE_DIR, rel_path), 'r', encoding='utf-8') as f:
        return f.read()


def csv_rows(rel_path):
    with open(os.path.join(BASE_DIR, rel_path), 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


class ArithmeticTests(unittest.TestCase):
    """The supplied allocation tables must be arithmetically exact."""

    def test_spuce_ranges_cover_ee00_efff_exactly(self):
        cursor = 0xEE00
        total = 0
        for name, start, end, size in validator.SPUCE_ALLOCATIONS:
            self.assertEqual(start, cursor, f"{name} leaves a gap/overlap")
            self.assertEqual(validator.inclusive_size(start, end), size,
                             f"{name} inclusive size mismatch")
            cursor = end + 1
            total += size
        self.assertEqual(cursor - 1, 0xEFFF)
        self.assertEqual(total, 0xEFFF - 0xEE00 + 1)

    def test_spuce_sizes_match_supplied_map(self):
        expected = {
            "Vulcan": 48, "Gallifreyan": 48, "Atlantean": 48, "Valyrian": 48,
            "Dovahzul": 48, "Utopian": 32, "Global Alphabet": 48,
            "Ditema": 48, "Quốc âm tân tự": 144,
        }
        actual = {n: validator.inclusive_size(s, e) for n, s, e, _ in validator.SPUCE_ALLOCATIONS}
        self.assertEqual(actual, expected)

    def test_set2_destinations_contiguous_sized_and_ordered(self):
        cursor = 0xE820
        for name, old_s, old_e, new_s, new_e in validator.RELOCATED_SCRIPTS:
            self.assertEqual(new_s, cursor, f"{name} destination not contiguous")
            self.assertEqual(validator.inclusive_size(new_s, new_e),
                             validator.inclusive_size(old_s, old_e),
                             f"{name} changed size during relocation")
            cursor = new_e + 1
        self.assertEqual(cursor - 1, 0xE99F)


class RegistryDataTests(unittest.TestCase):
    """The final Set 1 and Set 2 registry records."""

    def setUp(self):
        self.s1 = csv_rows(os.path.join('data', 'set1_master.csv'))
        self.s2 = csv_rows(os.path.join('data', 'set2_sandbox.csv'))

    def test_set1_contains_the_nine_spuce_allocations(self):
        by_name = {r['Script_Name']: r for r in self.s1}
        for name, start, end, _ in validator.SPUCE_ALLOCATIONS:
            self.assertIn(name, by_name, f"missing Set 1 SPUCE row {name}")
            row = by_name[name]
            self.assertEqual(validator.parse_hex(row['Start_Code_Point']), start)
            self.assertEqual(validator.parse_hex(row['End_Code_Point']), end)

    def test_no_stale_set1_record_for_displaced_scripts(self):
        forbidden = set()
        for name, *_ in validator.RELOCATED_SCRIPTS:
            forbidden.add(name)
            forbidden.update(validator.DISPLACED_NAME_ALIASES.get(name, []))
        for row in self.s1:
            self.assertNotIn(row['Script_Name'], forbidden)
            start = validator.parse_hex(row['Start_Code_Point'])
            end = validator.parse_hex(row['End_Code_Point'])
            for _, old_s, old_e, _, _ in validator.RELOCATED_SCRIPTS:
                # every overlap with the old intervals must be a SPUCE row
                if validator.check_overlap(start, end, old_s, old_e):
                    self.assertIn(row['Script_Name'],
                                  [n for n, _, _, _ in validator.SPUCE_ALLOCATIONS])

    def test_former_provisional_reservations_removed(self):
        for old_s, old_e in validator.FORMER_PROVISIONAL_RANGES:
            for row in self.s1:
                looks_provisional = ('PROVISIONAL' in row['Script_Name'].upper()
                                     or '???' in row['Script_Name'])
                if looks_provisional:
                    self.assertFalse(
                        validator.check_overlap(validator.parse_hex(row['Start_Code_Point']),
                                                validator.parse_hex(row['End_Code_Point']),
                                                old_s, old_e))

    def test_set2_relocations_exact(self):
        by_name = {r['Project_Name']: r for r in self.s2}
        for name, _, _, new_s, new_e in validator.RELOCATED_SCRIPTS:
            self.assertIn(name, by_name, f"missing Set 2 relocation row {name}")
            row = by_name[name]
            self.assertEqual(validator.parse_hex(row['Start_Code_Point']), new_s)
            self.assertEqual(validator.parse_hex(row['End_Code_Point']), new_e)

    def test_constantscript_unchanged(self):
        rows = [r for r in self.s2 if r['Project_Name'] == 'Constantscript']
        self.assertEqual(len(rows), 1)
        self.assertEqual(validator.parse_hex(rows[0]['Start_Code_Point']), 0xE000)
        self.assertEqual(validator.parse_hex(rows[0]['End_Code_Point']), 0xE81F)

    def test_no_provisional_record_migrated_to_set2(self):
        for row in self.s2:
            self.assertNotIn('???', row['Project_Name'])
            self.assertNotIn('PROVISIONAL', row['Project_Name'].upper())

    def test_set2_open_sandbox_begins_after_relocations(self):
        sandbox = [r for r in self.s2 if r['Project_Name'] == 'OPEN_SANDBOX'
                   and validator.parse_hex(r['End_Code_Point']) <= 0xF8FF]
        self.assertTrue(sandbox)
        # The open sandbox resumes at U+EB00, immediately after the relocated
        # Placeholder allocation (U+E9A0-U+EAFF).
        self.assertEqual(validator.parse_hex(sandbox[0]['Start_Code_Point']), 0xEB00)

    def test_named_placeholder_allocation_relocated_to_set2(self):
        """Placeholder now lives in Set 2 at U+E9A0-U+EAFF, not in Set 1."""
        s2_ph = [r for r in self.s2 if r['Project_Name'] == 'Placeholder']
        self.assertEqual(len(s2_ph), 1)
        self.assertEqual(validator.parse_hex(s2_ph[0]['Start_Code_Point']), 0xE9A0)
        self.assertEqual(validator.parse_hex(s2_ph[0]['End_Code_Point']), 0xEAFF)
        # Set 1 must no longer carry the named Placeholder allocation.
        s1_ph = [r for r in self.s1 if r['Script_Name'] == 'Placeholder']
        self.assertEqual(s1_ph, [])

    def test_set1_vacated_range_is_subdivided_into_three_ranges(self):
        """U+F5C0-U+F71F is split into ??? / SPUCE / ??? with no overlap."""
        rows = {(validator.parse_hex(r['Start_Code_Point']),
                 validator.parse_hex(r['End_Code_Point'])): r for r in self.s1}
        expected = {
            (0xF5C0, 0xF5FF): 'PROVISIONAL_RNUR_OPEN_SLOT',
            (0xF600, 0xF6FF): 'Miscellaneous Symbols Extended-I',
            (0xF700, 0xF71F): 'PROVISIONAL_RNUR_OPEN_SLOT',
        }
        for rng, name in expected.items():
            self.assertIn(rng, rows, f"Set 1 missing subdivision range {rng}")
            self.assertEqual(rows[rng]['Script_Name'], name)
        # the subdivision covers the vacated range exactly, contiguously
        cursor = 0xF5C0
        for rng in sorted(expected):
            self.assertEqual(rng[0], cursor, "subdivision gap/overlap")
            cursor = rng[1] + 1
        self.assertEqual(cursor - 1, 0xF71F)

    def test_set1_provisional_subdivision_uses_established_convention(self):
        """The two ??? ranges carry no name, status or Placeholder residue."""
        for start, end in ((0xF5C0, 0xF5FF), (0xF700, 0xF71F)):
            rows = [r for r in self.s1
                    if validator.parse_hex(r['Start_Code_Point']) == start
                    and validator.parse_hex(r['End_Code_Point']) == end]
            self.assertEqual(len(rows), 1)
            row = rows[0]
            self.assertEqual(row['Script_Name'], 'PROVISIONAL_RNUR_OPEN_SLOT')
            self.assertEqual(row['Status'], 'Provisional Allocation / Open for Submission')
            self.assertNotIn('Placeholder', row['Description'])
            self.assertNotIn('Placeholder', row['Author'])
            self.assertNotIn('Placeholder', row['Flags'])

    def test_set1_spuce_subdivision_uses_spuce_representation(self):
        rows = [r for r in self.s1
                if validator.parse_hex(r['Start_Code_Point']) == 0xF600
                and validator.parse_hex(r['End_Code_Point']) == 0xF6FF]
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row['Script_Name'], 'Miscellaneous Symbols Extended-I')
        self.assertEqual(row['Author'], 'SPUCE')
        self.assertEqual(row['Status'], 'SPUCE Allocation')
        self.assertEqual(row['Flags'], 'SPUCE')
        self.assertTrue(row['Description'].startswith('SPUCE Allocation:'))

    def test_placeholder_relocation_preserves_size_and_contiguity(self):
        """352 code points, Set 2 destination starts right after Foldian."""
        s, e = validator.PLACEHOLDER_SET2_RANGE
        self.assertEqual(validator.inclusive_size(s, e), 352)
        self.assertEqual(validator.inclusive_size(*validator.PLACEHOLDER_SET1_RANGE),
                         352)
        self.assertEqual(s, validator.FOLDIAN_SET2_RANGE[1] + 1)
        # Foldian itself is untouched by the relocation.
        fold = [r for r in self.s2 if r['Project_Name'] == 'Foldian']
        self.assertEqual(len(fold), 1)
        self.assertEqual(validator.parse_hex(fold[0]['Start_Code_Point']), 0xE960)
        self.assertEqual(validator.parse_hex(fold[0]['End_Code_Point']), 0xE99F)

    def test_placeholder_relocation_does_not_overwrite_set2(self):
        """The new Set 2 allocation must not collide with any other record."""
        s, e = validator.PLACEHOLDER_SET2_RANGE
        for row in self.s2:
            if row['Project_Name'] == 'Placeholder':
                continue
            start = validator.parse_hex(row['Start_Code_Point'])
            end = validator.parse_hex(row['End_Code_Point'])
            self.assertFalse(validator.check_overlap(s, e, start, end),
                             f"relocated Placeholder overlaps {row['Project_Name']}")


class ArtifactConsistencyTests(unittest.TestCase):
    """Blocks, roadmaps and the specification must match the CSVs."""

    def test_set1_blocks_contains_the_spuce_map(self):
        blocks = validator.load_blocks(os.path.join(BASE_DIR, 'UNIDATA', 'S1', 'Blocks.txt'))
        for name, start, end, _ in validator.SPUCE_ALLOCATIONS:
            self.assertIn((start, end, name), blocks)
        # displaced scripts must not remain active Set 1 blocks in EE00..EFFF
        for name, old_s, old_e, _, _ in validator.RELOCATED_SCRIPTS:
            for s, e, n in blocks:
                if n == name:
                    self.assertFalse(validator.check_overlap(s, e, old_s, old_e))
        # the vacated Placeholder block is gone from Set 1 ...
        self.assertNotIn((0xF5C0, 0xF71F, 'Placeholder'), blocks)
        for s, e, n in blocks:
            if n == 'Placeholder':
                self.assertFalse(validator.check_overlap(s, e, 0xF5C0, 0xF71F))
        # ... and replaced by the three subdivision blocks
        self.assertIn((0xF5C0, 0xF5FF, 'PROVISIONAL_RNUR_OPEN_SLOT'), blocks)
        self.assertIn((0xF600, 0xF6FF, 'Miscellaneous Symbols Extended-I'), blocks)
        self.assertIn((0xF700, 0xF71F, 'PROVISIONAL_RNUR_OPEN_SLOT'), blocks)

    def test_set2_blocks_contains_relocations(self):
        blocks = validator.load_blocks(os.path.join(BASE_DIR, 'UNIDATA', 'S2', 'Blocks.txt'))
        self.assertIn((0xE000, 0xE81F, 'Constantscript'), blocks)
        for name, _, _, new_s, new_e in validator.RELOCATED_SCRIPTS:
            self.assertIn((new_s, new_e, name), blocks)
        # the relocated Placeholder block, and the open slot that resumes after it
        self.assertIn((0xE9A0, 0xEAFF, 'Placeholder'), blocks)
        self.assertIn((0xEB00, 0xF8FF, 'OPEN_SLOT'), blocks)
        self.assertNotIn((0xE9A0, 0xF8FF, 'OPEN_SLOT'), blocks)
        self.assertNotIn((0xE820, 0xF8FF, 'OPEN_SLOT'), blocks)
        for _, _, n in blocks:
            self.assertNotIn('PROVISIONAL', n.upper())

    def test_roadmaps_and_spec_match(self):
        s1 = read(os.path.join('S1', 'Roadmap', 'bmp_pua_roadmap.md'))
        s2 = read(os.path.join('S2', 'Roadmap', 'bmp_pua_roadmap.md'))
        spec = read(os.path.join('core', 'SPECIFICATION.md'))
        for name, start, end, _ in validator.SPUCE_ALLOCATIONS:
            self.assertTrue(validator.roadmap_has_range(s1, name, start, end),
                            f"S1 roadmap missing {name}")
            self.assertIn(f"`U+{start:04X}`–`U+{end:04X}`", spec)
        for name, old_s, old_e, new_s, new_e in validator.RELOCATED_SCRIPTS:
            self.assertFalse(validator.roadmap_has_range(s1, name, old_s, old_e),
                             f"S1 roadmap still charts {name} in Set 1")
            self.assertTrue(validator.roadmap_has_range(s2, name, new_s, new_e),
                            f"S2 roadmap missing {name}")
            self.assertIn(f"`U+{new_s:04X}`–`U+{new_e:04X}`", spec)
        self.assertNotIn('??? (', s2)
        self.assertNotIn('??? (EE60-EE8F)', s1)
        self.assertNotIn('??? (EFB0-EFFF)', s1)
        self.assertIn('dissolved into permanent space', spec)

    def test_roadmaps_and_spec_track_the_placeholder_relocation(self):
        """Roadmaps and the specification must chart the new Set 1/Set 2 layout."""
        s1 = read(os.path.join('S1', 'Roadmap', 'bmp_pua_roadmap.md'))
        s2 = read(os.path.join('S2', 'Roadmap', 'bmp_pua_roadmap.md'))
        spec = read(os.path.join('core', 'SPECIFICATION.md'))
        # Set 1: the vacated range is charted as ??? / SPUCE / ???
        self.assertIn('??? (F5C0-F5FF)', s1)
        self.assertIn('??? (F700-F71F)', s1)
        self.assertTrue(validator.roadmap_has_range(
            s1, 'Miscellaneous Symbols Extended-I', 0xF600, 0xF6FF))
        self.assertNotIn('Placeholder (F5C0-F71F)', s1)
        # Set 2: the relocated allocation is charted at its new destination
        self.assertTrue(validator.roadmap_has_range(
            s2, 'Placeholder', 0xE9A0, 0xEAFF))
        self.assertNotIn('Placeholder (F5C0-F71F)', s2)
        # Specification
        for start, end in ((0xE9A0, 0xEAFF), (0xF5C0, 0xF5FF),
                           (0xF600, 0xF6FF), (0xF700, 0xF71F)):
            self.assertIn(f"`U+{start:04X}`–`U+{end:04X}`", spec)

    def test_tier_classification_of_bmp_provisional_gaps(self):
        """The BMP ??? gaps are Tier B (provisional), never Tier A."""
        spec = read(os.path.join('core', 'SPECIFICATION.md'))
        self.assertIn('##### 3.5.3.1', spec)
        self.assertIn('##### 3.5.3.2', spec)
        tier_a = spec.split('##### 3.5.3.1', 1)[1].split('##### 3.5.3.2', 1)[0]
        tier_b = spec.split('##### 3.5.3.2', 1)[1].split('##### 3.5.4', 1)[0]
        rows = {
            (validator.parse_hex(r['Start_Code_Point']), validator.parse_hex(r['End_Code_Point'])): r
            for r in csv_rows(os.path.join('data', 'set1_master.csv'))
        }
        for s, e in validator.TIER_B_BMP_PROVISIONAL_RANGES:
            self.assertNotIn(f"U+{s:04X}", tier_a,
                             f"Tier A must not claim provisional U+{s:04X}-U+{e:04X}")
            self.assertIn(f"U+{s:04X}", tier_b,
                          f"Tier B must name provisional U+{s:04X}-U+{e:04X}")
            row = rows.get((s, e))
            self.assertIsNotNone(row, f"CSV missing BMP provisional range U+{s:04X}-U+{e:04X}")
            self.assertEqual(row['Script_Name'], 'PROVISIONAL_RNUR_OPEN_SLOT')

    def test_provisional_bmp_cells_carry_question_marks(self):
        """Tier B BMP gaps must render as ??? cells, never bare ranges."""
        s1 = read(os.path.join('S1', 'Roadmap', 'bmp_pua_roadmap.md'))
        for s, e in validator.TIER_B_BMP_PROVISIONAL_RANGES:
            bare = f"({s:04X}-{e:04X})"
            self.assertTrue(f"??? {bare}" in s1 or f"???{bare}" in s1,
                            f"S1 roadmap missing ??? marker for {bare}")

    def test_governance_distinction_is_explicit(self):
        """SPUCE supplies the definitions; RNUR owns Set 1 / Set 2."""
        spec = read(os.path.join('core', 'SPECIFICATION.md'))
        self.assertIn('SPUCE does not use RNUR', spec)
        for rel in (os.path.join('data', 'set1_master.csv'),
                    os.path.join('data', 'set2_sandbox.csv'),
                    os.path.join('UNIDATA', 'S1', 'Blocks.txt'),
                    os.path.join('UNIDATA', 'S2', 'Blocks.txt'),
                    os.path.join('S1', 'Roadmap', 'bmp_pua_roadmap.md'),
                    os.path.join('S2', 'Roadmap', 'bmp_pua_roadmap.md'),
                    os.path.join('core', 'SPECIFICATION.md')):
            text = read(rel)
            self.assertNotIn('SPUCE Set 1', text, f"{rel} uses 'SPUCE Set 1'")
            self.assertNotIn('SPUCE Set 2', text, f"{rel} uses 'SPUCE Set 2'")

    def test_full_invariant_check_passes_on_repository(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(validator.check_migration_invariants(BASE_DIR))
            self.assertTrue(validator.run_full_database_scan(BASE_DIR))


class Plane15October2026Tests(unittest.TestCase):
    """The 2026-10-19 Plane 15 reconciliation: the Fragments reduction, the
    UCSUR-origin classification of Hacm, Liparxe, Shaleian, and Visible Speech
    Extended-I, and the withdrawal of L8, with the seven UCSUR-included Plane 15
    scripts whose detailed proposals are not yet written charted as `¿...?`
    inside the UCSUR-Only (🟩) class."""

    def setUp(self):
        self.blocks = validator.load_blocks(
            os.path.join(BASE_DIR, 'UNIDATA', 'S1', 'Blocks.txt'))
        self.blocks_text = read(os.path.join('UNIDATA', 'S1', 'Blocks.txt'))
        self.roadmap = read(os.path.join('S1', 'Roadmap', 'spua-a_roadmap.md'))
        self.spec = read(os.path.join('core', 'SPECIFICATION.md'))
        self.csv = csv_rows(os.path.join('data', 'set1_master.csv'))

    def test_fragments_allocation_reduced(self):
        self.assertIn((0xFFFC0, 0xFFFEF, 'Fragments'), self.blocks)
        self.assertNotIn((0xFFF00, 0xFFFEF, 'Fragments'), self.blocks)
        self.assertEqual(0xFFFEF - 0xFFFC0 + 1, 48)

    def test_released_range_is_provisional_open_slot(self):
        self.assertIn((0xFFF00, 0xFFFBF, 'PROVISIONAL_RNUR_OPEN_SLOT'), self.blocks)
        self.assertEqual(0xFFFBF - 0xFFF00 + 1, 192)
        self.assertIn('??? (FFF00–FFFBF)', self.roadmap)
        self.assertIn('🟥 Fragments (FFFC0–FFFEF)', self.roadmap)
        self.assertIn('`U+FFF00`–`U+FFFBF`', self.spec)
        self.assertIn('`FFFC0–FFFEF`', self.spec)

    def test_ucsur_origin_scripts_are_reconciled(self):
        expected = {
            (0xF2700, 0xF27FF, '¿Hacm?'),
            (0xF2800, 0xF282F, '¿Liparxe?'),
            (0xF2830, 0xF289F, '¿Shaleian?'),
            (0xF2900, 0xF295F, '¿Visible Speech Extended-I?'),
        }
        for block in expected:
            self.assertIn(block, self.blocks)
        for marker in ('¿Hacm?', '¿Liparxe?', '¿Shaleian?',
                       '¿Visible Speech Extended-I?'):
            self.assertIn(marker, self.blocks_text)
            self.assertIn(marker, self.roadmap)

    def test_blocks_sections_reflect_ownership(self):
        green = self.blocks_text.split(
            '# --- UCSUR-Only Allocations (🟩) ---', 1)[1].split(
            '# --- SPUCE Project Allocations (🟥) ---', 1)[0]
        spuce = self.blocks_text.split(
            '# --- SPUCE Project Allocations (🟥) ---', 1)[1].split(
            '# --- SPUCE Project Allocations (Reserved for', 1)[0]

        for name in ('¿Hacm?', '¿Liparxe?', '¿Shaleian?',
                     '¿Visible Speech Extended-I?', 'Zbalermorna'):
            self.assertIn(name, green)
            self.assertNotIn(name, spuce)
        # The `¿...?` scripts are UCSUR-included, so they are charted in the
        # same UCSUR-Only (🟩) class -- not in a separate "unconfirmed" section.
        for name in ('¿Sitelen Pona Extended-A?', '¿Sitelen Pona Extended-B?',
                     '¿Quikscript?'):
            self.assertIn(name, green)
            self.assertNotIn(name, spuce)
        self.assertNotIn('Unconfirmed by UCSUR', self.blocks_text)

    def test_roadmap_cells_use_reconciled_colors(self):
        for cell in (
            '🟩 ¿Hacm? (F2700–F27FF)',
            '🟩 ¿Liparxe? (F2800–F282F)',
            '🟩 ¿Shaleian? (F2830–F289F)',
            '🟩 ¿Visible Speech Extended-I? (F2900–F295F)',
            '🟩 Zbalermorna (F28A0–F28DF)',
            '🟩 ¿Sitelen Pona Extended-A? (F1A00–F1AFF)',
            '🟩 ¿Sitelen Pona Extended-B? (F1F00–F1FFF)',
            '🟩 ¿Quikscript? (F2680–F26AF)',
        ):
            self.assertIn(cell, self.roadmap)

    def test_csv_does_not_track_ucsur_allocations(self):
        by_name = {r['Script_Name'] for r in self.csv}
        for name in ('Hacm', 'Liparxe', 'Shaleian', 'Visible Speech Extended-I',
                     'Visible Speech Extended', 'Zbalermorna'):
            self.assertNotIn(name, by_name)

    def test_csv_tracks_released_range(self):
        rows = [r for r in self.csv
                if r['Script_Name'] == 'PROVISIONAL_RNUR_OPEN_SLOT'
                and validator.parse_hex(r['End_Code_Point']) == 0xFFFBF]
        self.assertEqual(len(rows), 1)
        self.assertEqual(validator.parse_hex(rows[0]['Start_Code_Point']), 0xFFF00)

    def test_spec_documents_reconciliation(self):
        self.assertIn('`U+FFFF0`–`U+FFFFF`', self.spec)
        self.assertNotIn('`U+FFF00`–`U+FFFFF`', self.spec)
        self.assertIn('Visible Speech Extended-I', self.spec)
        self.assertIn('UCSUR-only allocations (🟩)', self.spec)
        self.assertIn('allocated in UCSUR rather than CSUR', self.spec)
        self.assertIn('observed font usage', self.spec)
        self.assertIn('public SPUCE Plane 15 Roadmap still showed the pre-reduction', self.spec)

    def test_withdrawn_plane15_allocations_removed(self):
        # L8 (FE7E0–FE7FF) was withdrawn by its creator, and the current public
        # SPUCE Plane 15 Roadmap renders the whole FE780–FE7FF tail as blank
        # erictom333-reserved space (Gerudo/Gerudo Presentation Forms no longer
        # appear in the FE7xx row there either).
        self.assertIn((0xFE780, 0xFE7FF, 'Layout Sandbox Space (erictom333 Reserved)'),
                      self.blocks)
        for block in ((0xFE780, 0xFE79F, 'Gerudo'),
                      (0xFE7A0, 0xFE7DF, 'Gerudo Presentation Forms'),
                      (0xFE7E0, 0xFE7FF, 'L8')):
            self.assertNotIn(block, self.blocks)
        self.assertNotIn('L8', self.blocks_text)
        for cell in ('🟨 L8 (FE7E0–FE7FF)',
                     '🟨 Gerudo (FE780–FE79F)',
                     '🟨 Gerudo Presentation Forms (FE7A0–FE7DF)'):
            self.assertNotIn(cell, self.roadmap)
        self.assertIn('🟨 Layout Sandbox Space (FE780–FE7FF)', self.roadmap)
        self.assertIn('FED80–FEDAF', self.roadmap)  # unrelated FEDxx Gerudo kept

    def test_question_mark_notation_means_missing_detailed_proposal(self):
        # `¿Script Name?` marks a UCSUR-included script whose detailed proposal
        # has not yet been written. It is a proposal-completeness marker and is
        # NOT an "unconfirmed by UCSUR" flag.
        seven = ((0xF2700, 0xF27FF, '¿Hacm?'),
                 (0xF2800, 0xF282F, '¿Liparxe?'),
                 (0xF2830, 0xF289F, '¿Shaleian?'),
                 (0xF2900, 0xF295F, '¿Visible Speech Extended-I?'),
                 (0xF1A00, 0xF1AFF, '¿Sitelen Pona Extended-A?'),
                 (0xF1F00, 0xF1FFF, '¿Sitelen Pona Extended-B?'),
                 (0xF2680, 0xF26AF, '¿Quikscript?'))
        for block in seven:
            self.assertIn(block, self.blocks)
        for text in (self.spec, self.roadmap):
            self.assertIn(
                'UCSUR-included script whose detailed proposal has not yet '
                'been written', text)
        self.assertIn('proposal-completeness marker', self.spec)

    def test_affected_scripts_are_not_marked_unconfirmed(self):
        self.assertNotIn('Unconfirmed by UCSUR', self.blocks_text)
        self.assertNotIn('Unconfirmed by UCSUR', self.roadmap)
        for old_cell in ('⬛ ¿Sitelen Pona Extended-A? (F1A00–F1AFF)',
                         '⬛ ¿Sitelen Pona Extended-B? (F1F00–F1FFF)',
                         '⬛ ¿Quikscript? (F2680–F26AF)'):
            self.assertNotIn(old_cell, self.roadmap)

    def test_question_mark_allocations_unchanged(self):
        # The semantics correction must not move, resize, or reassign ranges.
        expected = {
            (0xF2700, 0xF27FF, '¿Hacm?'): 256,
            (0xF2800, 0xF282F, '¿Liparxe?'): 48,
            (0xF2830, 0xF289F, '¿Shaleian?'): 112,
            (0xF2900, 0xF295F, '¿Visible Speech Extended-I?'): 96,
            (0xF1A00, 0xF1AFF, '¿Sitelen Pona Extended-A?'): 256,
            (0xF1F00, 0xF1FFF, '¿Sitelen Pona Extended-B?'): 256,
            (0xF2680, 0xF26AF, '¿Quikscript?'): 48,
        }
        for block, size in expected.items():
            self.assertIn(block, self.blocks)
            self.assertEqual(block[1] - block[0] + 1, size)

    def test_provisional_slot_notation_stays_distinct(self):
        # `???` continues to mean the Provisional RNUR Open Slot and must not be
        # merged with the `¿...?` proposal-completeness marker.
        self.assertIn((0xFFF00, 0xFFFBF, 'PROVISIONAL_RNUR_OPEN_SLOT'),
                      self.blocks)
        self.assertIn('??? (FFF00–FFFBF)', self.roadmap)
        self.assertIn('Provisional RNUR Open Slot', self.roadmap)
        self.assertIn('PROVISIONAL_RNUR_OPEN_SLOT', self.spec)
        provisional = {n for _, _, n in self.blocks
                       if n == 'PROVISIONAL_RNUR_OPEN_SLOT'}
        for name in ('¿Sitelen Pona Extended-A?', '¿Sitelen Pona Extended-B?',
                     '¿Quikscript?'):
            self.assertNotIn(name, provisional)


class UnidataMirrorTests(unittest.TestCase):
    """The UNIDATA mirrors must follow the Placeholder relocation exactly."""

    def _data_rows(self, rel):
        rows = []
        for line in read(rel).splitlines():
            if not line or line.startswith('#'):
                continue
            rows.append(line)
        return rows

    def test_set2_unicodedata_holds_the_full_relocated_repertoire(self):
        rows = self._data_rows(os.path.join('UNIDATA', 'S2', 'UnicodeData.txt'))
        self.assertEqual(len(rows), 352)
        cps = [int(r.split(';')[0], 16) for r in rows]
        self.assertEqual(cps, list(range(0xE9A0, 0xEB00)))
        self.assertEqual(len(set(cps)), 352)
        for r in rows:
            self.assertEqual(r.split(';')[1], 'PLACEHOLDER-' + r.split(';')[0])

    def test_set2_nameslist_holds_the_full_relocated_repertoire(self):
        rows = self._data_rows(os.path.join('UNIDATA', 'S2', 'NamesList.txt'))
        self.assertEqual(len(rows), 352)
        cps = [int(r.split()[0], 16) for r in rows]
        self.assertEqual(cps, list(range(0xE9A0, 0xEB00)))

    def test_set1_unicodedata_no_longer_holds_the_bmp_repertoire(self):
        rows = self._data_rows(os.path.join('UNIDATA', 'S1', 'UnicodeData.txt'))
        cps = [int(r.split(';')[0], 16) for r in rows]
        self.assertFalse([c for c in cps if 0xF5C0 <= c <= 0xF71F],
                         "Set 1 still carries the relocated BMP repertoire")
        # the separate SPUCE Plane 15 Placeholder allocation is untouched
        self.assertTrue([c for c in cps if 0xF92C0 <= c <= 0xF941F])

    def test_case_folding_shifts_with_the_repertoire(self):
        """The folding block must keep the original shape (26 pairs, +0x1A)."""
        rows = []
        for line in read(os.path.join('UNIDATA', 'S2', 'CaseFolding.txt')).splitlines():
            if not line or line.startswith('#'):
                continue
            src, status, dst = [p.strip() for p in line.split(';')[:3]]
            rows.append((int(src, 16), status, int(dst, 16)))
        self.assertEqual(len(rows), 26)
        for i, (src, status, dst) in enumerate(rows):
            self.assertEqual(src, 0xE9A0 + i)
            self.assertEqual(status, 'C')
            self.assertEqual(dst, src + 0x1A)
        self.assertEqual(rows[-1][2], 0xE9D3)


class RoadmapGridGeometryTests(unittest.TestCase):
    """Every BMP grid cell must cover exactly the range it is labelled with."""

    _ROW = re.compile(r'<td align="center"><b>([0-9A-F]{2})xx</b></td>')
    _CELL = re.compile(r'<td colspan="(\d+)"[^>]*>.*?\(([0-9A-F]{4})-([0-9A-F]{4})\)</td>')

    def _rows(self, rel_path):
        lines = read(rel_path).splitlines()
        rows = []
        i = 0
        while i < len(lines):
            m = self._ROW.search(lines[i])
            if not m:
                i += 1
                continue
            cells = []
            j = i + 1
            while j < len(lines) and '</tr>' not in lines[j]:
                cm = self._CELL.search(lines[j])
                if cm:
                    cells.append((int(cm.group(1)), cm.group(2), cm.group(3)))
                j += 1
            rows.append((m.group(1), cells))
            i = j + 1
        return rows

    def test_bmp_grid_cells_match_their_spans(self):
        for rel_path in (os.path.join('S1', 'Roadmap', 'bmp_pua_roadmap.md'),
                         os.path.join('S2', 'Roadmap', 'bmp_pua_roadmap.md')):
            rows = self._rows(rel_path)
            self.assertTrue(rows, f"no grid rows found in {rel_path}")
            for prefix, cells in rows:
                total = sum(c[0] for c in cells)
                self.assertEqual(total, 16,
                                 f"{rel_path} row {prefix}xx spans {total} columns")
                cursor = int(prefix + '00', 16)
                for colspan, start, end in cells:
                    expected_end = cursor + colspan * 16 - 1
                    self.assertEqual(int(start, 16), cursor,
                                     f"{rel_path} row {prefix}xx cell {start} misaligned")
                    self.assertEqual(int(end, 16), expected_end,
                                     f"{rel_path} row {prefix}xx cell {start}-{end} "
                                     f"does not match its colspan={colspan}")
                    cursor = expected_end + 1
                self.assertEqual(cursor - 1, int(prefix + 'FF', 16),
                                 f"{rel_path} row {prefix}xx does not fill the row")


class NegativeDetectionTests(unittest.TestCase):
    """The validators must actually fail on regressions (mutant repositories)."""

    def _mutant(self, mutate):
        tmp = tempfile.mkdtemp(prefix='rnur-mutant-')
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        for part in ('data', 'UNIDATA', 'core', os.path.join('S1', 'Roadmap'),
                     os.path.join('S2', 'Roadmap')):
            src = os.path.join(BASE_DIR, part)
            dst = os.path.join(tmp, part)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copytree(src, dst, dirs_exist_ok=True)
        mutate(tmp)
        return tmp

    def _run_quiet(self, func, tmp):
        with contextlib.redirect_stdout(io.StringIO()):
            return func(tmp)

    def _append_csv(self, tmp, name, line):
        with open(os.path.join(tmp, 'data', name), 'a', encoding='utf-8') as f:
            f.write(line + '\n')

    def _replace_in_file(self, tmp, rel_path, old, new):
        path = os.path.join(tmp, rel_path)
        with open(path, encoding='utf-8') as f:
            text = f.read()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text.replace(old, new))

    def test_detects_reintroduced_displaced_script(self):
        def mutate(tmp):
            self._append_csv(tmp, 'set1_master.csv',
                             '1,U+EE10,U+EE5F,Loopiform,Nobody,Provisional Lease / '
                             'Pending Upstream Ratification,"regression",NONE')
        self.assertFalse(self._run_quiet(validator.check_migration_invariants, self._mutant(mutate)))

    def test_detects_reintroduced_provisional_reservation(self):
        def mutate(tmp):
            self._append_csv(tmp, 'set1_master.csv',
                             '1,U+EE60,U+EE8F,PROVISIONAL_RNUR_OPEN_SLOT,NONE,'
                             'Provisional Allocation / Open for Submission,"??? regression",NONE')
        self.assertFalse(self._run_quiet(validator.check_migration_invariants, self._mutant(mutate)))

    def test_detects_provisional_migrated_into_set2(self):
        def mutate(tmp):
            self._append_csv(tmp, 'set2_sandbox.csv',
                             '2,U+EA00,U+EA2F,PROVISIONAL_RNUR_OPEN_SLOT,NONE,Active,"??? regression"')
        self.assertFalse(self._run_quiet(validator.check_migration_invariants, self._mutant(mutate)))

    def test_detects_moved_constantscript(self):
        def mutate(tmp):
            self._replace_in_file(tmp, os.path.join('data', 'set2_sandbox.csv'),
                                  '2,U+E000,U+E81F,Constantscript',
                                  '2,U+E000,U+E80F,Constantscript')
        self.assertFalse(self._run_quiet(validator.check_migration_invariants, self._mutant(mutate)))

    def test_detects_wrong_relocation_destination(self):
        def mutate(tmp):
            self._replace_in_file(tmp, os.path.join('data', 'set2_sandbox.csv'),
                                  '2,U+E830,U+E87F,Loopiform',
                                  '2,U+E830,U+E880,Loopiform')
        self.assertFalse(self._run_quiet(validator.check_migration_invariants, self._mutant(mutate)))

    def test_detects_spuce_gap(self):
        def mutate(tmp):
            self._replace_in_file(tmp, os.path.join('data', 'set1_master.csv'),
                                  '1,U+EE30,U+EE5F,Gallifreyan',
                                  '1,U+EE31,U+EE5F,Gallifreyan')
        self.assertFalse(self._run_quiet(validator.check_migration_invariants, self._mutant(mutate)))

    def test_detects_removed_placeholder(self):
        def mutate(tmp):
            path = os.path.join(tmp, 'data', 'set2_sandbox.csv')
            with open(path, encoding='utf-8') as f:
                lines = f.readlines()
            with open(path, 'w', encoding='utf-8') as f:
                for line in lines:
                    if ',Placeholder,' not in line:
                        f.write(line)
        self.assertFalse(self._run_quiet(validator.check_migration_invariants, self._mutant(mutate)))

    def test_detects_placeholder_left_in_set1(self):
        def mutate(tmp):
            self._append_csv(tmp, 'set1_master.csv',
                             '1,U+F5C0,U+F71F,Placeholder,NONE,Provisional Lease / '
                             'Pending Upstream Ratification,"regression",NONE')
        self.assertFalse(self._run_quiet(validator.check_migration_invariants, self._mutant(mutate)))

    def test_detects_placeholder_with_wrong_set2_destination(self):
        def mutate(tmp):
            self._replace_in_file(tmp, os.path.join('data', 'set2_sandbox.csv'),
                                  '2,U+E9A0,U+EAFF,Placeholder',
                                  '2,U+E9A0,U+EAFF,PlaceholderX')
        self.assertFalse(self._run_quiet(validator.check_migration_invariants, self._mutant(mutate)))

    def test_detects_placeholder_resizing(self):
        def mutate(tmp):
            self._replace_in_file(tmp, os.path.join('data', 'set2_sandbox.csv'),
                                  '2,U+E9A0,U+EAFF,Placeholder',
                                  '2,U+E9A0,U+EAEF,Placeholder')
        self.assertFalse(self._run_quiet(validator.check_migration_invariants, self._mutant(mutate)))

    def test_detects_missing_set1_subdivision_range(self):
        def mutate(tmp):
            path = os.path.join(tmp, 'data', 'set1_master.csv')
            with open(path, encoding='utf-8') as f:
                lines = f.readlines()
            with open(path, 'w', encoding='utf-8') as f:
                for line in lines:
                    if '1,U+F700,U+F71F,PROVISIONAL_RNUR_OPEN_SLOT' not in line:
                        f.write(line)
        self.assertFalse(self._run_quiet(validator.check_migration_invariants, self._mutant(mutate)))

    def test_detects_subdivision_range_with_placeholder_residue(self):
        def mutate(tmp):
            self._replace_in_file(
                tmp, os.path.join('data', 'set1_master.csv'),
                'Vacated by the SPUCE allocation update of 2026-10-22',
                'Vacated by the relocation of the Placeholder allocation')
        self.assertFalse(self._run_quiet(validator.check_migration_invariants, self._mutant(mutate)))

    def test_detects_subdivision_range_not_marked_spuce(self):
        def mutate(tmp):
            self._replace_in_file(tmp, os.path.join('data', 'set1_master.csv'),
                                  '1,U+F600,U+F6FF,Miscellaneous Symbols Extended-I,SPUCE,SPUCE Allocation',
                                  '1,U+F600,U+F6FF,Miscellaneous Symbols Extended-I,NONE,Provisional Allocation / Open for Submission')
        self.assertFalse(self._run_quiet(validator.check_migration_invariants, self._mutant(mutate)))

    def test_detects_governance_violation(self):
        def mutate(tmp):
            self._replace_in_file(tmp, os.path.join('core', 'SPECIFICATION.md'),
                                  'Governance distinction.',
                                  'SPUCE Set 1 note.')
        self.assertFalse(self._run_quiet(validator.check_migration_invariants, self._mutant(mutate)))

    def test_detects_tier_a_claiming_provisional_gap(self):
        def mutate(tmp):
            self._replace_in_file(
                tmp, os.path.join('core', 'SPECIFICATION.md'),
                'permanent structural space tracking slots of Plane 16.',
                'permanent structural space tracking slots of Plane 16 '
                '(including U+F720-U+F7FF).')
        self.assertFalse(self._run_quiet(validator.check_migration_invariants, self._mutant(mutate)))

    def test_detects_provisional_cell_missing_question_marks(self):
        def mutate(tmp):
            self._replace_in_file(tmp, os.path.join('S1', 'Roadmap', 'bmp_pua_roadmap.md'),
                                  '??? (F820-F87F)',
                                  '(F820-F87F)')
        self.assertFalse(self._run_quiet(validator.check_migration_invariants, self._mutant(mutate)))

    def test_detects_overlap_within_set(self):
        def mutate(tmp):
            self._append_csv(tmp, 'set1_master.csv',
                             '1,U+EE20,U+EE40,Overlap Test,Nobody,SPUCE Allocation,"overlap",SPUCE')
        self.assertFalse(self._run_quiet(validator.run_full_database_scan, self._mutant(mutate)))

    def test_invalid_inclusive_range_detected(self):
        def mutate(tmp):
            self._append_csv(tmp, 'set1_master.csv',
                             '1,U+EE40,U+EE20,Backwards Range,Nobody,SPUCE Allocation,"bad",SPUCE')
        self.assertFalse(self._run_quiet(validator.run_full_database_scan, self._mutant(mutate)))


class HelperTests(unittest.TestCase):
    def test_check_overlap_boundaries(self):
        self.assertTrue(validator.check_overlap(0xEE00, 0xEE0F, 0xEE0F, 0xEE20))
        self.assertFalse(validator.check_overlap(0xEE00, 0xEE0F, 0xEE10, 0xEE20))

    def test_inclusive_size(self):
        self.assertEqual(validator.inclusive_size(0xEE00, 0xEE2F), 48)
        self.assertEqual(validator.inclusive_size(0xEF70, 0xEFFF), 144)


if __name__ == '__main__':
    unittest.main()
