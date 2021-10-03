# =============================================================================================
# QtVSCodeStyle.
#
#  Copyright (c) 2015- Microsoft Corporation
#  Copyright (c) 2021- Yunosuke Ohsugi
#
#  Distributed under the terms of the MIT License.
#  See https://github.com/microsoft/vscode/blob/main/LICENSE.txt
#
# Original code:
#   https://github.com/microsoft/vscode/blob/main/src/vs/platform/theme/common/colorRegistry.ts
#
# (see NOTICE.md in the QtVSCodeStyle root directory for details)
# =============================================================================================

from __future__ import annotations

from enum import Enum, auto
from typing import Optional, Union

from qtvscodestyle.vscode.color import RGBA, Color


class _ColorIdentifier(str):
    pass


_ColorValue = Union[Color, str, _ColorIdentifier, dict, None]


class _ColorTransformType(Enum):
    Darken = auto()
    Lighten = auto()
    Transparent = auto()
    OneOf = auto()
    LessProminent = auto()
    IfDefinedThenElse = auto()


class ColorRegistry:
    _default_colors: dict[str, dict[str, _ColorValue]] = {"dark": {}, "light": {}, "hc": {}}

    def __init__(self) -> None:
        self._colors = {
            "dark": ColorRegistry._default_colors["dark"].copy(),
            "light": ColorRegistry._default_colors["light"].copy(),
            "hc": ColorRegistry._default_colors["hc"].copy(),
        }

    @classmethod
    def _register_default_color(cls, id: str, defaults: Union[dict[str, _ColorValue], None]) -> _ColorIdentifier:
        cls._default_colors["dark"][id] = None if defaults is None else defaults["dark"]
        cls._default_colors["light"][id] = None if defaults is None else defaults["light"]
        cls._default_colors["hc"][id] = None if defaults is None else defaults["hc"]
        return _ColorIdentifier(id)

    def register_color(self, id: str, color: str, theme: str) -> None:
        if self._colors[theme].get(id):
            self._colors[theme][id] = color

    def get_colors(self, theme: str) -> dict[str, Optional[Color]]:
        colors_resolved = {}
        for id, color_value in self._colors[theme].items():
            color_value_resolved = self._resolve_color_value(color_value, theme)
            colors_resolved[id] = color_value_resolved
        return colors_resolved

    def _resolve_color_value(self, color_value: _ColorValue, theme: str) -> Union[Color, None]:
        if color_value is None:
            return None
        elif type(color_value) is str:
            if color_value == "transparent":
                return Color(RGBA(0, 0, 0, 0))
            return Color.from_hex(color_value)
        elif type(color_value) is Color:
            return color_value
        elif type(color_value) is _ColorIdentifier:
            return self._resolve_color_value(self._colors[theme][color_value], theme)
        elif type(color_value) is dict:
            return self._execute_transform(color_value, theme)

    def _is_defines(self, color_id: _ColorIdentifier, theme: str) -> bool:
        return ColorRegistry._default_colors[theme][color_id] != self._colors[theme][color_id]

    def _execute_transform(self, transform: dict, theme: str) -> Union[Color, None]:
        if transform["op"] is _ColorTransformType.Darken:
            color_value = self._resolve_color_value(transform["value"], theme)  # type: ignore
            if type(color_value) is Color:
                return color_value.darken(transform["factor"])  # type: ignore
        elif transform["op"] is _ColorTransformType.Lighten:
            color_value = self._resolve_color_value(transform["value"], theme)  # type: ignore
            if type(color_value) is Color:
                return color_value.lighten(transform["factor"])  # type: ignore
        elif transform["op"] is _ColorTransformType.Transparent:
            color_value = self._resolve_color_value(transform["value"], theme)  # type: ignore
            if type(color_value) is Color:
                return color_value.transparent(transform["factor"])  # type: ignore
        elif transform["op"] is _ColorTransformType.OneOf:
            for candidate in transform["values"]:  # type: ignore
                color = self._resolve_color_value(candidate, theme)
                if color:
                    return color
        elif transform["op"] is _ColorTransformType.IfDefinedThenElse:
            return self._resolve_color_value(
                transform["then"] if self._is_defines(transform["if_"], theme) else transform["else_"],  # type: ignore
                theme,
            )
        elif transform["op"] is _ColorTransformType.LessProminent:
            from_ = self._resolve_color_value(transform["value"], theme)  # type: ignore
            if not from_:
                return None
            background_color = self._resolve_color_value(transform["background"], theme)  # type: ignore
            if not background_color:
                return from_.transparent(transform["factor"] * transform["transparency"])  # type: ignore
            return (
                Color.get_lighter_color(from_, background_color, transform["factor"]).transparent(  # type: ignore
                    transform["transparency"]  # type: ignore
                )
                if from_.is_darker_than(background_color)
                else Color.get_darker_color(from_, background_color, transform["factor"]).transparent(  # type: ignore
                    transform["transparency"]  # type: ignore
                )
            )
        return None


register_color = ColorRegistry._register_default_color


def darken(color_value: _ColorValue, factor: float) -> dict:
    return {"op": _ColorTransformType.Darken, "value": color_value, "factor": factor}


def lighten(color_value: _ColorValue, factor: float) -> dict:
    return {"op": _ColorTransformType.Lighten, "value": color_value, "factor": factor}


def transparent(color_value: _ColorValue, factor: float) -> dict:
    return {"op": _ColorTransformType.Transparent, "value": color_value, "factor": factor}


def one_of(*color_values: _ColorValue) -> dict:
    return {"op": _ColorTransformType.OneOf, "values": list(color_values)}


def if_defined_then_else(if_arg: _ColorIdentifier, then_arg: _ColorValue, else_arg: _ColorValue) -> dict:
    return {"op": _ColorTransformType.IfDefinedThenElse, "if_": if_arg, "then": then_arg, "else_": else_arg}


def less_prominent(
    color_value: _ColorValue, background_color_value: _ColorValue, factor: float, transparency: float
) -> dict:
    return {
        "op": _ColorTransformType.LessProminent,
        "value": color_value,
        "background": background_color_value,
        "factor": factor,
        "transparency": transparency,
    }
