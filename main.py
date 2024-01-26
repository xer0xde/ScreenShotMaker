import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import json
import time

# Pfade festlegen
input_folder = "C:\\Users\\nicoh\\Documents\\ScreenShotMaker\\input"
output_folder = "C:\\Users\\nicoh\\Documents\\ScreenShotMaker\\output"
extension_path = "C:\\Pfad\\Zur\\Erweiterung" 

os.makedirs(output_folder, exist_ok=True)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-gpu")

# Füge die Erweiterung hinzu
chrome_options.add_argument(f"--load-extension={extension_path}")

driver = webdriver.Chrome(options=chrome_options)

for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        json_file = os.path.join(input_folder, filename)

        # Lade die JSON-Datei
        with open(json_file) as f:
            data = json.load(f)

        for item in data:
            title = item['title']
            url = item['website']
            screenshot = item.get('screenshot', True)

            if url is not None and screenshot:
                driver.get(url)

                try:
                    accept_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
                    accept_button.click()
                except Exception as e:
                    print(f"Button nicht gefunden: {e}")

                time.sleep(5)

                screenshot_filename = os.path.join(output_folder, f"{title}.png")

                driver.set_window_size(1920, 1080)  # 16:9-Aspektverhältnis
                driver.save_screenshot(screenshot_filename, 'png')

driver.quit()
