from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QLabel, QCheckBox, QComboBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import os
import sys
import json
import multiprocessing
import Macro

app = QApplication(sys.argv)

class MacroGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app = QApplication.instance()  # Get the QApplication instance
        self.stylesheets = ['StyleDefaultDark.qss', 'StyleDefaultLight.qss', 'StyleDarkColored.qss']  # List of .qss files
        self.current_stylesheet = 0  # Counter for the current .qss file

        self.load_settings()

        self.setWindowTitle("Macro")
        font = QFont()
        font.setPointSize(18)  # Set font size

        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.record_button = QPushButton('Start/Stop Recording', self)
        self.record_button.setObjectName('RecordButton')
        self.record_button.setFont(font)  # Set font
        self.record_button.setFixedSize(175, 50)  # Adjust button size
        self.record_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Set size policy to Fixed
        self.record_button.clicked.connect(self.record_macro)  # Connect clicked signal

        self.play_button = QPushButton('Start/Stop Playing', self)
        self.play_button.setObjectName('PlayButton')
        self.play_button.setFont(font)  # Set font
        self.play_button.setFixedSize(175, 50)  # Adjust button size
        self.play_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Set size policy to Fixed
        self.play_button.clicked.connect(self.play_macro)  # Connect clicked signal

        self.button_layout = QHBoxLayout()  # Use QHBoxLayout for buttons
        self.button_layout.setSpacing(0)  # Set spacing to 0
        self.button_layout.addWidget(self.record_button)
        self.button_layout.addWidget(self.play_button)


        self.layout = QVBoxLayout()  # Use QVBoxLayout for overall layout
        self.layout.setSpacing(0)  # Set spacing to 0


        self.layout.addItem(spacer_top)  # Add spacer at the top
        self.layout.addLayout(self.button_layout)
        self.layout.addItem(spacer)  # Add spacer at the bottom

        # Create a QCheckBox
        self.advanced_settings_check = QCheckBox(self)
        self.advanced_settings_check.stateChanged.connect(self.toggle_advanced_settings)

        # Create a QLabel
        self.advanced_settings_label = QLabel("Advanced Settings", self)
        self.advanced_settings_label.setEnabled(False)  # Initially disabled

        # Create a QComboBox for switching stylesheets
        self.style_combobox = QComboBox(self)
        self.style_combobox.addItems(['Default Dark', 'Default Light', 'Dark Colored'])
        self.style_combobox.currentIndexChanged.connect(self.switch_stylesheet)

        # Add the QCheckBox, QLabel, and QComboBox to the layout
        self.layout.addWidget(self.advanced_settings_check)
        self.layout.addWidget(self.advanced_settings_label)
        self.layout.addWidget(self.style_combobox)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.setFixedSize(500, 500)

        self.load_settings()
        self.switch_stylesheet(self.current_stylesheet)  # Apply the loaded stylesheet

    def switch_stylesheet(self, index):
        # Update the current_stylesheet counter based on the selected index
        self.current_stylesheet = index

        # Get the directory of the script
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Read and apply the new .qss file
        self.styles_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'styles')
        stylesheet_path = os.path.join(self.styles_dir, self.stylesheets[index])
        with open(stylesheet_path, 'r') as f:
            self.app.setStyleSheet(f.read())

        self.save_settings()

    def toggle_advanced_settings(self, state):
        if state == Qt.Checked:
            self.advanced_settings_label.setEnabled(True)
        else:
            self.advanced_settings_label.setEnabled(False)

        self.save_settings()

    def record_macro(self):
        # Implement recording functionality here
        print("Recording...")

    def play_macro(self):
        # Implement playing functionality here
        print("Playing...")

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.current_stylesheet = settings.get('stylesheet', 0)
                self.advanced_settings_check.setChecked(settings.get('advanced_settings', False))
        except FileNotFoundError:
            pass  # It's okay if the file doesn't exist

    def save_settings(self):
        settings = {
            'stylesheet': self.current_stylesheet,
            'advanced_settings': self.advanced_settings_check.isChecked()
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

def main():
    app = QApplication(sys.argv)

    # Get the directory of the script
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Set the application icon
    app.setWindowIcon(QIcon(os.path.join(dir_path, 'Icon.ico')))

    gui = MacroGUI()
    gui.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    
