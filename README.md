QtVSCodeStyle
=============
[![PyPI Latest Release](https://img.shields.io/pypi/v/qtvscodestyle.svg?color=orange)](https://pypi.org/project/qtvscodestyle/)
[![Python Versions](https://img.shields.io/pypi/pyversions/qtvscodestyle.svg?color=blue)](https://www.python.org/downloads/)
[![Qt Versions](https://img.shields.io/badge/Qt-5%20|%206-blue.svg?&logo=Qt&logoWidth=18&logoColor=white)](https://www.qt.io/qt-for-python)
[![License](https://img.shields.io/github/license/5yutan5/QtVSCodeStyle.svg?color=green)](https://github.com/5yutan5/QtVSCodeStyle/blob/main/LICENSE.txt/)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/5yutan5/QtVSCodeStyle.svg?logo=lgtm&logoWidth=18&color=success)](https://lgtm.com/projects/g/5yutan5/QtVSCodeStyle/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/5yutan5/QtVSCodeStyle.svg?logo=lgtm&logoWidth=18&color=success)](https://lgtm.com/projects/g/5yutan5/QtVSCodeStyle/context:python)
[![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/python/black)

VS Code Style for PySide and PyQt.

QtVSCodeStyle enables to use VS Code themes in pyqt and pyside.
The default and extension themes of VS Code can be used.


## SCREENSHOTS
|[Dark (Visual Studio)](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_dark.png)|[Light (Visual Studio)](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_light.png)|[Dark High Contrast](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_hc.png)|
| :--: | :--: | :--: |
|[![widget_gallery_dark_theme](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_dark.png)](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_dark.png)|[![widget_gallery_light_them](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_light.png)](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_light.png)|[![widget_gallery_light_them](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_hc.png)](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_hc.png)|
|[Night Owl](https://github.com/sdras/night-owl-vscode-theme)|[One Dark Pro](https://github.com/Binaryify/OneDark-Pro)|[Ayu Light](https://github.com/ayu-theme/vscode-ayu)|
|[![Night Owl](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_night_owl.png)](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_night_owl.png)|[![widget_gallery_one_dark_pro_theme](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_one_dark_pro.png)](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_one_dark_pro.png)|[![widget_gallery_ayu_light_them](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_ayu_light.png)](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_ayu_light.png)

etc...


## Requirements

- [Python 3.7+](https://www.python.org/downloads/)
- PySide6, PyQt6, PyQt5 or PySide2

Not tested on linux.

## Installation Method

- Last released version
   ```plaintext
   pip install qtvscodestyle
   ```
- Latest development version
   ```plaintext
   pip install git+https://github.com/5yutan5/QtVSCodeStyle
   ```

## Usage

### Use default theme

To apply VS Code's default theme, run:

```Python
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

import qtvscodestyle as qtvsc

app = QApplication(sys.argv)
main_win = QMainWindow()
push_button = QPushButton("QtVSCodeStyle!!")
main_win.setCentralWidget(push_button)

stylesheet = qtvsc.load_stylesheet(qtvsc.Theme.DARK_VS)
# stylesheet = load_stylesheet(qtvsc.Theme.LIGHT_VS)
app.setStyleSheet(stylesheet)

main_win.show()

app.exec()

```

> ⚠ The image quality may be lower on Qt5(PyQt5, PySide2) due to the use of svg. You can add the following [attribute](https://doc.qt.io/qt-5/qt.html#ApplicationAttribute-enum) to improve the quality of images.
> ```Python
> app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
> ```

#### Available Themes

To check available themes, run:

```Python
qtvsc.list_themes()
```

```plaintext
Theme name             Symbol
___________            ______

Light (Visual Studio): LIGHT_VS
Quiet Light          : QUIET_LIGHT
Solarized Light      : SOLARIZED_LIGHT
Abyss                : ABYSS
Dark (Visual Studio) : DARK_VS
Kimbie Dark          : KIMBIE_DARK
Monokai              : MONOKAI
Monokai Dimmed       : MONOKAI_DIMMED
Red                  : RED
Solarized Dark       : SOLARIZED_DARK
Tomorrow Night Blue  : TOMORROW_NIGHT_BLUE
Dark High Contrast   : DARK_HIGH_CONTRAST
```

### Use extension themes

If you want to use a third party theme, you will need to download the theme file from the repository and load theme by using `load_stylesheet()`.  

Simple example using [One Dark Pro](https://github.com/Binaryify/OneDark-Pro).  
One Dark Pro is one of the most used themes for VS Code.
1. First of all, download or copy and paste [the theme file from the repository](https://github.com/Binaryify/OneDark-Pro/blob/master/themes/OneDark-Pro.json).  
1. Then load the stylesheet using the saved file.
   ```Python
   theme_file = r"OneDark-Pro.json"
   stylesheet = qtvsc.load_stylesheet(theme_file)
   app.setStyleSheet(stylesheet)
   ```

### Color customization

The configuration method is the same as [workbench.colorCustomizations](https://code.visualstudio.com/api/extension-guides/color-theme#workbench-colors) of VSCode.  
About color code format, see [https://code.visualstudio.com/api/references/theme-color#color-formats](https://code.visualstudio.com/api/references/theme-color#color-formats).

```Python
# Set the button text color to red.
custom_colors = {"button.foreground": "#ff0000"}
stylesheet = qtvsc.load_stylesheet(qtvsc.Theme.DARK_VS, custom_colors)
```

To check available color id, run:

```Python
qtvsc.list_color_id()
```

Color ids is almost the same as [VS Code's theme color document](https://code.visualstudio.com/api/references/theme-color). Some own color ids like disabled attribute are available.

### SVG and Font QIcon for VS Code style

You can also use various icon fonts and svg as QIcon.

[![VS Code style icon](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/qicon_for_vscode_style.gif)](https://github.com/5yutan5/QtVSCodeStyle/blob/main/images/qicon_for_vscode_style.gif)

QtVSCodeStyle identifies icons by symbolic and  icon name.  
The following symbolic are currently available to use:

- [Font Awesome Free(5.15.4)](https://fontawesome.com/) - Font Icon
   - `FaRegular`: Regular style
   - `FaSolid` : Solid style
   - `FaBrands`: Brands style
- [vscode-codicons](https://github.com/microsoft/vscode-codicons)
   - `Vsc`: VS Code style - SVG Icon

You can use icon browser that displays all the available icons.

```Plaintext
python -m qtvscodestyle.examples.icon_browser
```

Two functions, `theme_icon()` and `icon()` are available.  
`theme_icon()` create QIcon will automatically switch the color based on the set color-id when you call `load_stylesheet(Another Theme)`.

```Python
star_icon = qtvsc.theme_icon(qtvsc.Vsc.STAR_FULL, "icon.foreground")
button = QToolButton()
button.setIcon(star_icon)

# star_icon switch to the MONOKAI's "icon.foreground" color.
qtvsc.load_stylesheet(qtvsc.Theme.MONOKAI)
```


`icon()` create QIcon with static color.
```Python
# Set red
star_icon = qtvsc.icon(qtvsc.Vsc.STAR_FULL, "#FF0000")
button = QToolButton()
button.setIcon(star_icon)

# Keep red.
qtvsc.load_stylesheet(qtvsc.Theme.MONOKAI)
```


### Create new theme

You can create your own theme. The configuration method is the same as theme extension of VS Code.
The only properties to set are the theme type and colors.

Dictionary, json file(json with comment), and string formats are supported.

- Dictionary
   ```Python
   custom_theme = {
       "type": "dark",  # dark or light or hc(high contrast)
       "colors": {
           "button.background": "#1e1e1e",
           "foreground": "#d4d4d4",
           "selection.background": "#404040",
       },
   }
   stylesheet = qtvsc.load_stylesheet(custom_theme)
   ```
- String(Json with comment text)
   ```Python
   custom_theme = """
   {
      "type": "dark",
      "colors": {
         "button.background": "#1e1e1e",
         "foreground": "#d4d4d4",
         "selection.background": "#404040"
      }
   }
   """
   # You need to use loads_stylesheet
   stylesheet = qtvsc.loads_stylesheet(custom_theme)
   ```
- Json with comment
   ```Python
   custom_theme_path = r"custom_theme.json"
   # or you can use pathlib.Path object
   # custom_theme_path = pathlib.Path("custom_theme.json")
   stylesheet = qtvsc.load_stylesheet(custom_theme_path)
   ```

If you customize using json files, you can use json schema.
Copy json schema from `qvscodestyle/validate_colors.json`
Using schema example for VS Code: https://code.visualstudio.com/docs/languages/json#_json-schemas-and-settings

## Check common widgets

To check common widgets, run:

```plaintext
python -m qtvscodestyle.examples.widget_gallery
```

## Custom properties

This module provides several custom properties for applying VS Code's style.  

For example, if you set the `activitybar` to `type` custom property of QToolbar, the style of the activitybar will be applied.

```Python
activitybar = QToolBar()
activitybar.setProperty("type", "activitybar")
```

| Widget      | Property | Property value | Command for demo                              |
|-------------|----------|----------------|-----------------------------------------------|
| QToolBar    | type     | activitybar    | `python -m qtvscodestyle.examples.activitybar` |
| QPushButton | type     | secondary      | `python -m qtvscodestyle.examples.pushbutton`  |
| QLineEdit   | state    | warning, error | `python -m qtvscodestyle.examples.lineedit`    |
| QFrame      | type     | h_line, v_line | `python -m qtvscodestyle.examples.line`        |

## Build resources

QtVSCodeStyle creates and deletes icon files dynamically using temporary folder.  
The style sheet you created will no longer be available after you exit the program.  
Therefore, QtVSCodeStyle provides the tool to build style sheets with resources that can be used after you exit the program.  

In order to build style sheets, run:
```plaintext
python -m qtvscodestyle.resource_builder --theme dark_vs
```

It is also possible to apply custom colors.

```plaintext
python -m qtvscodestyle.resource_builder -t dark_vs --custom-colors-path custom.json
```

```json
// custom.json
{
   "focusBorder": "#ff0000",
   "foreground": "#ff00ff"
}
```

In order check details of the command, run:

```plaintext
python -m qtvscodestyle.resource_builder --help
```
> ⚠ Resource files and svg folders should always be in the same directory.

> ⚠ Not support on PyQt6. PyQt6 removed Qt’s resource system.

## How to use in Qt Designer

1. Run the `qtvscodestyle.resource_builder` command and generate resources.
1. Copy the stylesheet text from `stylesheet.qss`.
1. Paste the copied stylesheet into stylesheet property of the top-level widget.
1. Register the `resource.qrc` in generated folder to the resource browser. If you use Qt Creator, add `resource.qrc` and svg folder to your project.


## License

MIT, see [LICENSE.txt](https://github.com/5yutan5/QtVSCodeStyle/blob/main/LICENSE.txt).  
QtVSCodeStyle incorporates image assets from external sources.
The icons for the QtVSCodeStyle are derived from:

- Font Awesome Free 5.15.4 (Font Awesome; SIL OFL 1.1)
- Material design icons (Google; Apache License Version 2.0)
- vscode-codicons (Microsoft Corporation; CC-BY-SA-4.0 License)

See [NOTICE.md](https://github.com/5yutan5/QtVSCodeStyle/blob/main/NOTICE.md) for full license information.

## Acknowledgements

This package has been created with reference to the following repositories.

- [QDarkStyleSheet](https://github.com/ColinDuquesnoy/QDarkStyleSheet)
- [BreezeStyleSheets](https://github.com/Alexhuszagh/BreezeStyleSheets)
- [qt-material](https://github.com/UN-GCPDS/qt-material)
- [vscode](https://github.com/microsoft/vscode)
- [QtAwesome](https://github.com/spyder-ide/qtawesome)
- [Napari](https://github.com/napari/napari)
