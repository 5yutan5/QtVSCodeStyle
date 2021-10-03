import sys

import qtvscodestyle as qtvsc
from qtvscodestyle.qtpy.QtCore import Qt
from qtvscodestyle.qtpy.QtGui import QAction, QActionGroup
from qtvscodestyle.qtpy.QtWidgets import QApplication, QLabel, QMainWindow, QStackedWidget, QToolBar

app = QApplication(sys.argv)
# Fix the svg icon display becoming low quality in Qt5.
# PyQt6 doesn't have attribute AA_UseHighDpiPixmaps.
if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)  # type: ignore
main_win = QMainWindow()

# Create icon
home_icon = qtvsc.theme_icon(qtvsc.FaSolid.FONT, "activityBar.foreground")
favorite_icon = qtvsc.theme_icon(qtvsc.FaSolid.BOLD, "activityBar.foreground")

# Create action
action_move_page_1 = QAction(home_icon, "Move Page 1")
action_move_page_2 = QAction(favorite_icon, "Move Page2")
action_move_page_1.setCheckable(True)
action_move_page_2.setCheckable(True)
action_move_page_1.setChecked(True)
action_group = QActionGroup(main_win)
action_group.addAction(action_move_page_1)
action_group.addAction(action_move_page_2)
action_group.setExclusive(True)

# Create pages
page_1 = QLabel("Page 1")
page_2 = QLabel("Page 2")

# Create stack widget
stack_widget = QStackedWidget()
stack_widget.addWidget(page_1)
stack_widget.addWidget(page_2)
stack_widget.setMinimumSize(300, 300)

# Create activitybar============================================
activitybar = QToolBar()
activitybar.addActions([action_move_page_1, action_move_page_2])
activitybar.setMovable(False)
activitybar.setProperty("type", "activitybar")
# ==========================================================

# Setup Singal
action_move_page_1.triggered.connect(lambda: stack_widget.setCurrentIndex(0))
action_move_page_2.triggered.connect(lambda: stack_widget.setCurrentIndex(1))

main_win.addToolBar(Qt.ToolBarArea.LeftToolBarArea, activitybar)
main_win.setCentralWidget(stack_widget)

app.setStyleSheet(qtvsc.load_stylesheet())
main_win.show()
app.exec()
