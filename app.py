import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.count = 0

        self.setWindowTitle("BlitzLog")

        self.label = QLabel(f'<h1>Count: {self.count}</h1>')

        self.button = QPushButton("Press Me!")
        self.button.clicked.connect(self.onClick)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        window = QWidget()
        window.setLayout(layout)

        self.setCentralWidget(window)

    def onClick(self):
        self.count += 1
        self.label.setText(f'<h1>Count: {self.count}</h1>')

    
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()