# import MySQLdb
import pymysql


class DatabaseUtils:
    HOST = "127.0.0.1"
    USER = "root"
    PASSWORD = "65390057y"
    DATABASE = "test"

    def __init__(self, connection=None):
        if(connection == None):
            connection = pymysql.connect(DatabaseUtils.HOST, DatabaseUtils.USER,
                                         DatabaseUtils.PASSWORD, DatabaseUtils.DATABASE)
        self.connection = connection

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def createBookTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists Book (
                    BookID int not null auto_increment,
                    Title text not null,
                    Author text not null,
                    PublishedDate date not null,
                    constraint PK_Book primary key (BookID)
                )""")
        self.connection.commit()

    def insertBook(self, title, author,publisheddate):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "insert into Book (Title,Author,PublishedDate) values (%s,%s,%s)", (title, author,publisheddate))
        self.connection.commit()

        return cursor.rowcount == 1

    def getBook(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select BookID, Title from Book")
            return cursor.fetchall()

    def deleteBook(self, BookID):
        with self.connection.cursor() as cursor:
            # Note there is an intentionally placed bug here: != should be =
            cursor.execute("delete from Book where BookID = %s", (BookID,))
        self.connection.commit()
