import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from storyo.grammar import Grammar, NodeDefinition, Reference
from storyo.graph_audit import summarize_reference_graph


class ReferenceGraphAuditTests(unittest.TestCase):
    def test_reports_topology_without_relabeling_edges(self):
        g = Grammar("fixture", "1", "test", "1",
                    nodes=(NodeDefinition("a", "variant"), NodeDefinition("b", "conflict"),
                           NodeDefinition("isolated", "master-clause")),
                    references=(Reference("r1", "a", "b", direction="carryon"),))
        report = summarize_reference_graph(g)
        self.assertEqual(report["counts"]["references"], 1)
        self.assertEqual(report["counts"]["reference_directions"], {"carryon": 1})
        self.assertEqual(report["counts"]["reference_endpoint_node_types"], {"variant->conflict": 1})
        self.assertEqual(report["connectivity"]["weak_component_count"], 2)
        self.assertEqual(report["connectivity"]["isolated_node_count"], 1)
        self.assertIn("no causal", report["interpretation_guard"])

    def test_top_n_must_be_nonnegative(self):
        with self.assertRaises(ValueError):
            summarize_reference_graph(Grammar("g", "1", "test", "1"), top_n=-1)


if __name__ == "__main__":
    unittest.main()
