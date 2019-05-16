import os
import hashlib
import binascii
import sqlite3
from hash_pass import verify_password, hash_password


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
            "insert into Users (UserId,UserPassword, FirstName, LastName,Email) values (?,?,?,?,?)", (userId, hash_password(userPwd), userFName, userLName, userEmail,))
    else:
        print('This user has been existed.')
connection.close()