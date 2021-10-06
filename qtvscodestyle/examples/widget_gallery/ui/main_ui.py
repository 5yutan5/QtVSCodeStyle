import qtvscodestyle as qtvsc
from qtvscodestyle.examples.widget_gallery.ui.dock import DockUI
from qtvscodestyle.examples.widget_gallery.ui.home import HomeUI
from qtvscodestyle.qtpy.QtCore import Qt
from qtvscodestyle.qtpy.QtGui import QAction, QActionGroup
from qtvscodestyle.qtpy.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QSizePolicy,
    QStackedWidget,
    QStatusBar,
    QToolBar,
    QToolButton,
    QWidget,
)


class UI:
    def setup_ui(self, main_win: QMainWindow) -> None:
        # Icons
        home_icon = qtvsc.theme_icon(qtvsc.Vsc.HOME, "activityBar.foreground")
        multi_windows_icon = qtvsc.theme_icon(qtvsc.Vsc.MULTIPLE_WINDOWS, "activityBar.foreground")
        settings_icon = qtvsc.theme_icon(qtvsc.Vsc.SETTINGS_GEAR, "activityBar.foreground")
        folder_open_icon = qtvsc.theme_icon(qtvsc.Vsc.FOLDER)
        palette_icon = qtvsc.theme_icon(qtvsc.Vsc.SYMBOL_COLOR)
        circle_icon = qtvsc.theme_icon(qtvsc.Vsc.CIRCLE_LARGE_OUTLINE)
        clear_icon = qtvsc.theme_icon(qtvsc.Vsc.CLOSE)
        theme_icon = qtvsc.theme_icon(qtvsc.Vsc.COLOR_MODE)

        # Actions
        self.action_change_home = QAction(home_icon, "Move to home")
        self.action_change_dock = QAction(multi_windows_icon, "Move to dock")
        self.action_open_folder = QAction(folder_open_icon, "Open folder dialog")
        self.action_open_color_dialog = QAction(palette_icon, "Open color dialog", main_win)
        self.action_enable = QAction(circle_icon, "Enable")
        self.action_disable = QAction(clear_icon, "Disable")
        self.actions_theme = [QAction(theme.value["name"]) for theme in qtvsc.Theme]

        self.action_group_toolbar = QActionGroup(main_win)

        # Widgets
        self.central_window = QMainWindow()
        self.stack_widget = QStackedWidget()

        activitybar = QToolBar("activitybar")
        toolbar = QToolBar("Toolbar")
        statusbar = QStatusBar()
        menubar = QMenuBar()
        tool_button_settings = QToolButton()
        tool_button_enable = QToolButton()
        tool_button_disable = QToolButton()
        tool_button_theme = QToolButton()

        self.spacer = QToolButton()

        # Setup Actions
        self.action_change_home.setCheckable(True)
        self.action_change_dock.setCheckable(True)
        self.action_change_home.setChecked(True)
        self.action_group_toolbar.addAction(self.action_change_home)
        self.action_group_toolbar.addAction(self.action_change_dock)

        # Setup Widgets
        self.spacer.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.spacer.setEnabled(False)

        activitybar.setMovable(False)
        activitybar.addActions([self.action_change_home, self.action_change_dock])
        activitybar.addWidget(self.spacer)
        activitybar.addWidget(tool_button_settings)

        tool_button_settings.setIcon(settings_icon)
        tool_button_settings.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        tool_button_enable.setDefaultAction(self.action_enable)
        tool_button_disable.setDefaultAction(self.action_disable)
        tool_button_theme.setIcon(theme_icon)
        tool_button_theme.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        toolbar.addActions([self.action_open_folder, self.action_open_color_dialog])
        toolbar.addSeparator()
        toolbar.addWidget(tool_button_theme)

        statusbar.addPermanentWidget(tool_button_enable)
        statusbar.addPermanentWidget(tool_button_disable)
        statusbar.showMessage("Enable")

        menu_toggle = menubar.addMenu("&Toggle")
        menu_toggle.addActions([self.action_enable, self.action_disable])
        menu_theme = menubar.addMenu("&Theme")
        menu_theme.addActions(self.actions_theme)
        menu_dialog = menubar.addMenu("&Dialog")
        menu_dialog.addActions([self.action_open_folder, self.action_open_color_dialog])

        tool_button_settings.setMenu(menu_toggle)
        tool_button_theme.setMenu(menu_theme)

        self.action_enable.setEnabled(False)

        # setup custom property
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
