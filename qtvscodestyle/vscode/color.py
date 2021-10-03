# ===========================================================================
# QtVSCodeStyle.
#
#  Copyright (c) 2015- Microsoft Corporation
#  Copyright (c) 2021- Yunosuke Ohsugi
#
#  Distributed under the terms of the MIT License.
#  See https://github.com/microsoft/vscode/blob/main/LICENSE.txt
#
# Original code:
#   https://github.com/microsoft/vscode/blob/main/src/vs/base/common/color.ts
#
# (see NOTICE.md in the QtVSCodeStyle root directory for details)
# ============================================================================


from __future__ import annotations

import colorsys
from functools import lru_cache
import math
from typing import Union


class RGBA:
    def __init__(self, r: float, g: float, b: float, a: float = 1) -> None:
        self._r = min(255, max(0, r))
        self._g = min(255, max(0, g))
        self._b = min(255, max(0, b))
        self._a = max(min(1, a), 0)

    def __str__(self) -> str:
        return f"rgba({self.r:.3f}, {self.g:.3f}, {self.b:.3f}, {self.a:.3f})"

    def __getitem__(self, item: int) -> float:
        return [self.r, self.g, self.b, self.a][item]

    @property
    def r(self) -> float:
        return self._r

    @property
    def g(self) -> float:
        return self._g

    @property
    def b(self) -> float:
        return self._b

    @property
    def a(self) -> float:
        return self._a


class HSLA:
    def __init__(self, h: float, s: float, l: float, a: float = 1) -> None:  # noqa: E741
        self._h = max(min(360, h), 0)
        self._s = max(min(1, s), 0)
        self._l = max(min(1, l), 0)
        self._a = max(min(1, a), 0)

    def __str__(self) -> str:
        return f"hsla({self.h:.3f}, {self.s:.3%}, {self.l:.3%}, {self.a:.3f})"

    @property
    def h(self) -> float:
        return self._h

    @property
    def s(self) -> float:
        return self._s

    @property
    def l(self) -> float:  # noqa: E741, E743
        return self._l

    @property
    def a(self) -> float:
        return self._a

    @staticmethod
    @lru_cache()
    def from_rgba(rgba: RGBA) -> HSLA:
        hls = colorsys.rgb_to_hls(rgba.r / 255, rgba.g / 255, rgba.b / 255)
        return HSLA(hls[0] * 360, hls[2], hls[1], rgba.a)

    @staticmethod
    @lru_cache()
    def to_rgba(hsla: HSLA) -> RGBA:
        rgb = colorsys.hls_to_rgb(hsla.h / 360, hsla.l, hsla.s)
        return RGBA(rgb[0] * 255, rgb[1] * 255, rgb[2] * 255, hsla.a)


class HSVA:
    def __init__(self, h: float, s: float, v: float, a: float = 1) -> None:
        self._h = max(min(360, h), 0)
        self._s = max(min(1, s), 0)
        self._v = max(min(1, v), 0)
        self._a = max(min(1, a), 0)

    def __str__(self) -> str:
        return f"hsla({self.h:.3f}, {self.s:.3%}, {self.v:.3%}, {self.a:.3f})"

    @property
    def h(self) -> float:
        return self._h

    @property
    def s(self) -> float:
        return self._s

    @property
    def v(self) -> float:
        return self._v

    @property
    def a(self) -> float:
        return self._a

    @staticmethod
    @lru_cache()
    def from_rgba(rgba: RGBA) -> HSVA:
        hsv = colorsys.rgb_to_hsv(rgba.r / 255, rgba.g / 255, rgba.b / 255)
        return HSVA(hsv[0] * 360, hsv[1], hsv[2], rgba.a)

    @staticmethod
    @lru_cache()
    def to_rgba(hsva: HSVA) -> RGBA:
        rgb = colorsys.hsv_to_rgb(hsva.h / 360, hsva.s, hsva.v)
        return RGBA(rgb[0] * 255, rgb[1] * 255, rgb[2], hsva.a)


