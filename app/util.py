import os
import ctypes

def alert(message: str):
    ctypes.windll.user32.MessageBoxW(0, message, "BlitzLog App Alert", 1)

def startInDefaultProgram(path):
    if (os.path.exists(path)):
        os.startfile(path)
    else:
        alert(f"Failed to find path:\t{path}")

