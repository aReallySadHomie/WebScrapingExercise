from concurrent.futures import ThreadPoolExecutor
from ***REMOVED***ToScrape import MAX_THREADS
from psycopg2 import pool
from new_directory.DeepBookScraper import Book


class DatabaseManager:
    def __init__(self):
        self.parameters = {"host": "***REMOVED***",
                           "port": "***REMOVED***",
                           "database": "***REMOVED***",
                           "user": "***REMOVED***",
                           "password": "***REMOVED***"}

        self.connection_pool = pool.ThreadedConnectionPool(1, 10, **self.parameters)
        self._create_table()


    def insert_book(self, book: Book):
        connection = self.connection_pool.getconn()

        # perché l'SQL injection è una cosa brutta
        query = """
                INSERT INTO books (title, price, description, rating, availability, upc, url)
                VALUES (%s,%s,%s,%s,%s,%s,%s,)
                ON CONFLICT (upc) DO UPDATE SET
                    title = excluded.title,
                    price = EXCLUDED.price,
                    description = EXCLUDED.description,
                    rating = EXCLUDED.rating,
                    url = EXCLUDED.url
                """

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (book.to_list()))
                connection.commit()

        finally:
            self.connection_pool.putconn(connection)


    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS books (
        title TEXT NOT NULL,
        price NUMERIC(10, 2),
        description TEXT,
        rating NUMERIC,
        availability NUMERIC,
        upc VARCHAR(16) PRIMARY KEY,
        url TEXT);"""

        connection = self.connection_pool.getconn()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        finally:
            self.connection_pool.putconn(connection)




def to_db(book_list: list[Book]):
    db = DatabaseManager()
    print(f"Saving {len(book_list)} books into database...")
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(db.insert_book, book_list)