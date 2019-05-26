# Reference: https://docs.python.org/2/library/unittest.html
import unittest
import MySQLdb
from database_utils import DatabaseUtils

class TestDatabaseUtils(unittest.TestCase):
    HOST = "35.244.109.255"
    USER = "root"
    PASSWORD = "65390057y"
    DATABASE = "TestBook"

    def setUp(self):
        self.connection = MySQLdb.connect(TestDatabaseUtils.HOST, TestDatabaseUtils.USER,
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
            cursor.execute("insert into Book (Title) values ('Math')")
            cursor.execute("insert into Book (Title) values ('English')")
            cursor.execute("insert into Book (Title) values ('Machine Learning')")
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

    def bookExists(self, personID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Book where BookID = %s", (BookID,))
            return cursor.fetchone()[0] == 1

    def test_insertBook(self):
        with DatabaseUtils(self.connection) as db:
            count = self.countBook()
            self.assertTrue(db.insertBook("Java"))
            self.assertTrue(count + 1 == self.countBook())
            self.assertTrue(db.insertBook("Ruby"))
            self.assertTrue(count + 2 == self.countBook())

    def test_getBook(self):
        with DatabaseUtils(self.connection) as db:
            self.assertTrue(self.countBook() == len(db.getBook()))

    def test_deleteBook(self):
        with DatabaseUtils(self.connection) as db:
            count = self.countBook()
            BookID = 1

            self.assertTrue(self.bookExists(BookID))

            db.deleteBook(BookID)

            self.assertFalse(self.bookExists(BookID))
            self.assertTrue(count - 1 == self.countBook())

if __name__ == "__main__":
    unittest.main()