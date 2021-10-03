import sys

import qtvscodestyle as qtvsc
from qtvscodestyle.qtpy.QtWidgets import QApplication, QDialog, QGroupBox, QHBoxLayout, QPushButton, QVBoxLayout

app = QApplication(sys.argv)
main_win = QDialog()

# Create pushbutton==========================================
push_button_outlined_normal = QPushButton("Normal")
push_button_outlined_toggle = QPushButton("Toggle")
push_button_contained_normal = QPushButton("Normal")
push_button_contained_toggle = QPushButton("Toggle")

push_button_contained_normal.setProperty("type", "secondary")
push_button_contained_toggle.setProperty("type", "secondary")
# ===========================================================

push_button_outlined_toggle.setCheckable(True)
push_button_outlined_toggle.setChecked(True)
push_button_contained_toggle.setCheckable(True)
push_button_contained_toggle.setChecked(True)

# Create label
group_outlined = QGroupBox("Main")
group_contained = QGroupBox("Secondary")

# Setup layout
v_layout_outlined = QVBoxLayout()
v_layout_outlined.addWidget(push_button_outlined_normal)
v_layout_outlined.addWidget(push_button_outlined_toggle)
group_outlined.setLayout(v_layout_outlined)

v_layout_contained = QVBoxLayout()
v_layout_contained.addWidget(push_button_contained_normal)
v_layout_contained.addWidget(push_button_contained_toggle)
group_contained.setLayout(v_layout_contained)

h_layout_main = QHBoxLayout(main_win)
h_layout_main.addWidget(group_outlined)
h_layout_main.addWidget(group_contained)

main_win.setMinimumSize(300, 200)

app.setStyleSheet(qtvsc.load_stylesheet())
main_win.show()
app.exec()
