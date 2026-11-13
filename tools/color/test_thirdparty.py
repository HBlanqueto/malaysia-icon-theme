import io, os, sys, unittest

import resvg_py
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import thirdparty

SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{}</svg>'
BRIGHT_WITH_PURPLE_SHADOW = SVG.format('<rect width="100" height="70" fill="#ffd34d"/><rect y="70" width="100" height="30" fill="#6a1b9a"/>')
DARK_WITH_YELLOW_LIGHT = SVG.format('<rect width="100" height="70" fill="#2a1038"/><rect y="70" width="100" height="30" fill="#ffd34d"/>')
GRAY = SVG.format('<rect width="100" height="100" fill="#808080"/>')


def plate_of(svg):
    image = Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=svg, width=64))).convert("RGBA")
    return thirdparty.plate_lobe(list(thirdparty.pixels(image)))


class PlateRule(unittest.TestCase):
    def test_a_bright_logo_takes_the_hue_of_its_darkest_color(self):
        lobe, bright = plate_of(BRIGHT_WITH_PURPLE_SHADOW)
        self.assertTrue(bright)
        self.assertTrue(290 < lobe.hue < 340)

    def test_a_dark_logo_takes_the_hue_of_its_lightest_color(self):
        lobe, bright = plate_of(DARK_WITH_YELLOW_LIGHT)
        self.assertFalse(bright)
        self.assertTrue(70 < lobe.hue < 120)

    def test_a_gray_logo_has_no_hue_to_take(self):
        self.assertIsNone(plate_of(GRAY)[0])

    def test_duplicated_ids_and_their_references_are_renamed_together(self):
        renamed = thirdparty.suffix_ids('<g id="a"><path fill="url(#a)"/><use href="#a"/><path fill="#fff" id="b"/></g>', "-s")
        self.assertEqual(renamed, '<g id="a-s"><path fill="url(#a-s)"/><use href="#a-s"/><path fill="#fff" id="b-s"/></g>')


if __name__ == "__main__":
    unittest.main()
