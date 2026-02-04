from sqlalchemy import Column, String, Numeric, Text

from PersistenceLogic.db_connector import Base

class BookModel(Base):
    __tablename__ = 'books'

    title = Column(Text, nullable=False)
    price = Column(Numeric(10, 2))
    description = Column(Text)
    rating = Column(Numeric)
    availability = Column(Numeric)
    upc = Column(String(16), primary_key=True)
    url = Column(Text, nullable=False)