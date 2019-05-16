#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import socket, json, sys
sys.path.append("..")
import socket_utils

HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
             # Note "0.0.0.0" also works but only with IPv4.
PORT = 63000 # Port to listen on (non-privileged ports are > 1023).
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
                menu(user)

                socket_utils.sendJson(conn, { "logout": True })

def menu(user):
    while(True):
        print("Welcome {}".format(user["username"]))
        print("1. Display user details")
        print("0. Logout")
        print()

        text = input("Select an option: ")
        print()

        if(text == "1"):
            print("Username  : {}".format(user["username"]))
            print("First Name: {}".format(user["firstname"]))
            print("Last Name : {}".format(user["lastname"]))
            print()
        elif(text == "0"):
            print("Goodbye.")
            print()
            break
        else:
            print("Invalid input, try again.")
            print()

# Execute program.
if __name__ == "__main__":
    main()
