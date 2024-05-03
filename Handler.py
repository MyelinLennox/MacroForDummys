from fileinput import filename
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QLabel, QCheckBox, QComboBox, QGroupBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

import os
import re
import sys
import json
import multiprocessing
import Macro

app = QApplication(sys.argv)

class MacroGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app = QApplication.instance()  # Get the QApplication instance
        self.stylesheets = [file for file in os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "styles")) if file.endswith('.qss')]
        self.current_stylesheet = 0  # Counter for the current .qss file
        self.setWindowTitle("Macro")
        font = QFont()
        font.setPointSize(18)  # Set font size
        
        # Def Style Dropdown Menu
        self.style_combobox = QComboBox(self)
        for file in self.stylesheets:
            filename = os.path.splitext(file)[0]
            self.style_combobox.addItem(filename)
        self.style_combobox.currentIndexChanged.connect(self.switch_stylesheet)


        # Def Advanced Settings GroupBox
        self.advanced_settings_groupbox = QGroupBox("Advanced Settings", self)
        self.advanced_settings_groupbox.setCheckable(True)  # Add a checkbox next to the title
        self.advanced_settings_groupbox.setChecked(False)  # Initially unchecked
        self.advanced_settings_groupbox.toggled.connect(self.toggle_advanced_settings)  # Connect toggled signal
        
        self.advanced_settings_groupbox_layout = QVBoxLayout()  # Use QVBoxLayout for the groupbox layout
        self.advanced_settings_groupbox_layout.addWidget(self.style_combobox)  # Add the combobox to the groupbox layout
        self.advanced_settings_groupbox.setLayout(self.advanced_settings_groupbox_layout)  # Set the layout to the groupbox
        
        # Def Spacer
        vertical_spacer = QSpacerItem(0, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)
        horizontal_spacer = QSpacerItem(40, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Def Record Button
        self.record_button = QPushButton('Start/Stop Recording', self)
        self.record_button.setObjectName('RecordButton')
        self.record_button.setFont(font)  # Set font
        self.record_button.setFixedSize(175, 50)  # Adjust button size
        self.record_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Set size policy to Fixed
        self.record_button.clicked.connect(self.record_macro)  # Connect clicked signal

        # Def Play Button
        self.play_button = QPushButton('Start/Stop Playing', self)
        self.play_button.setObjectName('PlayButton')
        self.play_button.setFont(font)  # Set font
        self.play_button.setFixedSize(175, 50)  # Adjust button size
        self.play_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Set size policy to Fixed
        self.play_button.clicked.connect(self.play_macro)  # Connect clicked signal

        # Def Button Layout
        self.button_layout = QHBoxLayout()  # Use QHBoxLayout for buttons
        self.button_layout.setSpacing(50)  # Set spacing to 0
        self.button_layout.addWidget(self.record_button)
        self.button_layout.addWidget(self.play_button)
        self.button_layout.setAlignment(Qt.AlignCenter)  # Center the buttons horizontally
        
        # Layout Order
        self.layout = QVBoxLayout()  # Use QVBoxLayout for overall layout
        self.layout.setContentsMargins(50, 50, 50, 50)  # Set margins around the border of the window
        self.layout.addLayout(self.button_layout)
        self.layout.addItem(vertical_spacer)
        self.layout.addWidget(self.advanced_settings_groupbox)  # Add the groupbox to the layout
        self.layout.setAlignment(Qt.AlignTop)  # Align the layout to the top
        
        # Layout settings
        self.layout.setSpacing(20)  # Set spacing to 0
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
            self.style_combobox.setEnabled(True)  # Enable the combobox
        else:
            self.style_combobox.setEnabled(False)  # Disable the combobox
        self.style_combobox.setEnabled(state)  # Enable or disable the combobox based on the state of the checkbox
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
                self.style_combobox.setCurrentIndex(self.current_stylesheet)  # Set the current index
                advanced_settings = settings.get('advanced_settings', False)
                self.advanced_settings_groupbox.setChecked(advanced_settings)
                self.style_combobox.setEnabled(advanced_settings)  # Enable or disable the combobox based on the advanced_settings
        except FileNotFoundError:
            pass  # It's okay if the file doesn't exist

    def save_settings(self):
        settings = {
            'stylesheet': self.current_stylesheet,
            'advanced_settings': self.advanced_settings_groupbox.isChecked()
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
    
