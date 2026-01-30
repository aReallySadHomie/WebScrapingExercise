import os.path
import csv
import threading
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from new_directory.db_implementation import to_db
from new_directory.PageProcessor import process_page
from config import MAXPAGES, MAXBOOKS, BOOKS_FILENAME, MAX_THREADS


def book_scraper():
    shared_lock = threading.Lock()
    base_url = "http://books.toscrape.com/catalogue/"
    all_books = []
    seen_books = set()
    csv_header = ["Title", "Price(£)", "Description", "Rating", "Availability", "UPC", "URL"]
    progress_bar_pages = tqdm(range(1, MAXPAGES + 1), desc="Scanned pages", position=0, leave=True)
    progress_bar_books = tqdm(range(1, MAXBOOKS + 1), desc="Scanned books", position=1, leave=True)

    if not os.path.exists(BOOKS_FILENAME):
        with open(BOOKS_FILENAME, "w", newline="", encoding="UTF-8-sig") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow(csv_header)

    with open(BOOKS_FILENAME, "a", newline="", encoding="UTF-8-sig") as csvfile:
        writer = csv.writer(csvfile, delimiter=";", quotechar='"')

        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            # Ricordati che executor.map() accetta solamente una funzione con un solo argomento (che arriva dall'iterabile)
            executor.map(lambda page: process_page(page, base_url, writer, progress_bar_pages,
                                                   progress_bar_books, all_books, seen_books, shared_lock),
                         range(1, MAXPAGES + 1))

    progress_bar_pages.close()
    progress_bar_books.close()
    print(f"Found {len(all_books)} books:\n")

    return all_books


if __name__ == '__main__':
    detailed_book_list = book_scraper()
    input("Press enter to continue...")
    to_db(detailed_book_list)

    print("\n\n")
    input("Press enter to exit...")
