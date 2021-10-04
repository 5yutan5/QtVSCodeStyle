import sys

from PySide6.QtWidgets import QMessageBox

import qtvscodestyle as qtvsc
from qtvscodestyle.qtpy.QtCore import Qt
from qtvscodestyle.qtpy.QtGui import QAction, QActionGroup
from qtvscodestyle.qtpy.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QSizePolicy,
    QStackedWidget,
    QToolBar,
    QToolButton,
)

app = QApplication(sys.argv)
# Fix the svg icon display becoming low quality in Qt5.
# PyQt6 doesn't have attribute AA_UseHighDpiPixmaps.
if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)  # type: ignore
main_win = QMainWindow()

# Create icon
home_icon = qtvsc.theme_icon(qtvsc.FaSolid.FONT, "activityBar.foreground")
favorite_icon = qtvsc.theme_icon(qtvsc.FaSolid.BOLD, "activityBar.foreground")
settings_icon = qtvsc.theme_icon(qtvsc.Vsc.SETTINGS_GEAR, "activityBar.foreground")

# Create action
action_move_page_a = QAction(home_icon, "Move Page A")
action_move_page_b = QAction(favorite_icon, "Move Page B")
action_move_page_a.setCheckable(True)
action_move_page_b.setCheckable(True)
action_move_page_a.setChecked(True)
action_group = QActionGroup(main_win)
action_group.addAction(action_move_page_a)
action_group.addAction(action_move_page_b)
action_group.setExclusive(True)

action_press_settings_icon = QAction(settings_icon, "Settings")

# Create pages
page_1, page_2 = QLabel("Page 1"), QLabel("Page 2")

# Create stack widget
stack_widget = QStackedWidget()
stack_widget.addWidget(page_1)
stack_widget.addWidget(page_2)
stack_widget.setMinimumSize(300, 300)

# Create activitybar =======================================
activitybar = QToolBar()
activitybar.addActions([action_move_page_a, action_move_page_b])

# You can divide icon with spacer of QToolButton.
spacer = QToolButton()
spacer.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
activitybar.addWidget(spacer)

activitybar.addAction(action_press_settings_icon)

activitybar.setMovable(False)
activitybar.setProperty("type", "activitybar")
# ==========================================================

# Setup Singal
action_move_page_a.triggered.connect(lambda: stack_widget.setCurrentIndex(0))
action_move_page_b.triggered.connect(lambda: stack_widget.setCurrentIndex(1))
action_press_settings_icon.triggered.connect(lambda: QMessageBox.information(main_win, "", "Settings action"))

main_win.addToolBar(Qt.ToolBarArea.LeftToolBarArea, activitybar)
main_win.setCentralWidget(stack_widget)

app.setStyleSheet(qtvsc.load_stylesheet())
main_win.show()
app.exec()
