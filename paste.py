import keyboard
import pyperclip
import time

# Global variable to track the F2 hook
f2_hook = None

# Function to handle character-by-character pasting
def paste_char_by_char(text):
    global f2_hook  # Use the global hook so we can unhook it later

    total_chars = len(text)
    current_char = 0

    def on_key_press(event):
        nonlocal current_char
        global f2_hook  # Declare f2_hook as global inside the inner function too

        if current_char < total_chars:
            # Paste the current character
            keyboard.write(text[current_char])
            current_char += 1
        else:
            print("All characters pasted!")
            if f2_hook:
                # Unhook the F2 key after pasting all characters
                keyboard.unhook(f2_hook)
                f2_hook = None  # Reset the hook variable

    # If there is an existing F2 hook, unhook it first
    if f2_hook is not None:
        keyboard.unhook(f2_hook)

    # Bind F2 to paste characters, and store the hook ID
    f2_hook = keyboard.on_press_key("f2", on_key_press, suppress=True)

    print("Press 'F2' to paste characters one by one.")

# Function to check clipboard content and handle it in a loop
def monitor_clipboard():
    previous_text = ""

    while True:
        # Get the current clipboard content
        current_text = pyperclip.paste()

        if current_text != "" and current_text != previous_text:
            # New text detected, print it and start pasting process
            print(f"New text copied: {current_text}")
            paste_char_by_char(current_text)

            # After pasting, clear the clipboard and reset the text
            pyperclip.copy("")
            previous_text = current_text
            print("Clipboard cleared. Waiting for new copied text...")

        # Sleep for a short while to avoid constant polling
        time.sleep(1)

if __name__ == "__main__":
    # Clear the clipboard initially
    pyperclip.copy("")

    print("Monitoring clipboard for new text...")
    monitor_clipboard()
