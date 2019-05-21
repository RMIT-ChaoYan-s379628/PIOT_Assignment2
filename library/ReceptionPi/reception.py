#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
from hash_pass import verify_password, hash_password
from capture import captureFace
from encode import encodeFace
from recognise import recogniseFace
import socket_utils
import socket
import json
import sys
import sqlite3

# import pymysql

sys.path.append("..")

with open("config.json", "r") as file:
    data = json.load(file)

HOST = data["masterpi_ip"]  # The server's hostname or IP address.
PORT = 63000  # The port used by the server.
ADDRESS = (HOST, PORT)


def connectDB():
    # connection = pymysql.connect(host='127.0.0.1',
    #                              user='root',
    #                              password='65390057y',
    #                              db='library')
    # return connection
    connection = sqlite3.connect('user.db')
    return connection


def main():
    while (True):
        print("****************************************************\n")
        print("1. Login by password")
        print("2. Login by face recognising")
        print("3. Register")
        print("0. Quit")
        print()

        text = input("Select an option: ")
        print()

        if (text == "1"):
            getUser()
        elif (text == "2"):
            userId = input("Please insert your account.\n")
            if (recogniseFace(userId)):
                connection = connectDB()
                cursor = connection.cursor()
                cursor.execute(
                    "select * from Users where UserId = (?)", (userId,))
                row = cursor.fetchone()
                msg = "Login successfully."
                print(msg)
                currentUser = {
                    "userId": row[0], "username": row[2] + row[3], "firstname": row[2], "lastname": row[3]}
                login(currentUser)
        elif (text == "3"):
            register()
        elif (text == "0"):
            print("Goodbye.")
            print()
            break
        else:
            print("Invalid input, try again.")
            print()


def getUser():
    userId = input("Please insert your account.\n")
    userPwd = input("Please insert your password.\n")
    connection = connectDB()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT EXISTS(SELECT * FROM Users WHERE userId=(?))", (userId,))
    res = cursor.fetchone()
    if (res[0] == 1):
        cursor.execute(
            "select * from Users where UserId = (?)", (userId,))
        row = cursor.fetchone()
        pwd = row[1]
        if verify_password(pwd, userPwd):
            msg = "Login successfully."
            print(msg)
            currentUser = {
                "userId": row[0], "username": row[2] + row[3], "firstname": row[2], "lastname": row[3]}
            login(currentUser)
        else:
            msg = "Your password is wrong. Please insert again.\n"
            print(msg)
    else:
        print("The user is not existed. Please insert again or register.\n")

    # with connection.cursor() as cursor:
    #     try:
    #         # cursor.execute("SELECT EXISTS(SELECT * FROM Users WHERE userId='%s')" % userId)
    #         cursor.execute(
    #             "SELECT EXISTS(SELECT * FROM Users WHERE userId=(?))", (userId,))
    #         res = cursor.fetchone()
    #         if (res[0] == 1):
    #             # cursor.execute("select * from Users where UserId = '%s'" % userId)
    #             cursor.execute(
    #                 "select * from Users where UserId = (?)", (userId,))
    #             row = cursor.fetchone()
    #             pwd = row[1]
    #             if verify_password(pwd, userPwd):
    #                 msg = "Login successfully."
    #                 print(msg)
    #                 # currentUser = User(row[0], row[1], row[2], row[3], row[4])
    #                 currentUser = {
    #                     "userId": row[0], "username": row[2] + row[3], "firstname": row[2], "lastname": row[3]}
    #                 login(currentUser)
    #             else:
    #                 msg = "Your password is wrong. Please insert again.\n"
    #                 print(msg)
    #         else:
    #             print("The user is not existed. Please insert again or register.\n")
    #     except Exception as e:
    #         print(e)
    connection.close()


def login(user):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting to {}...".format(ADDRESS))
        s.connect(ADDRESS)
        print("Connected.")

        print("Logging in as {}".format(user["username"]))
        socket_utils.sendJson(s, user)

        print("Waiting for Master Pi...")
        while (True):
            object = socket_utils.recvJson(s)
            if ("logout" in object):
                print("Master Pi logged out.")
                print()
                break


def register():
    userId = input("Please insert your account.")
    userPwd = input("Please insert your password.")
    userFName = input("Please insert your first name.")
    userLName = input("Please insert your last name.")
    userEmail = input("Please insert your email.")
    connection = connectDB()
    cursor = connection.cursor()
    cursor.execute("select * from Users where UserId = (?)", (userId,))
    row = cursor.fetchone()
    if (row == None):
        cursor.execute(
            "insert into Users (UserId,UserPassword, FirstName, LastName,Email) values ((?),(?),(?),(?),(?))", (
                userId, hash_password(userPwd), userFName, userLName, userEmail,))
        connection.commit()
        print()
        print("Do you want to register for face recognising? ")
        print("1. Yes")
        print("2. No")
        print()
        choice = input("Please choose your option.")
        if (choice == "1"):
            captureFace(userId)
            encodeFace()
            print("Register successfully.")
            print("You can use login via face recognising now.")
            print()
        elif (choice == "2"):
            print("Register successfully.")
        else:
            print("Invalid input, try again.")
            print()
    else:
        print('This user has been existed.')
        print('Please insert again.\n')
        register()

    # with connection.cursor() as cursor:
    #     # cursor.execute("select * from Users where UserId = '%s'" % userId)
    #     cursor.execute("select * from Users where UserId = (?)", (userId,))
    #     row = cursor.fetchone()
    #     if (row == None):
    #         # cursor.execute(
    #         #     "insert into Users (UserId,UserPassword, FirstName, LastName,Email) values ('%s','%s','%s','%s','%s')" % (
    #         #         userId, hash_password(userPwd), userFName, userLName, userEmail))
    #         cursor.execute(
    #             "insert into Users (UserId,UserPassword, FirstName, LastName,Email) values ((?),(?),(?),(?),(?))", (
    #                 userId, hash_password(userPwd), userFName, userLName, userEmail,))
    #         connection.commit()
    #     else:
    #         print('This user has been existed.')
    #         print('Please insert again.\n')
    #         register()
    connection.close()


# Execute program.
if __name__ == "__main__":
    main()
