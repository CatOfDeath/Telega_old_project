from sqlalchemy import create_engine
from .models import Books, Borrows
from sqlalchemy.orm import sessionmaker
import datetime
import psycopg2


 
 
# engine = create_engine("postgresql+psycopg2://yeseniaw:@localhost:5433/")
# connection = engine.connect()
# Session = sessionmaker(engine)
# session = Session()


class DatabaseConnector:
    def __init__(self, url_base):
        self.url_base = url_base
    
    def get_connection(self):
        engine = create_engine(self.url_base)
        Session = sessionmaker(bind=engine)
        return Session()

    def get_add(self,data):
        session = self.get_connection()
        data["date_added"] = datetime.date.today()
        store = Books(title = data['title'], author = data['author'],
        published = data['published'], date_added = data['date_added'])
        try:
            session.add(store)
            session.commit()
        except:
            
            raise psycopg2.errors.UndefinedTable
        return {'book_id': store.book_id}

 
 
    def get_delete(self, book_id):
        session = self.get_connection()
        book = session.query(Books).filter(Books.book_id == book_id).first()
        if book and not book.date_deleted and not self.get_borrow(book_id=book_id):
            book.date_deleted = datetime.date.today()
            session.commit()
            return True
        return False
    
    def list_book(self):
        session = self.get_connection()
        cs = session.query(Books).all()
        divv = []
        for i in cs:
            loc_div = []
            loc_div.append(i.title)
            loc_div.append(i.author)
            loc_div.append(str(i.published))
            if i.date_deleted is not None:
                loc_div.append("(удалена)")
            divv.append(", ".join(loc_div)+";")
        return divv
    
    def get_book(self, dic):
        session = self.get_connection()
        cs = session.query(Books).where(Books.title == dic["title"]).where(Books.author == dic["author"]).where(Books.published == dic["published"]).first()
        if cs:
            return cs.book_id
    
    
    def borrow(self, users_id, books_id):
        session = self.get_connection()
        if not self.get_borrow(book_id=books_id, user_id=users_id) and (session.query(Books).filter(Books.book_id == books_id).first()).date_deleted is None:
            new_borrow = Borrows(book_id=books_id, user_id=users_id, date_start=datetime.datetime.now())
            session.add(new_borrow)
            session.commit()
            return new_borrow.borrows_id
        return False

    def get_borrow(self, user_id =None, book_id =None):
        session = self.get_connection()
        query = session.query(Borrows)
        if book_id and user_id:
            query = query.filter(Borrows.book_id == book_id, Borrows.user_id == user_id, Borrows.date_end == None)
        elif book_id:
            query = query.filter(Borrows.book_id == book_id, Borrows.date_end == None)
        elif user_id:
            query = query.filter(Borrows.user_id == user_id, Borrows.date_end == None)

        borrow = query.first()
        return borrow.borrows_id if borrow else None

    
    def retrieve(self, users_id):
        session = self.get_connection()
        ans = []
        users = session.query(Borrows).filter(Borrows.user_id == users_id, Borrows.date_end == None).first()
        if users is not None:
            books = session.query(Books).where(Books.book_id == users.book_id).first()
            users.date_end = datetime.datetime.now()
            session.commit()
            ans = []
            ans.append(books.title)
            ans.append(books.author)
            ans.append(str(books.published))
        else: pass
        return ans

