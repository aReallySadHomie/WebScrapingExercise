import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

from PersistenceLogic.save_to_db import to_db
from ScrapingLogic.PageProcessor import process_page
from config.config import MAXPAGES, MAX_THREADS, BASE_URL, SAVE_TO_CSV
from PersistenceLogic.csv_implementation import to_csv, generate_csv


def start_scraping(urls):

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:

        futures = [executor.submit(process_page, page) for page in urls]
        for future in as_completed(futures):
            yield future.result()

# recupero delle pagine esistenti
def discover_pages(url = BASE_URL)-> list | None:

    with tqdm(range(1, MAXPAGES+1), desc="Analysing pages", unit="pages") as pbar:

        def try_url(i):
            trying_url = f"{url}page-{i}.html"
            try:
                response = requests.head(trying_url, timeout=5)
                response.raise_for_status()
                return trying_url
            except requests.exceptions.RequestException:
                return None
            finally:
                pbar.update(1)

        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            results = list(executor.map(try_url, range(1, MAXPAGES + 1)))

    valid_urls = [url for url in results if url is not None]
    return valid_urls


if __name__ == '__main__':
    all_books = set()
    all_pages = discover_pages()
    scraped = start_scraping(all_pages)

    if SAVE_TO_CSV:
        generate_csv()

    for data in tqdm(scraped, total=len(all_pages), desc="Scraping from pages"):
        if data:
            if SAVE_TO_CSV:
                for d in data:
                    to_csv(d.to_list())
            all_books.update(data)


    print(f"Found {len(all_books)} books:\n")
    input("Press enter to continue...")

    to_db(all_books)

    print("\n\n")
    input("Press enter to exit...")