# ===========================================================================
# QtVSCodeStyle.
#
#  Copyright (c) 2015 The Spyder development team
#  Copyright (c) 2021- Yunosuke Ohsugi
#
#  Distributed under the terms of the MIT License.
#   see https://github.com/spyder-ide/qtawesome/blob/master/LICENSE.txt
#
# Original code:
#   https://github.com/spyder-ide/qtawesome/blob/master/qtawesome/iconic_font.py
#
# (see NOTICE.md in the QtVSCodeStyle root directory for details)
# ============================================================================

from __future__ import annotations

from importlib import resources
from typing import Type, Union

from qtvscodestyle.base import global_current_colors
from qtvscodestyle.const import FaBrands, FaRegular, FaSolid, Vsc
from qtvscodestyle.qtpy.QtGui import QFont, QFontDatabase, QIcon
from qtvscodestyle.vscode.color import Color

from .iconic_font import CharIconEngine
from .svg import SVGBufferIconEngine

global_icon_engine_map: dict[str, list[Union[SVGBufferIconEngine, CharIconEngine]]] = {}

FONT_FILES = {FaSolid: "fa-solid-900.ttf", FaBrands: "fa-brands-400.ttf", FaRegular: "fa-regular-400.ttf"}
font_family_cash: dict[Union[Type[FaSolid], Type[FaBrands], Type[FaRegular]], str] = {}

FontIdentifier = Union[FaSolid, FaRegular, FaBrands]


class FontError(Exception):
    """Exception for font errors."""


def load_font_family(font_identifier: FontIdentifier) -> str:
    font_file = FONT_FILES[font_identifier.__class__]
    font_data = resources.read_binary("qtvscodestyle.fonts", font_file)
    id = QFontDatabase.addApplicationFontFromData(font_data)
    font_families = QFontDatabase.applicationFontFamilies(id)

    if len(font_families) == 0:
        with resources.path("qtvscodestyle.fonts", font_file) as font_path:
            pass
        raise FontError(
            f"Font at '{font_path}' appears to be empty. "
            "If you are on Windows 10, please read "
            "https://support.microsoft.com/"
            "en-us/kb/3053676 "
            "to know how to prevent Windows from blocking "
            "the fonts that come with QtAwesome."
        )

    font_family_cash[font_identifier.__class__] = font_families[0]
    return font_families[0]


def _iconic_icon_engine(icon_id: FontIdentifier, color: Color) -> CharIconEngine:
    font_family = font_family_cash.get(icon_id.__class__)
    if font_family is None:
        font_family = load_font_family(icon_id)
    char = chr(icon_id.value)
    font = QFont()
    font.setFamily(font_family)
    # For the solid icon, the styleName must be set to "Solid".
    if type(icon_id) is FaSolid:
        font.setStyleName("Solid")
    return CharIconEngine(font, char, color)


def _vs_icon_engine(icon_id: Vsc, color: Color) -> SVGBufferIconEngine:
    xml = resources.read_text("qtvscodestyle.vscode.icons", icon_id.value)
    return SVGBufferIconEngine(xml, color)


def _icon(
    icon_id: Union[Vsc, FaSolid, FaRegular, FaBrands], color_id: str = None, color: Color = Color.white()
) -> QIcon:
    if color_id is not None:
        current_color = global_current_colors.get(color_id)
        if current_color:
            color = current_color

    if type(icon_id) is Vsc:
        engine = _vs_icon_engine(icon_id, color)
    elif type(icon_id) is FaSolid:
        engine = _iconic_icon_engine(icon_id, color)
    elif type(icon_id) is FaRegular:
        engine = _iconic_icon_engine(icon_id, color)
    elif type(icon_id) is FaBrands:
        engine = _iconic_icon_engine(icon_id, color)
    else:
        raise TypeError(f"icon_id argument must be a Vs, FaSolid, FaRegular, FaBrands, not {type(icon_id)}")

    # Register icon
    if color_id is not None:
        if global_icon_engine_map.get(color_id) is None:
            global_icon_engine_map[color_id] = []
        global_icon_engine_map[color_id].append(engine)
    return QIcon(engine)


def theme_icon(icon_id: Union[Vsc, FaSolid, FaRegular, FaBrands], color_id: str = "icon.foreground") -> QIcon:
    return _icon(icon_id, color_id)


def icon(icon_id: Union[Vsc, FaSolid, FaRegular, FaBrands], color_code: str = "#FFFFFF") -> QIcon:
    color = Color.from_hex(color_code)
    return _icon(icon_id, color=color)
