#importing libraries
import threading
import socket
import os

#client-side setup
ip = "127.0.0.1"#input("Enter an ip address: ") #server ip
port = 55555 #port to be connected

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((ip, port))
    
except:
    print("Could not connect to server!")
    input("")
    
username =""

#receive
def receive():
    global username
    opt = ""
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == '-CHOOSE-':
                opt = input("Choose a opt(login[L]/SignUp[S]): ")
                if opt == "L":
                    client.send("-LOGIN-".encode('ascii'))
                if opt == "S":
                    client.send("-SIGNUP-".encode('ascii'))
            elif message == '-DETAILS-':
                if opt == "L":
                    username = input("Enter username: ")
                    pwd = input("Enter password: ")
                    client.send(f"{username} {pwd}".encode('ascii'))
                if opt == "S":
                    username = input("Choose a username: ")
                    pwd = input("Choose a password: ")
                    client.send(f"{username} {pwd}".encode('ascii'))
            elif message == "-PERFECT-":
                write_thread = threading.Thread(target=write)
                write_thread.start()
            elif message == "-Username-in-use-":
                print("Username already in use!")
            elif message == "-Already-Logged-In-":
                print("Already Logged in!")
            elif message == "-INVALID-USERNAME-":
                print("Invalid Username!")
            elif message == "-INCORRECT-PWD-":
                print("Incorrect Password!")
            else:
                print(message)
        except:
            client.close()
            os._exit(0)

#write
def write():
    global username
    while True:
        Sntc = input("")
        if Sntc == "/ext":
            client.close()
            os._exit(0)
        else:
            words = Sntc.split()
            if len(words) > 0:
                word = words[0]
                char = list(word)
                n = 1
                un = ""
                msg = ""
                if len(char) > 0:
                    code = char[0]
                    if code == "@":  
                        while (n < len(char)):
                            un += char[n]
                            n += 1
                        n = 1
                        while (n < len(words)):
                            msg += words[n] + " "
                            n += 1
                        if un == "":
                            print("unknown target", "r")
                        elif msg == "":
                            print("invaild message", "r")
                        else:
                            message = f'@DM {un} {msg}'
                            client.send(message.encode('ascii'))
                    else:
                        message = f'{username}: {Sntc}'
                        client.send(message.encode('ascii'))

#start threads
receive_thread = threading.Thread(target=receive)
receive_thread.start()