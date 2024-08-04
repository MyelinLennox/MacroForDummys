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

        ThemeFolder = os.path.join(os.path.dirname(__file__), "Themes")
        self.ComboBoxList = []
        if os.path.exists(ThemeFolder):
            for folder_name in os.listdir(ThemeFolder):
                if os.path.isdir(os.path.join(ThemeFolder, folder_name)):
                    self.ComboBoxList.append(folder_name)

        self.DarkLightModeBool = tk.BooleanVar(value=self.InterpratSettings(2))
        self.DarkLightModeBool.trace_add("write", self.DarkLightModeScheduler)

        self.UseMouseBool = tk.BooleanVar(value=self.InterpratSettings(3))
        self.UseMouseBool.trace_add("write", lambda *args: self.SaveSettings(3, self.UseMouseBool.get()))

        self.UseKeyboardBool = tk.BooleanVar(value=self.InterpratSettings(4))
        self.UseKeyboardBool.trace_add("write", lambda *args: self.SaveSettings(4, self.UseKeyboardBool.get()))

        #self.UseConsoleBool = tk.BooleanVar(value=self.InterpratSettings(5))
        #self.UseConsoleBool.trace_add("write", self.ConsoleScheduler)

        self.root.bind("<Configure>", lambda *args: self.SaveSettings(6, self.root.geometry()))
        self.root.geometry(self.InterpratSettings(6))

        # OUTLINE FRAME -----------------------------------------------------------------------------------------------------------------------------

        self.MainFrame = ttk.Frame(self, padding=10, relief="ridge")
        self.MainFrame.grid(sticky="nsew", padx=10, pady=10)

        self.Header = ttk.Label(self.MainFrame, text="Macro For Dummys", justify="center", font=("-size", 25, "-weight", "bold"))
        self.Header.grid(row=0, column=0, pady=(15, 25), columnspan=2, sticky="nsew", padx=50)

        self.RecordButton = ttk.Button(self.MainFrame, text="Start/Stop Recording", style="Bigger.TButton", width=20)
        self.RecordButton.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(20, 35), ipady=(10))

        self.PlaybackButton = ttk.Button(self.MainFrame, text="Start/Stop Playback", style="Bigger.TButton", width=20)
        self.PlaybackButton.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=(20, 35), ipady=(10))

        self.AdvancedSettingsFrame = ttk.LabelFrame(self.MainFrame, text="Advanced Settings", padding=(20, 10))
        self.AdvancedSettingsFrame.grid(row=2, column=0, pady=(30,0), columnspan=2, sticky="nsew")

        # ADVANCED SETTINGS -------------------------------------------------------------------------------------------------------------------------
        
        self.ComboBoxLabel = ttk.Label(self.AdvancedSettingsFrame, text="Theme:", font=("-size", 11))
        self.ComboBoxLabel.grid(row=0, column=0, sticky="w")

        self.ComboBox = ttk.Combobox(self.AdvancedSettingsFrame, state="readonly", values=self.ComboBoxList)
        self.ComboBox.grid(row=0, column=1, padx=5, ipady=5, sticky="ew")
        self.ComboBox.current(self.ComboBoxList.index(self.InterpratSettings(1)))
        self.ComboBox.bind("<<ComboboxSelected>>", self.ChangeTheme)

        # FRAMES ------------------------------------------------------------------------------------------------------------------------------------
        
        self.DarkModeToggleFrame = ttk.Frame(self.AdvancedSettingsFrame)
        self.DarkModeToggleFrame.grid(row=1, column=0, columnspan=3, pady=(5), sticky="ew")

        self.ThemesSeperator = ttk.Separator(self.AdvancedSettingsFrame, orient="horizontal")
        self.ThemesSeperator.grid(row=2, column=0, columnspan=3, pady=(10), sticky="ew")

        self.KeyboardMouseFrame = ttk.Frame(self.AdvancedSettingsFrame)
        self.KeyboardMouseFrame.grid(row=3, column=0, columnspan=3, pady=(5), sticky="ew")

        #self.ThemesSeperator = ttk.Separator(self.AdvancedSettingsFrame, orient="horizontal")
        #self.ThemesSeperator.grid(row=4, column=0, columnspan=3, pady=(10), sticky="ew")

        #self.ConsoleToggleFrame = ttk.Frame(self.AdvancedSettingsFrame)
        #self.ConsoleToggleFrame.grid(row=5, column=0, columnspan=3, pady=(5), sticky="ew")

        # ADVANCED CONTENT --------------------------------------------------------------------------------------------------------------------------
        
        self.DarkModeToggleLabel = ttk.Label(self.DarkModeToggleFrame, text="Dark Mode:", font=("-size", 11))
        self.DarkModeToggleLabel.grid(row=0, column=0, sticky="w", pady=(5))

        self.DarkModeToggle = ttk.Checkbutton(self.DarkModeToggleFrame, style='Switch.TCheckbutton', variable=self.DarkLightModeBool)
        self.DarkModeToggle.grid(row=0, column=1, padx=5, sticky="ew", pady=(5))

        self.ToggleMouseLabel = ttk.Label(self.KeyboardMouseFrame, text="Use Mouse:", font=("-size", 11))
        self.ToggleMouseLabel.grid(row=2, column=0, sticky="w",pady=5)

        self.ToggleMouse = ttk.Checkbutton(self.KeyboardMouseFrame, style='Switch.TCheckbutton', variable=self.UseMouseBool)
        self.ToggleMouse.grid(row=2, column=1, padx=5, sticky="ew",pady=5)

        self.ToggleKeyboardLabel = ttk.Label(self.KeyboardMouseFrame, text="Use Keyboard:", font=("-size", 11))
        self.ToggleKeyboardLabel.grid(row=3, column=0, sticky="w",pady=5)

        self.ToggleKeyboard = ttk.Checkbutton(self.KeyboardMouseFrame, style='Switch.TCheckbutton', variable=self.UseKeyboardBool)
        self.ToggleKeyboard.grid(row=3, column=1, padx=5, sticky="ew",pady=5)

        #self.ToggleConsoleLabel = ttk.Label(self.ConsoleToggleFrame, text="Show Console:", font=("-size", 11))
        #self.ToggleConsoleLabel.grid(row=4, column=0, sticky="w",pady=5)

        #self.ToggleConsole = ttk.Checkbutton(self.ConsoleToggleFrame, style='Switch.TCheckbutton', variable=self.UseConsoleBool)
        #self.ToggleConsole.grid(row=4, column=1, padx=5, sticky="ew",pady=5)

        # THEME LOAD --------------------------------------------------------------------------------------------------------------------------------

        self.ChangeTheme()

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
        SettingsFile = os.path.join(os.path.dirname(__file__), "Settings")
        with open(SettingsFile, 'r') as file:
            lines = file.readlines()

        if LineNumber is not None and 1 <= LineNumber <= len(lines):
            lines[LineNumber - 1] = f"{Value}\n"
        else:
            raise IndexError("Line number out of range")

        with open(SettingsFile, 'w') as file:
            file.writelines(lines)

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

        self.MainFrame.update()
        canvas_width = self.MainFrame.winfo_width()
        canvas_height = self.MainFrame.winfo_height()
        self.root.geometry(f"{canvas_width+20}x{canvas_height+20}")

        # Fix vulnerable widgets, disgraceful hack (I have no idea why this happens, too lazy to find out)
        self.FixThemes()
        
    def FixThemes(self):
        Widgets = [self.root]
        while Widgets:
            widget = Widgets.pop()

            if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.Text, ttk.Label, ttk.Button, ttk.Entry)):
                try:
                    widget.config(background=self.Style.lookup("TFrame", "background"))
                except Exception as e:
                    try:
                        widget.config(bg=self.Style.lookup("TFrame", "background"))
                    except Exception as e:
                        print(f"Failed to process widget: {widget}")
                        pass
            
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.Text, ttk.Label, ttk.Button, ttk.Entry)):
                try:
                    widget.config(foreground=self.Style.lookup("TFrame", "foreground"))
                except Exception as e:
                    try:
                        widget.config(fg=self.Style.lookup("TFrame", "foreground"))
                    except Exception as e:
                        print(f"Failed to process widget: {widget}")
                        pass

            if isinstance(widget, (tk.Frame, ttk.Frame)):
                try:
                    widget.config(background=self.Style.lookup("TFrame", "background"))
                except Exception as e:
                    try:
                        widget.config(bg=self.Style.lookup("TFrame", "background"))
                    except Exception as e:
                        print(f"Failed to process widget: {widget}")
                        pass

            Widgets.extend(widget.winfo_children())

    def DarkLightModeScheduler(self, *args):
        self.SaveSettings(2, self.DarkLightModeBool.get())
        self.ReloadRefreshSchedule()

    def ConsoleScheduler(self, *args):
        self.SaveSettings(5, self.UseConsoleBool.get())
        self.ReloadRefreshSchedule()

    def ReloadRefreshSchedule(self):
        if not self.ReloadPending:
            self.ReloadPending = True
            self.root.after(10, self.RefreshWindow)

    def RefreshWindow(self):
        self.ReloadPending = False
        self.root.quit()

        Python = sys.executable
        PythonW = Python.replace("python.exe", "pythonw.exe")

        #f.flush()
        #os.fsync(f.fileno())
        os.execl(Python, Python, *sys.argv)
        #if self.UseConsoleBool.get():
        #    os.execl(Python, Python, *sys.argv)
        #else:
        #    os.execl(PythonW, PythonW, *sys.argv)

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    root.iconbitmap(os.path.join(os.path.dirname(__file__), "Icon.ico"))
    root.title("Macro")

    Interface = Main(root)
    Interface.pack(fill="both", expand=True)

    root.mainloop()

