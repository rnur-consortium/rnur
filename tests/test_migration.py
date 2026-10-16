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
        self.assertEqual(validator.parse_hex(sandbox[0]['Start_Code_Point']), 0xE9A0)

    def test_named_placeholder_allocation_preserved(self):
        names = [r['Script_Name'] for r in self.s1
                 if validator.parse_hex(r['Start_Code_Point']) == 0xF5C0]
        self.assertIn('Placeholder', names)
        for row in self.s2:
            self.assertNotEqual(row['Project_Name'], 'Placeholder')


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
        # placeholder survives
        self.assertIn((0xF5C0, 0xF71F, 'Placeholder'), blocks)

    def test_set2_blocks_contains_relocations(self):
        blocks = validator.load_blocks(os.path.join(BASE_DIR, 'UNIDATA', 'S2', 'Blocks.txt'))
        self.assertIn((0xE000, 0xE81F, 'Constantscript'), blocks)
        for name, _, _, new_s, new_e in validator.RELOCATED_SCRIPTS:
            self.assertIn((new_s, new_e, name), blocks)
        self.assertIn((0xE9A0, 0xF8FF, 'OPEN_SLOT'), blocks)
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
            path = os.path.join(tmp, 'data', 'set1_master.csv')
            with open(path, encoding='utf-8') as f:
                lines = f.readlines()
            with open(path, 'w', encoding='utf-8') as f:
                for line in lines:
                    if ',Placeholder,' not in line:
                        f.write(line)
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
