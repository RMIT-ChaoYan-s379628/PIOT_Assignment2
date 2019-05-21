import sqlite3

DB_NAME = "user.db"

connection = sqlite3.connect(DB_NAME)

with connection:
    connection.execute("""
        create table Users (UserId text not null primary key, UserPassword text not null, FirstName text not null, LastName text not null,Email text not null)
        """)

    connection.execute("""
        insert into Users (UserId,UserPassword, FirstName, LastName,Email) values ('test', '123', 'Chao','Yan','yy987y@gamil.com')
        """)

connection.close()
