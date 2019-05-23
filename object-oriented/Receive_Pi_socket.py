#!/usr/bin/env python3
import os
import socket
import sys
from sqlalchemy import *
import getpass
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from hash_pass import verify_password, hash_password
from capture import captureFace
from encode import encodeFace
from recognise import recogniseFace

basedir = os.path.abspath(os.path.dirname(__file__))
db = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
engine = create_engine(db)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hash = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)

    def __repr__(self):
        return "<User:%s>" % self.username


def check_user():
    '''
    Check the username and password
    :return:username -> str
    '''
    try_time = 0
    while try_time < 3:
        username = input("Username:")
        res = session.query(User.password_hash).filter(User.username == username).first()
        if res:
            password = getpass.getpass("Password:")
            if verify_password(res[0], password):
                print("Login Successfully!\n")
                return username
            else:
                print("Wrong password! Try again!\n")
                try_time += 1
        else:
            print("No such user! Check your username!\n")
            try_time += 1
    print("You tried too many times! Maybe you can register first!\n")
    return None


def loginByface():
    '''
    Check the username
    :return:username -> str
    '''
    try_time = 0
    while try_time < 3:
        username = input("Username:")
        encodeFace()
        res = session.query(User.username).filter(User.username == username).first()
        if res:
            if (recogniseFace(username) == True):
                print("Login Successfully!\n")
                return username
            else:
                print("Face Invalid! Try again!\n")
                try_time += 1
        else:
            print("No such user! Check your username!\n")
            try_time += 1
    print("You tried too many times! Maybe you can register first!\n")
    return None


def add_user():
    '''
    add user to Users
    :return: username->str
    '''
    print("New User Info:")
    repeated_name = True
    while repeated_name:
        username = input("Username:")
        res = session.query(User.username).filter(User.username == repeated_name).first()
        if res:
            print("Username already exist!\n")
        else:
            repeated_name = False

    first_name_flag = False
    while not first_name_flag:
        first_name = input("First Name:")
        if first_name != '':
            first_name_flag = True
        else:
            print("First name can not be empty!")

    last_name_flag = False
    while not last_name_flag:
        last_name = input("Last Name:")
        if last_name != '':
            last_name_flag = True
        else:
            print("Last name can not be empty!")

    email_flag = False
    while not email_flag:
        email = input("Email:")
        if email != '':
            if '@' not in email:
                print("Invalid email!")
            else:
                email_flag = True
        else:
            print("Email can not be empty!")

    while True:
        password = getpass.getpass("Password:")
        re_enter = getpass.getpass("Confirm your password:")
        if password == re_enter:
            password = hash_password(password)
            session.add(User(username=username,
                             password_hash=password,
                             first_name=first_name,
                             last_name=last_name,
                             email=email))
            session.commit()
            print("Do you want to register for face recognising? ")
            print("1. Yes")
            print("2. No")
            print()
            choice = input("Please select your option.")
            if (choice == "1"):
                captureFace(username)
                encodeFace()
                print("Register successfully.")
                print("You can use login via face recognising now.\n")
                print()
            elif (choice == "2"):
                print("Register successfully.\n")
            else:
                print("Invalid input, try again.")
                print()
            # print("Register Successfully!\n")
            return username
        else:
            print("Password is not the same.Try again.")


def connect_to_server_socket():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 9999
    clientsocket.connect((host, port))
    return clientsocket


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    while True:
        username = None
        while username is None:
            print("****************************************************\n")
            print("1. Login by password")
            print("2. Login by face recognising")
            print("3. Register")
            print("0. Quit")
            print()
            choice = input("Please select your option.\n")
            if choice == "1":
                username = check_user()
            elif choice == "2":
                username = loginByface()
            elif choice == "3":
                username = add_user()  # Auto-login after register
            elif choice == "0":
                print("Goodbye.")
                print()
                os._exit(0)
            else:
                print("Invalid input! Try again!\n")

        conn = connect_to_server_socket()
        conn.send(username.encode('utf-8'))

        logout = False
        while not logout:
            msg = conn.recv(1024)
            print(msg.decode())
            if msg.decode() == "logout":
                logout = True
                conn.close()
