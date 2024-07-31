import tkinter as tk
from tkinter import ttk
import os
import sys

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.Style = ttk.Style(self)
        self.ReloadPending = False

        # Theme establishment
        ThemeFolder = os.path.join(os.path.dirname(__file__), "Themes")
        self.ComboBoxList = []
        if os.path.exists(ThemeFolder):
            for folder_name in os.listdir(ThemeFolder):
                if os.path.isdir(os.path.join(ThemeFolder, folder_name)):
                    self.ComboBoxList.append(folder_name)

        self.DarkLightModeBool = tk.BooleanVar(value=self.InterpratSettings(2))
        self.DarkLightModeBool.trace_add("write", self.DarkLightModeShitFix)

        self.UseMouseBool = tk.BooleanVar(value=self.InterpratSettings(3))
        self.UseMouseBool.trace_add("write", lambda *args: self.SaveSettings(3, self.UseMouseBool.get()))

        self.UseKeyboardBool = tk.BooleanVar(value=self.InterpratSettings(4))
        self.UseKeyboardBool.trace_add("write", lambda *args: self.SaveSettings(4, self.UseKeyboardBool.get()))

        # STYLE FIX ---------------------------------------------------------------------------------------------------------------------------------
        self.Style.configure("Bigger.TButton", font=("-size", 20))

        # OUTLINE FRAME -----------------------------------------------------------------------------------------------------------------------------
        # Frame
        self.MainFrame = ttk.Frame(self, padding=10, relief="ridge")
        self.MainFrame.grid(sticky="nsew", padx=10, pady=10)

        # Header
        self.Header = ttk.Label(self.MainFrame, text="Macro For Dummys", justify="center", font=("-size", 25, "-weight", "bold"))
        self.Header.grid(row=0, column=0, pady=(15, 25), columnspan=2, sticky="nsew", padx=50)

        # Record button
        self.RecordButton = ttk.Button(self.MainFrame, text="Start/Stop Recording", style="Bigger.TButton", width=20)
        self.RecordButton.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(20, 35), ipady=(10))

        # Playback button
        self.PlaybackButton = ttk.Button(self.MainFrame, text="Start/Stop Playback", style="Bigger.TButton", width=20)
        self.PlaybackButton.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=(20, 35), ipady=(10))

        # Advanced settings frame
        self.AdvancedSettingsFrame = ttk.LabelFrame(self.MainFrame, text="Advanced Settings", padding=(20, 10))
        self.AdvancedSettingsFrame.grid(row=3, column=0, pady=(30, 0), columnspan=2, sticky="nsew")

        # ADVANCED SETTINGS -------------------------------------------------------------------------------------------------------------------------
        self.ComboBoxLabel = ttk.Label(self.AdvancedSettingsFrame, text="Theme:", font=("-size", 11))
        self.ComboBoxLabel.grid(row=0, column=0, sticky="w")

        self.ComboBox = ttk.Combobox(self.AdvancedSettingsFrame, state="readonly", values=self.ComboBoxList)
        self.ComboBox.grid(row=0, column=1, padx=5, ipady=5, sticky="ew")

        saved_theme = self.InterpratSettings(1)
        if saved_theme in self.ComboBoxList:
            self.ComboBox.current(self.ComboBoxList.index(saved_theme))
        else:
            self.ComboBox.current(0)

        #self.ComboBox.bind("<<ComboboxSelected>>", self.ComboboxShitFix)
        self.ComboBox.bind("<<ComboboxSelected>>", self.ChangeTheme)

        # FRAMES ------------------------------------------------------------------------------------------------------------------------------------
        self.DarkModeToggleFrame = ttk.Frame(self.AdvancedSettingsFrame)
        self.DarkModeToggleFrame.grid(row=1, column=0, columnspan=3, pady=(10, 0), sticky="ew")

        self.ThemesSeperator = ttk.Separator(self.AdvancedSettingsFrame, orient="horizontal")
        self.ThemesSeperator.grid(row=2, column=0, columnspan=4, pady=(25, 25), sticky="ew")

        self.KeyboardMouseFrame = ttk.Frame(self.AdvancedSettingsFrame)
        self.KeyboardMouseFrame.grid(row=3, column=0, columnspan=3, pady=(10, 0), sticky="ew")

        # CONTENT -----------------------------------------------------------------------------------------------------------------------------------
        self.DarkModeToggleLabel = ttk.Label(self.DarkModeToggleFrame, text="Dark Mode:", font=("-size", 11))
        self.DarkModeToggleLabel.grid(row=0, column=0, sticky="w", pady=(0, 15))

        self.DarkModeToggle = ttk.Checkbutton(self.DarkModeToggleFrame, style='Switch.TCheckbutton', variable=self.DarkLightModeBool)
        self.DarkModeToggle.grid(row=0, column=1, padx=5, sticky="ew", pady=(0, 15))

        self.ToggleMouseLabel = ttk.Label(self.KeyboardMouseFrame, text="Use Mouse:", font=("-size", 11))
        self.ToggleMouseLabel.grid(row=2, column=0, sticky="w", pady=5)

        self.ToggleMouse = ttk.Checkbutton(self.KeyboardMouseFrame, style='Switch.TCheckbutton', variable=self.UseMouseBool)
        self.ToggleMouse.grid(row=2, column=1, padx=5, sticky="ew", pady=5)

        self.ToggleKeyboardLabel = ttk.Label(self.KeyboardMouseFrame, text="Use Keyboard:", font=("-size", 11))
        self.ToggleKeyboardLabel.grid(row=3, column=0, sticky="w", pady=5)

        self.ToggleKeyboard = ttk.Checkbutton(self.KeyboardMouseFrame, style='Switch.TCheckbutton', variable=self.UseKeyboardBool)
        self.ToggleKeyboard.grid(row=3, column=1, padx=5, sticky="ew", pady=5)

        # THEME LOAD --------------------------------------------------------------------------------------------------------------------------------
        self.ChangeTheme()  # Load theme on startup

