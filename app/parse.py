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
    url = "https://quotes.toscrape.com/"
    text = requests.get(url).content
    soup = BeautifulSoup(text, "html.parser")
    with open(output_csv_path, "w", encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        for block in soup.find_all("div", class_="quote"):
            quote = Quote(
                text=block.find('span', class_="text").string,
                author=block.find('small', class_="author").string,
                tags=block.find_all('a', class_="tag")
            )
            writer.writerow(f"{quote.text} | {quote.author} | {[tag.string for tag in quote.tags]}")


if __name__ == "__main__":
    main("quotes.csv")
