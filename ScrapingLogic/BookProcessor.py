from bs4 import BeautifulSoup
import requests

from ScrapingLogic.book_class import Book

# TODO process_book potrebbe essere un setter della classe book


def process_book(url) -> Book | None:

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        try:
            soup = BeautifulSoup(response.text, "lxml")
        except:
            soup = BeautifulSoup(response.text, "html.parser")

        article = soup.find("article", class_="product_page")
        if not article: return None

        # hardcoded, non ne vado fiero
        title = article.find("div", class_="col-sm-6 product_main").h1.get_text()
        price = article.find("p", class_="price_color").get_text()
        rating = article.find("p", class_="star-rating")["class"][1]
        description = article.find_all("p")[3].get_text()

        table = article.find("table", class_="table")
        rows = table.find_all("tr")
        upc = rows[0].td.text
        availability = rows[5].td.get_text()

        return Book(title=title,
                    price=price,
                    rating=rating,
                    availability=availability,
                    upc=upc,
                    description=description,
                    url=url)

    except Exception as e:
        return None