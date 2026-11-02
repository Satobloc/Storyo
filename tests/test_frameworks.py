import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from storyo.frameworks import load_template_catalog


class FrameworkTemplateTests(unittest.TestCase):
    def test_user_frameworks_load_and_source_hashes_match(self):
        templates = load_template_catalog(
            ROOT / "docs/frameworks/structural-templates.v0.1.json", source_root=ROOT
        )
        self.assertEqual({x.template_id for x in templates}, {
            "storyo.bio-tragic-loop", "storyo.vignette-expansion"
        })
        bio, vignette = templates
        self.assertEqual(len(bio.source_assertions), 2)
        self.assertTrue(all(x["status"] == "author_asserted" for x in bio.source_assertions))
        self.assertEqual(len(bio.source_structures["emotional_spine_order"]), 5)
        phase = next(x for x in bio.elements if x.element_id == "revelatory_scene")
        self.assertIn("Awe and revulsion coexist", phase.attributes["description"])
        self.assertEqual(vignette.source_structures["placement_rule"], "thematic resonance, not chronology")
        core_step = next(x for x in vignette.elements if x.element_id == "identify_core")
        self.assertTrue(core_step.attributes["goal"])
        self.assertTrue(core_step.attributes["actions"])
        self.assertTrue(core_step.attributes["output"])
        self.assertIn("microstage_1", {x.element_id for x in vignette.elements})

    def test_template_relations_are_not_world_causal_edges(self):
        templates = load_template_catalog(
            ROOT / "docs/frameworks/structural-templates.v0.1.json", source_root=ROOT
        )
        for template in templates:
            self.assertTrue(all(r.scope == "template" for r in template.relations))
            self.assertFalse(any(r.relation_type == "causal" for r in template.relations))


if __name__ == "__main__":
    unittest.main()
