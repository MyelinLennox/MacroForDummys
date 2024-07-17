import tkinter as tk

def button1_clicked():
    print("Button 1 clicked")

def button2_clicked():
    print("Button 2 clicked")

root = tk.Tk()
root.geometry("250x500")
root.resizable(False, False)

# Create a big header text
header_label = tk.Label(root, text="Header Text", font=("Arial", 24))
header_label.pack(pady=20)

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Create Button 1
button1 = tk.Button(button_frame, text="Button 1", width=10, command=button1_clicked)
button1.pack(side=tk.LEFT, padx=5)

# Create Button 2
button2 = tk.Button(button_frame, text="Button 2", width=10, command=button2_clicked)
button2.pack(side=tk.LEFT, padx=5)


# Create a frame for the advanced settings
settings_frame = tk.Frame(root)
settings_frame.pack()

# Create a checkbox for advanced settings
checkbox_var = tk.BooleanVar()
checkbox = tk.Checkbutton(settings_frame, text="Advanced Settings", variable=checkbox_var)
checkbox.pack()

root.mainloop()