# SETTINGS LOADER -----------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def InterpratSettings(LineNumber=None):
        with open(os.path.join(os.path.dirname(__file__), "Settings"), 'r') as file:
            Lines = file.readlines()

        InterpretedLines = []
        for line in Lines:
            StrippedLine = line.strip()
            if StrippedLine == "True":
                InterpretedLines.append(True)
            elif StrippedLine == "False":
                InterpretedLines.append(False)
            else:
                InterpretedLines.append(StrippedLine)

        if LineNumber is not None:
            if 1 <= LineNumber <= len(InterpretedLines):
                return InterpretedLines[LineNumber - 1]
            else:
                raise IndexError("Line number out of range")

        return InterpretedLines

    @staticmethod
    def SaveSettings(LineNumber, Value):
        settings_path = os.path.join(os.path.dirname(__file__), "Settings")
        with open(settings_path, 'r') as file:
            lines = file.readlines()

        if LineNumber is not None and 1 <= LineNumber <= len(lines):
            lines[LineNumber - 1] = f"{Value}\n"
        else:
            raise IndexError("Line number out of range")

        with open(settings_path, 'w') as file:
            file.writelines(lines)

# THEME CHANGE --------------------------------------------------------------------------------------------------------------------------------------
    def ChangeTheme(self, *args):
        self.Style = ttk.Style(self)
        SelectedTheme = self.ComboBox.get()
        ThemePath = os.path.join(os.path.dirname(__file__), "Themes", SelectedTheme, f"{SelectedTheme}.tcl")

        if self.DarkLightModeBool.get():
            ThemeMode = "dark"
        else:
            ThemeMode = "light"

        try:
            self.root.tk.call("source", ThemePath)
            self.root.tk.call("set_theme", ThemeMode)
        except:
            ttk.Style().theme_use(f"{SelectedTheme.lower()}-{ThemeMode}")

        self.configure_text_widget_styles()  # Configure text widget styles after setting the theme
        print(f"Updated Theme: {SelectedTheme}, Mode: {ThemeMode}")

    def configure_text_widget_styles(self):
        self.Style.configure("TLabel", background="#2e2e2e", foreground="white")
        self.Style.configure("TEntry", background="#2e2e2e", foreground="white")
        self.Style.configure("TText", background="#2e2e2e", foreground="white")

    def ComboboxShitFix(self, *args):
        self.SaveSettings(1, self.ComboBox.get())
        self.ReloadSchedule()

    def DarkLightModeShitFix(self, *args):
        self.SaveSettings(2, self.DarkLightModeBool.get())
        self.ReloadSchedule()

    def ReloadSchedule(self):
        if not self.ReloadPending:
            self.ReloadPending = True
            self.root.after(10, self.ReloadWindow)

    def ReloadWindow(self):
        self.ReloadPending = False
        self.root.quit()
        python = sys.executable
        os.execl(python, python, *sys.argv)


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
   
