import pyautogui
import pytesseract
import cv2
import numpy as np
import random
import time
import threading
import keyboard  # for detecting space bar to stop the script

# Configure Tesseract executable path if necessary
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Nicholas\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Set coordinates
text_region = (162, 322, 526 - 162, 367 - 322)

def capture_screenshot(region):
    screenshot = pyautogui.screenshot(region=region)
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def read_text_from_image(image):
    return pytesseract.image_to_string(image)

def is_desired_text(text):
    return "LEVEL OF ALL SPELL " in text

def random_left_click():
    # Click at the current mouse position
    pyautogui.click()

def stop_script():
    print("Press the Space bar to stop the script...")
    keyboard.wait('space')
    global running
    running = False

def check_shift_key():
    global running, paused
    while running:
        if not keyboard.is_pressed('shift'):
            if not paused:
                print("Shift key released. Pausing...")
                paused = True
        else:
            if paused:
                print("Shift key pressed. Resuming...")
                paused = False
        time.sleep(0.1)

# Main script
print("Setup complete. Press shift to start the script.")
keyboard.wait('shift')

running = True
paused = False

stop_thread = threading.Thread(target=stop_script)
stop_thread.start()

pause_thread = threading.Thread(target=check_shift_key)
pause_thread.start()

try:
    while running:
        if not paused:
            image = capture_screenshot(text_region)
            if image is None or image.size == 0:
                print("Failed to capture a valid screenshot. Exiting...")
                break

            text = read_text_from_image(image)
            print(f"Detected text: {text}")

            if is_desired_text(text):
                print("Desired skill found!")
                break

            random_left_click()
            time.sleep(random.uniform(0.05, 0.2))  # Random delay to mimic human behavior
        else:
            time.sleep(0.1)

    print("Script finished.")
except KeyboardInterrupt:
    print("Script stopped by user.")
