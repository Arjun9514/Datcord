#importing libraries
from colorit import *
import data.color_it as ci 
import time as t
import threading 
import socket
import os

#clears the terminal 
ci.cln()

#setting up local host & port
host = ''
port = 55555

#setting the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

#arrays
clients = []
usernames = []

#booleans
kicked = False

#Server main
def main():
    sf.prnt("Server is online...", "g")
    sf.prnt("/help for helpful information","o")
    input_thread = threading.Thread(target=sf.input)
    input_thread.start()
    
    sf.CntnwClt()

#Server Functions
class sf:
    
    #prints colorful text to terminal
    def prnt(msg="",cr="",ed="\n"):
        c = ci.clr(cr)
        print(color(msg, c),end=ed)

    #Broadcast message 
    def broadcast(message):
        for client in clients:
            client.send(message)

    #Connect new Client
    def CntnwClt():
        while True:
            client, address = server.accept()

            client.send('NICK'.encode('ascii'))
            username = client.recv(1024).decode('ascii')
            usernames.append(username)

            sf.prnt(f'{username} connected with {str(address)}', "p")
            sf.broadcast(f'{username} joined the chat!'.encode('ascii'))
            clients.append(client)
            client.send('Connected to the server!'.encode('ascii'))

            thread = threading.Thread(target=sf.handle, args=(client,username,))
            thread.start()
    
    #Input
    def input():
        while True:
            Sntc = f'{input("")}'
            words = Sntc.split()
            
            if len(words) > 1:
                code = words[0]
                if code == "/snd":
                    words = Sntc.split(' ', 1)
                    msg = words[1]
                    sf.send(msg)
                elif code == "/dm":
                    if len(words) > 2:
                        words = Sntc.split(' ', 2)    
                        trgt = words[1]
                        msg = words[2]
                        sf.dm("Server", trgt, msg)
                    else:
                        sf.prnt("Syntax error", "r")
                elif code == "/kick":
                    words = Sntc.split(' ', 1)    
                    trgt = words[1]
                    sf.kick(trgt)
                elif code == "/sd":
                    words = Sntc.split(' ', 1)
                    try: 
                        tmr = int(words[1])
                        sf.shtdwn(tmr)
                    except:
                        sf.prnt("Syntax error", "r")
                else:
                    sf.prnt("invalid command", "r")
            elif len(words) == 1:
                code = words[0]
                if code == "/stp":
                    sf.shtdwn(0)
                elif code == "/stats":
                    sf.stats()
                elif code == "/help":
                    sf.prnt("Commands      Description","y")
                    sf.prnt("/snd          to send messages","y")
                    sf.prnt("/dm           to send messages privately","y")
                    sf.prnt("/kick         to kick out a client","y")
                    sf.prnt("/stats        returns the stats of server","y")
                    sf.prnt("/sd           to shutdown server","y")
                    sf.prnt("/stp          to stop server","y")
                    sf.prnt("","y")
                else:
                    sf.prnt("invalid command", "r")
            else:
                sf.prnt("invalid command", "r")
        
    #Send message
    def send(msg=""):
        message = f'Server: {msg}'
        sf.prnt(message,"b")
        message = f'Server: {msg}'
        sf.broadcast(message.encode('ascii'))
    
    #Direct message
    def dm(snder="",target="",msg=""):
        if target == "svr":
            sf.prnt(f'{snder} (whispered to Server): {msg}', "w")
            i = usernames.index(snder)
            client = clients[i]
            message = f'{snder} (whispered to Server): {msg}'
            client.send(message.encode('ascii'))
        else:
            n = 0
            sent = False
            if snder == "Server":
                pass
            else:
                i = usernames.index(snder)
                client = clients[i]

            for un in usernames:
                if target == un:
                    message = f'{snder} (whispered to {un}): {msg}'
                    if snder == "Server":
                        sf.prnt(message, "w")
                    else:
                        message = f'{snder} (whispered to {un}): {msg}'
                        client.send(message.encode('ascii'))
                    message = f'{snder} (whispered to you): {msg}'
                    clients[n].send(message.encode('ascii'))
                    sent = True
                    break
                else:
                    n += 1
            if sent == False:
                if snder == "Server":
                    sf.prnt("unknown target", "r")
                else:
                    client.send(f'unknown target'.encode('ascii'))
    
    #Stats
    def stats():
        sf.prnt(f"Number of Clients: {len(clients)}","p")
        sf.prnt("Online Memembers:","p")
        for un in usernames:
            sf.prnt(un+"   ",cr="p",ed="")
        print()

    #Kick client
    def kick(target=""):
        n = 0
        global kicked
        kicked = False
        for un in usernames:
            if target == un:
                a = un
                message = f'Server kicked {a} from the chatroom'
                sf.prnt(message, "o")
                message = f'Server kicked you from the chatroom'
                clients[n].send(message.encode('ascii'))
                kicked = True
                break
            else:
                n += 1
        if kicked == True:
            username = usernames[n]
            usernames.remove(username)
            client = clients[n]
            clients.remove(client)
            client.close()
            sf.broadcast(f'{username} was kicked by Server'.encode('ascii'))
        else:
            sf.prnt("unknown target", "r")
    
    #Handle client
    def handle(client,un = ""):
        global kicked
        kick = False
        while True:
            kick = sf.check(un) 
            try:
                message = client.recv(1024)
                inmsg = message.decode('ascii')
                #print(inmsg)
                words = inmsg.split()
                if words[0] == "@DM":
                    words = inmsg.split(' ', 2)
                    trgt = words[1]
                    msg = words[2]
                    sf.dm(un, trgt, msg)
                else:
                    sf.prnt(message.decode('ascii'), "b")
                    sf.broadcast((f'{inmsg}').encode('ascii'))
            except:
                if kicked == True:
                    if kick == True:
                        kicked = False
                        break
                else:
                    index = clients.index(client)
                    clients.remove(client)
                    client.close()
                    username = usernames[index]
                    sf.prnt(f'{username} left the chat', "o")
                    sf.broadcast(f'{username} left the chat'.encode('ascii'))
                    usernames.remove(username)
                    break
    
    #Check the username
    def check(un=""):
        kick = 0
        for usn in usernames:
            if un == usn:
                kick += 1 
            else:
                pass
        if kick == 1:
            return True
        else:
            return False

    #Shutdown the Server
    def shtdwn(tmr=0):
        if tmr == 0:
            sf.prnt("Server is stopped...", "r")
            sf.broadcast(f'Server went offline!'.encode('ascii'))
            os._exit(0) 
        else:
            sf.prnt("Server is shutting down in...", "y")
            while (tmr > 0):
                t.sleep(1)
                sf.prnt(tmr, "y")
                tmr -= 1
            t.sleep(1)
            sf.prnt("Server shutdown complete!", "g")
            sf.broadcast(f'Server went offline!'.encode('ascii'))
            os._exit(0)

#Run Server main 
main()
