#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import socket, json, sys

sys.path.append("..")
import socket_utils
import pymysql
import tabulate

HOST = ""  # Empty string means to listen on all IP's on the machine, also works with IPv6.
# Note "0.0.0.0" also works but only with IPv4.
PORT = 63000  # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(ADDRESS)
        s.listen()

        print("Listening on {}...".format(ADDRESS))
        while True:
            print("Waiting for Reception Pi...")
            conn, addr = s.accept()
            with conn:
                print("Connected to {}".format(addr))
                print()

                user = socket_utils.recvJson(conn)
                print(user["userId"])
                print(user["username"])
                menu(user)

                socket_utils.sendJson(conn, {"logout": True})


def connectDB():
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='65390057y',
                                 db='library')
    return connection


def menu(user):
    CurrentUserID = look_up_user_ID(user)
    print (CurrentUserID)
    while (True):
        print("Welcome to the Library Management System, {} \n".format(user["username"]))
        print("****************************************************\n")
        print("1. Display user details")
        print("2. Search the book")
        print("3. Borrow the book")
        print("4. Return the book")
        print("0. Logout")
        print()

        text = input("Select an option: ")
        print()

        if (text == "1"):
            print("UserId    : {}".format(user["userId"]))
            print("Username  : {}".format(user["username"]))
            print("First Name: {}".format(user["firstname"]))
            print("Last Name : {}".format(user["lastname"]))
            print()
        elif (text == "2"):
            searchMenu()
            print()
        elif (text == "3"):
            borrowBooks(CurrentUserID)
            print()
        elif (text == "0"):
            print("Goodbye.")
            print()
            break
        else:
            print("Invalid input, try again.")
            print()


def look_up_user_ID(user):
    connection = connectDB()
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT EXISTS(SELECT * FROM LMSUser WHERE UserName='%s')" % user["userId"])
            res = cursor.fetchone()
            if (res[0] == 1):
                cursor.execute("select LmsUserID from LMSUser where UserName ='%s'" % user["userId"])
                resCur = cursor.fetchone()
                CurrentUserID = resCur[0]


            else:
                cursor.execute(
                    "insert into LmsUser (UserName, Name) values ('%s','%s')" % (user["userId"], user["username"]))
                connection.commit()
                cursor.execute("select LmsUserID from LMSUser where UserName ='%s'" % user["userId"])
                resCur = cursor.fetchone()
                CurrentUserID = resCur[0]
            connection.close()
            return CurrentUserID
        except Exception as e:
            print(e)
    # res = cursor.fetchone()
    # if res:
    #     CurrentUserID = res[0]
    # return True
    # print("User not found!")
    # return False


def searchMenu():
    print("Search by: ")
    print("1. Book Title")
    print("2. Author")
    print("3. Back")
    print()
    opt = None
    while opt is None:
        opt = input("Select an option: ")
        if opt == '1':
            title = input("Please input title:")
            format_and_print_books(searchBooks("Title", title))
        elif opt == '2':
            author = input("Please input author name:")
            format_and_print_books(searchBooks("Author", author))
        else:
            print("Invalid input! Retry!")
            opt = None


def searchBooks(method, value):
    connection = connectDB()
    if method == 'BookID':
        sql = "select * from BooK where %s=%s" % (method, value)
    else:
        sql = "select * from BooK where %s='%s'" % (method, value)
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)
    connection.commit()
    res = cursor.fetchall()
    connection.close()
    return res


def format_and_print_books(res):
    books = []
    for item in res:
        book = []
        for attr in item:
            book.append(attr)
        books.append(book)
    header = ['BookID', 'Title', 'Author', 'Published time']
    print(tabulate.tabulate(books, headers=header))


def borrow_book(BookID, CurrentUserID):
    connection = connectDB()
    with connection.cursor() as cursor:
        try:
            sql = "insert into BookBorrowed (LmsUserID, BookID, Status, BorrowedDate) values (%s, %s, 'borrowed', CURRENT_DATE )" \
                  % (CurrentUserID, BookID)
            cursor.execute(sql)
        except Exception as e:
            print(e)
    res = connection.commit()
    if res == 1:
        print("Borrow the book successfully!")

def borrowBooks(CurrentUserID):
    BookID = None
    while BookID is None:
        BookID = input("Please input the ID of the book you want to borrow: ")
        res = searchBooks('BookID', BookID)
        if not res:
            print("No such book!")
            BookID = None
        else:
            borrow_book(BookID,CurrentUserID)


def show_borrowed_books(CurrentUserID):
    connection = connectDB()
    cursor = connection.cursor()
    try:
        sql = "select BookBorrowedID, BookID from BookBorrowed where LmsUserID = %s and Status='borrowed'" % CurrentUserID
        cursor.execute(sql)
    except Exception as e:
        print(e)
    connection.commit()
    res = cursor.fetchall()
    books = []
    for book in res:
        add_book = []
        id = book[1]
        add_book.append(book[0])
        sql = "select * from Book where BookID = %s " % id
        cursor.execute(sql)
        connection.commit()
        ans = cursor.fetchone()
        for item in ans:
            add_book.append(item)
        books.append(add_book)
    print(tabulate.tabulate(books, headers=["BorrowID", "BookID", "Title", "Author", "Published Time"]))


def return_books(BookBorrowedID):
    conn = connectDB()
    with conn.cursor() as cursor:
        try:
            sql = "update BookBorrowed set Status='returned', ReturnedDate = CURRENT_DATE where BookBorrowedID = %s" % BookBorrowedID
            cursor.execute(sql)
        except Exception as e:
            print(e)
    res = conn.commit()
    if res == 1:
        print("Return the book successfully!")


def returnBook(CurrentUserID):
    show_borrowed_books(CurrentUserID)
    return_finished = False
    while not return_finished:
        borrowedID = input("Please input the Borrowed ID to return the book:")
        return_books(borrowedID)
        continue_return = input("Continue returning books? (y/n)")
        if continue_return == 'N' or 'n':
            return_finished = True


# Execute program.
if __name__ == "__main__":
    main()
