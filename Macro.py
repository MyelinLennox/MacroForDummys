import tkinter as tk
from tkinter import ttk
from tkinter import Canvas, Tk, ALL
from tkinter import Toplevel, Label, SOLID

import keyboard
import mouse
import time
import multiprocessing

# Define the key variables
record_key = 'f9'
activate_key = 'f10'

def record_macro():
    macro_data = []
    start_time = time.time()

    while True:
        if keyboard.is_pressed(record_key):
            print("Stopped recording macro.")
            while keyboard.is_pressed(record_key):  # Wait for the record key to be released
                pass
            break

        event_time = time.time() - start_time
        key_event = keyboard.read_event()

        # Skip if the key is the record or playback key
        if key_event.name in [record_key, activate_key]:
            continue

        event = {
            'type': 'keyboard',
            'event_time': event_time,
            'key': key_event.name,
            'event_type': key_event.event_type  # Record whether it's a key down or key up event
        }
        macro_data.append(event)
    
    # Save macro data to a file
    print("Saving macro data to file...")
    with open('macro_data.txt', 'w') as file:
        for event in macro_data:
            file.write(f"{event['type']},{event['event_time']},{event['key']},{event['event_type']}\n")

    print("Macro data saved successfully.")

def load_macro_data():
    macro_data = []

    with open('macro_data.txt', 'r') as file:
        for line in file:
            type, event_time, key, event_type = line.strip().split(',')
            event = {
                'type': type,
                'event_time': float(event_time),
                'key': key,
                'event_type': event_type
            }
            macro_data.append(event)

    return macro_data

def play_macro():
    # Load macro data from file
    macro_data = load_macro_data()

    sleep_time = 0  # Initialize sleep_time
    while not keyboard.is_pressed(activate_key):
        # Play the macro
        start_time = time.time()
        for event in macro_data:
            if sleep_time > 0:  # Ensure sleep time is non-negative
                time.sleep(sleep_time)

            elapsed_time = time.time() - start_time
            sleep_time = event['event_time'] - elapsed_time  # Shift sleep time to next iteration

            if event['type'] == 'keyboard':
                print(f"{event['event_type']} key: {event['key']}")
                if event['event_type'] == 'down':
                    keyboard.press(event['key'])
                else:
                    keyboard.release(event['key'])

def start_recording():
    record_process = multiprocessing.Process(target=record_macro)
    record_process.start()
    record_process.join()
    print("Recording finished.")

def start_playback():
    play_process = multiprocessing.Process(target=play_macro)
    play_process.start()
    while keyboard.is_pressed(activate_key):  # Wait for the activate key to be released
        pass
    time.sleep(0.1)  # Add a small delay to prevent the condition from being checked again immediately
    play_process.terminate()
    play_process.join()
    print("Playback stopped.")

# Create the GUI

tooltips = {}

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.id = None

    def show_tooltip(self):
        def _show_tooltip():
            x, y, _, _ = self.widget.bbox(self.widget.find_withtag("current")[0])
            x += self.widget.winfo_rootx() + 25
            y += self.widget.winfo_rooty() + self.widget.winfo_height() + 20
            self.tooltip = Toplevel(self.widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            label = Label(self.tooltip, text=self.text, bg="#ffffff", relief=SOLID, borderwidth=1)
            label.pack()

        self.id = self.widget.after(500, _show_tooltip)  # 500 ms delay

    def hide_tooltip(self):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

def create_rounded_button(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

def on_button_hover(event, button, color):
    canvas.itemconfig(button, fill=color)
    tooltips[button] = ToolTip(canvas, "Click to set the start/stop key")
    tooltips[button].show_tooltip()

def on_button_unhover(event, button, color):
    canvas.itemconfig(button, fill=color)
    if button in tooltips:
        tooltips[button].hide_tooltip()
        del tooltips[button]

def on_button_click(event, button, color):
    canvas.itemconfig(button, fill=color)
    text_items = canvas.find_withtag(f"text{button}")
    if text_items:  # Check if the tuple is not empty
        text_item = text_items[0]
        canvas.itemconfig(text_item, text="Press start/stop key", fill="#4c515d")

def on_button_release(event, button, color, set_key):
    canvas.itemconfig(button, fill=color)
    root.bind('<Key>', set_key)

def create_button_group(canvas, x, y, text, hotkey, radius=20, fill="#2b2f3b", text_fill="#ffffff", outline="#4c515d", padding=15):
    text_with_hotkey = f"{text} ({hotkey})"
    text_item = canvas.create_text(x, y, text=text_with_hotkey, fill=text_fill)
    bbox = canvas.bbox(text_item)
    canvas.delete(text_item)
    # Increase the padding around the text when creating the button
    button = create_rounded_button(canvas, bbox[0]-padding, bbox[1]-padding, bbox[2]+padding, bbox[3]+padding, radius, fill=fill, outline=outline)
    text_item = canvas.create_text(x, y, text=text_with_hotkey, fill=text_fill)
    return [button, text_item]

def start_recording(event=None):
    global record_key
    record_key = event.char.upper() if event else record_key
    button = record_button_group[0]
    text_items = canvas.find_withtag(f"text{button}")
    if text_items:  # Check if the tuple is not empty
        text_item = text_items[0]
        canvas.itemconfig(text_item, text=f"Start Recording\n{record_key}", fill="#ffffff")

def set_record_key(event):
    global record_key
    record_key = event.keysym
    text_item = record_button_group[1]  # Assuming the second item in the group is the text
    canvas.itemconfig(text_item, text=f"Start Recording ({record_key})", fill="#ffffff")
    print("Record key set to:", record_key)

def set_activate_key(event):
    global activate_key
    activate_key = event.keysym
    text_item = play_button_group[1]  # Assuming the second item in the group is the text
    canvas.itemconfig(text_item, text=f"Start Playback ({activate_key})", fill="#ffffff")
    print("Activate key set to:", activate_key)
    
root = Tk()
bg_color = "#232528"
canvas = Canvas(root, width=300, height=200, bd=0, highlightthickness=0, bg=bg_color)
canvas.pack()

root.title("Macro Recorder")
root.geometry("400x200")

root.configure(bg=bg_color)

# Set the background color
root.configure(bg="#232528")

record_button_group = create_button_group(canvas, 70, 100,  "Start Recording", record_key.upper())
for item in record_button_group:
    canvas.tag_bind(item, "<Enter>", lambda event: on_button_hover(event, record_button_group[0], "#3b3f4b"))
    canvas.tag_bind(item, "<Leave>", lambda event: on_button_unhover(event, record_button_group[0], "#2b2f3b"))
    canvas.tag_bind(item, "<Button-1>", lambda event: on_button_click(event, record_button_group[0], "#1b1f2b"))
    canvas.tag_bind(item, "<ButtonRelease-1>", lambda event, item=item: on_button_release(event, item, "#444654", set_record_key))

play_button_group = create_button_group(canvas, 230, 100, "Start Playback", activate_key.upper())
for item in play_button_group:
    canvas.tag_bind(item, "<Enter>", lambda event: on_button_hover(event, play_button_group[0], "#3b3f4b"))
    canvas.tag_bind(item, "<Leave>", lambda event: on_button_unhover(event, play_button_group[0], "#2b2f3b"))
    canvas.tag_bind(item, "<Button-1>", lambda event: on_button_click(event, play_button_group[0], "#1b1f2b"))
    canvas.tag_bind(item, "<ButtonRelease-1>", lambda event, item=item: on_button_release(event, item, "#444654", set_activate_key))
root.mainloop()