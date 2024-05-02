from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QCoreApplication

import os
import sys
import multiprocessing

import Macro


class MacroGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.record_button = QPushButton('Start/Stop Recording', self)
        self.record_button.setObjectName('RecordButton')
        self.record_button.move(50, 50)
        self.record_button.clicked.connect(self.record_macro)

        self.play_button = QPushButton('Start/Stop Playing', self)
        self.play_button.setObjectName('PlayButton')
        self.play_button.move(200, 50)  # Adjust the x-coordinate here
        self.play_button.clicked.connect(self.play_macro)

        self.setFixedSize(350, 150)  # Set fixed window size

    def record_macro(self):
        self.record_process = multiprocessing.Process(target=Macro.start_recording)
        self.record_process.start()

    def play_macro(self):
        self.play_process = multiprocessing.Process(target=Macro.start_playback)
        self.play_process.start()


def main():
    app = QApplication(sys.argv)
    gui = MacroGUI()
    gui.show()

    # Get the directory of the script
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Read and apply CSS file
    with open(os.path.join(dir_path, 'style.css'), 'r') as f:
        app.setStyleSheet(f.read())

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()