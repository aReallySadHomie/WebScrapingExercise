from sqlalchemy.orm import Session

from PersistenceLogic.models import BookModel
from ScrapingLogic.book_class import Book

def get_book(db : Session, upc : str):
    return db.query(BookModel).filter(BookModel.upc == upc).first()


def insert_book(db : Session, book : Book):
    book_datas = BookModel(
        title=book.title,
        price=book.price,
        description=book.description,
        rating=book.rating,
        upc=book.upc,
        url=book.url
    )
    db.merge(book_datas)
    db.commit()


def get_stats(db : Session):
    from sqlalchemy import func

    avg_price = db.query(func.avg(BookModel.price)).scalar()
    count = db.query(func.count(BookModel.upc)).scalar()
    return {"Average Price": avg_price, "Count": count}