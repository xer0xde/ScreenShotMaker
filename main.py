import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import json
import time
import concurrent.futures

input_folder = "C:\\Users\\nicoh\\Documents\\ScreenShotMaker\\input"
output_folder = "C:\\Users\\nicoh\\Documents\\ScreenShotMaker\\output"
extension_path = "C:\\Pfad\\Zur\\Erweiterung"  # Passe dies an den tatsächlichen Pfad an

os.makedirs(output_folder, exist_ok=True)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-gpu")

chrome_options.add_argument(f"--load-extension={extension_path}")

def capture_screenshot(title, url, screenshot_filename):
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        time.sleep(5)

        try:
            accept_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
            accept_button.click()
        except Exception as e:
            print(f"Button nicht gefunden: {e}")

        driver.set_window_size(1920, 1080)

        driver.save_screenshot(screenshot_filename, 'png')
    finally:
        driver.quit()

with concurrent.futures.ThreadPoolExecutor() as executor:
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            json_file = os.path.join(input_folder, filename)

            with open(json_file) as f:
                data = json.load(f)

            futures = []

            for item in data:
                title = item['title']
                url = item['website']
                screenshot = item.get('screenshot', True)

                if url is not None and screenshot:
                    screenshot_filename = os.path.join(output_folder, f"{title}.png")

                    future = executor.submit(capture_screenshot, title, url, screenshot_filename)
                    futures.append(future)

            concurrent.futures.wait(futures)
