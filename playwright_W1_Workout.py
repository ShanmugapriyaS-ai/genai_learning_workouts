from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime
import json
import pandas as pd
import sys

url = "https://www.socialeagle.in/"

try:
    with sync_playwright() as p:
        # ---------------- LAUNCH BROWSER ----------------
        browser = p.chromium.launch(headless=False)  # set True for headless
        page = browser.new_page()
        page.goto(url, timeout=60000)

        # ---------------- AUTO SCROLL ----------------
        page.evaluate("""
            async () => {
                for (let i = 0; i < 10; i++) {
                    window.scrollTo(0, document.body.scrollHeight);
                    await new Promise(resolve => setTimeout(resolve, 800));
                }
            }
        """)

        # ---------------- SCREENSHOT ----------------
        page.screenshot(path="socialeagle_playwright.png", full_page=True)

        # ---------------- PAGE SOURCE ----------------
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        # ---------------- METADATA ----------------
        title = soup.title.string.strip() if soup.title else "N/A"

        description = "N/A"
        desc = soup.find("meta", attrs={"name": "description"})
        if desc:
            description = desc.get("content", "N/A")

        og_tags = {}
        for tag in soup.find_all("meta"):
            if tag.get("property", "").startswith("og:"):
                og_tags[tag["property"]] = tag.get("content", "")

        # ---------------- CONTENT ----------------
        page_content = page.inner_text("body")

        browser.close()

        # ---------------- TIMESTAMP ----------------
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ---------------- SAVE TXT ----------------
        with open("socialeagle_playwright.txt", "w", encoding="utf-8") as f:
            f.write(f"Timestamp: {timestamp}\n\n")
            f.write(f"URL: {url}\n\n")
            f.write(f"Title: {title}\n")
            f.write(f"Description: {description}\n\n")
            f.write("OpenGraph Metadata:\n")
            for k, v in og_tags.items():
                f.write(f"{k}: {v}\n")
            f.write("\nCONTENT:\n")
            f.write(page_content)

        # ---------------- SAVE JSON ----------------
        json_data = {
            "timestamp": timestamp,
            "url": url,
            "title": title,
            "description": description,
            "og_tags": og_tags,
            "content": page_content
        }

        with open("socialeagle_playwright.json", "w", encoding="utf-8") as jf:
            json.dump(json_data, jf, indent=4)

        # ---------------- SAVE CSV ----------------
        df = pd.DataFrame([{
            "timestamp": timestamp,
            "url": url,
            "title": title,
            "description": description
        }])
        df.to_csv("socialeagle_playwright.csv", index=False)

        print("✅ Playwright scraping completed successfully")

except Exception as e:
    print("❌ Error occurred:")
    print(str(e))
    sys.exit(1)
