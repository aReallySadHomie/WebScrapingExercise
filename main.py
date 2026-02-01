# TODO Provare a risolvere l'hardcoding dei selettori HTML: bassa priorità
# TODO Usare Pydantic per la validazione degli output della REST API
# TODO Utilizzare SQLAlchemy per migliorare la manutenibilità
# TODO Generare una barra di caricamento per il caricamento in PersistenceLogic
# TODO Caricare in batch le tuple nella tabella del PersistenceLogic anziché una per una
# TODO scraping delle pagine e libri max, oppure provare response.raise_for_status()


from fastapi import FastAPI, HTTPException
import uvicorn

from PersistenceLogic.book_repository import BookRepository
app = FastAPI(title="Book API")
db = BookRepository()


@app.get("/")
def homepage():
    return {"messaggio": "Welcome to Book API!"}

@app.get("/stats")
def get_stats():
    return db.get_stats()

@app.get("/book/{upc}")
def get_book(upc: str):
    db.get_book(upc)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
