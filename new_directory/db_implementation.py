from concurrent.futures import ThreadPoolExecutor
import psycopg2
from BooksToScrape import MAX_THREADS
from psycopg2 import pool
from new_directory.DeepBookScraper import Book
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.parameters = {"host": os.getenv("DB_HOST"),
                           "port": os.getenv("DB_PORT"),
                           "database": os.getenv("DB_NAME"),
                           "user": os.getenv("db_USER"),
                           "password": os.getenv("db_PASSWORD")}

        if not all(self.parameters.values()):
            raise EnvironmentError("Please set environment variables in .env file")

        self.connection_pool = pool.ThreadedConnectionPool(1, 10, **self.parameters)
        self._create_table()

    def insert_book(self, book: Book):

        # TODO generare una barra di caricamento
        connection = self.connection_pool.getconn()

        # perché l'SQL injection è una cosa brutta e non voglio avere in descrizione 'OR 1=1; DROP TABLE books;--
        query = """
                INSERT INTO books (title, price, description, rating, availability, upc, url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (upc) DO UPDATE SET title       = excluded.title,
                                                price       = EXCLUDED.price,
                                                description = EXCLUDED.description,
                                                rating      = EXCLUDED.rating,
                                                url         = EXCLUDED.url
                """

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (book.to_list()))
                connection.commit()
        except psycopg2.Error as e:
            connection.rollback()
            print(e)

        finally:
            self.connection_pool.putconn(connection)

    def _create_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS books
                (
                    title        TEXT NOT NULL,
                    price        NUMERIC(10, 2),
                    description  TEXT,
                    rating       NUMERIC,
                    availability NUMERIC,
                    upc          VARCHAR(16) PRIMARY KEY,
                    url          TEXT
                );"""

        connection = self.connection_pool.getconn()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        except psycopg2.Error as e:
            connection.rollback()
            print(e)
        finally:
            self.connection_pool.putconn(connection)


def to_db(book_list: list[Book]):
    db = DatabaseManager()
    print(f"Saving {len(book_list)} books into database...")
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(db.insert_book, book_list)
