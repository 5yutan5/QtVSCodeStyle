QtVSCodeStyle
=============
[![Qt Versions](https://img.shields.io/badge/Qt-5%20|%206-blue.svg?&logo=Qt&logoWidth=18&logoColor=white)](https://www.qt.io/qt-for-python)
[![License](https://img.shields.io/github/license/5yutan5/QtVSCodeStyle.svg?color=green)](https://github.com/5yutan5/QtVSCodeStyle/blob/main/LICENSE.txt/)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/5yutan5/QtVSCodeStyle.svg?logo=lgtm&logoWidth=18&color=success)](https://lgtm.com/projects/g/5yutan5/QtVSCodeStyle/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/5yutan5/QtVSCodeStyle.svg?logo=lgtm&logoWidth=18&color=success)](https://lgtm.com/projects/g/5yutan5/QtVSCodeStyle/context:python)
[![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/python/black)

VS Code Style for PySide and PyQt.

QtVSCodeStyle enables to use vscode themes in pyqt and pyside.
The default and third-party themes of VS Code can be used.


## SCREENSHOT
|[Dark (Visual Studio)](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_dark.png)|[Light (Visual Studio)](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_light.png)|[Dark High Contrast](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_hc.png)|
| :--: | :--: | :--: |
|[![widget_gallery_dark_theme](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_dark.png)](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_dark.png)|[![widget_gallery_light_them](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_light.png)](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_light.png)|[![widget_gallery_light_them](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_hc.png)](https://raw.githubusercontent.com/5yutan5/QtVSCodeStyle/main/images/widget_gallery_hc.png)|

etc...


## Requirements

- [Python 3.7+](https://www.python.org/downloads/)
- PySide6, PyQt6, PyQt5 or PySide2

Not tested on linux.

## Installation Method

PyPi is not yet. Please wait publish.

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

You can use VSCode's default theme by using `Theme` enum.

```Python
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

from qtvscodestyle import Theme, load_stylesheet

app = QApplication(sys.argv)
main_win = QMainWindow()
push_button = QPushButton("QtVSCodeStyle!!")
main_win.setCentralWidget(push_button)

stylesheet = load_stylesheet(Theme.DARK_VS)
# stylesheet = load_stylesheet(Theme.LIGHT_VS)
app.setStyleSheet(stylesheet)

main_win.show()

app.exec()

```

> ⚠ The quality of image may be low on Qt5(PyQt5, PySide2) when using svg. You can add the following [attribute](https://doc.qt.io/qt-5/qt.html#ApplicationAttribute-enum) to improve the quality of images.
> ```Python
> app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
> ```

#### Available Themes

To check available themes, run:

```Python
from qtvscodestyle import list_themes

# list theme name and symbol
list_themes()
```

```plaintext
Theme name:          : Symbol
_____________________________

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

### Use third party themes

If you want to use a third party theme, you will need to download the theme file from the repository and load theme by using `load_stylesheet()`.  

Simple example of using One Dark Pro.  
One Dark Pro is one of the most used themes for VS Code.
1. First of all, download or copy and paste [the theme file from the repository](https://github.com/Binaryify/OneDark-Pro/blob/master/themes/OneDark-Pro.json).  
1. Then load the stylesheet using the saved file.
   ```Python
   theme_file = r"OneDark-Pro.json"
   stylesheet = load_stylesheet(theme_file)
   app.setStyleSheet(stylesheet)
   ```

### Customize colors

You can customize color. The configuration method is the same as vscode's [workbench.colorCustomizations](https://code.visualstudio.com/api/extension-guides/color-theme#workbench-colors).  
About color code format, see [https://code.visualstudio.com/api/references/theme-color#color-formats](https://code.visualstudio.com/api/references/theme-color#color-formats).

```Python
# Set the button text color to red.
custom_colors = {"button.foreground": "#ff0000"}
stylesheet = load_stylesheet(Theme.DARK_VS, custom_colors)
```

The color id of VS Code can be used as it is.
Which id corresponds to which widget style has not been documented yet.
Please wait.

### Create theme

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
   stylesheet = load_stylesheet(custom_theme)
   ```
- String(Json with comment text)
   ```Python
   # You neet to use loads_stylesheet
   from qtvscodestyle import loads_stylesheet
   ...
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
   stylesheet = loads_stylesheet(custom_theme)
   ```
- Json with comment
   ```Python
   custom_theme_path = r"custom_theme.json"
   # or you can use pathlib.Path object
   # custom_theme_path = pathlib.Path("custom_theme.json")
   stylesheet = load_stylesheet(custom_theme_path)
   ```

## Check common widgets

To check common widgets, run:

```plaintext
python -m qtvscodestyle.examples.widget_gallery
```

## Custom Properties

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

## How to Use in Qt Designer

1. Run the `qtvscodestyle.resource_builder` command and generate resources.
1. Copy the stylesheet text from stylesheet.qss  in the generated folder.
1. Paste the copied stylesheet into stylesheet property of the top-level widget.
1. Register the resource.qrc in generated folder to the resource browser.

> ⚠ In PyQt6, support for Qt’s resource system has been removed. Therefore, if you want to use Qt Designer in PyQt6, you need to delete the stylesheet in the ui file and load the stylesheet using `load_stylesheet()`.

## License

All icons under `qtvscodestyle/google_fonts` are modified from [Material design icons](https://github.com/google/material-design-icons) (which uses an Apache 2.0 license), and are redistributed under the MIT license.  
See [NOTICE.md](https://github.com/5yutan5/QtVSCodeStyle/blob/main/NOTICE.md).

## Acknowledgements

This package has been created with reference to the following repositories.

- [QDarkStyleSheet](https://github.com/ColinDuquesnoy/QDarkStyleSheet)
- [BreezeStyleSheets](https://github.com/Alexhuszagh/BreezeStyleSheets)
- [qt-material](https://github.com/UN-GCPDS/qt-material)
- [vscode](https://github.com/microsoft/vscode)
