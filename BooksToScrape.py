import os.path
import csv
from DeepBookScraper import *
from tqdm import tqdm

# TODO scraping delle pagine max, oppure provare while response.status_code == 200 o altri HTTP response status codes
# TODO implementare il multithreading
# TODO passare da csv a PostgreSQL
MAXPAGES = 50
BOOKS_FILENAME = "books.csv"
# sistemare i parametri, impostare i default
def book_scraper():

    base_url = "http://books.toscrape.com/catalogue/"
    all_books = []

    csv_header = ["Title", "Price(£)","Description", "Rating", "Availability", "UPC", "URL"]
    if not os.path.exists(BOOKS_FILENAME):
        with open(BOOKS_FILENAME, "w", newline="", encoding="UTF-8-sig") as csvfile:
            writer = csv.writer(csvfile, delimiter= ";")
            writer.writerow(csv_header)

    for current_page in tqdm(range(1, MAXPAGES+1), desc = "Total progression", position=0):
        url = f"{base_url}page-{current_page}.html"
        response = requests.get(url, timeout=5)

        try:
            soup = BeautifulSoup(response.text, "lxml")
        except Exception as e:
            tqdm.write(f"Warning: lxml failed, using html.parser. Error: {e}")
            soup = BeautifulSoup(response.text, "html.parser")

        listed_books = soup.find_all("article", class_="product_pod")

        with open(BOOKS_FILENAME, "a", newline="", encoding="UTF-8-sig") as csvfile:
            writer = csv.writer(csvfile, delimiter=";", quotechar='"')

            for book in tqdm(listed_books, desc = f"Now scraping elements from page {current_page}",position = 1, leave = False):
                book_url_snippet = book.h3.a.get("href", "URL not found")
                book_url = base_url + book_url_snippet if book_url_snippet != "URL not found" else ""
                tqdm.write(f"Diving into: {book_url_snippet}")

                book_object = deep_book_scraper(book_url)
                if book_object:
                    writer.writerow([*book_object.to_list(), book_url])
                all_books.append(book_object)

    print(f"Found {len(all_books)} books:\n")

    return all_books

if __name__== '__main__':
    detailed_book_list = book_scraper()
    for element in detailed_book_list:
        print(element)

    print("\n\n")
    input("Press enter to exit...")