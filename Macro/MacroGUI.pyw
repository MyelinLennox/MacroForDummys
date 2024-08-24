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
        self.CurrentBindingButton = None

        self.RecordingsComboBoxList = []
        if os.path.exists(os.path.join(os.path.dirname(__file__), "Recordings")):
            for File in os.listdir(os.path.join(os.path.dirname(__file__), "Recordings")):
                if os.path.isfile(os.path.join(os.path.dirname(__file__), "Recordings", File)):
                    self.RecordingsComboBoxList.append(File)
        self.RecordingsComboBoxList.append("None")

        self.DarkLightModeBool = tk.BooleanVar(value=self.InterpratSettings(3))
        self.DarkLightModeBool.trace_add("write", lambda *args: self.ReloadWindowScheduler())

        self.CustomThemeColors = tk.BooleanVar(value=False)
        self.CustomThemeColors.trace_add("write", lambda *args: self.SaveSettings(2, self.CustomThemeColors.get()))

        self.UseMouseBool = tk.BooleanVar(value=self.InterpratSettings(4))
        self.UseMouseBool.trace_add("write", lambda *args: self.SaveSettings(4, self.UseMouseBool.get()))

        self.UseKeyboardBool = tk.BooleanVar(value=self.InterpratSettings(5))
        self.UseKeyboardBool.trace_add("write", lambda *args: self.SaveSettings(5, self.UseKeyboardBool.get()))
        self.UseConsoleBool = tk.BooleanVar(value=self.InterpratSettings(6))
        
        RecordingComboboxState = "readonly"

        # FRAMES --------------------------------------------------------------------------------------------------------------------------------------

        self.Container = ttk.Frame(self, padding=10, relief='solid', borderwidth=1)
        self.Container.grid(sticky="nsew", padx=10, pady=10)
        self.bind("<Configure>", self.ConfigureRootGeometry)

        self.MainFrame = ttk.Frame(self.Container, padding=(20, 10), relief='ridge', borderwidth=0)
        self.MainFrame.grid(row=0, column=0, pady=(0, 30), columnspan=3, sticky="ew")

        self.SettingsFrame = ttk.LabelFrame(self.Container, text="Settings", padding=(20, 10), relief='ridge', borderwidth=2, labelanchor='nw')
        self.SettingsFrame.grid(row=1, column=0, pady=(30, 0), columnspan=3, sticky="ew")

        self.VisualSettingsFrame = ttk.LabelFrame(self.Container, text="Visual", padding=(20, 10), relief='ridge', borderwidth=2, labelanchor='nw')
        self.VisualSettingsFrame.grid(row=2, column=0, pady=(30, 0), columnspan=3, sticky="ew")

        # MAIN --------------------------------------------------------------------------------------------------------------------------------------

        self.RecordButtonTextFrame = ttk.Frame(self.MainFrame)
        self.PlaybackButtonTextFrame = ttk.Frame(self.MainFrame)

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

        # SETTINGS ----------------------------------------------------------------------------------------------------------------------------------

        self.RecordingsComboxFrame = ttk.Frame(self.SettingsFrame)
        self.RecordingsComboxFrame.grid(row=1, column=0, columnspan=3, pady=5, sticky="ew")

        self.UseMouseFrame = ttk.Frame(self.SettingsFrame)
        self.UseMouseFrame.grid(row=6, column=0, columnspan=3, pady=5, sticky="ew")
        
        self.UseKeyboardFrame = ttk.Frame(self.SettingsFrame)
        self.UseKeyboardFrame.grid(row=7, column=0, columnspan=3, pady=5, sticky="ew")

        self.PlaybackButtonSubText = ttk.Label(self.PlaybackButtonTextFrame, text="(unbound)", font=("-size", 7), background=self.Style.lookup("TButton", "background"))
        self.PlaybackButtonSubText.grid(row=2, column=0, pady=(0, 2), sticky="n")
        
        self.RecordingsComboBoxLabel = ttk.Label(self.RecordingsComboxFrame, text="Profile:", font=("-size", 11))
        self.RecordingsComboBoxLabel.grid(row=0, column=0, sticky="w")

        self.RecordingsComboBox = ttk.Combobox(self.RecordingsComboxFrame, values=self.RecordingsComboBoxList, state=RecordingComboboxState)
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
        self.CreateFileButton = ttk.Button(self.RecordingsComboxFrame, image=self.CreateFileImageTk, width=5)
        self.CreateFileButton.bind("<Button-1>", self.CreateNewRecording, self.ChangeSelectedRecording)
        self.CreateFileButton.grid(row=0, column=2, padx=5, sticky="ew")

        if self.InterpratSettings(3) == "True":
            self.DeleteFileImage = Image.open(os.path.join(os.path.dirname(__file__), "DeleteFileLight.png"))
        else:
            self.DeleteFileImage = Image.open(os.path.join(os.path.dirname(__file__), "DeleteFileDark.png"))

        self.DeleteFileImage = self.DeleteFileImage.resize((25, 25), Image.LANCZOS)
        self.DeleteFileImageTk = ImageTk.PhotoImage(self.DeleteFileImage)
        self.DeleteFileButton = ttk.Button(self.RecordingsComboxFrame, image=self.DeleteFileImageTk, width=5)
        self.DeleteFileButton.bind("<Button-1>", self.DeleteRecording)
        self.DeleteFileButton.grid(row=0, column=3, padx=5, sticky="ew")

        self.ToggleMouseLabel = ttk.Label(self.UseMouseFrame, text="Use Mouse:", font=("-size", 11))
        self.ToggleMouseLabel.grid(row=0, column=0, sticky="w", pady=5)

        self.ToggleMouse = ttk.Checkbutton(self.UseMouseFrame, style='Switch.TCheckbutton', variable=self.UseMouseBool)
        self.ToggleMouse.grid(row=0, column=1, padx=5, sticky="e", pady=5)

        self.ToggleKeyboardLabel = ttk.Label(self.UseKeyboardFrame, text="Use Keyboard:", font=("-size", 11))
        self.ToggleKeyboardLabel.grid(row=0, column=0, sticky="w", pady=5)

        self.ToggleKeyboard = ttk.Checkbutton(self.UseKeyboardFrame, style='Switch.TCheckbutton', variable=self.UseKeyboardBool)
        self.ToggleKeyboard.grid(row=0, column=1, padx=5, sticky="e", pady=5)

        # VISUAL ------------------------------------------------------------------------------------------------------------------------------------
        
        self.RadioCheckFrame = ttk.Frame(self.VisualSettingsFrame, relief='solid', borderwidth=1, style="TLabelframe")
        self.RadioCheckFrame.grid(row=0, column=0, pady=5, sticky="nsew")

        self.ColorContainerFrame = ttk.Frame(self.VisualSettingsFrame, relief='solid', borderwidth=1, style="TLabelframe")
        self.ColorContainerFrame.grid(row=0, column=1, pady=5, sticky="nsew", padx=(10, 0))

        self.ColorContainer1 = ttk.Frame(self.ColorContainerFrame)
        self.ColorContainer1.grid(row=0, column=0, pady=5, padx=5, sticky="nsew")
        self.ColorContainer2 = ttk.Frame(self.ColorContainerFrame)
        self.ColorContainer2.grid(row=1, column=0, pady=5, padx=5, sticky="nsew")
        self.ColorContainer3 = ttk.Frame(self.ColorContainerFrame)
        self.ColorContainer3.grid(row=2, column=0, pady=5, padx=5, sticky="nsew")
        self.ColorContainer4 = ttk.Frame(self.ColorContainerFrame)
        self.ColorContainer4.grid(row=3, column=0, pady=5, padx=5, sticky="nsew")
        self.ColorContainer5 = ttk.Frame(self.ColorContainerFrame)
        self.ColorContainer5.grid(row=4, column=0, pady=5, padx=5, sticky="nsew")
        self.ColorContainer6 = ttk.Frame(self.ColorContainerFrame)
        self.ColorContainer6.grid(row=5, column=0, pady=5, padx=5, sticky="nsew")

        self.RadioCheck1 = ttk.Radiobutton(self.RadioCheckFrame, text="Light:", variable=self.DarkLightModeBool, value=False)
        self.RadioCheck1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.RadioCheck2 = ttk.Radiobutton(self.RadioCheckFrame, text="Dark:", variable=self.DarkLightModeBool, value=True)
        self.RadioCheck2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        self.RadioCheck3 = ttk.Radiobutton(self.RadioCheckFrame, text="Custom", variable=self.CustomThemeColors)

        self.HorizonalSeparator = ttk.Separator(self.RadioCheckFrame, orient="horizontal", style="TSeparator")
        self.HorizonalSeparator.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew", padx=5)

        self.RadioCheck3.bind("<Button-1>", self.UseCustomThemeColors)
        self.RadioCheck3.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

        self.ColorLabel1 = ttk.Label(self.ColorContainer1, text="fg:", font=("-size", 11))
        self.ColorLabel1.grid(row=0, column=0, sticky="w", padx=10)
        self.ColorLabel2 = ttk.Label(self.ColorContainer2, text="bg:", font=("-size", 11))
        self.ColorLabel2.grid(row=1, column=0, sticky="w", padx=10)
        self.ColorLabel3 = ttk.Label(self.ColorContainer3, text="disabledfg:", font=("-size", 11))
        self.ColorLabel3.grid(row=2, column=0, sticky="w", padx=10)
        self.ColorLabel4 = ttk.Label(self.ColorContainer4, text="disabledbg:", font=("-size", 11))
        self.ColorLabel4.grid(row=3, column=0, sticky="w", padx=10)
        self.ColorLabel5 = ttk.Label(self.ColorContainer5, text="selectfg:", font=("-size", 11))
        self.ColorLabel5.grid(row=4, column=0, sticky="w", padx=10)
        self.ColorLabel6 = ttk.Label(self.ColorContainer6, text="selectbg:", font=("-size", 11))
        self.ColorLabel6.grid(row=5, column=0, sticky="w", padx=10)

        self.ColorDisplay1 = ttk.Frame(self.ColorContainer1, width=30, height=30, style="ColorButton1.TButton")
        self.ColorDisplay1.grid(row=0, column=2, padx=(40, 5), sticky="e")
        self.ColorDisplay2 = ttk.Frame(self.ColorContainer2, width=30, height=30, style="ColorButton2.TButton")
        self.ColorDisplay2.grid(row=1, column=2, padx=(40, 5), sticky="e")
        self.ColorDisplay3 = ttk.Frame(self.ColorContainer3, width=30, height=30, style="ColorButton3.TButton")
        self.ColorDisplay3.grid(row=2, column=2, padx=(40, 5), sticky="e")
        self.ColorDisplay4 = ttk.Frame(self.ColorContainer4, width=30, height=30, style="ColorButton4.TButton")
        self.ColorDisplay4.grid(row=3, column=2, padx=(40, 5), sticky="e")
        self.ColorDisplay5 = ttk.Frame(self.ColorContainer5, width=30, height=30, style="ColorButton5.TButton")
        self.ColorDisplay5.grid(row=4, column=2, padx=(40, 5), sticky="e")
        self.ColorDisplay6 = ttk.Frame(self.ColorContainer6, width=30, height=30, style="ColorButton6.TButton")
        self.ColorDisplay6.grid(row=5, column=2, padx=(40, 5), sticky="e")

        self.ColorInput1 = ttk.Entry(self.ColorContainer1, width=10)
        self.ColorInput1.grid(row=0, column=3, ipady=5, sticky="e", padx=15)
        self.ColorInput1.bind("<KeyRelease>", lambda event: self.UseCustomThemeColors(1))
        self.ColorInput1.bind("<FocusIn>", lambda event: self.EntryPlaceholderFocIn(self.ColorInput1, self.GetThemeColors("fg")))
        self.ColorInput1.bind("<FocusOut>", lambda event: self.EntryPlaceholderFocOut(self.ColorInput1, self.GetThemeColors("fg")))
        self.ColorInput2 = ttk.Entry(self.ColorContainer2, width=10)
        self.ColorInput2.grid(row=1, column=3, ipady=5, sticky="e", padx=15)
        self.ColorInput2.bind("<KeyRelease>", lambda event: self.UseCustomThemeColors(2))
        self.ColorInput2.bind("<FocusIn>", lambda event: self.EntryPlaceholderFocIn(self.ColorInput2, self.GetThemeColors("bg")))
        self.ColorInput2.bind("<FocusOut>", lambda event: self.EntryPlaceholderFocOut(self.ColorInput2, self.GetThemeColors("bg")))
        self.ColorInput3 = ttk.Entry(self.ColorContainer3, width=10)
        self.ColorInput3.grid(row=2, column=3, ipady=5, sticky="e", padx=15)
        self.ColorInput3.bind("<KeyRelease>", lambda event: self.UseCustomThemeColors(3))
        self.ColorInput3.bind("<FocusIn>", lambda event: self.EntryPlaceholderFocIn(self.ColorInput3, self.GetThemeColors("disabledfg")))
        self.ColorInput3.bind("<FocusOut>", lambda event: self.EntryPlaceholderFocOut(self.ColorInput3, self.GetThemeColors("disabledfg")))
        self.ColorInput4 = ttk.Entry(self.ColorContainer4, width=10)
        self.ColorInput4.grid(row=3, column=3, ipady=5, sticky="e", padx=15)
        self.ColorInput4.bind("<KeyRelease>", lambda event: self.UseCustomThemeColors(4))
        self.ColorInput4.bind("<FocusIn>", lambda event: self.EntryPlaceholderFocIn(self.ColorInput4, self.GetThemeColors("disabledbg")))
        self.ColorInput4.bind("<FocusOut>", lambda event: self.EntryPlaceholderFocOut(self.ColorInput4, self.GetThemeColors("disabledbg")))
        self.ColorInput5 = ttk.Entry(self.ColorContainer5, width=10)
        self.ColorInput5.grid(row=4, column=3, ipady=5, sticky="e", padx=15)
        self.ColorInput5.bind("<KeyRelease>", lambda event: self.UseCustomThemeColors(5))
        self.ColorInput5.bind("<FocusIn>", lambda event: self.EntryPlaceholderFocIn(self.ColorInput5, self.GetThemeColors("selectfg")))
        self.ColorInput5.bind("<FocusOut>", lambda event: self.EntryPlaceholderFocOut(self.ColorInput5, self.GetThemeColors("selectfg")))
        self.ColorInput6 = ttk.Entry(self.ColorContainer6, width=10)
        self.ColorInput6.grid(row=5, column=3, ipady=5, sticky="e", padx=15)
        self.ColorInput6.bind("<KeyRelease>", lambda event: self.UseCustomThemeColors(6))
        self.ColorInput6.bind("<FocusIn>", lambda event: self.EntryPlaceholderFocIn(self.ColorInput6, self.GetThemeColors("selectbg")))
        self.ColorInput6.bind("<FocusOut>", lambda event: self.EntryPlaceholderFocOut(self.ColorInput6, self.GetThemeColors("selectbg")))

        for i in range(3):
            self.ColorContainer1.grid_columnconfigure(i, weight=1)
            self.ColorContainer2.grid_columnconfigure(i, weight=1)
            self.ColorContainer3.grid_columnconfigure(i, weight=1)
            self.ColorContainer4.grid_columnconfigure(i, weight=1)
            self.ColorContainer5.grid_columnconfigure(i, weight=1)
            self.ColorContainer6.grid_columnconfigure(i, weight=1)

        


    

        # FUNCTION LOAD -----------------------------------------------------------------------------------------------------------------------------

        self.ChangeTheme()
        self.ConfigureRootGeometry()
        self.ChangeSelectedRecording()

        self.EntryPlaceholderFocOut(self.ColorInput1, self.GetThemeColors("fg"))
        self.EntryPlaceholderFocOut(self.ColorInput2, self.GetThemeColors("bg"))
        self.EntryPlaceholderFocOut(self.ColorInput3, self.GetThemeColors("disabledfg"))
        self.EntryPlaceholderFocOut(self.ColorInput4, self.GetThemeColors("disabledbg"))
        self.EntryPlaceholderFocOut(self.ColorInput5, self.GetThemeColors("selectfg"))
        self.EntryPlaceholderFocOut(self.ColorInput6, self.GetThemeColors("selectbg"))
        
    def EntryPlaceholderFocIn(self, Entry, Placeholder):
        if Entry.get() == Placeholder:
            Entry.delete(0, "end")
            Entry.config(foreground=self.GetThemeColors("bg"))

    def EntryPlaceholderFocOut(self, Entry, Placeholder):
        if Entry.get() == "":
            Entry.insert(0, Placeholder)
            Entry.config(foreground=self.GetThemeColors("disabledfg"))


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
        Directory = os.path.join(os.path.dirname(__file__), "Profiles")
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

    def EnableComboboxEditing(self):
        self.RecordButton.config(state="normal")
        self.PlaybackButton.config(state="normal")

    def SaveComboboxEditing(self, filename):
        SelectedRecording = self.RecordingsComboBox.get()
        os.rename(os.path.join(os.path.dirname(__file__), "Recordings", filename), os.path.join(os.path.dirname(__file__), "Recordings", SelectedRecording))
        self.SaveSettings(1, filename)

    def UseCustomThemeColors(self, SelectedLabel, *args):
        if self.CustomThemeColors.get():
            self.RadioCheck1.config(state="normal", value=True)
            self.RadioCheck2.config(state="normal", value=False)
            self.RadioCheck3.config(state="normal", value=False)
        else:
            self.RadioCheck1.config(state="disabled", value=False)
            self.RadioCheck2.config(state="disabled", value=False)
        
        for i in range(6):
            LazyHack = ["fg", "bg", "disabledfg", "disabledbg", "selectfg", "selectbg"]
            Color = self.GetThemeColors(LazyHack[i])
            StyleName = f"ColorButton{i+1}.TButton"
            self.Style.configure(StyleName, background=Color)
            self.Style.layout(StyleName, [
                ('Button.background', {'children': [('Button.label', {'sticky': 'nswe'})], 'sticky': 'nswe'}),
                ('Button.focus', {'children': [('Button.background', {'children': [('Button.label', {'sticky': 'nswe'})], 'sticky': 'nswe'})], 'sticky': 'nswe'})
            ])
        
        #if SelectedLabel:
        #    Color = getattr(self, f"ColorInput{SelectedLabel}").get()
        #    StyleName = f"ColorButton{SelectedLabel}.TButton"
        #    self.Style.configure(StyleName, background=Color)

        #
        #    self.Style.layout(StyleName, [
        #        ('Button.background', {'children': [('Button.label', {'sticky': 'nswe'})], 'sticky': 'nswe'}),
        #        ('Button.focus', {'children': [('Button.background', {'children': [('Button.label', {'sticky': 'nswe'})], 'sticky': 'nswe'})], 'sticky': 'nswe'})
        #    ])


    def GetThemeColors(self, Color):
        IsDarkMode = self.DarkLightModeBool.get()

        colors = {
            "fg": ["#eeeeee", "#313131"],
            "bg": ["#313131", "#ffffff"],
            "disabledfg": ["#595959", "#595959"],
            "disabledbg": ["#ffffff", "#ffffff"],
            "selectfg": ["#ffffff", "#ffffff"],
            "selectbg": ["#217346", "#217346"]
        }

        return colors[Color][IsDarkMode]
        
    def ChangeTheme(self, *args):
        self.Style = ttk.Style(self)
        Theme = "Park"
        ThemePath = os.path.join(os.path.dirname(__file__), "Theme", Theme, f"{Theme}.tcl")

        self.SaveSettings(2, Theme)

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
                ttk.Style().theme_use(f"{Theme.lower()}-{ThemeMode}")
            except:
                self.ReloadWindowScheduler()

        self.ConfigureRootGeometry()

    def ReloadWindowScheduler(self, *args):
        if not self.ReloadPending:
            self.root.after(300, self.ReloadWindow)

    def ReloadWindow(self):
        self.SaveSettings(3, self.DarkLightModeBool.get())
        self.root.quit()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def ConfigureRootGeometry(self, event=None):
        self.root.update_idletasks()

        FrameWidth = self.Container.winfo_width()
        FrameHeight = self.Container.winfo_height()

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