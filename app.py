import sys

from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QLabel

from keybind import Keybind as KB
from blitz_log import BlitzLog
from screenshotter import Screenshotter

class MyEmitter(QObject):
    screenshot_taken = pyqtSignal()

keybind_emitter = MyEmitter()

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.blitzLog = BlitzLog()

        self.setWindowTitle("BlitzLog")

        self.startButton = QPushButton("START")
        self.startButton.clicked.connect(self.startClick)

        self.completeMissionButton = QPushButton("Complete Mission")
        self.completeMissionButton.clicked.connect(self.completeClick)

        self.failMissionButton = QPushButton("Fail Mission")
        self.failMissionButton.clicked.connect(self.failClick)

        self.pointsLabel = QLabel()
        self.logEdit = QTextEdit()
        self.logEdit.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.startButton)
        layout.addWidget(self.completeMissionButton)
        layout.addWidget(self.failMissionButton)
        layout.addWidget(self.pointsLabel)
        layout.addWidget(self.logEdit)

        window = QWidget()
        window.setLayout(layout)
        self.setCentralWidget(window)

        keybind_emitter.screenshot_taken.connect(self.completeClick)

    def startClick(self):
        self.blitzLog.start()
        self.refresh()

    def completeClick(self):
        self.blitzLog.completeMission(0)
        self.refresh()

    def failClick(self):
        self.blitzLog.failMission(0)
        self.refresh()

    def refresh(self):
        self.pointsLabel.setText(f'Points: {self.blitzLog.calcPoints()}')
        self.logEdit.setPlainText(f'{self.blitzLog.toLog()}')
    
app = QApplication(sys.argv)

window = MainWindow()
window.show()

screenshotter = Screenshotter()
screenshotter.setup()
def handleScreenshot():
    screenshotter.transfer(window.blitzLog.currentOp, window.blitzLog.currentMission)
    keybind_emitter.screenshot_taken.emit()

KB.SetupKeybinds(window, [
    KB("f12", handleScreenshot)
], "h")

app.exec()