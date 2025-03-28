from __future__ import annotations
import keyboard
from PyQt6.QtWidgets import QDialog, QMainWindow
import inspect
from typing import Iterable

class Keybind:
    def __init__(self, key: str, bind):
        self.key = key
        self.bind = lambda _: bind()
        # Metaprogramming silliness to determine a nice display string for 'bind'
        # info = inspect.getframeinfo(inspect.getouterframes(inspect.currentframe())[1][0]).code_context[0].strip()
        # arg = info[info.find('(') + 1:-1].split(',')[1]
        # self.displayBind = arg

    @staticmethod
    def SetupKeybinds(window: QMainWindow, keybinds: Iterable[Keybind], helpKey: str = None):
        def ShowKeybinds():
            # dlg = QDialog(window)
            # dlg.setWindowTitle("\n".join(map(lambda x: f'Key: {x.key}, Bind: {x.displayBind}', keybinds)))
            # dlg.exec()
            pass
        if (helpKey != None):
            keybinds.append(Keybind(helpKey, ShowKeybinds))
        for keybind in keybinds:
            keyboard.on_press_key(keybind.key, keybind.bind)

class BlitzBinds:
    def __init__(self, completeMission: str = None, failMission: str = None):
        self.completeMission = completeMission
        self.failMission = failMission