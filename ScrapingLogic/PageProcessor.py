import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from ScrapingLogic.BookProcessor import process_book
from ScrapingLogic.book_class import Book
from config.config import BASE_URL


def process_page(url: str) -> set[Book] | None:

    analysed_books = set()
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        try:
            soup = BeautifulSoup(response.text, "lxml")
        except Exception as e:
            tqdm.write(f"Warning: lxml failed, using html.parser. Error: {e}")
            soup = BeautifulSoup(response.text, "html.parser")

        listed_books = soup.find_all("article", class_="product_pod")

        for book in listed_books:
            book_url_snippet = book.h3.a.get("href", "URL not found")
            if book_url_snippet != "URL not found":
                book_url = BASE_URL + book_url_snippet
            else:
                continue
            book_obj = process_book(book_url)
            if book_obj:
                analysed_books.add(book_obj)

        return analysed_books

    except Exception as e:
        tqdm.write(f"Something is wrong with the HTTP request for page {url}\n{e}")
