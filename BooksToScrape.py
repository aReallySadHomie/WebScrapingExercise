import os.path
import csv
import threading
from tqdm import tqdm
from db_implementation import *
from new_directory.PageProcessor import process_page

# TODO scraping delle pagine e libri max, oppure provare response.raise_for_status()
# TODO passare da csv a PostgreSQL
MAXPAGES = 5
MAXBOOKS = MAXPAGES * 20
BOOKS_FILENAME = "books.csv"
MAX_THREADS = 10
csv.lock = threading.Lock()

# sistemare i parametri, impostare i default
def book_scraper():

    base_url = "http://books.toscrape.com/catalogue/"
    all_books = []
    seen_books = set()
    csv_header = ["Title", "Price(£)","Description", "Rating", "Availability", "UPC", "URL"]
    progress_bar_pages = tqdm(range(1, MAXPAGES+1), desc = "Scanned pages", position=0, leave=True)
    progress_bar_books = tqdm(range(1, MAXBOOKS+1), desc = "Scanned books",position=1 , leave=True)

    if not os.path.exists(BOOKS_FILENAME):
        with open(BOOKS_FILENAME, "w", newline="", encoding="UTF-8-sig") as csvfile:
            writer = csv.writer(csvfile, delimiter= ";")
            writer.writerow(csv_header)

    # TODO multithread in diverse pagine

    with open(BOOKS_FILENAME, "a", newline="", encoding="UTF-8-sig") as csvfile:
        writer = csv.writer(csvfile, delimiter=";", quotechar='"')

        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            executor.map(lambda page: process_page(page, base_url, writer, progress_bar_pages,
                                                   progress_bar_books, all_books, seen_books),
                         range(1, MAXPAGES+1))

    progress_bar_pages.close()
    progress_bar_books.close()
    print(f"Found {len(all_books)} books:\n")

    return all_books

if __name__== '__main__':
    detailed_book_list = book_scraper()
    input("Press enter to continue...")
    to_db(detailed_book_list)

    print("\n\n")
    input("Press enter to exit...")


#        progress_bar_books = tqdm(listed_books, desc = f"Now scraping elements from page {current_page}",position = 1, leave = False)
