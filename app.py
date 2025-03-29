import sys

from PyQt6.QtGui import QIcon, QFontMetrics
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QLabel, QFrame

from config import Config
from keybind import BlitzBinds, Keybind as KB
from blitz_log import BlitzLog
from screenshotter import Screenshotter

config = Config.ensureGet()
screenshotter = Screenshotter(config)
binds = BlitzBinds(
    "f12", # Complete Mission 
    "f9" # Fail Mission
)
blitzLog = BlitzLog()

class KeybindEmitter(QObject):
    screenshot_taken = pyqtSignal()
keybind_emitter = KeybindEmitter()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BlitzLog")

        top_layout = QHBoxLayout()
        self.startButton = QPushButton("START")
        self.startButton.clicked.connect(self.startClick)
        top_layout.addWidget(self.startButton)
        self.viewSourceScreenshotFolderButton = QPushButton("Settings")
        self.viewSourceScreenshotFolderButton.clicked.connect(self.settingsClick)
        top_layout.addWidget(self.viewSourceScreenshotFolderButton)
        self.viewSourceScreenshotFolderButton = QPushButton()
        self.viewSourceScreenshotFolderButton.setIcon(QIcon('icons/steam.png'))
        self.viewSourceScreenshotFolderButton.clicked.connect(screenshotter.viewSourceFolder)
        top_layout.addWidget(self.viewSourceScreenshotFolderButton)
        self.viewDestScreenshotFolderButton = QPushButton()
        self.viewDestScreenshotFolderButton.setIcon(QIcon('icons/op.svg'))
        self.viewDestScreenshotFolderButton.clicked.connect(screenshotter.viewDestFolder)
        top_layout.addWidget(self.viewDestScreenshotFolderButton)

        mission_layout = QHBoxLayout()
        self.completeMissionLabel = QLabel(f"Complete Mission [{binds.completeMission}]")
        mission_layout.addWidget(self.completeMissionLabel)
        self.failMissionButton = QPushButton(f"Fail Last Mission [{binds.failMission}]")
        self.failMissionButton.clicked.connect(self.failClick)
        mission_layout.addWidget(self.failMissionButton)
        self.pointsLabel = QLabel()
        mission_layout.addWidget(self.pointsLabel)

        log_Layout = QVBoxLayout()
        log_controls_layout = QHBoxLayout()
        self.saveButton = QPushButton("Reload")
        log_controls_layout.addWidget(self.saveButton)
        self.saveButton.clicked.connect(self.reload)
        self.loadButton = QPushButton("Overwrite")
        log_controls_layout.addWidget(self.loadButton)
        self.loadButton.clicked.connect(self.overwrite)
        log_Layout.addLayout(log_controls_layout)
        self.logEdit = QTextEdit()
        self.logEdit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        # self.logEdit.setReadOnly(True)
        log_Layout.addWidget(self.logEdit)

        outer_layout = QVBoxLayout()
        outer_layout.addLayout(top_layout)
        self.mission_controls = QFrame()
        self.mission_controls.setLayout(mission_layout)
        outer_layout.addWidget(self.mission_controls)
        outer_layout.addLayout(log_Layout)
        window = QWidget()
        window.setLayout(outer_layout)
        self.setCentralWidget(window)

        self.mission_controls.setEnabled(False)
        keybind_emitter.screenshot_taken.connect(self.completeMission)

    def startClick(self):
        blitzLog.start()
        self.mission_controls.setEnabled(True)
        self.refresh()
        self.resizeLogWidth()

    def settingsClick(self):
        Config.viewInDefaultProgram()

    def completeMission(self):
        blitzLog.completeMission()
        self.refresh()

    def failClick(self):
        blitzLog.failLastMission()
        self.refresh()

    def refresh(self):
        self.pointsLabel.setText(f'Points: {blitzLog.calcPoints()}')
        self.logEdit.setPlainText(f'{blitzLog.toLog()}')

    def reload(self):
        config.reload()
        self.refresh()

    def overwrite(self):
        self.logEdit.repaint() # update text
        logText = self.logEdit.toPlainText()
        log = BlitzLog.fromLog(logText)
        blitzLog.overwriteFrom(log)
        self.refresh()

    def resizeLogWidth(self):
        font = self.logEdit.font()
        metrics = QFontMetrics(font)
        lines = self.logEdit.toPlainText().splitlines()
        firstLongLine = '' if len(lines) < 2 else lines[1]
        width = metrics.horizontalAdvance(firstLongLine + '                                        ')
        self.logEdit.setMinimumWidth(width)
    
app = QApplication(sys.argv)
app.setWindowIcon(QIcon('icons/blitz.png'))
window = MainWindow()
window.refresh()
window.show()

def handleScreenshot():
    screenshotter.transfer(blitzLog.nameScreenshot())
    keybind_emitter.screenshot_taken.emit()
KB.SetupKeybinds(window, [
    KB(binds.completeMission, handleScreenshot)
])

app.exec()