#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import socket
import json
import sys
import pymysql

sys.path.append("..")
import socket_utils

from hash_pass import verify_password, hash_password

with open("config.json", "r") as file:
    data = json.load(file)

HOST = data["masterpi_ip"]  # The server's hostname or IP address.
PORT = 63000  # The port used by the server.
ADDRESS = (HOST, PORT)


def connectDB():
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='65390057y',
                                 db='library')
    return connection


def main():
    loginFlag = False
    while (loginFlag == False):
        print("****************************************************\n")
        print("1. Login")
        print("2. Register")
        print("0. Quit")
        print()

        text = input("Select an option: ")
        print()

        if (text == "1"):
            getUser()
            loginFlag = True
        elif (text == "2"):
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
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT EXISTS(SELECT * FROM Users WHERE userId='%s')" % userId)
            res = cursor.fetchone()
            if (res[0] == 1):
                cursor.execute("select * from Users where UserId = '%s'" % userId)
                row = cursor.fetchone()
                pwd = row[1]
                if verify_password(pwd, userPwd):
                    msg = "Login successfully."
                    print(msg)
                    currentUser = {"userId": row[0], "username": row[2] + row[3], "firstname": row[2],
                                   "lastname": row[3]}
                    login(currentUser)
                else:
                    msg = "Your password is wrong. Please insert again.\n"
                    print(msg)
            else:
                print("The user is not existed. Please insert again or register.\n")
        except Exception as e:
            print(e)
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
    with connection.cursor() as cursor:
        cursor.execute("select * from Users where UserId = '%s'" % userId)
        row = cursor.fetchone()
        if (row == None):
            cursor.execute(
                "insert into Users (UserId,UserPassword, FirstName, LastName,Email) values ('%s','%s','%s','%s','%s')" % (
                    userId, hash_password(userPwd), userFName, userLName, userEmail))
            connection.commit()
        else:
            print('This user has been existed.')
            print('Please insert again.\n')
            register()
    connection.close()


# Execute program.
if __name__ == "__main__":
    main()
