import time
import keyboard

def test_record_macro():
    # Test case 1: Record a simple macro with a single key press
    keyboard.read_event = lambda: keyboard.KeyboardEvent('down', 'A')
    keyboard.is_pressed = lambda key: key == 'Q'
    record_macro()
    # Assert that the macro data is saved correctly
    with open('macro_data.txt', 'r') as file:
        assert file.read() == 'keyboard,0.0,A,down\n'

    # Test case 2: Record a macro with multiple key presses
    keyboard.read_event = lambda: keyboard.KeyboardEvent('down', 'A')
    keyboard.is_pressed = lambda key: key == 'Q'
    record_macro()
    # Assert that the macro data is saved correctly
    with open('macro_data.txt', 'r') as file:
        assert file.read() == 'keyboard,0.0,A,down\nkeyboard,0.0,A,down\n'

    # Test case 3: Record a macro with record key pressed multiple times
    keyboard.read_event = lambda: keyboard.KeyboardEvent('down', 'A')
    keyboard.is_pressed = lambda key: key == 'Q' or key == 'R'
    record_macro()
    # Assert that the macro data is saved correctly
    with open('macro_data.txt', 'r') as file:
        assert file.read() == 'keyboard,0.0,A,down\n'

    print("All test cases passed.")

test_record_macro()