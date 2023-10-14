import os
from selenium import webdriver
import json

# Pfade festlegen
input_folder = "C:\\Users\\nicoh\\Documents\\ScreenShotMaker\\input"
output_folder = "C:\\Users\\nicoh\\Documents\\ScreenShotMaker\\output"

os.makedirs(output_folder, exist_ok=True)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("high-dpi-support=1")
chrome_options.add_argument("force-device-scale-factor=1.0")
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

            if url is not None:
                screenshot_filename = os.path.join(output_folder, f"{title}.png")

                driver.get(url)

                driver.implicitly_wait(5)

                try:
                    accept_button = driver.find_element("xpath", "//button[contains(text(), 'Accept')]")
                    accept_button.click()
                except Exception as e:
                    print(f"Button nicht gefunden: {e}")


                driver.save_screenshot(screenshot_filename)

# Schließe den Webdriver
driver.quit()
