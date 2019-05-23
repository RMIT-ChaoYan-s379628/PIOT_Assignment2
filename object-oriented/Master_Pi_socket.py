#!/usr/bin/env python3
import socket
import json
import sys
import pymysql
import tabulate
from googleCalendar import addEvent
from googleCalendar import deleteEvent


def connect_to_database():
    # conn = pymysql.connect(host='127.0.0.1',
    #                        user='root',
    #                        password='65390057y',
    #                        db='LMS')
    # return conn
    conn = pymysql.connect(host='35.244.109.255',
                                 user='root',
                                 password='65390057y',
                                 db='LMS')
    return conn



def look_up_user_ID(username):
    # conn = connect_to_database()
    # with conn.cursor() as cursor:
    #     try:
    #         sql = "select LmsUserID from LMSUser where UserName ='%s'" % username
    #         cursor.execute(sql)
    #     except Exception as e:
    #         print(e)
    # conn.commit()
    # res = cursor.fetchone()
    # if res:
    #     CurrentUserID = res[0]
    #     return True
    # print("User not found!")
    # return False
    conn = connect_to_database()
    with conn.cursor() as cursor:
        try:
            cursor.execute("SELECT EXISTS(SELECT * FROM LmsUser WHERE UserName='%s')" % username)
            res = cursor.fetchone()
            if (res[0] == 1):
                cursor.execute("select LmsUserID from LmsUser where UserName ='%s'" % username)
                resCur = cursor.fetchone()
                CurrentUserID = resCur[0]
            else:
                cursor.execute(
                    "insert into LmsUser (UserName, Name) values ('%s','%s')" % (username, username))
                conn.commit()
                cursor.execute("select LmsUserID from LmsUser where UserName ='%s'" % username)
                resCur = cursor.fetchone()
                CurrentUserID = resCur[0]
            conn.close()
            return CurrentUserID
        except Exception as e:
            print(e)


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
    conn = connect_to_database()
    with conn.cursor() as cursor:
        try:
            sql = "insert into BookBorrowed (LmsUserID, BookID, Status, BorrowedDate) values (%s, %s, 'borrowed', CURRENT_DATE )" \
                  % (CurrentUserID, BookID)
            cursor.execute(sql)
            conn.commit()
            if conn.affected_rows() == 1:
                cursor.execute("select Title,Author from Book where BookID = '%s' " % BookID)
                res1 = cursor.fetchone()
                title = res1[0]
                author = res1[1]
                cursor.execute("select Name from LmsUser where LMSUserID ='%s'" % CurrentUserID)
                res2 = cursor.fetchone()
                customerName = res2[0]
                eventId = addEvent(title, author, customerName)
                cursor.execute("select BookBorrowedID from BookBorrowed order by BookBorrowedID desc limit 1")
                res3 = cursor.fetchone()
                BookBorrowedID = res3[0]
                cursor.execute(
                    "update BookBorrowed set EventID='%s' where BookBorrowedID=%s" % (eventId, BookBorrowedID))
                conn.commit()
                print("Borrow the book successfully!")
        except Exception as e:
            print(e)


def return_books(BookBorrowedID):
    conn = connect_to_database()
    with conn.cursor() as cursor:
        try:
            sql = "update BookBorrowed set Status='returned', ReturnedDate = CURRENT_DATE where BookBorrowedID = %s" % BookBorrowedID
            cursor.execute(sql)
            conn.commit()
            if conn.affected_rows() == 1:
                cursor.execute("select EventID from BookBorrowed where BookBorrowedID=%s" % BookBorrowedID)
                res=cursor.fetchone()
                eventId=res[0]
                deleteEvent(eventId)
                print("Return the book successfully!")
        except Exception as e:
            print(e)


def show_borrowed_books(CurrentUserID):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        sql = "select BookBorrowedID, BookID from BookBorrowed where LmsUserID = %s and Status='borrowed'" % CurrentUserID
        cursor.execute(sql)
    except Exception as e:
        print(e)
    conn.commit()
    res = cursor.fetchall()
    books = []
    for book in res:
        add_book = []
        id = book[1]
        add_book.append(book[0])
        sql = "select * from Book where BookID = %s " % id
        cursor.execute(sql)
        conn.commit()
        ans = cursor.fetchone()
        for item in ans:
            add_book.append(item)
        books.append(add_book)
    print(tabulate.tabulate(books, headers=["BorrowID", "BookID", "Title", "Author", "Published Time"]))


def search_books(method, value):
    conn = connect_to_database()
    if method == 'BookID':
        sql = "select * from Book where %s=%s" % (method, value)
    else:
        sql = "select * from Book where %s='%s'" % (method, value)
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)
    conn.commit()
    res = cursor.fetchall()
    conn.close()
    return res


def init_socket_server():
    host = socket.gethostname()
    port = 9999
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((host, port))
    serversocket.listen(5)
    return serversocket


if __name__ == "__main__":
    server = init_socket_server()
    while True:
        client, addr = server.accept()
        username = client.recv(1024)
        CurrentUserID = look_up_user_ID(username.decode())
        if username is not None:
            print("Welcome to the Library Management System, {} \n".format(username.decode()))
            print("****************************************************\n")
            logout_flag = False
            while not logout_flag:
                print("1. Search the book")
                print("2. Borrow the book")
                print("3. Return the book")
                print("0. Logout")
                print()
                choice = input("Please select your option:")

                if choice == "1":
                    search_command = None
                    while search_command is None:
                        search_command = input("Search base on: 1.Title 2.Author name: ")
                        if search_command == '1':
                            title = input("Please input title:")
                            format_and_print_books(search_books("Title", title))
                        elif search_command == '2':
                            author = input("Please input author name:")
                            format_and_print_books(search_books("Author", author))
                        else:
                            print("Invalid input! Retry!")
                            search_command = None
                elif choice == "2":
                    BookID = None
                    while BookID is None:
                        BookID = input("Please input the ID of the book you want to borrow: ")
                        res = search_books('BookID', BookID)
                        if not res:
                            print("No such book!")
                            BookID = None
                        else:
                            borrow_book(BookID, CurrentUserID)
                elif choice == "3":
                    show_borrowed_books(CurrentUserID)
                    return_finished = False
                    while not return_finished:
                        borrowedID = input("Please input the Borrowed ID to return the book:")
                        continue_return = input("Continue returning books? (y/n)")
                        return_books(borrowedID)
                        if continue_return == 'N' or 'n':
                            return_finished = True

                elif choice == "0":
                    logout_flag = True
                    client.send("logout".encode('utf-8'))
                    print("Bye bye!")
                else:
                    print("Invalid input. Please retry!")
