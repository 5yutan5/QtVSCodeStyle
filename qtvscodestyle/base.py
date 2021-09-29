from __future__ import annotations

import json
import re
import shutil
from enum import Enum
from importlib import resources
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional, Union

from typing_extensions import Literal

from qtvscodestyle.build import build_stylesheet
from qtvscodestyle.util import multireplace
from qtvscodestyle.vscode.color import Color
from qtvscodestyle.vscode.color_registry import setup_default_color_registry
from qtvscodestyle.vscode.color_registry_manager import ColorRegistry

setup_default_color_registry()

# Setup project dir
_RESOURCES_BASE_DIR = Path.home() / ".q_vscode_style" / "resources"
# Clean up project dir
shutil.rmtree(str(_RESOURCES_BASE_DIR), ignore_errors=True)
_RESOURCES_BASE_DIR.mkdir(parents=True, exist_ok=True)


# In VSCode's default theme file, theme type is not set. Extension themes is no need.
# So the default theme type is defined here.
class Theme(Enum):
    LIGHT_VS = {"name": "Light (Visual Studio)", "file_name": "light_vs.json", "type": "light"}
    QUIET_LIGHT = {"name": "Quiet Light", "file_name": "quietlight-color-theme.json", "type": "light"}
    SOLARIZED_LIGHT = {"name": "Solarized Light", "file_name": "solarized-light-color-theme.json", "type": "light"}
    ABYSS = {"name": "Abyss", "file_name": "abyss_color_theme.json", "type": "dark"}
    DARK_VS = {"name": "Dark (Visual Studio)", "file_name": "dark_vs.json", "type": "dark"}
    KIMBIE_DARK = {"name": "Kimbie Dark", "file_name": "kimbie-dark-color-theme.json", "type": "dark"}
    MONOKAI = {"name": "Monokai", "file_name": "monokai-color-theme.json", "type": "dark"}
    MONOKAI_DIMMED = {"name": "Monokai Dimmed", "file_name": "dimmed-monokai-color-theme.json", "type": "dark"}
    RED = {"name": "Red", "file_name": "Red-color-theme.json", "type": "dark"}
    SOLARIZED_DARK = {"name": "Solarized Dark", "file_name": "solarized_dark_color_theme.json", "type": "dark"}
    TOMORROW_NIGHT_BLUE = {
        "name": "Tomorrow Night Blue",
        "file_name": "tomorrow-night-blue-color-theme.json",
        "type": "dark",
    }
    DARK_HIGH_CONTRAST = {"name": "Dark High Contrast", "file_name": "hc_black.json", "type": "dark"}


def _loads_jsonc(json_text: str) -> dict:
    """wrapper of json.loads() to load jsonc(json with comment) text.
    Allow comment and trailing commas(inside dictionaries or lists).
    """
    symbol_to_replace_word = {
        "//": "${one_line_comment_symbol}",
        "/*": "${multiple_line_comment_symbol_pre}",
        "*/": "${multiple_line_comment_symbol_post}",
        "[": "${key_bracket_left}",
        "]": "${key_bracket_right}",
        "{": "${curly_bracket_left}",
        "}": "${curly_bracket_right}",
    }

    # Replace invalid symbol to replace word in key or value
    # to exclude certain symbols in a string from substitution.
    def replace_comment_symbol(match: re.Match) -> str:
        return multireplace(match.group(), symbol_to_replace_word)

    text_replaced = re.sub(r'"(.*?)"', replace_comment_symbol, json_text)
    # Remove comment
    text_removed = re.sub(r"/\*[\s\S]*?\*/|//.*", "", text_replaced)
    # Remove trailing commas inside of dictionaries and lists.
    text_removed = re.sub(r",[ \t\r\n]+}", "}", text_removed)
    text_removed = re.sub(r",[ \t\r\n]+\]", "]", text_removed)

    # Restore replace words.
    replace_word_to_symbol = {v: k for k, v in symbol_to_replace_word.items()}
    result = multireplace(text_removed, replace_word_to_symbol)
    return json.loads(result)


def _merge_colors_to_default(
    colors: dict[str, str], type: Literal["dark", "light", "hc"]
) -> dict[str, Optional[Color]]:
    color_registry = ColorRegistry()
    for id, color in colors.items():
        color_registry.register_color(id, color, type)
    colors_generated = color_registry.get_colors(type)
    return {f"${id}".replace(".", "_"): color for id, color in colors_generated.items()}


def _load_stylesheet(
    theme: Union[Theme, str, Path, dict],
    custom_colors: dict[str, str],
    output_svg_path: Path,
    is_designer: bool = False,
) -> str:
    if type(theme) is Theme:
        theme_file_name = theme.value["file_name"]
        json_text = resources.read_text("qtvscodestyle.theme", theme_file_name)
        theme_property = _loads_jsonc(json_text)
        theme_property["type"] = theme.value["type"]
    elif type(theme) is str or type(theme) is Path:
        with Path(theme).open() as f:
            json_text = f.read()
        theme_property = _loads_jsonc(json_text)
    elif type(theme) is dict:
        theme_property = theme
    else:
        raise TypeError("Invalid type input to theme argument. ")

    colors = {**theme_property["colors"], **custom_colors}
    colors = _merge_colors_to_default(colors, theme_property["type"])
    return build_stylesheet(colors, theme_property["type"], output_svg_path, is_designer)


def load_stylesheet_for_designer(theme: Theme, custom_colors: dict[str, str], resource_folder_path: Path) -> str:
    return _load_stylesheet(theme, custom_colors, resource_folder_path, True)


def load_stylesheet(theme: Union[Theme, str, Path, dict] = Theme.DARK_VS, custom_colors: dict[str, str] = {}) -> str:
    """Load the style sheet which used by vscode."""
    global _temp_dir  # Set to global value the temporary directory so that it is not cached.
    _temp_dir = TemporaryDirectory(prefix="temp", dir=str(_RESOURCES_BASE_DIR))
    temp_dir_path = Path(_temp_dir.name)
    return _load_stylesheet(theme, custom_colors, temp_dir_path)


def loads_stylesheet(theme_text: str, custom_colors: dict[str, str] = {}) -> str:
    theme_property = _loads_jsonc(theme_text)
    return load_stylesheet(theme_property, custom_colors)


def list_themes():
    themes = {theme.value["name"]: theme.name for theme in Theme}
    # Align with a colon
    max_len = 0
    for name in themes.keys():
        max_len = max(len(name), max_len)
    print("Theme name:".ljust(max_len) + ": Symbol")
    print("___________".ljust(max_len, " ") + "  " + "______")
    print()
    for name, symbol in themes.items():
        print(name.ljust(max_len) + f": {symbol}")
