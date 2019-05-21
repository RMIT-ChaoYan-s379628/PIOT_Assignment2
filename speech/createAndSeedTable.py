import MySQLdb

HOST = "35.201.18.142"
USER = "root"
PASSWORD = "abc123"
DATABASE = "People"

connection = MySQLdb.connect(HOST, USER, PASSWORD, DATABASE)

with connection.cursor() as cursor:
    cursor.execute("""
        create table PersonDetails (
            PersonDetailsID int not null auto_increment,
            FirstName text not null,
            LastName text not null,
            Address text null,
            constraint PK_PersonDetails primary key (PersonDetailsID)
        )""")
    
    cursor.execute("""
        insert into PersonDetails (FirstName, LastName, Address)
        values (%s, %s, %s)""", ("Matthew", "Bolger", "123 Fake Street"))
    cursor.execute("""
        insert into PersonDetails (FirstName, LastName, Address)
        values (%s, %s, %s)""", ("Matthew", "Wright", "456 Real Street"))
    cursor.execute("""
        insert into PersonDetails (FirstName, LastName, Address)
        values (%s, %s, %s)""", ("Shekhar", "Kalra", None))
    cursor.execute("""
        insert into PersonDetails (FirstName, LastName, Address)
        values (%s, %s, %s)""", ("Rodney", "Cocker", None))
    
    connection.commit()

connection.close()
