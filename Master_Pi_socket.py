#!/usr/bin/env python3
import socket
import json
import sys
import pymysql
import tabulate
import speech_recognition as sr
import MySQLdb
import subprocess
import datetime
import imutils
import time
import cv2
from imutils.video import VideoStream
from pyzbar import pyzbar
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
            cursor.execute(
                "SELECT EXISTS(SELECT * FROM LmsUser WHERE UserName='%s')" % username)
            res = cursor.fetchone()
            if (res[0] == 1):
                cursor.execute(
                    "select LmsUserID from LmsUser where UserName ='%s'" % username)
                resCur = cursor.fetchone()
                CurrentUserID = resCur[0]
            else:
                cursor.execute(
                    "insert into LmsUser (UserName, Name) values ('%s','%s')" % (username, username))
                conn.commit()
                cursor.execute(
                    "select LmsUserID from LmsUser where UserName ='%s'" % username)
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
                cursor.execute(
                    "select Title,Author from Book where BookID = '%s' " % BookID)
                res1 = cursor.fetchone()
                title = res1[0]
                author = res1[1]
                cursor.execute(
                    "select Name from LmsUser where LMSUserID ='%s'" % CurrentUserID)
                res2 = cursor.fetchone()
                customerName = res2[0]
                eventId = addEvent(title, author, customerName)
                cursor.execute(
                    "select BookBorrowedID from BookBorrowed order by BookBorrowedID desc limit 1")
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
                cursor.execute(
                    "select EventID from BookBorrowed where BookBorrowedID=%s" % BookBorrowedID)
                res = cursor.fetchone()
                eventId = res[0]
                deleteEvent(eventId)
                print("Return the book successfully!")
        except Exception as e:
            print(e)


def return_books_qrcode(BookID, CurrentUserID):
    conn = connect_to_database()
    with conn.cursor() as cursor:
        try:
            sql = "update BookBorrowed set Status='returned', ReturnedDate = CURRENT_DATE where BookID = %s and LmsUserID=%s and Status='borrowed'" % (
                BookID, CurrentUserID)
            cursor.execute(sql)
            conn.commit()
            if conn.affected_rows() == 1:
                cursor.execute("select EventID from BookBorrowed where BookID = %s and LmsUserID=%s and ReturnedDate = CURRENT_DATE order by BookBorrowedID desc " % (
                    BookID, CurrentUserID))
                res = cursor.fetchone()
                eventId = res[0]
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
    print(tabulate.tabulate(books, headers=[
          "BorrowID", "BookID", "Title", "Author", "Published Time"]))


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


def speech_recognition():
    bookTitle = get_booktitle_to_search()

    if(bookTitle is None):
        print("Failed to get book.")
        return

    print()
    print("Looking for book with title '{}'...".format(bookTitle))
    print()

    rows = search_book_title(bookTitle)
    if(rows):
        print("Found:", rows)
    else:
        print("No results found.")


def get_booktitle_to_search():
    MIC_NAME = "Microsoft® LifeCam HD-3000: USB Audio (hw:1,0)"
    # To test searching without the microphone uncomment this line of code
    # return input("Enter the book title to search for: ")

    # Set the device ID of the mic that we specifically want to use to avoid ambiguity
    for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
        if(microphone_name == MIC_NAME):
            device_id = i
            break

    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone(device_index=device_id) as source:
        # clear console of errors
        subprocess.run("clear")

        # wait for a second to let the recognizer adjust the
        # energy threshold based on the surrounding noise level
        r.adjust_for_ambient_noise(source)

        print("Say the book title to search for.")
        try:
            audio = r.listen(source, timeout=1.5)
        except sr.WaitTimeoutError:
            return None

    # recognize speech using Google Speech Recognition
    bookTitle = None
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        bookTitle = r.recognize_google(audio)
        # bookTitle = r.recognize_google(audio, key="AIzaSyAPC3pbGKJGjY_FnYpnv71_dR5j1MyszL4")
    except(sr.UnknownValueError, sr.RequestError):
        pass
    finally:
        return bookTitle


def search_book_title(bookTitle):
    # connection = MySQLdb.connect(HOST, USER, PASSWORD, DATABASE)
    conn = connect_to_database()

    with conn.cursor() as cursor:
        cursor.execute("select * from Book where Title = %s", (bookTitle,))
        rows = cursor.fetchall()

    conn.close()
    return format_and_print_books(rows)


def barcode_scanner():
    # initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    # time.sleep(2.0)

    found = set()

    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it to
        # have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(frame)

        # loop over the detected barcodes
        for barcode in barcodes:
            # the barcode data is a bytes object so we convert it to a string
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # if the barcode text has not been seen before print it and update the set
            if barcodeData not in found:
                print("[FOUND] Type: {}, BookID: {}".format(
                    barcodeType, barcodeData))
                found.add(barcodeData)
                return barcodeData

    # # wait a little before scanning again
    # time.sleep(1)

    # # close the output CSV file do a bit of cleanup
    # print("[INFO] cleaning up...")
    # vs.stop()


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
            print("Welcome to the Library Management System, {} \n".format(
                username.decode()))
            print("****************************************************\n")
            logout_flag = False
            while not logout_flag:
                print("1. Search the book")
                print("2. Borrow the book")
                print("3. Return the book")
                print("0. Logout")
                print()
                choice = input("Please select your option: ")

                if choice == "1":
                    search_command = None
                    while search_command is None:
                        search_command = input(
                            "Search base on: 1.Title 2.Author 3.Speech Recognition Service: ")
                        if search_command == '1':
                            title = input("Please input title: ")
                            format_and_print_books(
                                search_books("Title", title))
                        elif search_command == '2':
                            author = input("Please input author name: ")
                            format_and_print_books(
                                search_books("Author", author))
                        elif search_command == '3':
                            speech_recognition()
                        else:
                            print("Invalid input! Retry!")
                            search_command = None
                elif choice == "2":
                    BookID = None
                    while BookID is None:
                        BookID = input(
                            "Please input the ID of the book you want to borrow: ")
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
                        return_command = None
                        while return_command is None:
                            print("Search base on: ")
                            print("1. BookID ")
                            print("2. QRCode ")
                            print("0. Back")

                            return_command = input(
                                "Please select your option: ")
                            if return_command == '1':
                                borrowedID = input(
                                    "Please input the Borrowed ID to return the book: ")
                            elif return_command == '2':
                                BookID = barcode_scanner()
                                return_books_qrcode(BookID, CurrentUserID)
                                break
                            elif return_command == '0':
                                return_finished = True
                                break
                            continue_return = input(
                                "Continue returning books? (y/n)")
                            return_books(borrowedID)
                            if continue_return == 'N' or 'n':
                                return_finished = True

                elif choice == "0":
                    logout_flag = True
                    client.send("logout".encode('utf-8'))
                    print("Bye bye!")
                else:
                    print("Invalid input. Please retry!")
