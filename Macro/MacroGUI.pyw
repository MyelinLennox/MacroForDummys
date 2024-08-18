import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.Style = ttk.Style(self)
        self.ReloadPending = False
        self.CurrentBindingButton = None  # Track the button currently being bound to a hotkey

        ThemeFolder = os.path.join(os.path.dirname(__file__), "Themes")
        self.ThemeComboBoxList = []
        if os.path.exists(ThemeFolder):
            for folder_name in os.listdir(ThemeFolder):
                if os.path.isdir(os.path.join(ThemeFolder, folder_name)):
                    self.ThemeComboBoxList.append(folder_name)

        self.RecordingsComboBoxList = []
        if os.path.exists(os.path.join(os.path.dirname(__file__), "Recordings")):
            for File in os.listdir(os.path.join(os.path.dirname(__file__), "Recordings")):
                if os.path.isfile(os.path.join(os.path.dirname(__file__), "Recordings", File)):
                    self.RecordingsComboBoxList.append(File)
        self.RecordingsComboBoxList.append("None")

        self.DarkLightModeBool = tk.BooleanVar(value=self.InterpratSettings(3))
        self.DarkLightModeBool.trace_add("write", lambda *args: self.ReloadWindowScheduler())

        self.UseMouseBool = tk.BooleanVar(value=self.InterpratSettings(4))
        self.UseMouseBool.trace_add("write", lambda *args: self.SaveSettings(4, self.UseMouseBool.get()))
        self.UseMouseBool.trace_add("write", lambda *args: self.SaveHeader(4, self.UseMouseBool.get()))

        self.UseKeyboardBool = tk.BooleanVar(value=self.InterpratSettings(5))
        self.UseKeyboardBool.trace_add("write", lambda *args: self.SaveSettings(5, self.UseKeyboardBool.get()))
        self.UseKeyboardBool.trace_add("write", lambda *args: self.SaveHeader(5, self.UseKeyboardBool.get()))

        self.UseConsoleBool = tk.BooleanVar(value=self.InterpratSettings(6))
        
        RecordingComboboxState = "readonly"

        # FRAMES -----------------------------------------------------------------------------------------------------------------------------

        self.MainFrame = ttk.Frame(self, padding=10, relief='solid', borderwidth=1)
        self.MainFrame.grid(sticky="nsew", padx=10, pady=10)
        self.bind("<Configure>", self.ConfigureRootGeometry)
        self.MainFrame.after(100, self.SetupSubtext)

        self.RecordButtonTextFrame = ttk.Frame(self)
        self.PlaybackButtonTextFrame = ttk.Frame(self)

        self.SettingsFrame = ttk.LabelFrame(self.MainFrame, text="Settings", padding=(20, 10), relief='ridge', borderwidth=2, labelanchor='n')
        self.SettingsFrame.grid(row=3, column=0, pady=(30, 0), columnspan=3, sticky="ew")

        self.RecordingsCombooxFrame = ttk.Frame(self.SettingsFrame)
        self.RecordingsCombooxFrame.grid(row=1, column=0, columnspan=3, pady=5, sticky="ew")

        self.ThemesSeperator = ttk.Separator(self.SettingsFrame, orient="horizontal")
        self.ThemesSeperator.grid(row=2, column=0, columnspan=3, pady=10, sticky="ew")

        self.ThemeComboboxFrame = ttk.Frame(self.SettingsFrame)
        self.ThemeComboboxFrame.grid(row=3, column=0, columnspan=3, pady=5, sticky="ew")

        self.DarkModeToggleFrame = ttk.Frame(self.SettingsFrame)
        self.DarkModeToggleFrame.grid(row=4, column=0, columnspan=3, pady=5, sticky="ew")

        self.ThemesSeperator = ttk.Separator(self.SettingsFrame, orient="horizontal")
        self.ThemesSeperator.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")

        self.UseMouseFrame = ttk.Frame(self.SettingsFrame)
        self.UseMouseFrame.grid(row=6, column=0, columnspan=3, pady=5, sticky="ew")
        
        self.UseKeyboardFrame = ttk.Frame(self.SettingsFrame)
        self.UseKeyboardFrame.grid(row=7, column=0, columnspan=3, pady=5, sticky="ew")

        # CONTENT ---------------------------------------------------------------------------------------------------------------------------

        self.Header = ttk.Label(self.MainFrame, text="Macro For Dummys", justify="center", font=("-size", 25, "-weight", "bold"))
        self.Header.grid(row=0, column=0, pady=(15, 25), columnspan=3, sticky="n")

        self.RecordButton = ttk.Button(self.MainFrame, style="Bigger.TButton", width=20, text="Record")
        self.RecordButton.grid(row=1, column=0, sticky="ew", padx=(5), ipady=12, ipadx=12)
        #self.RecordButton.bind("<Button-1>", self.)
        
        self.PlaybackButton = ttk.Button(self.MainFrame, style="Bigger.TButton", width=20, text="Playback")
        self.PlaybackButton.grid(row=1, column=2, sticky="ew", padx=(5), ipady=12, ipadx=12)
        #self.PlaybackButton.bind("<Button-1>", self.)

        self.RecordButtonText = ttk.Label(self.RecordButtonTextFrame, text="Record", font=("-size", 18), background=self.Style.lookup("TButton", "background"))
        self.RecordButtonText.grid(row=1, column=0, sticky="n")

        self.RecordButtonSubText = ttk.Label(self.RecordButtonTextFrame, text="(unbound)", font=("-size", 7), background=self.Style.lookup("TButton", "background"))
        self.RecordButtonSubText.grid(row=2, column=0, pady=(0, 2), sticky="n")

        self.PlaybackButtonText = ttk.Label(self.PlaybackButtonTextFrame, text="Playback", font=("-size", 18), background=self.Style.lookup("TButton", "background"))
        self.PlaybackButtonText.grid(row=1, column=0, sticky="n")

        self.PlaybackButtonSubText = ttk.Label(self.PlaybackButtonTextFrame, text="(unbound)", font=("-size", 7), background=self.Style.lookup("TButton", "background"))
        self.PlaybackButtonSubText.grid(row=2, column=0, pady=(0, 2), sticky="n")
        
        self.RecordingsComboBoxLabel = ttk.Label(self.RecordingsCombooxFrame, text="Recording:", font=("-size", 11))
        self.RecordingsComboBoxLabel.grid(row=0, column=0, sticky="w")

        self.RecordingsComboBox = ttk.Combobox(self.RecordingsCombooxFrame, values=self.RecordingsComboBoxList, state=RecordingComboboxState)
        self.RecordingsComboBox.grid(row=0, column=1, padx=(15,5), ipady=5, sticky="ew")
        self.RecordingsComboBox.current(self.RecordingsComboBoxList.index("None"))
        self.RecordingsComboBox.bind("<<ComboboxSelected>>", self.ChangeSelectedRecording)
        self.RecordingsComboBox.bind("<KeyPress>", self.SaveComboboxEditing)

        if self.InterpratSettings(3) == "True":
            self.CreateFileImage = Image.open(os.path.join(os.path.dirname(__file__), "CreateFileLight.png"))
        else:
            self.CreateFileImage = Image.open(os.path.join(os.path.dirname(__file__), "CreateFileDark.png"))

        self.CreateFileImage = self.CreateFileImage.resize((25, 25), Image.LANCZOS)
        self.CreateFileImageTk = ImageTk.PhotoImage(self.CreateFileImage)
        self.CreateFileButton = ttk.Button(self.RecordingsCombooxFrame, image=self.CreateFileImageTk, width=5)
        self.CreateFileButton.bind("<Button-1>", self.CreateNewRecording, self.ChangeSelectedRecording)
        self.CreateFileButton.grid(row=0, column=2, padx=5, sticky="ew")

        if self.InterpratSettings(3) == "True":
            self.DeleteFileImage = Image.open(os.path.join(os.path.dirname(__file__), "DeleteFileLight.png"))
        else:
            self.DeleteFileImage = Image.open(os.path.join(os.path.dirname(__file__), "DeleteFileDark.png"))

        self.DeleteFileImage = self.DeleteFileImage.resize((25, 25), Image.LANCZOS)
        self.DeleteFileImageTk = ImageTk.PhotoImage(self.DeleteFileImage)
        self.DeleteFileButton = ttk.Button(self.RecordingsCombooxFrame, image=self.DeleteFileImageTk, width=5)
        self.DeleteFileButton.bind("<Button-1>", self.DeleteRecording)
        self.DeleteFileButton.grid(row=0, column=3, padx=5, sticky="ew")

        self.ThemeComboBoxLabel = ttk.Label(self.ThemeComboboxFrame, text="Theme:", font=("-size", 11))
        self.ThemeComboBoxLabel.grid(row=0, column=0, sticky="w")

        self.ThemeComboBox = ttk.Combobox(self.ThemeComboboxFrame, state="readonly", values=self.ThemeComboBoxList)
        self.ThemeComboBox.grid(row=0, column=1, padx=5, ipady=5, sticky="ew")
        self.ThemeComboBox.current(self.ThemeComboBoxList.index(self.InterpratSettings(2)))
        self.ThemeComboBox.bind("<<ComboboxSelected>>", self.ChangeTheme)

        self.DarkModeToggleLabel = ttk.Label(self.DarkModeToggleFrame, text="Dark Mode:", font=("-size", 11))
        self.DarkModeToggleLabel.grid(row=0, column=0, sticky="w", pady=5)

        self.DarkModeToggle = ttk.Checkbutton(self.DarkModeToggleFrame, style='Switch.TCheckbutton', variable=self.DarkLightModeBool)
        self.DarkModeToggle.grid(row=0, column=1, padx=5, sticky="ew", pady=5)

        self.ToggleMouseLabel = ttk.Label(self.UseMouseFrame, text="Use Mouse:", font=("-size", 11))
        self.ToggleMouseLabel.grid(row=0, column=0, sticky="w", pady=5)

        self.ToggleMouse = ttk.Checkbutton(self.UseMouseFrame, style='Switch.TCheckbutton', variable=self.UseMouseBool)
        self.ToggleMouse.grid(row=0, column=1, padx=5, sticky="e", pady=5)

        self.ToggleKeyboardLabel = ttk.Label(self.UseKeyboardFrame, text="Use Keyboard:", font=("-size", 11))
        self.ToggleKeyboardLabel.grid(row=0, column=0, sticky="w", pady=5)

        self.ToggleKeyboard = ttk.Checkbutton(self.UseKeyboardFrame, style='Switch.TCheckbutton', variable=self.UseKeyboardBool)
        self.ToggleKeyboard.grid(row=0, column=1, padx=5, sticky="e", pady=5)

        # THEME LOAD --------------------------------------------------------------------------------------------------------------------------------

        self.ChangeTheme()
        self.ConfigureRootGeometry()

    @staticmethod
    def InterpratSettings(LineNumber=None):
        SettingsFilePath = os.path.join(os.path.dirname(__file__), "Settings.ini")

        with open(SettingsFilePath, "r") as SettingsFile:
            SettingsList = []
            for line in SettingsFile:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if ':' in line:
                    _, value = line.split(':', 1)
                    SettingsList.append(value.strip())

        if LineNumber is not None:
            if 1 <= LineNumber <= len(SettingsList):
                return SettingsList[LineNumber - 1]
            else:
                raise IndexError("Line number out of range")
        return SettingsList

    @staticmethod
    def SaveSettings(LineNumber, Value):
        SettingsFilePath = os.path.join(os.path.dirname(__file__), "Settings.ini")
        SettingsList = Main.InterpratSettings()

        if 1 <= LineNumber <= len(SettingsList):
            SettingsList[LineNumber - 1] = Value
        else:
            raise IndexError("Line number out of range")

        with open(SettingsFilePath, "r") as SettingsFile:
            lines = SettingsFile.readlines()

        with open(SettingsFilePath, "w") as SettingsFile:
            SettingsIndex = 0
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    if ':' in line:
                        prefix, _ = line.split(':', 1)
                        SettingsFile.write(f"{prefix}: {SettingsList[SettingsIndex]}\n")
                        SettingsIndex += 1
                    else:
                        SettingsFile.write(line + "\n")
                else:
                    SettingsFile.write(line + "\n")

    def SetupSubtext(self):
        self.update_idletasks()

        RecordButtonX = self.RecordButton.winfo_x()
        RecordButtonY = self.RecordButton.winfo_y() + self.RecordButton.winfo_height()

        PlaybackButtonX = self.PlaybackButton.winfo_x()
        PlaybackButtonY = self.PlaybackButton.winfo_y() + self.PlaybackButton.winfo_height()

        #self.RecordButtonTextFrame.place(x=RecordButtonX + self.RecordButton.winfo_width() / 2, y=RecordButtonY - 39, anchor="n")
        #self.PlaybackButtonTextFrame.place(x=PlaybackButtonX + self.PlaybackButton.winfo_width() / 2, y=PlaybackButtonY - 39, anchor="n")

    def ChangeSelectedRecording(self, *args):
        SelectedRecording = self.RecordingsComboBox.get()
        if SelectedRecording == "None":
            self.RecordingsComboBox.config(state="readonly")
            self.DisableComboboxEditing()
        else:
            self.RecordingsComboBox.config(state="normal")
            self.EnableComboboxEditing(SelectedRecording)
    
        self.SaveSettings(1, SelectedRecording)

    def CreateNewRecording(self, event=None):
        Directory = os.path.join(os.path.dirname(__file__), "Recordings")
        ExistingFiles = [f for f in os.listdir(Directory) if os.path.isfile(os.path.join(Directory, f))]
        FileCount = len(ExistingFiles) + 1

        filename = f"Recording_{FileCount}.txt"
        filepath = os.path.join(Directory, filename)

        with open(filepath, 'w') as new_file:
            new_file.write("")

        self.RecordingsComboBoxList.append(filename)
        self.RecordingsComboBox.config(values=self.RecordingsComboBoxList)
        self.RecordingsComboBox.set(filename)

        self.SaveSettings(1, filename)

    def DeleteRecording(self, event=None):
        SelectedRecording = self.RecordingsComboBox.get()
        if SelectedRecording != "None":
            os.remove(os.path.join(os.path.dirname(__file__), "Recordings", SelectedRecording))

            self.RecordingsComboBoxList.remove(SelectedRecording)
            self.RecordingsComboBox.config(values=self.RecordingsComboBoxList)

            self.RecordingsComboBox.set("None")

            self.SaveSettings(1, "None")
            self.DisableComboboxEditing()

    def DisableComboboxEditing(self):
        self.RecordButton.config(state="disabled")
        self.PlaybackButton.config(state="disabled")

    def EnableComboboxEditing(self, filename):
        self.RecordButton.config(state="normal")
        self.PlaybackButton.config(state="normal")

    def SaveComboboxEditing(self, filename):
        SelectedRecording = self.RecordingsComboBox.get()
        os.rename(os.path.join(os.path.dirname(__file__), "Recordings", filename), os.path.join(os.path.dirname(__file__), "Recordings", SelectedRecording))
        self.SaveSettings(1, filename)

    def ChangeTheme(self, *args):
        self.Style = ttk.Style(self)
        SelectedTheme = self.ThemeComboBox.get()
        ThemePath = os.path.join(os.path.dirname(__file__), "Themes", SelectedTheme, f"{SelectedTheme}.tcl")

        self.SaveSettings(2, SelectedTheme)

        if self.DarkLightModeBool.get():
            ThemeMode = "dark"
        else:
            ThemeMode = "light"

        try:
            self.root.tk.call("source", ThemePath)
            self.root.tk.call("set_theme", ThemeMode)
        except Exception as e:
            print(f"Failed to load theme from {ThemePath}: {e}")
            try:
                ttk.Style().theme_use(f"{SelectedTheme.lower()}-{ThemeMode}")
            except:
                self.ReloadWindowScheduler()

        self.RecordButtonText.config(background=self.Style.lookup("TButton", "background"))
        self.PlaybackButtonText.config(background=self.Style.lookup("TButton", "background"))
        self.RecordButtonSubText.config(background=self.Style.lookup("TButton", "background"))
        self.PlaybackButtonSubText.config(background=self.Style.lookup("TButton", "background"))

        self.ConfigureRootGeometry()

    def ReloadWindowScheduler(self, *args):
        if not self.ReloadPending:
            self.root.after(300, self.ReloadWindow)

    def ReloadWindow(self):
        self.SaveSettings(2, self.ThemeComboBox.get())
        self.SaveSettings(3, self.DarkLightModeBool.get())
        self.root.quit()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def ConfigureRootGeometry(self, event=None):
        self.root.update_idletasks()

        FrameWidth = self.MainFrame.winfo_width()
        FrameHeight = self.MainFrame.winfo_height()

        Width = FrameWidth + 20
        Height = FrameHeight + 20

        self.root.minsize(Width, Height)

        ScreenWidth = self.root.winfo_screenwidth()
        ScreenHeight = self.root.winfo_screenheight()

        X = (ScreenWidth // 2) - (Width // 2)
        Y = (ScreenHeight // 2) - (Height // 2)

        self.root.geometry(f"{Width}x{Height}+{X}+{Y}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Macro For Dummys")
    root.resizable(False, False)
    app = Main(root)
    app.pack(fill="both", expand=True)
    root.mainloop()