class Color:
    def __init__(self, color_code: Union[RGBA, HSLA, HSVA]) -> None:
        self._hsla, self._hsva = None, None
        if type(color_code) is RGBA:
            self._rgba = color_code
        elif type(color_code) is HSLA:
            self._hsla = color_code
            self._rgba = HSLA.to_rgba(self._hsla)
        elif type(color_code) is HSVA:
            self._hsva = color_code
            self._rgba = HSVA.to_rgba(self._hsva)

    def __str__(self) -> str:
        return str(self.rgba)

    @property
    def rgba(self) -> RGBA:
        return self._rgba

    @property
    def hsla(self):
        return self._hsla if self._hsla else HSLA.from_rgba(self.rgba)

    @property
    def hsva(self):
        return self._hsva if self._hsva else HSVA.from_rgba(self.rgba)

    @staticmethod
    @lru_cache()
    def from_hex(hex: str) -> Color:
        hex = hex.lstrip("#")
        r, g, b, a = 255, 0, 0, 1
        if len(hex) == 3:  # #RGB format
            r, g, b = [int(char, 16) for char in hex]
            r, g, b = 16 * r + r, 16 * g + g, 16 * b + b
        if len(hex) == 4:  # #RGBA format
            r, g, b, a = [int(char, 16) for char in hex]
            r, g, b = 16 * r + r, 16 * g + g, 16 * b + b
            a = (16 * a + a) / 255
        if len(hex) == 6:  # #RRGGBB format
            r, g, b = bytes.fromhex(hex)
            a = 1
        elif len(hex) == 8:  # #RRGGBBAA format
            r, g, b, a = bytes.fromhex(hex)
            a = a / 255
        return Color(RGBA(r, g, b, a))

    @staticmethod
    @lru_cache()
    def to_hex(color: Color) -> str:
        r, g, b, a = color.rgba.r, color.rgba.g, color.rgba.b, color.rgba.a
        return f"{math.floor(r):x}{math.floor(g):x}{math.floor(b):x}{math.floor(a*255):02x}"

    # http://www.w3.org/TR/WCAG20/#relativeluminancedef
    # Returns the number in the set [0, 1]. O => Darkest Black. 1 => Lightest white.
    def _get_relative_luminance(self) -> float:
        R = Color._relative_luminance_for_component(self.rgba.r)
        G = Color._relative_luminance_for_component(self.rgba.g)
        B = Color._relative_luminance_for_component(self.rgba.b)
        luminance = 0.2126 * R + 0.7152 * G + 0.0722 * B
        return luminance

    @staticmethod
    @lru_cache()
    def _relative_luminance_for_component(color: float) -> float:
        c = color / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    def is_lighter_than(self, another: Color) -> bool:
        lum1 = self._get_relative_luminance()
        lum2 = another._get_relative_luminance()
        return lum1 > lum2

    def is_darker_than(self, another: Color) -> bool:
        lum1 = self._get_relative_luminance()
        lum2 = another._get_relative_luminance()
        return lum1 < lum2

    def lighten(self, factor: float) -> Color:
        return Color(HSLA(self.hsla.h, self.hsla.s, self.hsla.l + self.hsla.l * factor, self.hsla.a))

    def darken(self, factor: float) -> Color:
        return Color(HSLA(self.hsla.h, self.hsla.s, self.hsla.l - self.hsla.l * factor, self.hsla.a))

    def transparent(self, factor: float) -> Color:
        return Color(RGBA(self.rgba.r, self.rgba.g, self.rgba.b, self.rgba.a * factor))

    @staticmethod
    @lru_cache()
    def get_lighter_color(of: Color, relative: Color, factor: float) -> Color:
        if of.is_lighter_than(relative):
            return of
        factor = factor if factor else 0.5
        lum1 = of._get_relative_luminance()
        lum2 = relative._get_relative_luminance()
        factor = factor * (lum2 - lum1) / lum2
        return of.lighten(factor)

    @staticmethod
    @lru_cache()
    def get_darker_color(of: Color, relative: Color, factor: float) -> Color:
        if of.is_darker_than(relative):
            return of
        factor = factor if factor else 0.5
        lum1 = of._get_relative_luminance()
        lum2 = relative._get_relative_luminance()
        factor = factor * (lum1 - lum2) / lum1
        return of.darken(factor)

    @staticmethod
    def white() -> Color:
        return Color(RGBA(255, 255, 255))

    @staticmethod
    def black() -> Color:
        return Color(RGBA(0, 0, 0))

    @staticmethod
    def red() -> Color:
        return Color(RGBA(255, 0, 0))

    @staticmethod
    def green() -> Color:
        return Color(RGBA(0, 255, 0))

    @staticmethod
    def blue() -> Color:
        return Color(RGBA(0, 0, 255))

    @staticmethod
    def cyan() -> Color:
        return Color(RGBA(0, 255, 255))

    @staticmethod
    def lightgrey() -> Color:
        return Color(RGBA(211, 211, 211))
