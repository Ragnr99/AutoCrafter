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

def capture_screenshot(region):
    screenshot = pyautogui.screenshot(region=region)
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def read_text_from_image(image):
    return pytesseract.image_to_string(image)

def is_desired_text(text):
    return "LEVEL OF ALL SPELL" in text

def random_click():


    x, y = pyautogui.position()
    pyautogui.click(x + random.uniform(-5, 5), y + random.uniform(-5, 5))

def get_coordinates():
    print("Move your mouse to the top left corner and press Enter.")
    while True:
        if keyboard.is_pressed('enter'):
            top_left = pyautogui.position()
            time.sleep(0.5)  # Adding a small delay to prevent multiple detections
            print(f"Top left corner at {top_left}")
            break
        time.sleep(0.1)

    print("Move your mouse to the bottom right corner and press Enter.")
    while True:
        if keyboard.is_pressed('enter'):
            bottom_right = pyautogui.position()
            time.sleep(0.5)  # Adding a small delay to prevent multiple detections
            print(f"Bottom right corner at {bottom_right}")
            break
        time.sleep(0.1)

    return top_left, bottom_right

def stop_script():
    print("Press the Space bar to stop the script...")
    keyboard.wait('space')
    global running
    running = False

# Main script
top_left, bottom_right = get_coordinates()
text_region = (top_left.x, top_left.y, bottom_right.x - top_left.x, bottom_right.y - top_left.y)

# Validate the region
if text_region[2] <= 0 or text_region[3] <= 0:
    print("Invalid region dimensions. Please ensure the bottom right corner is below and to the right of the top left corner.")
    exit()

print("Setup complete. Left-click to start the script.")
keyboard.wait('shift')

running = True
stop_thread = threading.Thread(target=stop_script)
stop_thread.start()

try:
    while running:
        image = capture_screenshot(text_region)
        if image is None or image.size == 0:
            print("Failed to capture a valid screenshot. Exiting...")
            break

        text = read_text_from_image(image)
        print(f"Detected text: {text}")

        if is_desired_text(text):
            print("Desired skill found!")
            break

        random_click()
        time.sleep(random.uniform(0.03, 0.1))  # Random delay to mimic human behavior



    print("Script finished.")
except KeyboardInterrupt:
    print("Script stopped by user.")
