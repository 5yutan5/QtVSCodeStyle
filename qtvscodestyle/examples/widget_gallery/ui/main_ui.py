import qtvscodestyle as qtvsc
from qtvscodestyle.examples.widget_gallery.ui.dock import DockUI
from qtvscodestyle.examples.widget_gallery.ui.home import HomeUI
from qtvscodestyle.qtpy.QtCore import Qt
from qtvscodestyle.qtpy.QtGui import QAction
from qtvscodestyle.qtpy.QtWidgets import (
    QMainWindow,
    QMenu,
    QMenuBar,
    QStackedWidget,
    QStatusBar,
    QToolBar,
    QToolButton,
    QWidget,
)


class UI:
    def setup_ui(self, main_win: QMainWindow) -> None:
        # VSCode icons
        home_icon = qtvsc.theme_icon(qtvsc.Vsc.HOME, "activityBar.foreground")
        multi_windows_icon = qtvsc.theme_icon(qtvsc.Vsc.MULTIPLE_WINDOWS, "activityBar.foreground")
        folder_open_icon = qtvsc.theme_icon(qtvsc.Vsc.FOLDER)
        palette_icon = qtvsc.theme_icon(qtvsc.Vsc.SYMBOL_COLOR)
        circle_icon = qtvsc.theme_icon(qtvsc.Vsc.CIRCLE_LARGE_OUTLINE)
        clear_icon = qtvsc.theme_icon(qtvsc.Vsc.CLOSE)
        settings_icon = qtvsc.theme_icon(qtvsc.Vsc.SETTINGS_GEAR)

        # Widgets
        self.central_window = QMainWindow()
        self.stack_widget = QStackedWidget()

        self.action_change_home_window = QAction(home_icon, "Move home")
        self.action_change_dock_window = QAction(multi_windows_icon, "Move dock")
        self.action_open_folder = QAction(folder_open_icon, "Open folder dialog")
        self.action_open_color_dialog = QAction(palette_icon, "Open color dialog", main_win)
        self.action_enable = QAction(circle_icon, "Enable")
        self.action_disable = QAction(clear_icon, "Disable")
        self.actions_theme = [QAction(theme.value["name"]) for theme in qtvsc.Theme]

        activitybar = QToolBar("activitybar")
        toolbar = QToolBar("Toolbar")
        statusbar = QStatusBar()
        menubar = QMenuBar()
        tool_button_settings = QToolButton()
        tool_button_enable = QToolButton()
        tool_button_disable = QToolButton()

        # Setup Widgets
        self.action_change_home_window.setCheckable(True)
        self.action_change_dock_window.setCheckable(True)
        self.action_change_home_window.setChecked(True)
        activitybar.setMovable(False)
        activitybar.addActions([self.action_change_home_window, self.action_change_dock_window])

        tool_button_settings.setIcon(settings_icon)
        tool_button_settings.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        tool_button_enable.setDefaultAction(self.action_enable)
        tool_button_disable.setDefaultAction(self.action_disable)

        toolbar.addActions([self.action_open_folder, self.action_open_color_dialog])
        toolbar.addSeparator()
        toolbar.addWidget(tool_button_settings)

        statusbar.addPermanentWidget(tool_button_enable)
        statusbar.addPermanentWidget(tool_button_disable)
        statusbar.showMessage("Enable")

        menu = menubar.addMenu("&Menu")
        menu.addAction(self.action_open_folder)
        menu.addSeparator()
        menu_toggle_status = menu.addMenu("&Toggle Status")
        menu_toggle_status.addActions([self.action_enable, self.action_disable])

        menu_settings = QMenu(main_win)
        menu_settings.addActions([self.action_enable, self.action_disable])
        menu_theme = menu_settings.addMenu("theme")
        menu_theme.addActions(self.actions_theme)
        tool_button_settings.setMenu(menu_settings)

        self.action_enable.setEnabled(False)

        # setup qss property
        activitybar.setProperty("type", "activitybar")

        # layout
        stack_1 = QWidget()
        home_ui = HomeUI()
        home_ui.setup_ui(stack_1)
        self.stack_widget.addWidget(stack_1)
        stack_2 = QMainWindow()
        dock_ui = DockUI()
        dock_ui._setup_ui(stack_2)
        self.stack_widget.addWidget(stack_2)

        self.central_window.setCentralWidget(self.stack_widget)
        self.central_window.addToolBar(toolbar)

        main_win.setCentralWidget(self.central_window)
        main_win.addToolBar(Qt.ToolBarArea.LeftToolBarArea, activitybar)
        main_win.setMenuBar(menubar)
        main_win.setStatusBar(statusbar)
