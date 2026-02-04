from sqlalchemy.dialects.postgresql import insert as postgresinsert
from sqlalchemy.dialects.sqlite import insert as sqliteinsert

from PersistenceLogic.db_connector import SessionLocal, engine, Base
from PersistenceLogic.models import BookModel
from ScrapingLogic.book_class import Book


def to_db(book_list : set[Book]):

    #Creazione della tabella book tramite l'oggetto Base
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        data = [b.to_dict() for b in book_list]
        statement = postgresinsert(BookModel).values(data)

        update_cols = {
            "title" : statement.excluded.title,
            "price" : statement.excluded.price,
            "description" : statement.excluded.description,
            "rating" : statement.excluded.rating,
            "availability" : statement.excluded.availability,
            "url" : statement.excluded.url,
        }
        update_statement = statement.on_conflict_do_update(
            index_elements=["upc"],
            set_=update_cols
        )

        db.execute(update_statement)
        db.commit()

    except Exception as error:
        db.rollback()
        print(error)
    finally:
        db.close()