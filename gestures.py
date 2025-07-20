import os
import time
# from pynput.keyboard import Key, Controller
# import time
# import keyboard;
# import pyautogui
# def gestures(command):
#     if (command=="swipe left"):
# keyboard.press('ctrl',)
# keyboard.press('left')
# keyboard.release('left')
# keyboard.release('ctrl')
# keyboard.send('ctrl+space') 
# keyboard.press_and_release('ctrl+left') # Simulate Ctrl+S (save)

# pyautogui.hotkey('ctrl', 'left')


# keyboard = Controller()

# # Give the system a moment to focus the correct window
# time.sleep(1)

# # Press and release Ctrl + Left
# with keyboard.pressed(Key.ctrl):
#     keyboard.press(Key.space)
#     keyboard.release(Key.space)

# os.system('osascript -e \'tell application "System Events" to key code 123 using control down\'')

def gesture(command):
    def swipe(direction):
        if direction == 'left' :
            key_code = 123 
        else:
            key_code = 124
        os.system(f"osascript -e 'tell application \"System Events\" to key code {key_code} using control down'")
        
    # Example usage:
    if "left" in command:
        print("swiping to left window")
        swipe('left')
        return "to left window";
    elif "right" in command:
        print("swiping to right window")
        swipe('right')
        return "to right window";
