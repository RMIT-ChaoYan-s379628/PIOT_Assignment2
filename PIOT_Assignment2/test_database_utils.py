# Reference: https://docs.python.org/2/library/unittest.html
import unittest
# import MySQLdb
import pymysql
from database_utils import DatabaseUtils

class TestDatabaseUtils(unittest.TestCase):
    HOST = "127.0.0.1"
    USER = "root"
    PASSWORD = "65390057y"
    DATABASE = "test"

    def setUp(self):
        self.connection = pymysql.connect(TestDatabaseUtils.HOST, TestDatabaseUtils.USER,
            TestDatabaseUtils.PASSWORD, TestDatabaseUtils.DATABASE)
        
        with self.connection.cursor() as cursor:
            cursor.execute("drop table if exists Book")
            cursor.execute("""
                create table if not exists Book (
                    BookID int not null auto_increment,
                    Title text not null,
                    Author text not null,
                    PublishedDate date not null,
                    constraint PK_Book primary key (BookID)
                )""")
            cursor.execute("insert into Book (Title,Author,PublishedDate) values ('book1','author1','2010-10-10')")
            cursor.execute("insert into Book (Title,Author,PublishedDate) values ('book2','author2','2010-10-10')")
            cursor.execute("insert into Book (Title,Author,PublishedDate) values ('book3','author3','2010-10-10')")
        self.connection.commit()

    def tearDown(self):
        try:
            self.connection.close()
        except:
            pass
        finally:
            self.connection = None

    def countBook(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Book")
            return cursor.fetchone()[0]

    def bookExists(self, BookID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Book where BookID = %s", (BookID,))
            return cursor.fetchone()[0] == 1

    def test_insertBook(self):
        with DatabaseUtils(self.connection) as db:
            count = self.countBook()
            self.assertTrue(db.insertBook("book4","auth4","2010-10-10"))
            self.assertTrue(count + 1 == self.countBook())
            self.assertTrue(db.insertBook("book6","auth6","2010-10-10"))
            self.assertTrue(count + 2 == self.countBook())

    def test_getBook(self):
        with DatabaseUtils(self.connection) as db:
            self.assertTrue(self.countBook() == len(db.getBook()))

    # def test_deleteBook(self):
    #     with DatabaseUtils(self.connection) as db:
    #         count = self.countBook()
    #         BookID = 1

    #         self.assertTrue(self.bookExists(BookID))

    #         db.deleteBook(BookID)

    #         self.assertFalse(self.bookExists(BookID))
    #         self.assertTrue(count - 1 == self.countBook())

if __name__ == "__main__":
    unittest.main()
