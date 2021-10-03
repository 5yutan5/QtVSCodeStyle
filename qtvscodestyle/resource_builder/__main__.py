from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Union
from xml.etree import ElementTree as ET

from qtvscodestyle.base import Theme, load_stylesheet_for_designer


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="This program generates a template for applying the vscode style to QtDesigner."
    )
    parser.add_argument(
        "-t",
        "--theme",
        help=f"""Theme symbol. Available symbols: {[theme.name.lower() for theme in Theme]}
        """,
        default=Theme.DARK_VS.name.lower(),
    )
    parser.add_argument(
        "-p",
        "--path",
        help="Path of the dir to output the template. Default path is current working directory(cwd).",
        default=str(Path.cwd()),
    )
    parser.add_argument(
        "-c", "--custom-colors-path", help="Path of the json file where the custom colors are saved.",
    )
    args = parser.parse_args()
    return args


def _build_resources(save_dir_path: Union[Path, str], custom_colors: dict[str, str], theme: Theme) -> None:
    save_dir_path = Path(save_dir_path)
    try:
        save_dir_path.mkdir()
    except FileExistsError:
        raise FileExistsError("This folder contains files. Resources can only build to empty folder.") from None

    svg_dir = save_dir_path / "svg"
    svg_dir.mkdir(exist_ok=True)

    stylesheet_file_path = save_dir_path / "stylesheet.qss"
    resource_file_path = save_dir_path / "resource.qrc"

    # generate stylesheet file
    stylesheet = load_stylesheet_for_designer(theme, custom_colors, svg_dir)
    with stylesheet_file_path.open(mode="w", encoding="utf-8") as f:
        f.write(stylesheet)

    # generate resource file
    main_tag = ET.Element("RCC", {"version": "1.0"})
    main_tag.text = "\n  "
    qt_resource_tag = ET.SubElement(main_tag, "qresource", {"prefix": "vscode"})
    qt_resource_tag.tail = "\n"
    qt_resource_tag.text = "\n    "

    for file in svg_dir.iterdir():
        file_tag = ET.SubElement(qt_resource_tag, "file", {"alias": file.name})
        file_tag.text = f"{svg_dir.name}/{file.name}"
        file_tag.tail = "\n    "

    resource_file_name = str(resource_file_path)
    ET.ElementTree(main_tag).write(resource_file_name, "utf-8")


if __name__ == "__main__":
    args = _parse_args()
    theme_symbol = args.theme.lower()
    output_dir_path = Path(args.path) / "qtvscodestyle_resources"
    custom_colors_dir_path = args.custom_colors_path

    for default_theme in Theme:
        if default_theme.name.lower() == theme_symbol:
            theme = default_theme
            break
    else:
        raise Exception(
            f"Invalid symbol in theme option. Available symbols: {[theme.name.lower() for theme in Theme]}"
        )

    if custom_colors_dir_path is not None:
        with open(custom_colors_dir_path) as f:
            custom_colors = json.load(f)
    else:
        custom_colors = {}

    _build_resources(output_dir_path, custom_colors, theme)
