import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "render_animated_diagram.py"


def load_renderer():
    spec = importlib.util.spec_from_file_location("render_animated_diagram", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TextFittingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.renderer = load_renderer()
        cls.image = Image.new("RGBA", (300, 160), (0, 0, 0, 0))
        cls.draw = ImageDraw.Draw(cls.image)

    def test_wraps_english_text_to_width(self):
        text, size, font = self.renderer.fit_text(
            self.draw,
            "long evidence synthesis label",
            90,
            44,
            16,
            min_size=10,
            bold=True,
        )

        width, height = self.renderer.text_size(self.draw, text, font)
        self.assertLessEqual(width, self.renderer.c(90))
        self.assertLessEqual(height, self.renderer.c(44))
        self.assertLessEqual(size, 16)
        self.assertIn("\n", text)

    def test_wraps_cjk_text_without_spaces(self):
        text, _, font = self.renderer.fit_text(
            self.draw,
            "研究问题收敛与证据综合",
            70,
            48,
            16,
            min_size=10,
        )

        width, height = self.renderer.text_size(self.draw, text, font)
        self.assertLessEqual(width, self.renderer.c(70))
        self.assertLessEqual(height, self.renderer.c(48))
        self.assertIn("\n", text)

    def test_preserves_words_when_label_height_is_tight(self):
        text, size, font = self.renderer.fit_text(
            self.draw,
            "Discover Evidence",
            100,
            28,
            20,
            min_size=15,
            hand=True,
            bold=True,
        )

        width, height = self.renderer.text_size(self.draw, text, font)
        self.assertLessEqual(width, self.renderer.c(100))
        self.assertLessEqual(height, self.renderer.c(28))
        self.assertLess(size, 15)
        self.assertIn("Discover", text)
        self.assertIn("Evidence", text)

    def test_preserves_all_text_when_fitting_is_impossible(self):
        text, _, _ = self.renderer.fit_text(
            self.draw,
            "alpha beta gamma delta epsilon",
            30,
            8,
            16,
            min_size=12,
        )

        flattened = text.replace("\n", " ")
        for word in ["alpha", "beta", "gamma", "delta", "epsilon"]:
            self.assertIn(word, flattened)

    def test_render_writes_wrapped_text_to_excalidraw(self):
        spec = json.loads((ROOT / "assets" / "default-spec.json").read_text(encoding="utf-8"))
        spec["decision"]["body"] = "checkpoint confirmation required"
        with tempfile.TemporaryDirectory() as tmp:
            result = self.renderer.write_outputs(spec, Path(tmp), "sample")
            excalidraw = json.loads(Path(result["excalidraw"]).read_text(encoding="utf-8"))

        text_values = [element["text"] for element in excalidraw["elements"] if element.get("type") == "text"]
        self.assertIn("checkpoint\nconfirmation\nrequired", text_values)


if __name__ == "__main__":
    unittest.main()
