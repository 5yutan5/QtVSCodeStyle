from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from distutils.version import LooseVersion
from importlib import resources
from pathlib import Path
from typing import Optional

from qtvscodestyle.util import multireplace
from qtvscodestyle.vscode.color import Color


# A class that handle the properties of the $url{...} variable in the stylesheet template.
@dataclass(unsafe_hash=True, frozen=True)
class _Url:
    icon_name: str
    color_id: str
    rotate: str
    file_name: str


def _parse_env_patch(stylesheet: str) -> dict[str, str]:
    from qtvscodestyle.qtpy import __version__ as qt_version  # type: ignore

    qualifiers = {
        "equal": "==",
        "unequal": "!=",
        "greater": ">",
        "less": "<",
        "greater_equal": ">=",
        "less_equal": "<=",
    }
    functions = {
        "==": lambda version, value: value if LooseVersion(qt_version) == LooseVersion(version) else "",
        "!=": lambda version, value: value if LooseVersion(qt_version) != LooseVersion(version) else "",
        ">": lambda version, value: value if LooseVersion(qt_version) > LooseVersion(version) else "",
        "<": lambda version, value: value if LooseVersion(qt_version) < LooseVersion(version) else "",
        ">=": lambda version, value: value if LooseVersion(qt_version) >= LooseVersion(version) else "",
        "<=": lambda version, value: value if LooseVersion(qt_version) <= LooseVersion(version) else "",
    }
    replacements = {}

    for match in re.finditer(r"(?<=\$env_patch)\{.+\}", stylesheet):
        json_text = match.group()
        match_text = f"$env_patch{json_text}"
        property: dict[str, str] = json.loads(json_text)

        qualifier = ""
        if qualifiers["equal"] in property["version"]:
            qualifier = qualifiers["equal"]
        elif qualifiers["unequal"] in property["version"]:
            qualifier = qualifiers["unequal"]
        elif qualifiers["greater_equal"] in property["version"]:
            qualifier = qualifiers["greater_equal"]
        elif qualifiers["less_equal"] in property["version"]:
            qualifier = qualifiers["less_equal"]
        elif qualifiers["greater"] in property["version"]:
            qualifier = qualifiers["greater"]
        elif qualifiers["less"] in property["version"]:
            qualifier = qualifiers["less"]

        version = property["version"].replace(qualifier, "")
        replacements[match_text] = functions[qualifier](version, property["value"])
    return replacements


def _parse_theme_type_patch(stylesheet: str, theme_type) -> dict[str, str]:
    replacements = {}
    for match in re.finditer(r"(?<=\$type_patch)\{[\s\S]*?\};", stylesheet):
        json_text = match.group().rstrip(";")
        property: dict[str, str] = json.loads(json_text)
        theme_types = property["types"].replace(" ", "").split("|")
        value = property["value"]
        qss_text = "\n".join(value if type(value) is list else [value])
        replacements[f"$type_patch{json_text}"] = qss_text if theme_type in theme_types else ""
    return replacements


def _parse_url(stylesheet: str) -> set[_Url]:
    urls = set()
    for match in re.finditer(r"(?<=\$url)\{.+\}", stylesheet):
        icon_name, color_id, rotate = json.loads(match.group()).values()
        urls.add(_Url(icon_name, color_id, rotate, f"{icon_name}_{color_id}_{rotate}.svg"))
    return urls


def _output_converted_svg_file(colors: dict[str, Optional[Color]], urls: set[_Url], dir_path: Path) -> None:
    contents = resources.contents("qtvscodestyle.google_fonts")
    svg_codes = {}
    for content in contents:
        if ".svg" in content:
            svg_text = resources.read_text("qtvscodestyle.google_fonts", content)
            icon_name = content.replace(".svg", "")
            svg_codes[icon_name] = svg_text

    # QSvg does not support rgba(...).
    # Therefore, we need to set the alpha value to fill-opacity instead.
    def to_svg_color(color: Optional[Color]) -> str:
        if color is not None:
            r, g, b, a = color.rgba
            return f'"rgb({r}, {g}, {b})" fill-opacity="{a}"'
        return '""'

    for url in urls:
        color = colors["$" + url.color_id]
        svg_code = svg_codes[url.icon_name]
        # Change color and rotate.
        replacements = {'"#FFFFFF"': to_svg_color(color), "rotate(0,": f"rotate({url.rotate},"}
        svg_code_converted = multireplace(svg_code, replacements)

        with (dir_path / url.file_name).open("w") as f:
            f.write(svg_code_converted)


def build_stylesheet(
    colors: dict[str, Optional[Color]], theme_type: str, output_svg_path: Path, is_designer: bool
) -> str:
    stylesheet_template = resources.read_text("qtvscodestyle", "template.qss")

    # Parse $type_patch{...} and $env_patch{...} in template stylesheet.
    type_patch_replacements = _parse_theme_type_patch(stylesheet_template, theme_type)
    env_patch_replacements = _parse_env_patch(stylesheet_template)

    # Replace value before parsing $url{...}.
    patch_replacements = {**type_patch_replacements, **env_patch_replacements}
    stylesheet_template = multireplace(stylesheet_template, patch_replacements)

    # Parse $url{...} in template stylesheet.
    urls = _parse_url(stylesheet_template)
    _output_converted_svg_file(colors, urls, output_svg_path)
    url_replacements = {}
    for url in urls:
        url_dict = asdict(url)
        file_name = url_dict.pop("file_name")
        if is_designer:
            value = f'url(":/vscode/{file_name}")'
        else:
            value = f'url("{output_svg_path / file_name}")'
        url_replacements[f"$url{json.dumps(url_dict)}"] = value

    # Create stylesheet
    colors_str = {id: ("" if color is None else str(color)) for id, color in colors.items()}
    replacements = {**colors_str, **url_replacements}
    stylesheet = multireplace(stylesheet_template, replacements)
    return stylesheet
