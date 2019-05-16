#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import socket, json, sqlite3, sys
from hash_pass import verify_password, hash_password

sys.path.append("..")
import socket_utils

DB_NAME = "library.db"

with open("config.json", "r") as file:
    data = json.load(file)

HOST = data["masterpi_ip"]  # The server's hostname or IP address.
PORT = 63000  # The port used by the server.
ADDRESS = (HOST, PORT)


def main():
    while (True):
        print("1. Login")
        print("2. Register")
        print("0. Quit")
        print()

        text = input("Select an option: ")
        print()

        if (text == "1"):
            userId = input("Please insert your account.")
            userPwd = input("Please insert your password.")
            getUser(userId, userPwd)
            # login(user)
        elif(text == "2"):
            register()
        elif (text == "0"):
            print("Goodbye.")
            print()
            break
        else:
            print("Invalid input, try again.")
            print()


def getUser(userId, userPwd):
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    with connection:
        cursor = connection.cursor()
        cursor.execute("select * from Users where UserId = ?", (userId,))
        pwd = cursor.fetchone()[1]
        if verify_password(pwd,userPwd):
            msg = "Login successfully."
        else:
            msg = "Your account or password is wrong. Please insert again."
    connection.close()
    return print(msg)


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
    connection = sqlite3.connect('library.db')
    connection.row_factory = sqlite3.Row
    with connection:
        cursor = connection.cursor()
        cursor.execute("select * from Users where UserId = ?", (userId,))
        row = cursor.fetchone()
        if (row == None):
            cursor.execute(
                "insert into Users (UserId,UserPassword, FirstName, LastName,Email) values (?,?,?,?,?)",
                (userId, hash_password(userPwd), userFName, userLName, userEmail,))
        else:
            print('This user has been existed.')
            print('Please insert again.\n')
            register()
    connection.close()


# Execute program.
if __name__ == "__main__":
    main()
