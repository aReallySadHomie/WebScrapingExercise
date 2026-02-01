from concurrent.futures import ThreadPoolExecutor

from PersistenceLogic.book_repository import BookRepository
from ScrapingLogic.book_class import Book
from config.config import MAX_THREADS


def to_db(book_set: set[Book]):
    repo = BookRepository()
    print(f"Saving {len(book_set)} books into database...")
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(repo.insert_book, book_set)