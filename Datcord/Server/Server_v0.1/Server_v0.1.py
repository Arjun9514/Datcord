#importing libraries
from colorit import *
import data.color_it as ci 
import pandas as pd
import random as r
import time as t
import threading 
import socket
import os

path = "H:\Dhatcord\Data\data.xlsx"

#database
database = pd.read_excel(path)

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
muted = []
banned=[]

#booleans
kicked = False
saving = False

#Server main
def main():
    sf.prnt("Server is online...", "g")
    sf.prnt("/help for helpful information","o")
    sf.load()
    input_thread = threading.Thread(target=sf.input)
    input_thread.start()
    auto_bkup = threading.Thread(target=sf.auto_bkup)
    auto_bkup.start()
    sf.CntnwClt()

#Server Functions
class sf:
    
    #Prints colorful text to terminal
    def prnt(msg="",cr="",ed="\n"):
        c = ci.clr(cr)
        if cr == "r":
            print(color("Error: "+msg, c),end=ed)
        else:
            print(color(msg, c),end=ed)

    #Broadcast message 
    def broadcast(message=""):
        for client in clients:
            client.send(message.encode('ascii'))

    #Load Data
    def load():
        for d in (w:=list(database["Muted"].values)):
            if (T:=eval(d))[0] == True:
                sf.mute(database["Username"][w.index(d)],T[1],"s")
        for d in (w:=list(database["Banned"].values)):
            if d == True:
                banned.append(database["Username"][w.index(d)])

    #Connect new Client
    def CntnwClt():
        try:
            while True:
                client, address = server.accept()
                thread = threading.Thread(target=sf.handle, args=(client,address))
                thread.start()
        except:
            pass    
    
    #Input
    def input():
        global muted,banned
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
                elif code == "/mute":
                    if len(words) > 2:
                        words = Sntc.split(' ', 2)    
                        trgt = words[1]
                        tim = words[2]
                        if trgt not in muted:
                            sf.mute(trgt, float(tim[:-1]),tim[-1:])
                        else:
                            sf.prnt('target is already muted','r')
                    else:
                        sf.prnt("Syntax error", "r")
                elif code == "/unmute":
                    words = Sntc.split(' ', 1)    
                    trgt = words[1]
                    if trgt in muted:
                        muted = sf.dlt(trgt=trgt,list=muted)
                        sf.prnt(f'{trgt} is unmuted',"y")
                        sf.broadcast(f'{trgt} is unmuted now')
                    else:
                        sf.prnt('target not found','r')
                elif code == "/ban":
                    words = Sntc.split(' ', 1)    
                    trgt = words[1]
                    if trgt not in banned:
                        banned.append(trgt)
                        sf.prnt(f'{trgt} is banned',"o")
                        sf.broadcast(f'{trgt} is banned')
                    else:
                        sf.prnt("target is already banned","r")
                elif code == "/unban":
                    words = Sntc.split(' ', 1)    
                    trgt = words[1]
                    if trgt in banned:
                        banned = sf.dlt(trgt,banned)
                        sf.prnt(f'{trgt} is unbanned',"y")
                        sf.broadcast(f'{trgt} is unbanned now')
                    else:
                        sf.prnt('target not found','r')
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
                elif code == "/bkup":
                    sf.svbk()
                elif code == "/help":
                    sf.prnt("Commands                  Description","y")
                    sf.prnt("/snd                      to send messages","y")
                    sf.prnt("/dm <username>            to send messages privately","y")
                    sf.prnt("/mute <username> <time>   to mute a client","y")
                    sf.prnt("/unmute <username>        to unmute a client","y")
                    sf.prnt("/ban                      to ban a client")
                    sf.prnt("/unban                    to unban a client")
                    sf.prnt("/kick <username>          to kick out a client","y")
                    sf.prnt("/bkup                     to backup data","y")
                    sf.prnt("/stats                    returns the stats of server","y")
                    sf.prnt("/sd <time>                to shutdown server","y")
                    sf.prnt("/stp                      to stop server","y")
                    sf.prnt("                  ** **","y")
                else:
                    sf.prnt("invalid command", "r")
            else:
                sf.prnt("invalid command", "r")
        
    #Send message
    def send(msg=""):
        message = f'Server: {msg}'
        sf.prnt(message,"b")
        message = f'Server: {msg}'
        sf.broadcast(message)
    
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
        sf.prnt("Total Number of Clients:","p")
        for un in list(database["Username"].values):
            sf.prnt(un+"   ",cr="p",ed="")
        print()
        sf.prnt("Online Clients:","p")
        for un in usernames:
            sf.prnt(un+"   ",cr="p",ed="")
        print()
        sf.prnt("Muted Clients:","p")
        for un in muted:
            sf.prnt(un+"   ",cr="p",ed="")
        print()
        sf.prnt("Banned Clients:","p")
        for un in banned:
            sf.prnt(un+"   ",cr="p",ed="")
        print()

    #Mute client
    def mute(target="", tim="",unit=""):
        sf.prnt(f'{target} is muted for {tim}{unit}',"o")
        sf.broadcast(f'{target} is muted for {tim}{unit}')
        muted.append(target)
        if unit == "h":
            tim = tim * 3600
        elif unit == "m":
            tim = tim * 60
        timer = threading.Thread(target=sf.timer, args=(target,tim))
        timer.start()

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
            sf.broadcast(f'{username} was kicked by Server')
        else:
            sf.prnt("unknown target", "r")
    
    #Handle client
    def handle(client,add):
        un,rcvdat = "",""
        global database
        try:
            while(True): 
                    client.send('-CHOOSE-'.encode('ascii'))
                    rcvdat = client.recv(1024).decode('ascii')
                    if(rcvdat == "-LOGIN-" or rcvdat == "-SIGNUP-"):
                        break
            while(True):
                client.send('-DETAILS-'.encode('ascii'))
                rcdat = (client.recv(1024).decode('ascii')).split(" ")
                username = rcdat[0]
                pwd = rcdat[1]
                if(rcvdat == "-SIGNUP-"):
                    connect = True
                    for usn in list(database["Username"].values):
                        if(username == usn):
                            client.send('-Username-in-use-'.encode('ascii'))
                            connect = False
                    if connect == True:
                        client.send('-PERFECT-'.encode('ascii'))
                        usernames.append(username)
                        database =  database.append({"Username":username,"Password":pwd,"Muted":[False,"-"],"Banned":False},ignore_index=True)
                        sf.prnt(f'{username} connected with {str(add)}', "p")
                        sf.broadcast(f'{username} joined the chat!')
                        clients.append(client)
                        client.send('Connected to the server!'.encode('ascii'))
                        un = username
                        break
                if(rcvdat == "-LOGIN-"):            
                    connect = False
                    une = False
                    for usn in list(database["Username"].values):
                        if(username == usn):
                            une = True
                            if(pwd == database["Password"][list(database["Username"].values).index(usn)]):
                                connect = True
                            else:
                                client.send('-INCORRECT-PWD-'.encode('ascii'))
                    for usn in usernames:
                        if(usn == username):
                            une = True
                            connect = False
                            client.send('-Already-Logged-In-'.encode('ascii'))
                    if connect == True:
                        client.send('-PERFECT-'.encode('ascii'))
                        usernames.append(username)
                        
                        sf.prnt(f'{username} connected with {str(add)}', "p")
                        sf.broadcast(f'{username} joined the chat!')
                        clients.append(client)
                        client.send('Connected to the server!'.encode('ascii'))
                        un = username
                        break
                    if une == False:
                        client.send('-INVALID-USERNAME-'.encode('ascii'))
            global kicked
            kick = False
            is_banned = False
            for u in banned:
                if un == u:
                    is_banned = True
                    client.send(f"You are banned from the Chatroom!".encode('ascii'))
                    client.send(f"You can request to lift the ban by /request <msg>".encode('ascii'))
                    break
            while True:
                kick = sf.check(un) 
                try:
                    is_banned = False
                    is_muted = False
                    message = client.recv(1024)
                    inmsg = message.decode('ascii')
                    for u in muted:
                        if un == u:
                            is_muted = True
                            break
                    for u in banned:
                        if un == u:
                            is_banned = True
                            break
                    words = inmsg.split()
                    if words[0] == "@DM":
                        words = inmsg.split(' ', 2)
                        trgt = words[1]
                        msg = words[2]
                        sf.dm(un, trgt, msg)
                    elif words[0] == "/request":
                        if is_banned == True:
                            msg=""
                            for i in words[1:]:
                                msg += i + " "
                            sf.prnt(f"{username}'s request: {msg}")
                    else:
                        if is_muted == False and is_banned == False:
                            sf.prnt(message.decode('ascii'), "b")
                            sf.broadcast((f'{inmsg}'))
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
                        sf.broadcast(f'{username} left the chat')
                        usernames.remove(username)
                        break
        except:
            pass

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
        global saving
        saving = True
        sf.svbk()
        if tmr == 0:
            sf.prnt("Server is stopped...", "r")
        else:
            sf.prnt("Server is shutting down in...", "y")
            while (tmr > 0):
                t.sleep(1)
                sf.prnt(tmr, "y")
                tmr -= 1
            sf.prnt("Server shutdown complete!", "g")
        sf.broadcast(f'Server went offline!')
        server.close()
        os._exit(0)

    #Save/BackUp
    def svbk():
        global saving
        saving = True
        t.sleep(1)
        for u in list(database["Username"].values):
            if u in banned:
                database.at[list(database["Username"].values).index(u),"Banned"] = True
            else:
                database.at[list(database["Username"].values).index(u),"Banned"] = False
        database.to_excel(path,index=False)
        saving = False
        sf.prnt("Backup complete!","g")

    #Auto Backup
    def auto_bkup():
        while(True):
            sf.prnt("Auto-Backup in 30m","y")
            seconds = 1800
            while seconds > 0:
                t.sleep(1)
                seconds -= 1
            sf.svbk() 
    
    #Timer
    def timer(trgt,seconds):
        global saving,muted
        while seconds > 0:
            if(saving == True):
                database.at[list(database["Username"].values).index(trgt),"Muted"] = [True,seconds]
            t.sleep(1)
            seconds -= 1
        database.at[list(database["Username"].values).index(trgt),"Muted"] = [False,0]
        muted = sf.dlt(trgt=trgt,list=muted)

    #Delete
    def dlt(trgt="",list=[]):
        for l in list:
            if(l == trgt):
                idx = list.index(l)
                del list[idx]
                return list

#Run Server main 
main()
