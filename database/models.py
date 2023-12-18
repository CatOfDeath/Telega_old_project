from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String, Date, DateTime
from sqlalchemy.orm import  declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy_utils import create_database, database_exists


Base = declarative_base()
metadata = MetaData()
class Books(Base):
    __tablename__ = 'books'
 
    book_id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    author = Column(String(200), nullable=False)
    published = Column(Integer, nullable=False)
    date_added = Column(Date, nullable=False)
    date_deleted = Column(Date)
 
class Borrows(Base):
    __tablename__ = 'borrows'
 
    borrows_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime)
    user_id = Column(Integer, nullable=False)
 
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/bot_base")
if database_exists("postgresql+psycopg2://postgres:postgres@localhost:5432/bot_base") == False:
    create_database("postgresql+psycopg2://postgres:postgres@localhost:5432/bot_base")
Base.metadata.create_all(engine)

