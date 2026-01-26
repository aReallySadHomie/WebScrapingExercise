from bs4 import BeautifulSoup
import requests
import csv
from DeepBookScraper import *
from tqdm import tqdm

# TODO scraping delle pagine max, oppure provare while response.status_code == 200 o altri HTTP response status codes
MAXPAGES = 3

# sistemare i parametri, impostare i default
def book_scraper():

    base_url = "http://books.toscrape.com/catalogue/"
    all_books = []

    for current_page in tqdm(range(1, MAXPAGES+1), desc = "Total progression", position=0):
        url = f"{base_url}page-{current_page}.html"
        response = requests.get(url, timeout=5)
        #TODO try except usando il lxml + l'html.parser
        soup = BeautifulSoup(response.text, "lxml")
        listed_books = soup.find_all("article", class_="product_pod")

        for book in tqdm(listed_books, desc = f"Now scraping elements from page {current_page}",position = 1, leave = False):
            book_url_snippet = book.h3.a.get("href", "URL not found")
            book_url = base_url + book_url_snippet if book_url_snippet != "URL not found" else ""

            book_objects = deep_book_scraper(book_url)
            all_books.append(book_objects)

    print(f"Found {len(all_books)} books:\n")

    return all_books

if __name__== '__main__':
    detailed_book_list = book_scraper()
    for element in detailed_book_list:
        print(element)

    print("\n\n")
    input("Press enter to exit...")