from __future__ import annotations

import json
import operator
import re
from dataclasses import dataclass
from distutils.version import StrictVersion
from importlib import resources
from pathlib import Path
from typing import Optional

from qtvscodestyle.util import multireplace, to_svg_color_format
from qtvscodestyle.vscode.color import Color


# A class that handle the properties of the $url{...} variable in the stylesheet template.
@dataclass(unsafe_hash=True, frozen=True)
class _Url:
    icon: str
    id: str
    rotate: str
    path: Path


def _parse_env_patch(stylesheet: str) -> dict[str, str]:
    try:
        from qtvscodestyle.qtpy import __version__ as qt_version
    except ImportError:
        print("Failed to load Qt version. Load stylesheet as the latest version.")
        print("-----------------------------------------------------------------")
        qt_version = "10.0.0"  # Fairly future version for always setting latest version.

    # greater_equal and less_equal must be evaluated before greater and less.
    operators = {
        "==": operator.eq,  # equal
        "!=": operator.ne,  # unequal
        ">=": operator.ge,  # greater_equal
        "<=": operator.le,  # less_equal
        ">": operator.gt,  # greater
        "<": operator.lt,  # less
    }
    replacements = {}

    for match in re.finditer(r"\$env_patch\{[\s\S]*?\}", stylesheet):
        match_text = match.group()
        json_text = match_text.replace("$env_patch", "")
        property: dict[str, str] = json.loads(json_text)

        for qualifier in operators.keys():
            if qualifier in property["version"]:
                version = property["version"].replace(qualifier, "")
                break
        else:
            raise SyntaxError(f"invalid character in qualifier. Available qualifiers {list(operators.keys())}")

        is_true = operators[qualifier](StrictVersion(qt_version), StrictVersion(version))
        replacements[match_text] = property["value"] if is_true else ""
    return replacements


def _parse_theme_type_patch(stylesheet: str, theme_type: str) -> dict[str, str]:
    replacements = {}
    for match in re.finditer(r"\$type_patch\{[\s\S]*?\};", stylesheet):
        match_text = match.group().rstrip(";")
        json_text = match_text.replace("$type_patch", "")

        property: dict[str, str] = json.loads(json_text)
        theme_types = property["types"].replace(" ", "").split("|")
        value = property["value"]
        qss_text = "\n".join(value if type(value) is list else [value])
        replacements[match_text] = qss_text if theme_type in theme_types else ""
    return replacements


def _parse_url(stylesheet: str, dir_path: Path, is_designer: bool = False) -> tuple[dict[str, str], set[_Url]]:
    urls = set()
    replacements = {}
    for match in re.finditer(r"\$url\{.+\}", stylesheet):
        match_text = match.group()
        json_text = match_text.replace("$url", "")

        icon, id, rotate = json.loads(json_text).values()
        file_name = f"{icon.replace('.svg', '')}_{id}_{rotate}.svg"
        urls.add(_Url(icon, id, rotate, dir_path / file_name))

        # In windows, the path is a backslash. Replase backslash to slash.
        full_path = (dir_path / file_name).as_posix()
        value = f":/vscode/{file_name}" if is_designer else str(full_path)
        replacements[match_text] = f"url({value})"
    return replacements, urls


def _output_converted_svg_file(colors: dict[str, Optional[Color]], urls: set[_Url]) -> None:
    svg_codes: dict[str, str] = {}  # {file name: svg code}
    for content in resources.contents("qtvscodestyle.vscode.icons"):
        if ".svg" not in content:  # Only svg file
            continue
        svg_code = resources.read_text("qtvscodestyle.vscode.icons", content)
        svg_codes[content] = svg_code

    for content in resources.contents("qtvscodestyle.stylesheet.icons"):
        if ".svg" not in content:  # Only svg file
            continue
        svg_code = resources.read_text("qtvscodestyle.stylesheet.icons", content)
        svg_codes[content] = svg_code

    for url in urls:
        color = colors["$" + url.id]
        # Change color and rotate. See https://stackoverflow.com/a/15139069/13452582
        new_contents = f'{to_svg_color_format(color)} transform="rotate({url.rotate}, 8, 8)"'
        svg_code_converted = svg_codes[url.icon].replace('fill="currentColor"', new_contents)

        with url.path.open("w") as f:
            f.write(svg_code_converted)


def build_stylesheet(
    colors: dict[str, Optional[Color]], theme_type: str, output_svg_path: Path, is_designer: bool
) -> str:
    stylesheet_template = resources.read_text("qtvscodestyle.stylesheet", "template.qss")
    # Convert id for stylesheet variable
    colors = {f"${id}".replace(".", "_"): color for id, color in colors.items()}

    # Parse $type_patch{...} and $env_patch{...} in template stylesheet.
    type_patch_replacements = _parse_theme_type_patch(stylesheet_template, theme_type)
    env_patch_replacements = _parse_env_patch(stylesheet_template)

    # Replace value before parsing $url{...}.
    patch_replacements = {**type_patch_replacements, **env_patch_replacements}
    stylesheet_template = multireplace(stylesheet_template, patch_replacements)

    # Parse $url{...} in template stylesheet.
    url_replacements, urls = _parse_url(stylesheet_template, output_svg_path, is_designer)
    _output_converted_svg_file(colors, urls)

    # Create stylesheet
    colors_str = {id: ("" if color is None else str(color)) for id, color in colors.items()}
    replacements = {**colors_str, **url_replacements}
    stylesheet = multireplace(stylesheet_template, replacements)
    return stylesheet
