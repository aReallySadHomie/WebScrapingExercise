from bs4 import BeautifulSoup
import requests
import csv
from DeepBookScraper import *

# TODO scraping delle pagine max, oppure provare while response.status_code == 200 o altri HTTP response status codes
MAXPAGES = 50

# sistemare i parametri, impostare i default
def book_scraper():

    base_url = "http://books.toscrape.com/catalogue/"
    start_url = "http://books.toscrape.com/catalogue/page-1.html"
    all_books = []

    current_page = 1
    while current_page <= MAXPAGES:
        print(f"scanning page {current_page}/{MAXPAGES}")
        url = f"{base_url}page-{current_page}.html"
        response = requests.get(url)
        #TODO try except usando il lxml anziché l'html.parser
        soup = BeautifulSoup(response.text, "html.parser")
        listed_books = soup.find_all("article", class_="product_pod")

        for book in listed_books:
            book_url_snippet = book.h3.a.get("href", "URL not found")
            book_url = base_url + book_url_snippet if book_url_snippet != "URL not found" else ""

            book_details = deep_book_scraper(book_url)
            all_books.append(book_details)



        current_page += 1

if __name__== '__main__':
    book_scraper()