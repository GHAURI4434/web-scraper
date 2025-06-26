import requests
from bs4 import BeautifulSoup
import csv

URL = "https://quotes.toscrape.com"

def scrape_quotes(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")

        data = []

        for quote in quotes:
            text = quote.find("span", class_="text").get_text(strip=True)
            author = quote.find("small", class_="author").get_text(strip=True)
            tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]

            data.append([text, author, ", ".join(tags)])

        return data

    except Exception as e:
        print("❌ Error occurred:", e)
        return []

def save_to_csv(quotes):
    with open("quotes.csv", "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Quote", "Author", "Tags"])
        writer.writerows(quotes)

    print("✅ Quotes saved to quotes.csv")

def main():
    print("🕸️ Scraping quotes from:", URL)
    quotes = scrape_quotes(URL)

    if quotes:
        save_to_csv(quotes)

if __name__ == "__main__":
    main()
