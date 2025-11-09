# Import necessary libraries
import os
import time
import sys
import pandas as pd
import requests
import webbrowser
import subprocess

from bs4 import BeautifulSoup
from ddgs import DDGS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Setup output directories
output_dir = "ai_scraper_output"
screenshots_dir = os.path.join(output_dir, "screenshots")
os.makedirs(screenshots_dir, exist_ok=True)

# Prompt user for topic or get from input argument
topic = sys.argv[1] if len(sys.argv) > 1 else input("Enter the topic to search for: ")
preview_enabled = sys.argv[2].lower() == "preview" if len(sys.argv) > 2 else input("Preview pages? (yes/no): ").lower() == "yes"
try:
    return_results = int(sys.argv[3]) if len(sys.argv) > 3 else int(input("How many results should be returned? (default 2): ") or "2")
except ValueError:
    return_results = 2

# set timestamp for output files
timestamp = time.strftime("%Y%m%d-%H%M%S")

# Setup Chrome WebDriver
print("🧭 Setting up browser...")
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1920, 1080)

# Search DuckDuckGo
print(f"🔍 Searching DuckDuckGo for: {topic}")
print(f"🔢 Returning up to {return_results} result(s).")
if preview_enabled:
    duckduckgo_url = f"https://duckduckgo.com/?q={topic.replace(' ', '+')}"
    webbrowser.open(duckduckgo_url)

results = []
try:
    with DDGS() as ddgs:
        for r in ddgs.text(topic, max_results=return_results):
            result_url = r.get("href")
            if result_url:
                results.append(result_url)
except Exception as e:
    print(f"❌ Error during search: {e}")

# Process URLs
print("🌐 Processing URLs...")
data = []
count = 0
for url in results:
    if count >= return_results:
        break
    print(f"🔗 Processing: {url}")
    try:
        if preview_enabled :
            webbrowser.open(url)

        # get information about webpage
        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "No title"
        description = soup.find("meta", attrs={"name": "description"})
        desc_text = description["content"].strip() if description and "content" in description.attrs else "No description"

        driver.set_page_load_timeout(30)
        driver.get(url)
        time.sleep(2)
        screenshot_path = os.path.join(screenshots_dir, f"screenshot_{count+1}_{timestamp}.png")
        driver.save_screenshot(screenshot_path)

        data.append({
            "URL": url,
            "Description": desc_text,
            "Screenshot": screenshot_path,
            "Timestamp": timestamp
        })
        count += 1
        print(f"✅ Saved: {desc_text}")
    except Exception as e:
        print(f"⚠️ Error processing {url}: {e}")
# Kill the chrome driver
driver.quit()

# Save to Excel
print("📁 Saving results to Excel...")
excel_path = os.path.join(output_dir, "ai_scraper_results.xlsx")
df = pd.DataFrame(data)
# check if Excel file exists
if os.path.exists(excel_path):
    try:
        existing_df = pd.read_excel(excel_path, engine='openpyxl')
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.to_excel(excel_path, index=False)
    except Exception as e:
        print(f"⚠️ Failed to append to existing Excel file: {e}")
        df.to_excel(excel_path, index=False)
else:
    df.to_excel(excel_path, index=False)

print(f"\n✅ Workflow completed. Results saved to: {excel_path}")
print(f"🖼️ Screenshots saved in: {screenshots_dir}")
print("🚀 Opening output directory...")
try:
    subprocess.run(["xdg-open", os.path.abspath(output_dir)])
except Exception as e:
    print(f"⚠️ Failed to open Explorer: {e}")



print("✅ Process completed...")