import sys

import qtvscodestyle as qtvsc
from qtvscodestyle.examples.widget_gallery.ui.main_ui import UI
from qtvscodestyle.qtpy.QtCore import Qt, Slot
from qtvscodestyle.qtpy.QtWidgets import QApplication, QColorDialog, QFileDialog, QMainWindow


class WidgetGallery(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._ui = UI()
        self._ui.setup_ui(self)
        self._setup()

    def _setup(self) -> None:
        self._ui.action_change_home_window.triggered.connect(self._change_home_win)
        self._ui.action_change_dock_window.triggered.connect(self._change_dock_win)
        self._ui.action_open_folder.triggered.connect(
            lambda: QFileDialog.getOpenFileName(self, "Open File", options=QFileDialog.Option.DontUseNativeDialog)
        )
        self._ui.action_open_color_dialog.triggered.connect(
            lambda: QColorDialog.getColor(parent=self, options=QColorDialog.ColorDialogOption.DontUseNativeDialog)
        )
        self._ui.action_enable.triggered.connect(self._toggle_state)
        self._ui.action_disable.triggered.connect(self._toggle_state)
        for action in self._ui.actions_theme:
            action.triggered.connect(self._change_theme)

    @Slot()
    def _change_home_win(self) -> None:
        self._ui.stack_widget.setCurrentIndex(0)
        self._ui.action_change_home_window.setChecked(True)
        self._ui.action_change_dock_window.setChecked(False)

    @Slot()
    def _change_dock_win(self) -> None:
        self._ui.stack_widget.setCurrentIndex(1)
        self._ui.action_change_home_window.setChecked(False)
        self._ui.action_change_dock_window.setChecked(True)

    @Slot()
    def _toggle_state(self) -> None:
        state = self.sender().text()
        self._ui.central_window.centralWidget().setEnabled(state == "Enable")
        self._ui.action_enable.setEnabled(state == "Disable")
        self._ui.action_disable.setEnabled(state == "Enable")
        self.statusBar().showMessage(state)

    @Slot()
    def _change_theme(self) -> None:
        theme_name = self.sender().text()
        for theme in qtvsc.Theme:
            if theme.value["name"] == theme_name:
                QApplication.instance().setStyleSheet(qtvsc.load_stylesheet(theme))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Fix the svg icon display becoming low quality in Qt5.
    # PyQt6 doesn't have attribute AA_UseHighDpiPixmaps.
    if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):
        app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)  # type: ignore
    win = WidgetGallery()
    win.menuBar().setNativeMenuBar(False)
    app.setStyleSheet(qtvsc.load_stylesheet(qtvsc.Theme.DARK_VS))
    win.show()
    app.exec()
