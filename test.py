from PIL import ImageGrab
from screeninfo import get_monitors
import pyautogui

def screenshot_second_monitor():
    # Get monitor information
    monitors = get_monitors()
    print(monitors)
    if len(monitors) < 2:
        print("Second monitor not found!")
        return
    
    # Get the second monitor's position and size
    second_monitor = monitors[2]
    x = second_monitor.x
    y = second_monitor.y
    width = second_monitor.width
    height = second_monitor.height

    # Capture the second monitor's screen area
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    
    # Save the screenshot
    screenshot.save("screenshot_second_monitor.png")

screenshot_second_monitor()
