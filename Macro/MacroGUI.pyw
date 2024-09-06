import tkinter as tk
from tkinter import ttk
from tkinter.font import ITALIC
from PIL import Image, ImageTk
import os
import sys
import ast


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.Style = ttk.Style(self)

        self.ReloadPending = False

        self.ShouldRun = False

        self.CurrentBindingButton = None

        self.RecordingsComboBoxList = []
        if os.path.exists(os.path.join(os.path.dirname(__file__), "Recordings")):
            for File in os.listdir(os.path.join(os.path.dirname(__file__), "Recordings")):
                if os.path.isfile(os.path.join(os.path.dirname(__file__), "Recordings", File)):
                    self.RecordingsComboBoxList.append(File)
        self.RecordingsComboBoxList.append("None")

        self.IsDarkLightMode = tk.BooleanVar(value=self.InterpratSettings(3))

        self.IsCustomMode = tk.BooleanVar(value=self.InterpratSettings(4).lower() == "custom")

        self.UseMouseBool = tk.BooleanVar(value=self.InterpratSettings(5))
        self.UseMouseBool.trace_add("write", lambda *args: self.SaveSettings(5, self.UseMouseBool.get()))

        self.UseKeyboardBool = tk.BooleanVar(value=self.InterpratSettings(6))
        self.UseKeyboardBool.trace_add("write", lambda *args: self.SaveSettings(6, self.UseKeyboardBool.get()))
        
        RecordingComboboxState = "readonly"

        self.CustomThemeColors = {
            "fg" : self.GetThemeColors("fg", (self.IsDarkLightMode.get())),
            "bg" : self.GetThemeColors("bg", (self.IsDarkLightMode.get())),
            "disabledfg" : self.GetThemeColors("disabledfg", self.IsDarkLightMode.get()),
            "disabledbg" : self.GetThemeColors("disabledbg", self.IsDarkLightMode.get()),
            "selectfg" : self.GetThemeColors("selectfg", self.IsDarkLightMode.get()),
            "selectbg" : self.GetThemeColors("selectbg", self.IsDarkLightMode.get())}

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

        self.CreateFileButton = ttk.Button(self.RecordingsComboxFrame, width=5)
        self.CreateFileButton.bind("<Button-1>", self.CreateNewRecording, self.ChangeSelectedRecording)
        self.CreateFileButton.grid(row=0, column=2, padx=5, sticky="ew")

        self.DeleteFileButton = ttk.Button(self.RecordingsComboxFrame, width=5)
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

        self.RadioCheck1 = ttk.Radiobutton(self.RadioCheckFrame, text="Light:", variable=self.IsDarkLightMode, value=False)
        self.RadioCheck1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.RadioCheck1.bind("<Button-1>", lambda event: self.ChangeTheme(False, False))
        self.RadioCheck2 = ttk.Radiobutton(self.RadioCheckFrame, text="Dark:", variable=self.IsDarkLightMode, value=True)
        self.RadioCheck2.grid(row=1, column=0, padx=5, pady=(10), sticky="nsew")
        self.RadioCheck2.bind("<Button-1>", lambda event: self.ChangeTheme(True, False))

        self.HorizonalSeparator = ttk.Separator(self.RadioCheckFrame, orient="horizontal", style="TSeparator")
        self.HorizonalSeparator.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew", padx=5)

        self.RadioCheck3 = ttk.Radiobutton(self.RadioCheckFrame, text="Custom:", variable=self.IsCustomMode, value=True)
        self.RadioCheck3.grid(row=3, column=0, padx=5, pady=(5,0), sticky="nsew")
        self.RadioCheck3.bind("<Button-1>", lambda event: self.ChangeTheme(self.IsDarkLightMode.get(), True))

        self.WipWarning = ttk.Label(self.RadioCheckFrame, text="( WIP )", font=("-size", 8, "-slant", ITALIC), justify="center")
        self.WipWarning.grid(row=4, column=0, padx=5, sticky="n")
        self.WipWarning.config(foreground=self.GetThemeColors("disabledfg", self.IsDarkLightMode.get()))

        self.ColorLabel1 = ttk.Label(self.ColorContainer1, text="Text Color:", font=("-size", 11))
        self.ColorLabel1.grid(row=0, column=0, sticky="w", padx=10)
        self.ColorLabel2 = ttk.Label(self.ColorContainer2, text="Primary:", font=("-size", 11))
        self.ColorLabel2.grid(row=1, column=0, sticky="w", padx=10)
        self.ColorLabel3 = ttk.Label(self.ColorContainer3, text="Secondary:", font=("-size", 11))
        self.ColorLabel3.grid(row=2, column=0, sticky="w", padx=10)
        self.ColorLabel4 = ttk.Label(self.ColorContainer4, text="disabledbg:", font=("-size", 11))
        self.ColorLabel4.grid(row=3, column=0, sticky="w", padx=10)
        self.ColorLabel5 = ttk.Label(self.ColorContainer5, text="selectfg:", font=("-size", 11))
        self.ColorLabel5.grid(row=4, column=0, sticky="w", padx=10)
        self.ColorLabel6 = ttk.Label(self.ColorContainer6, text="Accent:", font=("-size", 11))
        self.ColorLabel6.grid(row=5, column=0, sticky="w", padx=10)

        self.ColorDisplay1 = ttk.Label(self.ColorContainer1)
        self.ColorDisplay1.grid(row=0, column=2, padx=(40, 5), sticky="e")
        self.ColorDisplay2 = ttk.Label(self.ColorContainer2)
        self.ColorDisplay2.grid(row=1, column=2, padx=(40, 5), sticky="e")
        self.ColorDisplay3 = ttk.Label(self.ColorContainer3)
        self.ColorDisplay3.grid(row=2, column=2, padx=(40, 5), sticky="e")
        self.ColorDisplay4 = ttk.Label(self.ColorContainer4)
        self.ColorDisplay4.grid(row=3, column=2, padx=(40, 5), sticky="e")
        self.ColorDisplay5 = ttk.Label(self.ColorContainer5)
        self.ColorDisplay5.grid(row=4, column=2, padx=(40, 5), sticky="e")
        self.ColorDisplay6 = ttk.Label(self.ColorContainer6)
        self.ColorDisplay6.grid(row=5, column=2, padx=(40, 5), sticky="e")

        self.ColorInput1 = ttk.Entry(self.ColorContainer1, width=10)
        self.ColorInput1.grid(row=0, column=3, ipady=5, sticky="e", padx=15)
        self.ColorInput1.bind("<KeyRelease>", lambda event: [self.ValidateHexEntry(self.ColorInput1, event), self.SetCustomThemeColors(1)])
        self.ColorInput1.bind("<FocusIn>", lambda event: self.EntryPlaceholderFocIn(self.ColorInput1, self.GetThemeColors("fg", self.IsDarkLightMode.get())))
        self.ColorInput1.bind("<FocusOut>", lambda event: self.EntryPlaceholderFocOut(self.ColorInput1, self.GetThemeColors("fg", self.IsDarkLightMode.get())))

        self.ColorInput2 = ttk.Entry(self.ColorContainer2, width=10)
        self.ColorInput2.grid(row=1, column=3, ipady=5, sticky="e", padx=15)
        self.ColorInput2.bind("<KeyRelease>", lambda event: [self.ValidateHexEntry(self.ColorInput2, event), self.SetCustomThemeColors(2)])
        self.ColorInput2.bind("<FocusIn>", lambda event: self.EntryPlaceholderFocIn(self.ColorInput2, self.GetThemeColors("bg", self.IsDarkLightMode.get())))
        self.ColorInput2.bind("<FocusOut>", lambda event: self.EntryPlaceholderFocOut(self.ColorInput2, self.GetThemeColors("bg", self.IsDarkLightMode.get())))

        self.ColorInput3 = ttk.Entry(self.ColorContainer3, width=10)
        self.ColorInput3.grid(row=2, column=3, ipady=5, sticky="e", padx=15)
        self.ColorInput3.bind("<KeyRelease>", lambda event: [self.ValidateHexEntry(self.ColorInput3, event), self.SetCustomThemeColors(3)])
        self.ColorInput3.bind("<FocusIn>", lambda event: self.EntryPlaceholderFocIn(self.ColorInput3, self.GetThemeColors("disabledfg", self.IsDarkLightMode.get())))
        self.ColorInput3.bind("<FocusOut>", lambda event: self.EntryPlaceholderFocOut(self.ColorInput3, self.GetThemeColors("disabledfg", self.IsDarkLightMode.get())))

        self.ColorInput4 = ttk.Entry(self.ColorContainer4, width=10)
        self.ColorInput4.grid(row=3, column=3, ipady=5, sticky="e", padx=15)
        self.ColorInput4.bind("<KeyRelease>", lambda event: [self.ValidateHexEntry(self.ColorInput4, event), self.SetCustomThemeColors(4)])
        self.ColorInput4.bind("<FocusIn>", lambda event: self.EntryPlaceholderFocIn(self.ColorInput4, self.GetThemeColors("disabledbg", self.IsDarkLightMode.get())))
        self.ColorInput4.bind("<FocusOut>", lambda event: self.EntryPlaceholderFocOut(self.ColorInput4, self.GetThemeColors("disabledbg", self.IsDarkLightMode.get())))

        self.ColorInput5 = ttk.Entry(self.ColorContainer5, width=10)
        self.ColorInput5.grid(row=4, column=3, ipady=5, sticky="e", padx=15)
        self.ColorInput5.bind("<KeyRelease>", lambda event: [self.ValidateHexEntry(self.ColorInput5, event), self.SetCustomThemeColors(5)])
        self.ColorInput5.bind("<FocusIn>", lambda event: self.EntryPlaceholderFocIn(self.ColorInput5, self.GetThemeColors("selectfg", self.IsDarkLightMode.get())))
        self.ColorInput5.bind("<FocusOut>", lambda event: self.EntryPlaceholderFocOut(self.ColorInput5, self.GetThemeColors("selectfg", self.IsDarkLightMode.get())))

        self.ColorInput6 = ttk.Entry(self.ColorContainer6, width=10)
        self.ColorInput6.grid(row=5, column=3, ipady=5, sticky="e", padx=15)
        self.ColorInput6.bind("<KeyRelease>", lambda event: [self.ValidateHexEntry(self.ColorInput6, event), self.SetCustomThemeColors(6)])
        self.ColorInput6.bind("<FocusIn>", lambda event: self.EntryPlaceholderFocIn(self.ColorInput6, self.GetThemeColors("selectbg", self.IsDarkLightMode.get())))
        self.ColorInput6.bind("<FocusOut>", lambda event: self.EntryPlaceholderFocOut(self.ColorInput6, self.GetThemeColors("selectbg", self.IsDarkLightMode.get())))


        for i in range(3):
            self.ColorContainer1.grid_columnconfigure(i, weight=1)
            self.ColorContainer2.grid_columnconfigure(i, weight=1)
            self.ColorContainer3.grid_columnconfigure(i, weight=1)
            self.ColorContainer4.grid_columnconfigure(i, weight=1)
            self.ColorContainer5.grid_columnconfigure(i, weight=1)
            self.ColorContainer6.grid_columnconfigure(i, weight=1)

        # FUNCTION LOAD -----------------------------------------------------------------------------------------------------------------------------

        self.ChangeTheme(self.IsDarkLightMode.get(), self.IsCustomMode.get())

        self.UpdateColorDisplays(self.CustomThemeColors)

        self.CustomThemeColors = ast.literal_eval(self.InterpratSettings(2))

        self.UpdateFileIcons(self.CustomThemeColors['fg'])
        
        self.ConfigureRootGeometry()
        self.ChangeSelectedRecording()
        
        self.EntryPlaceholderFocOut(self.ColorInput1, self.GetThemeColors("fg", (self.IsDarkLightMode.get())))
        self.EntryPlaceholderFocOut(self.ColorInput2, self.GetThemeColors("bg", (self.IsDarkLightMode.get())))
        self.EntryPlaceholderFocOut(self.ColorInput3, self.GetThemeColors("disabledfg", self.IsDarkLightMode.get()))
        self.EntryPlaceholderFocOut(self.ColorInput4, self.GetThemeColors("disabledbg", self.IsDarkLightMode.get()))
        self.EntryPlaceholderFocOut(self.ColorInput5, self.GetThemeColors("selectfg", self.IsDarkLightMode.get()))
        self.EntryPlaceholderFocOut(self.ColorInput6, self.GetThemeColors("selectbg", self.IsDarkLightMode.get()))

    def ValidateHexEntry(self, Entry, Event):
        Placeholder = Entry.placeholder_text
        Value = Entry.get()
        Chars = "0123456789abcdef"

        if Value == Placeholder:
            return "break"

        if Event.keysym in ('BackSpace', 'Delete'):
            if Entry.get() == "":
                Entry.insert(0, "#")
                return None
            else:
                return None

        if not Value.startswith('#'):
            Entry.insert(0, '#')
            Value = Entry.get()

        if Event.char.lower() not in Chars:
            Entry.delete(len(Value)-1, 'end')
            return "break"

        CutValue = Value[:7]

        FormattedValue = '#' + CutValue[1:].lower()

        Entry.delete(0, 'end')
        Entry.insert(0, FormattedValue)
        return None

    def EntryPlaceholderFocIn(self, Entry, Placeholder):
        if Entry.get() == Placeholder:
            Entry.delete(0, "end")
            Entry.config(foreground=self.GetThemeColors("bg", self.IsDarkLightMode.get()))
            Entry.insert(0, '#')

    def EntryPlaceholderFocOut(self, Entry, Placeholder):
        if Entry.get() == "#" or Entry.get() == "":
            Entry.delete(0, "end")
            Entry.insert(0, Placeholder)
            Entry.config(foreground=self.GetThemeColors("disabledfg", self.IsDarkLightMode.get()))
            Entry.placeholder_text = Placeholder
        else:
            Entry.config(foreground=self.GetThemeColors("bg", self.IsDarkLightMode.get()))

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

        filename = f"Recording_{FileCount}.dat"
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

    def UpdateColorDisplays(self, Colors):

        for i, key in enumerate(Colors):
            HexColor = Colors[key]
            RgbaColor = tuple(int(HexColor[j:j+2], 16) for j in (1, 3, 5)) + (255,)

            BaseImage = Image.open(os.path.join(os.path.dirname(__file__), "ColorDisplayBase.png"))
            ShadowImage = Image.open(os.path.join(os.path.dirname(__file__), "ColorDisplayShadow.png"))

            BaseImage = BaseImage.convert("RGBA")
            ShadowImage = ShadowImage.convert("RGBA")
            ResultImage = Image.new("RGBA", BaseImage.size, (0, 0, 0, 0))

            BaseData = BaseImage.load()
            AlphaChannel = BaseImage.split()[3]

            ResultData = ResultImage.load()

            threshold = 200
            for y in range(BaseImage.height):
                for x in range(BaseImage.width):
                    r, g, b, a = BaseData[x, y]
                    if r > threshold and g > threshold and b > threshold:
                        ResultData[x, y] = RgbaColor
                    else:
                        ResultData[x, y] = (0, 0, 0, 255)

            for y in range(BaseImage.height):
                for x in range(BaseImage.width):
                    r, g, b, _ = ResultData[x, y]
                    alpha = AlphaChannel.getpixel((x, y))
                    ResultData[x, y] = (r, g, b, alpha)

            CombinedImage = Image.alpha_composite(ShadowImage, ResultImage)

            ImageTkResult = ImageTk.PhotoImage(CombinedImage)
            Display = getattr(self, f"ColorDisplay{i+1}")
            Display.config(image=ImageTkResult)
            Display.image = ImageTkResult

    def UpdateFileIcons(self, Color):
        Images = {
            self.DeleteFileButton: os.path.join(os.path.dirname(__file__), "DeleteFile.png"),
            self.CreateFileButton: os.path.join(os.path.dirname(__file__), "CreateFile.png")
        }

        if self.IsCustomMode.get() == True:
            HexColor = Color
        else:
            HexColor = self.GetThemeColors("bg", self.IsDarkLightMode.get())

        RgbaColor = tuple(int(HexColor[j:j+2], 16) for j in (1, 3, 5)) + (255,)

        for button, image_path in Images.items():
            BaseImage = Image.open(image_path).convert("RGBA")
            ResultImage = Image.new("RGBA", BaseImage.size, (0, 0, 0, 0))

            BaseData = BaseImage.load()
            AlphaChannel = BaseImage.split()[3]
            ResultData = ResultImage.load()

            threshold = 200
            for y in range(BaseImage.height):
                for x in range(BaseImage.width):
                    r, g, b, a = BaseData[x, y]
                    if r > threshold and g > threshold and b > threshold:
                        ResultData[x, y] = RgbaColor
                    else:
                        ResultData[x, y] = (0, 0, 0, 255)

            for y in range(BaseImage.height):
                for x in range(BaseImage.width):
                    r, g, b, _ = ResultData[x, y]
                    alpha = AlphaChannel.getpixel((x, y))
                    ResultData[x, y] = (r, g, b, alpha)

            ImageTkResult = ImageTk.PhotoImage(ResultImage)
            ImageTkResult = ImageTkResult._PhotoImage__photo.subsample(22)

            button.config(image=ImageTkResult)
            button.image = ImageTkResult

    def SetCustomThemeColors(self, index, *args):
        NormalColorOrder = ["fg", "bg", "disabledfg", "disabledbg", "selectfg", "selectbg"]

        if self.IsCustomMode.get() == True:

            self.Style.configure('.', 
                background=self.GetThemeColors('bg', not(self.IsDarkLightMode.get())), 
                foreground=self.GetThemeColors('fg', not(self.IsDarkLightMode.get())),
                troughcolor=self.GetThemeColors('bg', self.IsDarkLightMode.get()), 
                focuscolor=self.GetThemeColors('selectbg', self.IsDarkLightMode.get()), 
                selectbackground=self.GetThemeColors('selectbg', self.IsDarkLightMode.get()), 
                selectforeground=self.GetThemeColors('selectfg', self.IsDarkLightMode.get()), 
                insertcolor=self.GetThemeColors('fg', self.IsDarkLightMode.get()),  
                fieldbackground=self.GetThemeColors('selectbg', self.IsDarkLightMode.get()))

            root.tk_setPalette(
                background=self.GetThemeColors('bg', not(self.IsDarkLightMode.get())), 
                foreground=self.GetThemeColors('fg', not(self.IsDarkLightMode.get())), 
                highlightColor=self.GetThemeColors('selectbg', self.IsDarkLightMode.get()), 
                selectBackground=self.GetThemeColors('selectbg', self.IsDarkLightMode.get()), 
                selectForeground=self.GetThemeColors('selectfg', self.IsDarkLightMode.get()), 
                activeBackground=self.GetThemeColors('selectbg', self.IsDarkLightMode.get()), 
                activeForeground=self.GetThemeColors('selectfg', self.IsDarkLightMode.get()))

            if index == 0:
                try:
                    self.CustomThemeColors = ast.literal_eval(self.InterpratSettings(2))
                except (ValueError, SyntaxError) as e:
                    print(f"Error parsing settings: {e}")
                    self.CustomThemeColors = {
                        "fg": "",
                        "bg": "",
                        "disabledfg": "",
                        "disabledbg": "",
                        "selectfg": "",
                        "selectbg": ""
                    }
                for i in self.CustomThemeColors:
                    if self.CustomThemeColors[i] == "":
                        self.CustomThemeColors[i] = self.GetThemeColors(i, self.IsDarkLightMode.get())

                for i in range(6):
                    self.EntryPlaceholderFocIn(getattr(self, f"ColorInput{i+1}", None), self.CustomThemeColors[NormalColorOrder[i]])

                    Label = getattr(self, f"ColorInput{i+1}", None)
                    Label.delete(0, "end")
                    Label.insert(0, self.CustomThemeColors[NormalColorOrder[i]])
                    
                    self.EntryPlaceholderFocOut(getattr(self, f"ColorInput{i+1}", None), self.CustomThemeColors[NormalColorOrder[i]])

                    FilledThemeColors = ast.literal_eval(self.InterpratSettings(2))

                    if FilledThemeColors[NormalColorOrder[i]] == "":
                        getattr(self, f"ColorInput{i+1}", None).config(foreground=self.GetThemeColors("disabledfg", self.IsDarkLightMode.get()))

            else:
                Label = getattr(self, f"ColorInput{index}", None)
                LabelText = Label.get()

                if LabelText != "#":
                    if len(LabelText) == 7 or (len(LabelText) == 1 and all(c in "0123456789ABCDEFabcdef" for c in LabelText[1:])):
                        self.CustomThemeColors[NormalColorOrder[index-1]] = LabelText
                    else:
                        self.CustomThemeColors[NormalColorOrder[index-1]] = self.GetThemeColors(NormalColorOrder[index-1], self.IsDarkLightMode.get())

                    self.Style.configure('.', 
                        background=self.GetThemeColors('bg', not(self.IsDarkLightMode.get())), 
                        foreground=self.GetThemeColors('fg', not(self.IsDarkLightMode.get())),
                        troughcolor=self.GetThemeColors('bg', self.IsDarkLightMode.get()), 
                        focuscolor=self.GetThemeColors('selectbg', self.IsDarkLightMode.get()), 
                        selectbackground=self.GetThemeColors('selectbg', self.IsDarkLightMode.get()), 
                        selectforeground=self.GetThemeColors('selectfg', self.IsDarkLightMode.get()), 
                        insertcolor=self.GetThemeColors('fg', self.IsDarkLightMode.get()),  
                        fieldbackground=self.GetThemeColors('selectbg', self.IsDarkLightMode.get()))

                    root.tk_setPalette(
                        background=self.GetThemeColors('bg', not(self.IsDarkLightMode.get())), 
                        foreground=self.GetThemeColors('fg', not(self.IsDarkLightMode.get())), 
                        highlightColor=self.GetThemeColors('selectbg', self.IsDarkLightMode.get()), 
                        selectBackground=self.GetThemeColors('selectbackground', self.IsDarkLightMode.get()), 
                        selectForeground=self.GetThemeColors('selectforeground', self.IsDarkLightMode.get()), 
                        activeBackground=self.GetThemeColors('selectbackground', self.IsDarkLightMode.get()), 
                        activeForeground=self.GetThemeColors('selectforeground', self.IsDarkLightMode.get()))

                if len(LabelText) == 7 or (LabelText == "#" and all(c in "#0123456789ABCDEFabcdef" for c in LabelText[1:])):
                    if not self.ShouldRun:
                        for i in range(6):
                            EntryValue = getattr(self, f"ColorInput{i+1}", None).get()
                            DefaultColor = self.GetThemeColors(NormalColorOrder[i], self.IsDarkLightMode.get())

                            if EntryValue == DefaultColor or EntryValue == "#":
                                self.CustomThemeColors[NormalColorOrder[i]] = ""
                            else:
                                self.CustomThemeColors[NormalColorOrder[i]] = EntryValue

                        print(self.CustomThemeColors)


                        self.SaveSettings(2, self.CustomThemeColors)

                        for i in range(6):
                            if self.CustomThemeColors[NormalColorOrder[i]] == "":
                                self.CustomThemeColors[NormalColorOrder[i]] = self.GetThemeColors(NormalColorOrder[i], not(self.IsDarkLightMode.get()))
                        print(self.CustomThemeColors)

                        self.UpdateColorDisplays(self.CustomThemeColors)
                        self.UpdateFileIcons(self.CustomThemeColors['fg'])
                        
                        self.ShouldRun = True 
                else:
                    self.ShouldRun = False

    def GetThemeColors(self, Color, IsDark):
        colors = {
            "fg": ["#eeeeee", "#313131"],
            "bg": ["#313131", "#ffffff"],
            "disabledfg": ["#595959", "#595959"],
            "disabledbg": ["#ffffff", "#ffffff"],
            "selectfg": ["#ffffff", "#ffffff"],
            "selectbg": ["#217346", "#217346"]
        }

        return colors[Color][IsDark]
        
    def ChangeTheme(self, Mode, IsCustom, *args):
        self.IsDarkLightMode.set(Mode)
        self.SaveSettings(3, Mode)
        self.IsCustomMode.set(IsCustom)
        self.SaveSettings(4, IsCustom)

        if Mode:
            Mode = "dark"
        else:
            Mode = "light"

        self.Style = ttk.Style(self)
        ThemePath = os.path.join(os.path.dirname(__file__), "Theme", "Park", "Park.tcl")

        if IsCustom == False:
            self.RadioCheck1.config(variable=self.IsDarkLightMode, value=False)
            self.RadioCheck2.config(variable=self.IsDarkLightMode, value=True)

            Mode = Mode.lower()
            try:
                self.root.tk.call("source", ThemePath)
                self.root.tk.call("set_theme", Mode)
            except Exception as e:
                self.ReloadWindowScheduler()
        else:
            self.RadioCheck1.config(value=not(self.IsDarkLightMode.get()))
            self.RadioCheck2.config(value=not(self.IsDarkLightMode.get()))

            self.SetCustomThemeColors(0)
            self.ToggleCustomColorsOverlay()

        self.ConfigureRootGeometry()

    def ToggleCustomColorsOverlay(self):
        self.ColorContainerFrame = ttk.Frame(self.Container)
        self.ColorContainerFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        FrameWidth = self.ColorContainerFrame.winfo_width()
        FrameHeight = self.ColorContainerFrame.winfo_height()

        Width = FrameWidth + 20
        Height = FrameHeight + 20

        ScreenWidth = self.root.winfo_screenwidth()
        ScreenHeight = self.root.winfo_screenheight()

        X = (ScreenWidth // 2) - (Width // 2)
        Y = (ScreenHeight // 2) - (Height // 2)
        print(X, Y)

        overlay_box = tk.Frame(self, bg="black")
        overlay_box.place(x=X, y=Y, width=Width, height=Height)
        overlay_box.lower()
        

    def ReloadWindowScheduler(self, *args):
        if not self.ReloadPending:
            self.root.after(300, self.ReloadWindow)

    def ReloadWindow(self):
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