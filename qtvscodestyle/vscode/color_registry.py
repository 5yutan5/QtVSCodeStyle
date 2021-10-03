# ==============================================================================================================
# QtVSCodeStyle.
#
#  Copyright (c) 2015- Microsoft Corporation
#  Copyright (c) 2021- Yunosuke Ohsugi
#
#  Distributed under the terms of the MIT License.
#  See https://github.com/microsoft/vscode/blob/main/LICENSE.txt
#
# Original codes:
#   https://github.com/microsoft/vscode/blob/main/src/vs/platform/theme/common/colorRegistry.ts
#   https://github.com/microsoft/vscode/blob/main/src/vs/workbench/common/theme.ts
#   https://github.com/microsoft/vscode/blob/main/src/vs/editor/common/view/editorColorRegistry.ts
#   https://github.com/microsoft/vscode/blob/main/src/vs/workbench/contrib/comments/browser/commentGlyphWidget.ts
#   https://github.com/microsoft/vscode/blob/main/src/vs/workbench/contrib/preferences/browser/settingsWidgets.ts
#
# (see NOTICE.md in the QtVSCodeStyle root directory for details)
# ===============================================================================================================

from qtvscodestyle.vscode.color import RGBA, Color
from qtvscodestyle.vscode.color_registry_manager import (
    darken,
    if_defined_then_else,
    less_prominent,
    lighten,
    register_color,
    transparent,
)


