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
