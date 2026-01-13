import pyautogui
import pyperclip
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import webbrowser
import json
import pandas as pd
import sys

url = "https://www.socialeagle.in/"

try:
    # ---------------- STEP 1: FETCH METADATA ----------------
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    meta_title = soup.title.string.strip() if soup.title else "N/A"

    meta_description = "N/A"
    desc = soup.find("meta", attrs={"name": "description"})
    if desc:
        meta_description = desc.get("content", "N/A")

    og_tags = {}
    for tag in soup.find_all("meta"):
        if tag.get("property", "").startswith("og:"):
            og_tags[tag["property"]] = tag.get("content", "")

    # ---------------- STEP 2: OPEN BROWSER ----------------
    webbrowser.open(url)
    time.sleep(6)

    # ---------------- STEP 3: AUTO-SCROLL PAGE ----------------
    for _ in range(10):
        pyautogui.scroll(-800)
        time.sleep(0.5)

    # ---------------- STEP 4: SCREENSHOT ----------------
    screenshot_name = "socialeagle_page.png"
    pyautogui.screenshot(screenshot_name)

    # ---------------- STEP 5: COPY CONTENT ----------------
    pyautogui.hotkey("ctrl", "a")
    time.sleep(1)
    pyautogui.hotkey("ctrl", "c")
    time.sleep(1)

    page_content = pyperclip.paste()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ---------------- STEP 6: SAVE TXT ----------------
    with open("socialeagle_data_pyautogui_w2.txt", "w", encoding="utf-8") as f:
        f.write(f"Timestamp: {timestamp}\n\n")
        f.write(f"URL: {url}\n\n")
        f.write(f"Title: {meta_title}\n")
        f.write(f"Description: {meta_description}\n\n")
        f.write("OpenGraph Metadata:\n")
        for k, v in og_tags.items():
            f.write(f"{k}: {v}\n")
        f.write("\nCONTENT:\n")
        f.write(page_content)

    # ---------------- STEP 7: SAVE JSON ----------------
    json_data = {
        "timestamp": timestamp,
        "url": url,
        "title": meta_title,
        "description": meta_description,
        "og_tags": og_tags,
        "content": page_content
    }

    with open("socialeagle_data_pyautogui.json", "w", encoding="utf-8") as jf:
        json.dump(json_data, jf, indent=4)

    # ---------------- STEP 8: SAVE CSV ----------------
    df = pd.DataFrame([{
        "timestamp": timestamp,
        "url": url,
        "title": meta_title,
        "description": meta_description
    }])

    df.to_csv("socialeagle_metadata_pyautogui.csv", index=False)

    # ---------------- SUCCESS POPUP ----------------
    pyautogui.alert(
        text="Scraping completed successfully!\nFiles saved:\nTXT | JSON | CSV | Screenshot",
        title="Task Completed",
        button="OK"
    )

except Exception as e:
    # ---------------- ERROR POPUP ----------------
    pyautogui.alert(
        text=f"Task Failed!\n\nError:\n{str(e)}",
        title="Error",
        button="OK"
    )
    sys.exit(1)
