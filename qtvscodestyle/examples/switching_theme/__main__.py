import sys

import qtvscodestyle as qtvsc
from qtvscodestyle.base import Theme
from qtvscodestyle.qtpy.QtWidgets import QApplication, QComboBox, QDialog, QHBoxLayout

app = QApplication(sys.argv)
main_win = QDialog()
main_win.setMinimumSize(300, 200)

theme_combobox = QComboBox()
theme_combobox.addItems([theme.value["name"] for theme in qtvsc.Theme])
theme_combobox.setCurrentText(Theme.DARK_VS.value["name"])


def change_theme(theme_name) -> None:
    for theme in qtvsc.Theme:
        if theme.value["name"] == theme_name:
            QApplication.instance().setStyleSheet(qtvsc.load_stylesheet(theme))


theme_combobox.currentTextChanged.connect(change_theme)

h_layout = QHBoxLayout(main_win)
h_layout.addWidget(theme_combobox)

app.setStyleSheet(qtvsc.load_stylesheet())
main_win.show()
app.exec()
