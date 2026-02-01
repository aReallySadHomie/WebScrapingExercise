from contextlib import contextmanager
import psycopg2
from dotenv import load_dotenv
from fastapi import HTTPException

from PersistenceLogic.db_connector import DatabaseConnector
from ScrapingLogic.book_class import Book

load_dotenv("config/.env")

class BookRepository(DatabaseConnector):
    def __init__(self):
        super().__init__()
        self._create_table()

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
            self.connection_pool.putconn(connection)

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
            cursor.execute(query, book.to_list())

    def get_stats(self):
        query = """
                SELECT ROUND(AVG(price), 2) FROM public.books;
                SELECT COUNT(*) FROM public.books
                """
        with self._get_cursor() as cursor:
            cursor.execute(query)
            avg_price, count = cursor.fetchone()
        return {"Number of books": count,
                "Average price": float(avg_price) if avg_price else 0}

    def get_book(self, upc: str):
        query = """
                SELECT title, price, description, rating, availability, upc, url
                FROM public.books WHERE upc = %s
                """
        with self._get_cursor() as cursor:
            cursor.execute(query, (upc,))
            book = cursor.fetchone()
            if book:
                return {
                    "title": book[0],
                    "price": book[1],
                    "description": book[2],
                    "rating": book[3],
                    "availability": book[4],
                    "upc": book[5],
                    "url": book[6],
                }

            raise HTTPException(status_code=404, detail="Book not found")