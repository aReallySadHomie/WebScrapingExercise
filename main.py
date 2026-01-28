from fastapi import FastAPI, HTTPException
from new_directory.db_implementation import DatabaseManager
import uvicorn

app = FastAPI(title="Book API")
db = DatabaseManager()

@app.get("/")
def homepage():
    return {"messaggio": "Welcome to Book API!"}

@app.get("/stats")
def get_stats():
    connection = db.connection_pool.getconn()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT ROUND(AVG(price), 2) FROM public.books")
            avg_price = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM public.books")
            count_books = cursor.fetchone()[0]
        return {
            "number_of_books": count_books,
            "avg_price": avg_price,
        }
    finally:
        db.connection_pool.putconn(connection)


@app.get("/book/{upc}")
def get_book(upc: str):
    connection = db.connection_pool.getconn()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT title, price, description, rating, availability, upc, url FROM public.books WHERE upc = %s", (upc,))
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
    finally:
        db.connection_pool.putconn(connection)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)