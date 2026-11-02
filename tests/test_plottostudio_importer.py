import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from storyo.plottostudio_importer import import_plottostudio_html


class PlottoStudioImporterTests(unittest.TestCase):
    def test_import_preserves_source_spans_and_does_not_infer_causality(self):
        data = {
            "entries": [{"id": 1, "category": "Test", "variants": [{
                "key": "a", "text": "(2) A * B ** (3a)", "links": [
                    {"target": 2, "variant": "", "direction": "leadup",
                     "notation": "2", "operations": [], "status": "interpreted",
                     "source_variant": "a", "start": 0},
                    {"target": 3, "variant": "a", "direction": "carryon",
                     "notation": "3a", "operations": [{"op": "change", "from": "B", "to": "A"}],
                     "status": "unresolved_target_variant", "source_variant": "a", "start": 13}
                ]
            }]}, {"id": 2, "category": "Test", "variants": [{"key": "", "text": "C", "links": []}]},
                {"id": 3, "category": "Test", "variants": [{"key": "b", "text": "D", "links": []}]}],
            "master": {"A": [{"id": 1, "text": "A clause"}], "B": [], "C": []}
        }
        html = "<script>const DATA=" + json.dumps(data) + ";</script>"
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "fixture.html"
            path.write_text(html, encoding="utf-8")
            grammar = import_plottostudio_html(path)

        self.assertEqual(len(grammar.references), 2)
        self.assertEqual(grammar.references[0].direction, "leadup")
        self.assertEqual(grammar.references[0].source.resolve("(2) A * B ** (3a)"), "(2)")
        self.assertEqual(grammar.references[1].status, "unresolved_target_variant")
        self.assertEqual(grammar.references[1].transformations[0].kind.value, "change")
        self.assertIn("plotto:master:A:1", {n.node_id for n in grammar.nodes})
        self.assertEqual(grammar.metadata["causal_promotion"], "prohibited-by-default")

    def test_rejects_link_offset_that_does_not_start_at_parenthesis(self):
        data = {"entries": [{"id": 1, "variants": [{
            "key": "a", "text": "x (2)", "links": [{
                "target": 1, "variant": "", "direction": "leadup",
                "notation": "2", "operations": [], "status": "interpreted", "start": 0
            }]
        }]}]}
        html = "<script>const DATA=" + json.dumps(data) + ";</script>"
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "bad-offset.html"
            path.write_text(html, encoding="utf-8")
            with self.assertRaises(ValueError):
                import_plottostudio_html(path)


if __name__ == "__main__":
    unittest.main()
