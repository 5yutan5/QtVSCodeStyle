import sys

import qtvscodestyle as qtvsc
from qtvscodestyle.qtpy.QtCore import Qt
from qtvscodestyle.qtpy.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QStyledItemDelegate,
    QToolButton,
    QWidget,
)

app = QApplication(sys.argv)
main_win = QDialog()
# Fix the svg icon display becoming low quality in Qt5.
# PyQt6 doesn't have attribute AA_UseHighDpiPixmaps.
if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)  # type: ignore


# Fix incurrent item size bug on mac.
class Combobox(QComboBox):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        delegate = QStyledItemDelegate(parent)
        self.setItemDelegate(delegate)

    def showPopup(self) -> None:
        width = self.view().sizeHintForColumn(0) + 20
        self.view().setMinimumWidth(width)
        super().showPopup()


theme_combobox = Combobox(main_win)
theme_combobox.addItems([theme.value["name"] for theme in qtvsc.Theme])
theme_combobox.setCurrentText(qtvsc.Theme.DARK_VS.value["name"])

# Create VSCode icon==========================================
icon = qtvsc.theme_icon(qtvsc.Vsc.STAR_FULL)
icon2 = qtvsc.theme_icon(qtvsc.Vsc.STAR_FULL, "focusBorder")
button, button_disabled = QToolButton(), QToolButton()
button2, button2_disabled = QToolButton(), QToolButton()

button.setIcon(icon)
button_disabled.setIcon(icon)
button_disabled.setEnabled(False)

button2.setIcon(icon2)
button2_disabled.setIcon(icon2)
button2_disabled.setEnabled(False)
# ===========================================================


def change_theme(theme_name) -> None:
    for theme in qtvsc.Theme:
        if theme.value["name"] == theme_name:
            QApplication.instance().setStyleSheet(qtvsc.load_stylesheet(theme))


theme_combobox.currentTextChanged.connect(change_theme)

# Layout
f_layout = QFormLayout()
f_layout.addRow("Normal (icon.foreground)", button)
f_layout.addRow("Disabled (icon.foreground)", button_disabled)
f_layout.addRow("Normal (focusBorder)", button2)
f_layout.addRow("Disabled (focusBorder)", button2_disabled)

h_layout = QHBoxLayout(main_win)
h_layout.addLayout(f_layout)
h_layout.addWidget(theme_combobox)

app.setStyleSheet(qtvsc.load_stylesheet())
main_win.show()

# # Demo code ====================================================================================
# # Switch theme auto
#
# from qtvscodestyle.qtpy.QtCore import QTimer
#
# timer = QTimer(main_win)
# timer.timeout.connect(lambda: theme_combobox.setCurrentIndex(theme_combobox.currentIndex() + 1))
# timer.start(900)
# # ===============================================================================================

app.exec()
