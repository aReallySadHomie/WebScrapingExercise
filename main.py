# TODO Provare a risolvere l'hardcoding dei selettori HTML: bassa priorità
# TODO Separare la logica di scraping dalla visualizzazione dei progressi
# TODO Usare un context manager per la gestione delle connessioni al DB
# TODO Usare Pydantic per la validazione degli output della REST API
# TODO Utilizzare SQLAlchemy per migliorare la manutenibilità
# TODO Generare una barra di caricamento per il caricamento in DB
# TODO Caricare in batch le tuple nella tabella del DB anziché una per una
# TODO refactoring delle directory: creare directory per lo scraping, per il db e per la rest
# TODO scraping delle pagine e libri max, oppure provare response.raise_for_status()




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
            cursor.execute(
                "SELECT title, price, description, rating, availability, upc, url FROM public.books WHERE upc = %s",
                (upc,))
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
