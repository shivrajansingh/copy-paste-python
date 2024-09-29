import pyperclip
import pyautogui
from pynput import keyboard
import time
import threading
import random


def on_press(key):
    global paused
    if key == keyboard.Key.esc:
        paused = True
    elif key == keyboard.Key.f2:
        if paused:
            paused = False
            threading.Thread(target=paste_text).start()
        elif not paused:
            threading.Thread(target=paste_text).start()

def paste_text():
    global index, paused, current_text
    text = pyperclip.paste()
    if text != current_text:
        current_text = text
        index = 0  # Reset index when new text is detected
    for i in range(index, len(text)):
        if paused:
            break
        pyautogui.press(text[i])
        time.sleep(random.uniform(0.01, 0.5))  # Adjust this delay as needed
        index += 1
    if index == len(text):
        print("All characters have been pasted.")
        index = 0  # Reset the index
        pyperclip.copy('')  # Clear the clipboard

def on_ctrl_d():
    print("CTRL+D detected. Exiting...")
    exit()

def on_ctrl_c():
    pass  # Do nothing when Ctrl+C is pressed

def on_esc():
    global paused
    paused = True

def on_f2():
    global paused
    if paused:
        paused = False
        threading.Thread(target=paste_text).start()
    elif not paused:
        threading.Thread(target=paste_text).start()

paused = False
index = 0
current_text = pyperclip.paste()  # Initialize with current clipboard content

# Start the key listener
with keyboard.GlobalHotKeys({
        '<ctrl>+c': on_ctrl_c,
        '<ctrl>+d': on_ctrl_d,
        '<esc>': on_esc,
        '<f2>': on_f2}) as h:
    h.join()
