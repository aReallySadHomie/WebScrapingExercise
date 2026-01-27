import os.path
import csv
from DeepBookScraper import *
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# TODO scraping delle pagine max, oppure provare while response.status_code == 200 o altri HTTP response status codes
# TODO passare da csv a PostgreSQL
MAXPAGES = 50
BOOKS_FILENAME = "books.csv"
MAX_THREADS = 10
# sistemare i parametri, impostare i default
def book_scraper():

    base_url = "http://books.toscrape.com/catalogue/"
    all_books = []

    csv_header = ["Title", "Price(£)","Description", "Rating", "Availability", "UPC", "URL"]
    if not os.path.exists(BOOKS_FILENAME):
        with open(BOOKS_FILENAME, "w", newline="", encoding="UTF-8-sig") as csvfile:
            writer = csv.writer(csvfile, delimiter= ";")
            writer.writerow(csv_header)

    progress_bar_pages = tqdm(range(1, MAXPAGES+1), desc = "Total progression", position=0)
    # TODO multithread in diverse pagine
    for current_page in progress_bar_pages:

        try:
            url = f"{base_url}page-{current_page}.html"
            response = requests.get(url, timeout=5)
        except Exception as e:
            print(f"Something is wrong with the HTTP request, go fix it... See you later\n{e}")
            break

        try:
            soup = BeautifulSoup(response.text, "lxml")
        except Exception as e:
            tqdm.write(f"Warning: lxml failed, using html.parser. Error: {e}")
            soup = BeautifulSoup(response.text, "html.parser")

        listed_books = soup.find_all("article", class_="product_pod")

        # Implementiamo sto multithreading
        books_urls = []
        for book in listed_books:
            book_url_snippet = book.h3.a.get("href", "URL not found")
            if book_url_snippet != "URL not found":
                book_url = base_url + book_url_snippet
            else:
                continue
            books_urls.append(book_url)

        with open(BOOKS_FILENAME, "a", newline="", encoding="UTF-8-sig") as csvfile:
            writer = csv.writer(csvfile, delimiter=";", quotechar='"')

            progress_bar_books = tqdm(listed_books, desc = f"Now scraping elements from page {current_page}",position = 1, leave = False)
            with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
                future_to_url = {executor.submit(deep_book_scraper, b_url): b_url for b_url in books_urls}

                for future in as_completed(future_to_url):
                    current_url = future_to_url[future]
                    try:
                        book_object = future.result()
                        if book_object:
                            writer.writerow([*book_object.to_list(), current_url])
                            all_books.append(book_object)
                    except Exception as e:
                        tqdm.write(f"Error scraping {current_url}: {e}")

                    progress_bar_books.update(1)


    print(f"Found {len(all_books)} books:\n")

    return all_books

if __name__== '__main__':
    detailed_book_list = book_scraper()
    for element in detailed_book_list:
        print(element)

    print("\n\n")
    input("Press enter to exit...")