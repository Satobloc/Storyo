import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from storyo.grammar import Grammar, NodeDefinition, Reference
from storyo.reference_paths import find_reference_paths


class ReferencePathTests(unittest.TestCase):
    def setUp(self):
        self.g = Grammar("fixture", "1", "test", "1",
                         nodes=tuple(NodeDefinition(x, "conflict") for x in "ABCD"),
                         references=(Reference("r1", "A", "B", direction="carryon"),
                                     Reference("r2", "B", "D", direction="carryon"),
                                     Reference("r3", "A", "C", direction="leadup"),
                                     Reference("r4", "C", "D", direction="carryon")))

    def test_finds_shortest_reference_paths_deterministically(self):
        paths = find_reference_paths(self.g, "A", "D", max_edges=4)
        self.assertEqual([p.reference_ids for p in paths], [("r1", "r2"), ("r3", "r4")])

    def test_direction_filter_is_exact(self):
        paths = find_reference_paths(self.g, "A", "D", directions={"carryon"})
        self.assertEqual([p.reference_ids for p in paths], [("r1", "r2")])

    def test_no_path_is_not_proof_of_nonexistence(self):
        self.assertEqual(find_reference_paths(self.g, "A", "D", max_edges=1), ())

    def test_unknown_node_and_bad_bounds_fail(self):
        with self.assertRaises(KeyError):
            find_reference_paths(self.g, "X", "D")
        with self.assertRaises(ValueError):
            find_reference_paths(self.g, "A", "D", max_edges=-1)


if __name__ == "__main__":
    unittest.main()
