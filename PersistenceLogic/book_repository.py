from contextlib import contextmanager
import psycopg2
from dotenv import load_dotenv

from PersistenceLogic.db_connector import DatabaseConnector
from ScrapingLogic.book_class import Book

load_dotenv("config/.env")

class BookRepository(DatabaseConnector):
    def __init__(self):
        super().__init__()
        self._create_table()

    @contextmanager
    def _get_cursor(self):
        connection = self.connection_pool.getconn()
        try:
            with connection.cursor() as cursor:
                yield cursor
            connection.commit()
        except psycopg2.Error as e:
            connection.rollback()
            print("Errore DB: ",e)
            raise
        finally:
            connection.connection_pool.putconn(connection)


    def insert_book(self, book: Book):
        # perché l'SQL injection è una cosa brutta e non voglio avere in descrizione 'OR 1=1; DROP TABLE books;--
        query = """
                INSERT INTO books (title, price, description, rating, availability, upc, url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (upc) DO UPDATE SET title       = excluded.title,
                                                price       = EXCLUDED.price,
                                                description = EXCLUDED.description,
                                                rating      = EXCLUDED.rating,
                                                url         = EXCLUDED.url \
                """
        with self._get_cursor() as cursor:
            cursor.execute(query)

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
        with self._get_cursor() as cursor:
            cursor.execute(query)