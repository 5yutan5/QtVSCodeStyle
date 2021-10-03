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

from qtvscodestyle.qtpy.QtCore import QPoint, QRect, QSize, Qt
from qtvscodestyle.qtpy.QtGui import QColor, QFont, QIcon, QIconEngine, QPainter, QPixmap
from qtvscodestyle.vscode.color import Color


class _CharIconPainter:
    def paint(self, painter: QPainter, rect: QRect, mode: QIcon.Mode, font: QFont, char: str, color: Color) -> None:
        # A 16 pixel-high icon yields a font size of 14, which is pixel perfect
        # for font-awesome. 16 * 0.875 = 14
        # The reason why the glyph size is smaller than the icon size is to
        # account for font bearing.
        draw_size = round(0.875 * rect.height())
        font.setPixelSize(draw_size)

        if mode == QIcon.Mode.Disabled:
            color = color.transparent(0.3)
        q_color = self._parse_color(color)

        painter.save()
        painter.setPen(q_color)
        painter.setFont(font)
        painter.drawText(rect, int(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter), char)
        painter.restore()

    @staticmethod
    def _parse_color(color: Color) -> QColor:
        r, g, b, a = color.rgba
        return QColor(int(r), int(g), int(b), int(a * 250))


class CharIconEngine(QIconEngine):
    def __init__(self, font: QFont, char: str, color: Color) -> None:
        self._painter = _CharIconPainter()
        self._font = font
        self._char = char
        self._color = color
        super().__init__()

    def paint(self, painter: QPainter, rect: QRect, mode: QIcon.Mode, state):
        """Paint the icon int ``rect`` using ``painter``."""
        self._painter.paint(painter, rect, mode, self._font, self._char, self._color)

    def clone(self):
        """Required to subclass abstract QIconEngine."""
        return CharIconEngine(self._font, self._char, self._color)

    def pixmap(self, size: QSize, mode: QIcon.Mode, state: QIcon.State):
        """Return the icon as a pixmap with requested size, mode, and state."""
        pixmap = QPixmap(size)
        pixmap.fill(Qt.GlobalColor.transparent)
        self.paint(QPainter(pixmap), QRect(QPoint(0, 0), size), mode, state)
        return pixmap

    def change_color(self, color: Color) -> None:
        self._color = color
