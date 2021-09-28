from importlib import resources

from qtvscodestyle.qtpy.QtGui import QIcon


def get_icon(icon_name: str) -> QIcon:
    """Creates an icon from svg file in `qtvscodestyle/google_fonts/app`.

    for details on available icons.
    """
    with resources.path("qtvscodestyle.google_fonts.app", f"{icon_name}.svg") as icon_path:
        return QIcon(str(icon_path))
