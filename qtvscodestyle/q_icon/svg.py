# ===========================================================================
# QtVSCodeStyle.
#
#  Copyright (c) 2018- Napari
#  Copyright (c) 2021- Yunosuke Ohsugi
#   Distributed under the terms of the Modified BSD License.
#   see https://github.com/napari/napari/blob/main/LICENSE
#
# Original code:
#   https://github.com/napari/napari/blob/main/napari/_qt/qt_resources/_svg.py
#
# (see NOTICE.md in the QtVSCodeStyle root directory for details)
# ============================================================================

"""
A Class for generating QIcons from SVGs with arbitrary colors at runtime.
"""
from __future__ import annotations

from qtvscodestyle.qtpy.QtCore import QPoint, QRect, QRectF, QSize, Qt
from qtvscodestyle.qtpy.QtGui import QIcon, QIconEngine, QImage, QPainter, QPixmap
from qtvscodestyle.qtpy.QtSvg import QSvgRenderer
from qtvscodestyle.util import to_svg_color_format
from qtvscodestyle.vscode.color import Color


class SVGBufferIconEngine(QIconEngine):
    """A custom QIconEngine that can render an SVG buffer.

    An icon engine provides the rendering functions for a ``QIcon``.
    Each icon has a corresponding icon engine that is responsible for drawing
    the icon with a requested size, mode and state.  While the built-in
    QIconEngine is capable of rendering SVG files, it's not able to receive the
    raw XML string from memory.

    This ``QIconEngine`` takes in SVG data as a raw xml string or bytes.

    see: https://doc.qt.io/qt-5/qiconengine.html
    """
    def __init__(self, xml: str, color: Color) -> None:
        self._xml = xml
        self._color = color
        super().__init__()

    def paint(self, painter: QPainter, rect: QRect, mode: QIcon.Mode, state):
        """Paint the icon int ``rect`` using ``painter``."""
        color = self._color
        if mode == QIcon.Mode.Disabled:
            color = self._color.transparent(0.3)

        xml = self._xml.replace('fill="currentColor"', to_svg_color_format(color))
        xml_byte = xml.encode("utf-8")

        renderer = QSvgRenderer(xml_byte)
        renderer.render(painter, QRectF(rect))

    def clone(self):
        """Required to subclass abstract QIconEngine."""
        return SVGBufferIconEngine(self._xml, self._color)

    def pixmap(self, size: QSize, mode: QIcon.Mode, state: QIcon.State):
        """Return the icon as a pixmap with requested size, mode, and state."""
        img = QImage(size, QImage.Format.Format_ARGB32)
        img.fill(Qt.GlobalColor.transparent)
        pixmap = QPixmap.fromImage(img, Qt.ImageConversionFlag.NoFormatConversion)
        self.paint(QPainter(pixmap), QRect(QPoint(0, 0), size), mode, state)
        return pixmap

    def change_color(self, color: Color) -> None:
        self._color = color
