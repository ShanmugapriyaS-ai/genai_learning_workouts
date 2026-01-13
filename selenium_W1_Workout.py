from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import json
import pandas as pd

url = "https://www.socialeagle.in/"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)
driver.maximize_window()
time.sleep(5)

# ---------------- AUTO SCROLL ----------------
for _ in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

# ---------------- SCREENSHOT ----------------
driver.save_screenshot("socialeagle_selenium.png")

# ---------------- METADATA ----------------
soup = BeautifulSoup(driver.page_source, "html.parser")

title = soup.title.string if soup.title else "N/A"

description = "N/A"
desc = soup.find("meta", attrs={"name": "description"})
if desc:
    description = desc.get("content", "N/A")

og_tags = {}
for tag in soup.find_all("meta"):
    if tag.get("property", "").startswith("og:"):
        og_tags[tag["property"]] = tag.get("content", "")

# ---------------- CONTENT ----------------
page_text = driver.find_element(By.TAG_NAME, "body").text

driver.quit()

# ---------------- SAVE FILES ----------------
data = {
    "url": url,
    "title": title,
    "description": description,
    "og_tags": og_tags,
    "content": page_text
}

with open("socialeagle_selenium.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

pd.DataFrame([{
    "url": url,
    "title": title,
    "description": description
}]).to_csv("socialeagle_selenium.csv", index=False)

with open("socialeagle_selenium.txt", "w", encoding="utf-8") as f:
    f.write(page_text)

print("✅ Selenium scraping completed successfully")
