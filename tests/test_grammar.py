import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from storyo.grammar import Grammar, NodeDefinition, Reference, ReferenceGroup, GroupMode, SegmentAddress, deterministic_choose
from storyo.plotto_adapter import PlottoAdapter
from storyo.graph_boundaries import import_references_as_dependencies

class GrammarTests(unittest.TestCase):
    def test_segment_address_is_content_addressed(self):
        text = "alpha * beta"
        address = SegmentAddress.from_text("fixture", text, 0, 5)
        self.assertEqual(address.resolve(text), "alpha")
        with self.assertRaises(ValueError):
            address.resolve(text + " changed")

    def test_group_semantics_are_explicit(self):
        grammar = Grammar("g","1","test","1",
            nodes=(NodeDefinition("a","conflict"),NodeDefinition("b","conflict")),
            references=(Reference("r","a","b"),),
            groups=(ReferenceGroup("choice",GroupMode.CHOOSE,("r",)),))
        grammar.validate()
        self.assertEqual(grammar.groups[0].mode,GroupMode.CHOOSE)

    def test_dangling_references_fail_validation(self):
        grammar = Grammar("g","1","test","1",nodes=(NodeDefinition("a","x"),),
            references=(Reference("r","a","missing"),))
        with self.assertRaises(ValueError):
            grammar.validate()

    def test_plotto_adapter_does_not_promote_reference_to_causality(self):
        grammar = PlottoAdapter().import_records({
            "source_version":"test-source","nodes":[{"id":"A"},{"id":"B"}],
            "references":[{"id":"R1","from":"A","to":"B","direction":"carry-on",
                "transformations":[{"operation":"transpose","target_role":"A"}]}],
            "groups":[{"id":"G1","mode":"choose","members":["R1"]}]})
        self.assertEqual(grammar.references[0].direction,"carry-on")
        self.assertEqual(grammar.references[0].transformations[0].kind.value,"transpose")
        self.assertEqual(grammar.metadata["causal_promotion"],"prohibited-by-default")
        with self.assertRaises(TypeError):
            import_references_as_dependencies(grammar.references)

    def test_deterministic_choice_receipt(self):
        a,ra=deterministic_choose(["x","y","z"],1234)
        b,rb=deterministic_choose(["x","y","z"],1234)
        self.assertEqual(a,b)
        self.assertEqual(ra,rb)
        self.assertEqual(ra.algorithm,"storyo-lcg32-v1")

if __name__ == "__main__":
    unittest.main()
