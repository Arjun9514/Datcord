#importing libraries
import socket
import threading
import os

#username
username = input("Choose a username:")

#client-side setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

#receive
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(username.encode('ascii'))
            else:
                print(message)
        except:
            client.close()
            os._exit(0)

#write
def write():
    while True:
        message = f'{username}: {input("")}'
        client.send(message.encode('ascii'))

#start threads
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
