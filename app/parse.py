import csv
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


@dataclass
class Quote:
    text: str
    author: str
    tags: list[str]


def main(output_csv_path: str) -> None:
    with open(output_csv_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["TEXT", "AUTHOR", "TAG"])

        page = 1
        while True:
            url = f"https://quotes.toscrape.com/page/{page}/"
            text = requests.get(url).content
            soup = BeautifulSoup(text, "html.parser")

            quotes = soup.find_all("div", class_="quote")
            if not quotes:
                break

            try:
                for block in quotes:
                    quote = Quote(
                        text=block.find("span", class_="text").get_text(),
                        author=block.find("small", class_="author").get_text(),
                        tags=[tag.get_text() for tag in block.find_all("a", class_="tag")],
                    )
                    writer.writerow([
                        quote.text,
                        quote.author,
                        ", ".join(quote.tags)
                    ])
                page += 1
            except Exception:
                break


if __name__ == "__main__":
    main("quotes.csv")
