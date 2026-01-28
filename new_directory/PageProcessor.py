import threading
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from new_directory.DeepBookScraper import deep_book_scraper


def process_page(current_page,
                 base_url,
                 writer,
                 progress_bar_pages,
                 progress_bar_books,
                 all_books,
                 seen_urls):

    url = f"{base_url}page-{current_page}.html"
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
                book_url = base_url + book_url_snippet
            else:
                continue

            with threading.Lock():
                if book_url in seen_urls:
                    progress_bar_books.update(1)
                    continue
                seen_urls.add(book_url)
            book_obj = deep_book_scraper(book_url)

            if book_obj:
                with threading.Lock():
                    writer.writerow(book_obj.to_list())
                all_books.append(book_obj)

            progress_bar_books.update(1)
        progress_bar_pages.update(1)

    except Exception as e:
        tqdm.write(f"Something is wrong with the HTTP request for page {url}\n{e}")