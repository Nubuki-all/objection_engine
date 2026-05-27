from enum import IntEnum
from objection_engine.loading import ASSETS_FOLDER

class TextType(IntEnum):
    DIALOGUE = 0
    NAME = 1

def get_font_array():
    return [
        # AA-Like > Pixel > Generic
        {'path': f'./{ASSETS_FOLDER}/textbox/font/igiari-cyrillic/igiari-cyrillic.ttf'},
        # AA-like, Latin, hiragana, katakana, (part of) cyrillic
        {'path': f'./{ASSETS_FOLDER}/textbox/font/igiari/Igiari.ttf'},
        # AA-like, Latin, hiragana, katakana, (part of) cyrillic
        {'path': f'./{ASSETS_FOLDER}/textbox/font/igiari/Galmuri11.ttf'},
        # Pixel, Kanji, Hiragana, Katakana
        {'path': f'./{ASSETS_FOLDER}/textbox/font/igiari/jackeyfont.ttf'},
        # Arabic
        {'path': f'./{ASSETS_FOLDER}/textbox/font/igiari/arabic-1.ttf', 'size': 12, 'offset': {TextType.NAME: (0, -5)}, 'rtl': True},
        # Pixel-font, Hebrew
        {'path': f'./{ASSETS_FOLDER}/textbox/font/igiari/STANRG__.ttf'},
        # Generic
        {'path': f'./{ASSETS_FOLDER}/textbox/font/igiari/NotoSans-Regular.ttf'},
        # Pixel font, Arabic
        {'path': f'./{ASSETS_FOLDER}/textbox/font/igiari/bitsy-font-with-arabic.ttf', 'size': 10, 'rtl': True},
    ]

def get_nametag_font_array():
    return [
        {'path': f'./{ASSETS_FOLDER}/textbox/font/ace-name/ace-name.ttf', 'size': 8}
    ] + get_font_array()

TEXT_COLORS = {
    "red": (240, 112, 56),
    "blue": (104, 192, 240),
    "green": (0, 240, 0)
}

MAX_LINE_WIDTH = 220
