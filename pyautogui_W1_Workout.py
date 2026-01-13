import pyautogui
import pyperclip
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import webbrowser

# ---------------- CONFIG ----------------
url = "https://www.socialeagle.in/"
output_file = "socialeagle_data.txt"

# ---------------- STEP 1: FETCH METADATA ----------------
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Page title
meta_title = soup.title.string.strip() if soup.title else "N/A"

# Meta description
meta_description = "N/A"
desc_tag = soup.find("meta", attrs={"name": "description"})
if desc_tag and desc_tag.get("content"):
    meta_description = desc_tag["content"]

# Open Graph metadata
og_tags = {}
for tag in soup.find_all("meta"):
    if tag.get("property", "").startswith("og:"):
        og_tags[tag["property"]] = tag.get("content", "")

# ---------------- STEP 2: OPEN PAGE IN BROWSER ----------------
print("Opening browser...")
webbrowser.open(url)
time.sleep(6)  # wait for page to load fully

# ---------------- STEP 3: COPY VISIBLE PAGE CONTENT ----------------
print("Copying visible page content...")

pyautogui.hotkey("ctrl", "a")   # Select all visible content
time.sleep(1)
pyautogui.hotkey("ctrl", "c")   # Copy
time.sleep(1)

page_content = pyperclip.paste()

# ---------------- STEP 4: WRITE TO TEXT FILE ----------------
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(output_file, "w", encoding="utf-8") as file:
    file.write("SOCIALEAGLE PAGE DATA\n")
    file.write("=" * 60 + "\n")
    file.write(f"Timestamp: {timestamp}\n\n")

    file.write("URL:\n")
    file.write(url + "\n\n")

    file.write("METADATA:\n")
    file.write(f"Title: {meta_title}\n")
    file.write(f"Description: {meta_description}\n\n")

    file.write("OPEN GRAPH METADATA:\n")
    for key, value in og_tags.items():
        file.write(f"{key}: {value}\n")
    file.write("\n")

    file.write("VISIBLE PAGE CONTENT:\n")
    file.write(page_content)

# ---------------- STEP 5: POPUP ALERT ----------------
pyautogui.alert(
    text="Metadata and page content successfully saved to socialeagle_data.txt",
    title="Task Completed",
    button="OK"
)

print("Done!")