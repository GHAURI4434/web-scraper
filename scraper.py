import requests
from bs4 import BeautifulSoup
import csv
import json
import os
from datetime import datetime

BASE_URL = "https://quotes.toscrape.com/page/{}/"
DATE_STR = datetime.now().strftime("%Y-%m-%d")
OUTPUT_DIR = "output"

def scrape_all_quotes():
    all_quotes = []
    page = 1

    while True:
        print(f"🔄 Scraping page {page}...")
        url = BASE_URL.format(page)
        response = requests.get(url)

        if response.status_code != 200:
            print("⚠️ No more pages or error occurred.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quote_blocks = soup.find_all("div", class_="quote")

        if not quote_blocks:
            break

        for quote in quote_blocks:
            text = quote.find("span", class_="text").get_text(strip=True)
            author = quote.find("small", class_="author").get_text(strip=True)
            tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]

            all_quotes.append({
                "quote": text,
                "author": author,
                "tags": tags
            })

        page += 1

    return all_quotes

def save_as_csv(quotes):
    filename = os.path.join(OUTPUT_DIR, f"quotes_{DATE_STR}.csv")
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Quote", "Author", "Tags"])
        for q in quotes:
            writer.writerow([q["quote"], q["author"], ", ".join(q["tags"])])
    print(f"✅ Saved to {filename}")

def save_as_json(quotes):
    filename = os.path.join(OUTPUT_DIR, f"quotes_{DATE_STR}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(quotes, f, indent=4, ensure_ascii=False)
    print(f"✅ Saved to {filename}")

def main():
    print("🕸️ Advanced Web Scraper — Quotes to Scrape\n")

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    quotes = scrape_all_quotes()

    if not quotes:
        print("❌ No quotes found.")
        return

    print(f"\n📊 {len(quotes)} quotes scraped.\n")

    format_choice = input("💾 Save as CSV or JSON? (csv/json): ").strip().lower()

    if format_choice == "json":
        save_as_json(quotes)
    else:
        save_as_csv(quotes)

if __name__ == "__main__":
    main()
