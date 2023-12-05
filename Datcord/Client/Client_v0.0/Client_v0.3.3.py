import threading
import socket
import os

# Client-side setup
# server_ip = "127.0.0.1"
# server_port = 55555
server_ip = "0.tcp.in.ngrok.io"
server_port = 17432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((server_ip, server_port))
except socket.error as e:
    print("Could not connect to the server!")
    print(f"Error: {e}")
    input("")

username = ""

# Receive messages from the server
def receive_messages():
    global username
    option = ""
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == '-CHOOSE-':
                option = input("Choose an option (login[L]/SignUp[S]): ")
                if option == "L":
                    client.send("-LOGIN-".encode('ascii'))
                elif option == "S":
                    client.send("-SIGNUP-".encode('ascii'))
                else:
                    client.send("-Error-".encode('ascii'))
            elif message == '-DETAILS-':
                if option == "L":
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    client.send(f"{username} {password}".encode('ascii'))
                if option == "S":
                    username = input("Choose a username: ")
                    password = input("Choose a password: ")
                    client.send(f"{username} {password}".encode('ascii'))
            elif message == "-PERFECT-":
                write_thread = threading.Thread(target=send_messages)
                write_thread.start()
            elif message == "-Username-in-use-":
                print("Username already in use!")
            elif message == "-Already-Logged-In-":
                print("Already logged in!")
            elif message == "-INVALID-USERNAME-":
                print("Invalid username!")
            elif message == "-INCORRECT-PWD-":
                print("Incorrect password!")
            else:
                print(message)
        except socket.error as e:
            print("An error occurred while receiving messages from the server!")
            print(f"Error: {e}")
            client.close()
            os._exit(0)

# Send messages to the server
def send_messages():
    global username
    while True:
        try:
            sentence = input("")
            if sentence == "/ext":
                client.close()
                os._exit(0)
            else:
                words = sentence.split()
                if len(words) > 0:
                    word = words[0]
                    characters = list(word)
                    n = 1
                    recipient = ""
                    message = ""
                    if len(characters) > 0:
                        code = characters[0]
                        if code == "@":
                            while n < len(characters):
                                recipient += characters[n]
                                n += 1
                            n = 1
                            while n < len(words):
                                message += words[n] + " "
                                n += 1
                            if recipient == "":
                                print("Unknown recipient")
                            elif message == "":
                                print("Invalid message")
                            else:
                                formatted_message = f'@DM {recipient} {message}'
                                client.send(formatted_message.encode('ascii'))
                        elif code[0] == "/":
                            client.send(sentence.encode('ascii'))
                        else:
                            formatted_message = f'{username}: {sentence}'
                            client.send(formatted_message.encode('ascii'))
        except socket.error as e:
            print("An error occurred while sending messages to the server!")
            print(f"Error: {e}")
            client.close()
            os._exit(0)

# Start threads
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Wait for threads to complete
receive_thread.join()
