# TODO Provare a risolvere l'hardcoding dei selettori HTML: bassa priorità
# TODO Usare Pydantic per la validazione degli output della REST API
# TODO Utilizzare SQLAlchemy per migliorare la manutenibilità
# TODO Generare una barra di caricamento per il caricamento in PersistenceLogic
# TODO Caricare in batch le tuple nella tabella del PersistenceLogic anziché una per una
# TODO scraping delle pagine e libri max, oppure provare response.raise_for_status()


from fastapi import FastAPI, Depends
import uvicorn
from requests import Session
from PersistenceLogic.db_connector import get_db, Base, engine
from PersistenceLogic import CRUD, models

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Book API")

@app.get("/")
def homepage():
    return {"messaggio": "Welcome to Book API!"}

@app.get("/stats")
def get_stats(db:Session = Depends(get_db)):
    return CRUD.get_stats(db)

@app.get("/book/{upc}")
def get_book(upc: str, db:Session = Depends(get_db)):
    return CRUD.get_book(db, upc)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
