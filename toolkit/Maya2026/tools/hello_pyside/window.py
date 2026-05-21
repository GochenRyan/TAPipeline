from __future__ import annotations

from PySide6 import QtWidgets
from shiboken6 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds

__version__ = "0.1.0"

WINDOW_OBJECT_NAME = "TAPipelineHelloPySideWindow"

def _maya_main_window() -> QtWidgets.QWidget:
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class HelloDialog(QtWidgets.QDialog):
    def __init__(self, parent : QtWidgets.QWidget | None = None) -> None:
        super(HelloDialog, self).__init__(parent or _maya_main_window())
        self.setObjectName(WINDOW_OBJECT_NAME)
        self.setWindowTitle(f"Hello PySide6 v{__version__}")
        self.setMinimumSize(320, 140)
        self._counter = 0
        self._build_ui()
    
    def _build_ui(self) -> None:
        layout = QtWidgets.QVBoxLayout(self)
        self._prefix = QtWidgets.QLineEdit(self)
        self._prefix.setPlaceholderText("Naming prefix, for example, myCube")
        layout.addWidget(self._prefix)

        row = QtWidgets.QHBoxLayout()
        for label, factory in (
            ("Cube", cmds.polyCube),
            ("Sphere", cmds.polySphere),
            ("Cylinder", cmds.polyCylinder),
        ):
            btn = QtWidgets.QPushButton(label, self)
            btn.clicked.connect(lambda _=False, f=factory: self._create(f))
            row.addWidget(btn)
        layout.addLayout(row)

    def _create(self, factory) -> None:
        self._counter += 1
        prefix = self._prefix.text() or "obj"
        name = f"{prefix}_{self._counter:03d}"
        factory(name=name)

_window : HelloDialog | None = None

def show() -> HelloDialog:
    global _window
    if _window is None:
        _window = HelloDialog()
    _window.show()
    _window.raise_()
    _window.activateWindow()
    return _window