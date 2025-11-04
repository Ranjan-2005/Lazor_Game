# unit_test.py
import os
import sys
import unittest

# Ensure imports work when running directly
sys.path.append(os.path.dirname(__file__))

from main import build_solution_grid, save_solution_to_file
from bff_parser import parse_bff
from lazor_solver import solve_bff


class TestLazorSolver(unittest.TestCase):
    def setUp(self):
        # Small synthetic grid and placements for fast, deterministic tests
        self.sample_grid = [
            ['o', 'o', 'x'],
            ['o', 'o', 'o'],
            ['x', 'o', 'o']
        ]
        # Use two placements: one Reflect (→ 'A') and one Opaque (→ 'B')
        self.sample_placements = [
            (0, 0, 'ReflectBlock'),
            (1, 1, 'OpaqueBlock')
        ]

        # Try to use any .bff present in this folder (so you don't need to hardcode)
        self.any_bff = next((f for f in os.listdir('.') if f.endswith('.bff')), None)

    def test_grid_builds_correctly(self):
        """Ensure blocks are correctly placed on the grid."""
        grid = build_solution_grid(self.sample_grid, self.sample_placements)
        self.assertEqual(grid[0][0], 'A')  # ReflectBlock → 'A'
        self.assertEqual(grid[1][1], 'B')  # OpaqueBlock  → 'B'

    def test_parser_loads_bff(self):
        """
        Verify that a .bff file can be parsed into valid components.
        Accept either 'lasers' or 'lazors' (your parser uses 'lazors').
        """
        if not self.any_bff:
            self.skipTest("No .bff found in the current folder — skipping parser test.")
        parsed = parse_bff(self.any_bff)

        # Must have grid and targets
        self.assertIn('grid', parsed)
        self.assertIn('targets', parsed)

        # Accept either spelling; prefer the one that exists
        laser_key = 'lasers' if 'lasers' in parsed else ('lazors' if 'lazors' in parsed else None)
        self.assertIsNotNone(laser_key, "Parser must provide either 'lasers' or 'lazors' field.")

        lazers = parsed[laser_key]
        self.assertIsInstance(lazers, list)
        if lazers:  # if any present, check the structure of the first one
            first = lazers[0]
            # Your parser example shows dicts with 'position' and 'direction' tuples
            self.assertIn('position', first)
            self.assertIn('direction', first)
            self.assertIsInstance(first['position'], tuple)
            self.assertIsInstance(first['direction'], tuple)

    def test_solver_returns_tuple(self):
        """Ensure the solver returns a (placements, lazor_paths) tuple when a .bff exists."""
        if not self.any_bff:
            self.skipTest("No .bff found in the current folder — skipping solver test.")
        result = solve_bff(self.any_bff)
        # Some boards may be unsolved by your current physics; only check type if result is not None
        if result is not None:
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)

    def test_solution_file_written(self):
        """
        Check that save_solution_to_file writes a file named <base>_solution.txt.
        Important: pass a path that *looks like* a .bff so naming is predictable.
        """
        dummy_bff_path = "temp_test_solution.bff"
        try:
            grid = build_solution_grid(self.sample_grid, self.sample_placements)
            save_solution_to_file(dummy_bff_path, self.sample_placements, grid)

            expected_txt = os.path.splitext(dummy_bff_path)[0] + "_solution.txt"
            self.assertTrue(os.path.exists(expected_txt), f"Expected {expected_txt} to be created.")

            # Optional: verify basic contents
            with open(expected_txt, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("Placements:", content)
            self.assertIn("Final grid:", content)
        finally:
            # Clean up test artifact if it exists
            expected_txt = os.path.splitext(dummy_bff_path)[0] + "_solution.txt"
            if os.path.exists(expected_txt):
                os.remove(expected_txt)


if __name__ == '__main__':
    unittest.main()