def setup_default_color_registry() -> None:
    # =============================================================================================
    # Main color
    # Rewrite:
    #   https://github.com/microsoft/vscode/blob/main/src/vs/platform/theme/common/colorRegistry.ts
    # =============================================================================================

    # ----- base colors
    foreground = register_color("foreground", {"dark": "#CCCCCC", "light": "#616161", "hc": "#FFFFFF"})
    register_color("errorForeground", {"dark": "#F48771", "light": "#A1260D", "hc": "#F48771"})
    iconForeground = register_color("icon.foreground", {"dark": "#C5C5C5", "light": "#424242", "hc": "#FFFFFF"})

    focusBorder = register_color("focusBorder", {"dark": "#007FD4", "light": "#0090F1", "hc": "#F38518"})

    contrastBorder = register_color(
        "contrastBorder", {"light": "transparent", "dark": "transparent", "hc": "#6FC3DF"}
    )  # Minor modification(None -> "transparent")
    activeContrastBorder = register_color("contrastActiveBorder", {"light": None, "dark": None, "hc": focusBorder})

    register_color(
        "selection.background", {"light": "#a9d8ff", "dark": "#5b89b4", "hc": "#a9d8ff"}
    )  # Minor modification(None -> color)

    # ------ text colors
    register_color("textLink.foreground", {"light": "#006AB1", "dark": "#3794FF", "hc": "#3794FF"})
    register_color("textLink.activeForeground", {"light": "#006AB1", "dark": "#3794FF", "hc": "#3794FF"})

    # ----- widgets

    inputBackground = register_color(
        "input.background", {"dark": "#3C3C3C", "light": Color.white(), "hc": Color.black()}
    )
    inputForeground = register_color("input.foreground", {"dark": foreground, "light": foreground, "hc": foreground})
    inputBorder = register_color(
        "input.border", {"dark": "transparent", "light": "#CECECE", "hc": contrastBorder}
    )  # Minor modification(None -> "transparent", None -> "#CECECE"(Same dropdown border))
    inputValidationWarningBorder = register_color(
        "inputValidation.warningBorder", {"dark": "#B89500", "light": "#B89500", "hc": contrastBorder}
    )
    inputValidationErrorBorder = register_color(
        "inputValidation.errorBorder", {"dark": "#BE1100", "light": "#BE1100", "hc": contrastBorder}
    )

    register_color(
        "input.placeholderForeground",
        {
            "light": transparent(foreground, 0.5),
            "dark": transparent(foreground, 0.5),
            "hc": transparent(foreground, 0.7),
        },
    )

    selectBackground = register_color(
        "dropdown.background", {"dark": "#3C3C3C", "light": Color.white(), "hc": Color.black()}
    )
    register_color("dropdown.listBackground", {"dark": None, "light": None, "hc": Color.black()})
    selectForeground = register_color("dropdown.foreground", {"dark": "#F0F0F0", "light": None, "hc": Color.white()})
    selectBorder = register_color(
        "dropdown.border", {"dark": selectBackground, "light": "#CECECE", "hc": contrastBorder}
    )

    simpleCheckboxBackground = register_color(
        "checkbox.background", {"dark": selectBackground, "light": selectBackground, "hc": selectBackground}
    )
    simpleCheckboxForeground = register_color(
        "checkbox.foreground", {"dark": selectForeground, "light": selectForeground, "hc": selectForeground}
    )
    simpleCheckboxBorder = register_color(
        "checkbox.border", {"dark": selectBorder, "light": selectBorder, "hc": selectBorder}
    )

    register_color("button.foreground", {"dark": Color.white(), "light": Color.white(), "hc": Color.white()})
    buttonBackground = register_color("button.background", {"dark": "#0E639C", "light": "#007ACC", "hc": None})
    register_color(
        "button.hoverBackground",
        {"dark": lighten(buttonBackground, 0.2), "light": darken(buttonBackground, 0.2), "hc": None},
    )
    register_color("button.border", {"dark": contrastBorder, "light": contrastBorder, "hc": contrastBorder})

    register_color("button.secondaryForeground", {"dark": Color.white(), "light": Color.white(), "hc": Color.white()})
    buttonSecondaryBackground = register_color(
        "button.secondaryBackground", {"dark": "#3A3D41", "light": "#5F6A79", "hc": None}
    )
    register_color(
        "button.secondaryHoverBackground",
        {"dark": lighten(buttonSecondaryBackground, 0.2), "light": darken(buttonSecondaryBackground, 0.2), "hc": None},
    )
    register_color(
        "scrollbarSlider.background",
        {
            "dark": Color.from_hex("#797979").transparent(0.4),
            "light": Color.from_hex("#646464").transparent(0.4),
            "hc": transparent(contrastBorder, 0.6),
        },
    )
    register_color(
        "scrollbarSlider.hoverBackground",
        {
            "dark": Color.from_hex("#646464").transparent(0.7),
            "light": Color.from_hex("#646464").transparent(0.7),
            "hc": transparent(contrastBorder, 0.8),
        },
    )
    register_color(
        "scrollbarSlider.activeBackground",
        {
            "dark": Color.from_hex("#BFBFBF").transparent(0.4),
            "light": Color.from_hex("#000000").transparent(0.6),
            "hc": contrastBorder,
        },
    )

    progressBarBackground = register_color(
        "progressBar.background",
        {"dark": Color.from_hex("#0E70C0"), "light": Color.from_hex("#0E70C0"), "hc": contrastBorder},
    )

    # Editor background color
    # Because of bug https://monacotools.visualstudio.com/DefaultCollection/Monaco/_workitems/edit/13254
    # we are *not* using the color white (or #ffffff, rgba(255,255,255)) but something very close to white.
    editorBackground = register_color(
        "editor.background", {"light": "#fffffe", "dark": "#1E1E1E", "hc": Color.black()}
    )

    # Editor foreground color.
    register_color("editor.foreground", {"light": "#333333", "dark": "#BBBBBB", "hc": Color.white()})

    # Editor widgets
    editorWidgetBackground = register_color(
        "editorWidget.background", {"dark": "#252526", "light": "#F3F3F3", "hc": "#0C141F"}
    )

    editorWidgetForeground = register_color(
        "editorWidget.foreground", {"dark": foreground, "light": foreground, "hc": foreground}
    )

    editorWidgetBorder = register_color(
        "editorWidget.border", {"dark": "#454545", "light": "#C8C8C8", "hc": contrastBorder}
    )

    register_color("editorWidget.resizeBorder", {"light": None, "dark": None, "hc": None})

    # Editor selection colors.
    editorSelectionBackground = register_color(
        "editor.selectionBackground", {"light": "#ADD6FF", "dark": "#264F78", "hc": "#f3f518"}
    )
    register_color("editor.selectionForeground", {"light": None, "dark": None, "hc": "#000000"})
    register_color(
        "editor.inactiveSelectionBackground",
        {
            "light": transparent(editorSelectionBackground, 0.5),
            "dark": transparent(editorSelectionBackground, 0.5),
            "hc": transparent(editorSelectionBackground, 0.5),
        },
    )  # deprecation
    register_color(
        "editor.selectionHighlightBackground",
        {
            "light": less_prominent(editorSelectionBackground, editorBackground, 0.3, 0.6),
            "dark": less_prominent(editorSelectionBackground, editorBackground, 0.3, 0.6),
            "hc": None,
        },
    )  # deprecation
    register_color("editor.selectionHighlightBorder", {"light": None, "dark": None, "hc": activeContrastBorder})

    # Editor hover
    register_color(
        "editorHoverWidget.background",
        {"light": editorWidgetBackground, "dark": editorWidgetBackground, "hc": editorWidgetBackground},
    )
    register_color(
        "editorHoverWidget.foreground",
        {"light": editorWidgetForeground, "dark": editorWidgetForeground, "hc": editorWidgetForeground},
    )
    register_color(
        "editorHoverWidget.border", {"light": editorWidgetBorder, "dark": editorWidgetBorder, "hc": editorWidgetBorder}
    )

    # List and tree colors
    listFocusBackground = register_color("list.focusBackground", {"dark": None, "light": None, "hc": None})
    register_color("list.focusForeground", {"dark": None, "light": None, "hc": None})
    register_color("list.focusOutline", {"dark": focusBorder, "light": focusBorder, "hc": activeContrastBorder})
    listActiveSelectionBackground = register_color(
        "list.activeSelectionBackground", {"dark": "#094771", "light": "#0060C0", "hc": editorBackground}
    )  # Minor modification(None -> editorBackground)
    listActiveSelectionForeground = register_color(
        "list.activeSelectionForeground", {"dark": Color.white(), "light": Color.white(), "hc": foreground}
    )  # Minor modification(None -> foreground)
    register_color(
        "list.activeSelectionIconForeground", {"dark": Color.white(), "light": Color.white(), "hc": Color.white()}
    )  # Minor modification(None -> color)
    register_color(
        "list.inactiveSelectionBackground", {"dark": "#37373D", "light": "#E4E6F1", "hc": editorBackground}
    )  # Minor modification(None -> editorBackground)
    register_color("list.inactiveSelectionForeground", {"dark": None, "light": None, "hc": None})
    register_color("list.inactiveFocusBackground", {"dark": None, "light": None, "hc": None})
    register_color("list.inactiveFocusOutline", {"dark": None, "light": None, "hc": None})
    register_color(
        "list.hoverBackground", {"dark": "#2A2D2E", "light": "#F0F0F0", "hc": "transparent"}
    )  # Minor modification(None -> "transparent")
    register_color("list.hoverForeground", {"dark": None, "light": None, "hc": None})
    register_color("list.dropBackground", {"dark": "#062F4A", "light": "#D6EBFF", "hc": None})
    listHighlightForeground = register_color(
        "list.highlightForeground", {"dark": "#18A3FF", "light": "#0066BF", "hc": focusBorder}
    )
    register_color(
        "list.focusHighlightForeground",
        {
            "dark": listHighlightForeground,
            "light": if_defined_then_else(listActiveSelectionBackground, listHighlightForeground, "#9DDDFF"),
            "hc": listHighlightForeground,
        },
    )
    treeIndentGuidesStroke = register_color(
        "tree.indentGuidesStroke", {"dark": "#585858", "light": "#a9a9a9", "hc": "#a9a9a9"}
    )

    # Menu colors
    register_color(
        "menu.border", {"dark": "transparent", "light": "transparent", "hc": contrastBorder}
    )  # Minor modification(None -> "transparent")
    register_color("menu.foreground", {"dark": selectForeground, "light": foreground, "hc": selectForeground})
    register_color("menu.background", {"dark": selectBackground, "light": selectBackground, "hc": selectBackground})
    register_color(
        "menu.selectionForeground",
        {
            "dark": listActiveSelectionForeground,
            "light": listActiveSelectionForeground,
            "hc": listActiveSelectionForeground,
        },
    )
    register_color(
        "menu.selectionBackground",
        {
            "dark": listActiveSelectionBackground,
            "light": listActiveSelectionBackground,
            "hc": listActiveSelectionBackground,
        },
    )
    register_color(
        "menu.selectionBorder", {"dark": "transparent", "light": "transparent", "hc": activeContrastBorder}
    )  # Minor modification(None -> "transparent")
    register_color("menu.separatorBackground", {"dark": "#BBBBBB", "light": "#888888", "hc": contrastBorder})

    # Toolbar colors
    toolbarHoverBackground = register_color(
        "toolbar.hoverBackground", {"dark": "#5a5d5e50", "light": "#b8b8b850", "hc": None}
    )
    register_color(
        "toolbar.hoverOutline", {"dark": "transparent", "light": "transparent", "hc": activeContrastBorder}
    )  # Minor modification(None -> "transparent")
    register_color(
        "toolbar.activeBackground",
        {"dark": lighten(toolbarHoverBackground, 0.1), "light": darken(toolbarHoverBackground, 0.1), "hc": None},
    )

    # =============================================================================================
    # Common colors
    # Rewrite:
    #   https://github.com/microsoft/vscode/blob/main/src/vs/workbench/common/theme.ts
    # =============================================================================================
    # < --- Tabs --- >

    # #region Tab Background

    TAB_ACTIVE_BACKGROUND = register_color(
        "tab.activeBackground", {"dark": editorBackground, "light": editorBackground, "hc": editorBackground}
    )

    register_color(
        "tab.unfocusedActiveBackground",
        {"dark": TAB_ACTIVE_BACKGROUND, "light": TAB_ACTIVE_BACKGROUND, "hc": TAB_ACTIVE_BACKGROUND},
    )

    TAB_INACTIVE_BACKGROUND = register_color(
        "tab.inactiveBackground", {"dark": "#2D2D2D", "light": "#ECECEC", "hc": None}
    )

    register_color(
        "tab.unfocusedInactiveBackground",
        {"dark": TAB_INACTIVE_BACKGROUND, "light": TAB_INACTIVE_BACKGROUND, "hc": TAB_INACTIVE_BACKGROUND},
    )

    # #endregion

    # #region Tab Foreground

    TAB_ACTIVE_FOREGROUND = register_color(
        "tab.activeForeground", {"dark": Color.white(), "light": "#333333", "hc": Color.white()}
    )

    TAB_INACTIVE_FOREGROUND = register_color(
        "tab.inactiveForeground",
        {
            "dark": transparent(TAB_ACTIVE_FOREGROUND, 0.5),
            "light": transparent(TAB_ACTIVE_FOREGROUND, 0.7),
            "hc": Color.white(),
        },
    )

    register_color(
        "tab.unfocusedActiveForeground",
        {
            "dark": transparent(TAB_ACTIVE_FOREGROUND, 0.5),
            "light": transparent(TAB_ACTIVE_FOREGROUND, 0.7),
            "hc": Color.white(),
        },
    )

    register_color(
        "tab.unfocusedInactiveForeground",
        {
            "dark": transparent(TAB_INACTIVE_FOREGROUND, 0.5),
            "light": transparent(TAB_INACTIVE_FOREGROUND, 0.5),
            "hc": Color.white(),
        },
    )

    # #endregion

    # #region Tab Hover Foreground/Background

    TAB_HOVER_BACKGROUND = register_color("tab.hoverBackground", {"dark": None, "light": None, "hc": None})

    register_color(
        "tab.unfocusedHoverBackground",
        {"dark": transparent(TAB_HOVER_BACKGROUND, 0.5), "light": transparent(TAB_HOVER_BACKGROUND, 0.7), "hc": None},
    )

    TAB_HOVER_FOREGROUND = register_color("tab.hoverForeground", {"dark": None, "light": None, "hc": None})

    register_color(
        "tab.unfocusedHoverForeground",
        {"dark": transparent(TAB_HOVER_FOREGROUND, 0.5), "light": transparent(TAB_HOVER_FOREGROUND, 0.5), "hc": None},
    )

    # #endregion

    # #region Tab Borders

    register_color("tab.border", {"dark": "#252526", "light": "#F3F3F3", "hc": contrastBorder})

    TAB_ACTIVE_BORDER = register_color("tab.activeBorder", {"dark": None, "light": None, "hc": None})

    register_color(
        "tab.unfocusedActiveBorder",
        {"dark": transparent(TAB_ACTIVE_BORDER, 0.5), "light": transparent(TAB_ACTIVE_BORDER, 0.7), "hc": None},
    )

    TAB_ACTIVE_BORDER_TOP = register_color("tab.activeBorderTop", {"dark": None, "light": None, "hc": None})

    register_color(
        "tab.unfocusedActiveBorderTop",
        {
            "dark": transparent(TAB_ACTIVE_BORDER_TOP, 0.5),
            "light": transparent(TAB_ACTIVE_BORDER_TOP, 0.7),
            "hc": None,
        },
    )

    TAB_HOVER_BORDER = register_color("tab.hoverBorder", {"dark": None, "light": None, "hc": None})

    register_color(
        "tab.unfocusedHoverBorder",
        {"dark": transparent(TAB_HOVER_BORDER, 0.5), "light": transparent(TAB_HOVER_BORDER, 0.7), "hc": None},
    )

    # #endregion

    #  < --- Editors --- >

    register_color("editorGroupHeader.tabsBackground", {"dark": "#252526", "light": "#F3F3F3", "hc": None})

    register_color("editorGroupHeader.tabsBorder", {"dark": None, "light": None, "hc": None})

    register_color(
        "editorGroupHeader.noTabsBackground",
        {"dark": editorBackground, "light": editorBackground, "hc": editorBackground},
    )

    register_color("editorGroupHeader.border", {"dark": None, "light": None, "hc": contrastBorder})

    register_color("editorGroup.border", {"dark": "#444444", "light": "#E7E7E7", "hc": contrastBorder})

    #  < --- Status --- >

    register_color("statusBar.foreground", {"dark": "#FFFFFF", "light": "#FFFFFF", "hc": "#FFFFFF"})

    STATUS_BAR_BACKGROUND = register_color("statusBar.background", {"dark": "#007ACC", "light": "#007ACC", "hc": None})

    register_color(
        "statusBar.border", {"dark": contrastBorder, "light": contrastBorder, "hc": contrastBorder}
    )  # Minor modification(None -> contrastBorder)

    register_color(
        "statusBarItem.activeBackground",
        {
            "dark": Color.white().transparent(0.18),
            "light": Color.white().transparent(0.18),
            "hc": Color.white().transparent(0.18),
        },
    )

    register_color(
        "statusBarItem.hoverBackground",
        {
            "dark": Color.white().transparent(0.12),
            "light": Color.white().transparent(0.12),
            "hc": Color.white().transparent(0.12),
        },
    )

    #  < --- Activity Bar --- >

    register_color("activityBar.background", {"dark": "#333333", "light": "#2C2C2C", "hc": "#000000"})

    ACTIVITY_BAR_FOREGROUND = register_color(
        "activityBar.foreground", {"dark": Color.white(), "light": Color.white(), "hc": Color.white()}
    )

    register_color(
        "activityBar.inactiveForeground",
        {
            "dark": transparent(ACTIVITY_BAR_FOREGROUND, 0.4),
            "light": transparent(ACTIVITY_BAR_FOREGROUND, 0.4),
            "hc": Color.white(),
        },
    )

    register_color(
        "activityBar.border", {"dark": contrastBorder, "light": contrastBorder, "hc": contrastBorder}
    )  # Minor modification(None -> contrastBorder)

    register_color(
        "activityBar.activeBorder", {"dark": ACTIVITY_BAR_FOREGROUND, "light": ACTIVITY_BAR_FOREGROUND, "hc": None}
    )

    register_color("activityBar.activeFocusBorder", {"dark": None, "light": None, "hc": None})

    register_color("activityBar.activeBackground", {"dark": None, "light": None, "hc": None})

    #  < --- Side Bar --- >

    register_color("sideBar.background", {"dark": "#252526", "light": "#F3F3F3", "hc": "#000000"})

    register_color("sideBar.foreground", {"dark": None, "light": None, "hc": None})

    register_color("sideBar.border", {"dark": None, "light": None, "hc": contrastBorder})

    #  < --- Title Bar --- >

    TITLE_BAR_ACTIVE_FOREGROUND = register_color(
        "titleBar.activeForeground", {"dark": "#CCCCCC", "light": "#333333", "hc": "#FFFFFF"}
    )

    register_color(
        "titleBar.inactiveForeground",
        {
            "dark": transparent(TITLE_BAR_ACTIVE_FOREGROUND, 0.6),
            "light": transparent(TITLE_BAR_ACTIVE_FOREGROUND, 0.6),
            "hc": None,
        },
    )

    TITLE_BAR_ACTIVE_BACKGROUND = register_color(
        "titleBar.activeBackground", {"dark": "#3C3C3C", "light": "#DDDDDD", "hc": "#000000"}
    )

    register_color(
        "titleBar.inactiveBackground",
        {
            "dark": transparent(TITLE_BAR_ACTIVE_BACKGROUND, 0.6),
            "light": transparent(TITLE_BAR_ACTIVE_BACKGROUND, 0.6),
            "hc": None,
        },
    )

    register_color(
        "titleBar.border", {"dark": "transparent", "light": "transparent", "hc": contrastBorder}
    )  # Minor modification(None -> "transparent")

    #  < --- Menubar --- >

    register_color(
        "menubar.selectionForeground",
        {"dark": TITLE_BAR_ACTIVE_FOREGROUND, "light": TITLE_BAR_ACTIVE_FOREGROUND, "hc": TITLE_BAR_ACTIVE_FOREGROUND},
    )

    register_color(
        "menubar.selectionBackground",
        {"dark": transparent(Color.white(), 0.1), "light": transparent(Color.black(), 0.1), "hc": None},
    )

    register_color(
        "menubar.selectionBorder",
        {
            "dark": "transparent",
            "light": "transparent",
            "hc": activeContrastBorder,
        },  # Minor modification(None -> "transparent")
    )

    # =============================================================================================
    # Other colors
    # =============================================================================================

    # Editor colors
    # Rewrite:
    #   https://github.com/microsoft/vscode/blob/main/src/vs/editor/common/view/editorColorRegistry.ts
    #   https://github.com/microsoft/vscode/blob/main/src/vs/workbench/contrib/comments/browser/commentGlyphWidget.ts

    register_color("editor.lineHighlightBackground", {"dark": None, "light": None, "hc": None})
    register_color("editor.lineHighlightBorder", {"dark": "#282828", "light": "#eeeeee", "hc": "#f38518"})

    # Settings editor colors
    # Rewrite:
    #   https://github.com/microsoft/vscode/blob/main/src/vs/workbench/contrib/preferences/browser/settingsWidgets.ts

    register_color("debugToolBar.background", {"dark": "#333333", "light": "#F3F3F3", "hc": "#000000"})

    register_color(
        "debugToolBar.border", {"dark": contrastBorder, "light": contrastBorder, "hc": contrastBorder}
    )  # Minor modification(None -> contrastBorder)

    # Settings editor colors
    # Rewrite:
    #   https://github.com/microsoft/vscode/blob/main/src/vs/workbench/contrib/preferences/browser/settingsWidgets.ts

    register_color("settings.headerForeground", {"light": "#444444", "dark": "#e7e7e7", "hc": "#ffffff"})
    register_color(
        "settings.modifiedItemIndicator",
        {"light": Color(RGBA(102, 175, 224)), "dark": Color(RGBA(12, 125, 157)), "hc": Color(RGBA(0, 73, 122))},
    )

    # Enum control colors
    register_color(
        "settings.dropdownBackground", {"dark": selectBackground, "light": selectBackground, "hc": selectBackground}
    )
    register_color(
        "settings.dropdownForeground", {"dark": selectForeground, "light": selectForeground, "hc": selectForeground}
    )
    register_color("settings.dropdownBorder", {"dark": selectBorder, "light": selectBorder, "hc": selectBorder})
    register_color(
        "settings.dropdownListBorder",
        {"dark": editorWidgetBorder, "light": editorWidgetBorder, "hc": editorWidgetBorder},
    )

    # Bool control colors
    register_color(
        "settings.checkboxBackground",
        {"dark": simpleCheckboxBackground, "light": simpleCheckboxBackground, "hc": simpleCheckboxBackground},
    )
    register_color(
        "settings.checkboxForeground",
        {"dark": simpleCheckboxForeground, "light": simpleCheckboxForeground, "hc": simpleCheckboxForeground},
    )
    register_color(
        "settings.checkboxBorder",
        {"dark": simpleCheckboxBorder, "light": simpleCheckboxBorder, "hc": simpleCheckboxBorder},
    )

    # Text control colors
    register_color(
        "settings.textInputBackground", {"dark": inputBackground, "light": inputBackground, "hc": inputBackground}
    )
    register_color(
        "settings.textInputForeground", {"dark": inputForeground, "light": inputForeground, "hc": inputForeground}
    )
    register_color("settings.textInputBorder", {"dark": inputBorder, "light": inputBorder, "hc": inputBorder})

    # Number control colors
    register_color(
        "settings.numberInputBackground", {"dark": inputBackground, "light": inputBackground, "hc": inputBackground}
    )
    register_color(
        "settings.numberInputForeground", {"dark": inputForeground, "light": inputForeground, "hc": inputForeground}
    )
    register_color("settings.numberInputBorder", {"dark": inputBorder, "light": inputBorder, "hc": inputBorder})

    focusedRowBackground = register_color(
        "settings.focusedRowBackground",
        {
            "dark": Color.from_hex("#808080").transparent(0.14),
            "light": transparent(listFocusBackground, 0.4),
            "hc": None,
        },
    )

    register_color(
        "settings.rowHoverBackground",
        {"dark": transparent(focusedRowBackground, 0.5), "light": transparent(focusedRowBackground, 0.7), "hc": None},
    )

    register_color(
        "settings.focusedRowBorder",
        {"dark": Color.white().transparent(0.12), "light": Color.black().transparent(0.12), "hc": focusBorder},
    )

    # =============================================================================================
    # QtVSCodeTheme original colors
    # =============================================================================================

    register_color(
        "focusBorder.disabled",
        {
            "dark": transparent(focusBorder, 0.4),
            "light": transparent(focusBorder, 0.4),
            "hc": transparent(focusBorder, 0.4),
        },
    )

    register_color(
        "foreground.disabled",
        {
            "dark": transparent(foreground, 0.4),
            "light": transparent(foreground, 0.4),
            "hc": transparent(foreground, 0.4),
        },
    )

    register_color(
        "icon.foreground.disabled",
        {
            "dark": transparent(iconForeground, 0.4),
            "light": transparent(iconForeground, 0.4),
            "hc": transparent(iconForeground, 0.4),
        },
    )

    register_color(
        "checkbox.foreground.disabled",
        {
            "dark": transparent(iconForeground, 0.4),
            "light": transparent(iconForeground, 0.4),
            "hc": transparent(iconForeground, 0.4),
        },
    )

    register_color(
        "checkbox.border.inActive",
        {
            "dark": simpleCheckboxBorder,
            "light": simpleCheckboxBorder,
            "hc": transparent(simpleCheckboxBorder, 0.6),
        },
    )

    register_color(
        "checkbox.border.active",
        {
            "dark": simpleCheckboxBorder,
            "light": simpleCheckboxBorder,
            "hc": simpleCheckboxBorder,
        },
    )

    register_color(
        "titleBar.activeForeground.disabled",
        {
            "dark": transparent(TITLE_BAR_ACTIVE_FOREGROUND, 0.4),
            "light": transparent(TITLE_BAR_ACTIVE_FOREGROUND, 0.4),
            "hc": transparent(TITLE_BAR_ACTIVE_FOREGROUND, 0.4),
        },
    )

    register_color(
        "statusBarItem.hoverBackground.disabled",
        {
            "dark": darken(STATUS_BAR_BACKGROUND, 0.4),
            "light": lighten(STATUS_BAR_BACKGROUND, 0.4),
            "hc": STATUS_BAR_BACKGROUND,
        },
    )

    register_color(
        "progressBar.background.disabled",
        {
            "dark": transparent(progressBarBackground, 0.3),
            "light": transparent(progressBarBackground, 0.3),
            "hc": progressBarBackground,
        },
    )

    register_color(
        "button.background.active",
        {
            "dark": lighten(buttonBackground, 0.5),
            "light": lighten(buttonBackground, 0.4),
            "hc": buttonBackground,
        },
    )

    register_color(
        "button.background.disabled",
        {
            "dark": transparent(buttonBackground, 0.4),
            "light": transparent(buttonBackground, 0.4),
            "hc": buttonBackground,
        },
    )

    register_color(
        "button.secondaryBackground.active",
        {
            "dark": lighten(buttonSecondaryBackground, 0.7),
            "light": darken(buttonSecondaryBackground, 0.7),
            "hc": buttonSecondaryBackground,
        },
    )

    register_color(
        "button.secondaryBackground.disabled",
        {
            "dark": transparent(buttonSecondaryBackground, 0.3),
            "light": transparent(buttonSecondaryBackground, 0.3),
            "hc": buttonSecondaryBackground,
        },
    )

    register_color(
        "button.flatBackground.hover",
        {
            "dark": Color.white().transparent(0.1),
            "light": Color.black().transparent(0.1),
            "hc": None,
        },
    )

    register_color(
        "button.flatBackground.active",
        {
            "dark": Color.white().transparent(0.2),
            "light": Color.black().transparent(0.2),
            "hc": None,
        },
    )

    register_color(
        "tree.indentGuidesStroke.inActive",
        {
            "dark": transparent(treeIndentGuidesStroke, 0.6),
            "light": transparent(treeIndentGuidesStroke, 0.6),
            "hc": transparent(treeIndentGuidesStroke, 0.6),
        },
    )

    register_color(
        "tree.indentGuidesStroke.disabled",
        {
            "dark": transparent(treeIndentGuidesStroke, 0.3),
            "light": transparent(treeIndentGuidesStroke, 0.3),
            "hc": transparent(treeIndentGuidesStroke, 0.3),
        },
    )

    register_color(
        "inputValidation.warningBorder.disabled",
        {
            "dark": transparent(inputValidationWarningBorder, 0.3),
            "light": transparent(inputValidationWarningBorder, 0.3),
            "hc": transparent(inputValidationWarningBorder, 0.3),
        },
    )

    register_color(
        "inputValidation.errorBorder.disabled",
        {
            "dark": transparent(inputValidationErrorBorder, 0.3),
            "light": transparent(inputValidationErrorBorder, 0.3),
            "hc": transparent(inputValidationErrorBorder, 0.3),
        },
    )
