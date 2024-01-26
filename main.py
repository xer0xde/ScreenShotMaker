import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import time
import concurrent.futures
import logging
from datetime import datetime

input_folder = "C:\\Users\\nicoh\\Documents\\ScreenShotMaker\\input"
output_folder = "C:\\Users\\nicoh\\Documents\\ScreenShotMaker\\output"
extension_path = "C:\\Pfad\\Zur\\Erweiterung"  an

os.makedirs(output_folder, exist_ok=True)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument(f"--load-extension={extension_path}")

# Setup logging
logging.basicConfig(filename='logs.json', level=logging.INFO)

def capture_screenshot(title, url, screenshot_filename, unique_id):
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        time.sleep(5)

        driver.set_window_size(1920, 1080)

        driver.save_screenshot(screenshot_filename, 'png')

        # Log screenshot information
        log_data = {
            'Image_ID': unique_id,
            'Website_Name': title,
            'Timestamp': str(datetime.now())
        }
        logging.info(json.dumps(log_data))

    finally:
        driver.quit()

with concurrent.futures.ThreadPoolExecutor() as executor:
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            json_file = os.path.join(input_folder, filename)

            with open(json_file) as f:
                data = json.load(f)

            futures = []

            for idx, item in enumerate(data, start=1):
                title = item['title']
                url = item['website']
                screenshot = item.get('screenshot', True)

                if url is not None and screenshot:
                    unique_id = f"{idx}_{title.replace(' ', '_')}"
                    screenshot_filename = os.path.join(output_folder, f"{unique_id}.png")

                    future = executor.submit(capture_screenshot, title, url, screenshot_filename, unique_id)
                    futures.append(future)

            concurrent.futures.wait(futures)
