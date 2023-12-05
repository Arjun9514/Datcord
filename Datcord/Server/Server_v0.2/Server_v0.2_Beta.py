#importing libraries
from colorit import *
import pandas as pd
import time as t
import threading 
import socket
import os

data_path = r"H:\Datcord\New\Data\data.xlsx"

# Database
database = pd.read_excel(data_path)

# Color it
class Color:
    red = Colors.red
    orange = Colors.orange
    yellow = Colors.yellow
    green = Colors.green
    blue = Colors.blue
    purple = Colors.purple
    white = Colors.white

    @staticmethod
    def get_color(color_code):
        if color_code == "r":
            return Color.red
        elif color_code == "o":
            return Color.orange
        elif color_code == "y":
            return Color.yellow
        elif color_code == "g":
            return Color.green
        elif color_code == "b":
            return Color.blue
        elif color_code == "p":
            return Color.purple
        elif color_code == "w":
            return Color.white
        else:
            return Color.white

    @staticmethod
    def initialize():
        init_colorit()

# Clear the terminal
Color.initialize()

# Setting up localhost & port
host = ''
port = 55555

# Setting up the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Dictionary
memory = {
    "clients": [],
    "usernames": [],
    "muted": [],
    "banned": [],
    "kicked": False,
    "saving": False
}

#Server main
def main():
    sf.prnt("Server is online...", "g")
    sf.prnt("/help for helpful information","o")
    sf.load()
    input_thread = threading.Thread(target=sf.input)
    input_thread.start()
    auto_backup = threading.Thread(target=sf.auto_bkup)
    auto_backup.start()
    sf.CntnwClt()

#Server Functions
class sf:
    
    #Prints colorful text to terminal
    def prnt(msg="",cr="",ed="\n",error=True):
        c = Color.get_color(cr)
        if cr == "r":
            if error == True:
                print(color("Error: "+msg, c),end=ed)
            else:
                print(color(msg, c),end=ed)   
        else:
            print(color(msg, c),end=ed)

    #Broadcast message 
    def broadcast(message=""):
        for client in memory["clients"]:
            client.send(message.encode('ascii'))

    #Load Data
    def load():
        for user  in (muted_users:=list(database["Muted"].values)):
            if (T:=eval(user))[0] == True:
                sf.mute(database["Username"][muted_users.index(user)],T[1],"s")
        for user in (banned_users:=list(database["Banned"].values)):
            if user == True:
                memory["banned"].append(database["Username"][banned_users.index(user)])

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
        global memory
        while True:
            sentence = input("")
            words = sentence.split()
            
            if len(words) > 1:
                code = words[0]
                if code == "/snd":
                    words = sentence.split(' ', 1)
                    msg = words[1]
                    sf.send(msg)
                elif code == "/dm":
                    if len(words) > 2:
                        words = sentence.split(' ', 2)    
                        trgt = words[1]
                        msg = words[2]
                        sf.dm("Server", trgt, msg)
                    else:
                        sf.prnt("Syntax error", "r")
                elif code == "/mute":
                    if len(words) > 2:
                        words = sentence.split(' ', 2)    
                        trgt = words[1]
                        tim = words[2]
                        if trgt not in memory["muted"]:
                            sf.mute(trgt, float(tim[:-1]),tim[-1:])
                        else:
                            sf.prnt('target is already muted','r')
                    else:
                        sf.prnt("Syntax error", "r")
                elif code == "/unmute":
                    words = sentence.split(' ', 1)    
                    trgt = words[1]
                    if trgt in memory["muted"]:
                        memory["muted"] = sf.dlt(trgt=trgt,list=memory["muted"])
                        sf.prnt(f'{trgt} is unmuted',"y")
                        sf.broadcast(f'{trgt} is unmuted now')
                    else:
                        sf.prnt('target not found','r')
                elif code == "/ban":
                    words = sentence.split(' ', 1)    
                    trgt = words[1]
                    if trgt not in memory["banned"]:
                        memory["banned"].append(trgt)
                        sf.prnt(f'{trgt} is banned',"o")
                        sf.broadcast(f'{trgt} is banned')
                    else:
                        sf.prnt("target is already banned","r")
                elif code == "/unban":
                    words = sentence.split(' ', 1)    
                    trgt = words[1]
                    if trgt in memory["banned"]:
                        memory["banned"] = sf.dlt(trgt,memory["banned"])
                        sf.prnt(f'{trgt} is unbanned',"y")
                        sf.broadcast(f'{trgt} is unbanned now')
                    else:
                        sf.prnt('target not found','r')
                elif code == "/kick":
                    words = sentence.split(' ', 1)    
                    trgt = words[1]
                    sf.kick(trgt)
                elif code == "/sd":
                    words = sentence.split(' ', 1)
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
                    help = """
            Available Commands
/snd                      to send messages
/dm <username>            to send messages privately
/mute <username> <time>   to mute a client
/unmute <username>        to unmute a client
/ban <username>           to ban a client")
/unban <username>         to unban a client")
/kick <username>          to kick out a client
/bkup                     to backup data
/stats                    returns the stats of server
/sd <time>                to shutdown server
/stp                      to stop server
                    ** **"""
                    sf.prnt(help,"y")
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
    def dm(sender="",target="",msg=""):
        if target == "svr":
            sf.prnt(f'{sender} (whispered to Server): {msg}', "w")
            i = memory["usernames"].index(sender)
            client = memory["clients"][i]
            message = f'{sender} (whispered to Server): {msg}'
            client.send(message.encode('ascii'))
        else:
            sent = False
            if sender == "Server":
                pass
            else:
                client = memory["clients"][memory["usernames"].index(sender)]
            for user in memory["usernames"]:
                if target == user:
                    message = f'{sender} (whispered to {user}): {msg}'
                    if sender == "Server":
                        sf.prnt(message, "w")
                    else:
                        message = f'{sender} (whispered to {user}): {msg}'
                        client.send(message.encode('ascii'))
                    message = f'{sender} (whispered to you): {msg}'
                    memory["clients"][memory["usernames"].index(user)].send(message.encode('ascii'))
                    sent = True
                    break
            if sent == False:
                if sender == "Server":
                    sf.prnt("unknown target", "r")
                else:
                    client.send(f'unknown target'.encode('ascii'))
    
    #Stats
    def stats():
        sf.prnt(f"Number of Clients: {len(memory['clients'])}","p")
        sf.prnt("Total Number of Clients:","p")
        for user in list(database["Username"].values):
            sf.prnt(user+"   ",cr="p",ed="")
        print()
        sf.prnt("Online Clients:","p")
        for user in memory["usernames"]:
            sf.prnt(user+"   ",cr="p",ed="")
        print()
        sf.prnt("Muted Clients:","p")
        for user in memory["muted"]:
            sf.prnt(user+"   ",cr="p",ed="")
        print()
        sf.prnt("Banned Clients:","p")
        for user in memory["banned"]:
            sf.prnt(user+"   ",cr="p",ed="")
        print()

    #Mute client
    def mute(target="", tim="",unit=""):
        sf.prnt(f'{target} is muted for {tim}{unit}',"o")
        sf.broadcast(f'{target} is muted for {tim}{unit}')
        memory["muted"].append(target)
        if unit == "h":
            tim = tim * 3600
        elif unit == "m":
            tim = tim * 60
        timer = threading.Thread(target=sf.timer, args=(target,tim))
        timer.start()

    #Kick client
    def kick(target=""):
        global memory
        memory["kicked"] = False
        for user in memory["usernames"]:
            if target == user:
                message = f'Server kicked {user} from the chatroom'
                sf.prnt(message, "o")
                message = f'Server kicked you from the chatroom'
                memory["clients"][memory["usernames"].index(user)].send(message.encode('ascii'))
                memory["kicked"] = True
                memory["clients"][memory["usernames"].index(user)].close()
                del memory["clients"][memory["usernames"].index(user)]
                del memory["usernames"][memory["usernames"].index(user)]
                sf.broadcast(f'{user} was kicked by Server')
                break
        if memory["kicked"] == False:
            sf.prnt("unknown target", "r")
    
    #Handle client
    def handle(client,add):
        user,rcvdat = "",""
        global database
        try:
            while(True):
                client.send('-CHOOSE-'.encode('ascii'))
                rcvdat = client.recv(1024).decode('ascii')    
                tempdat = rcvdat.split("-")[1:-1]
                condn = tempdat[0]
                username = tempdat[1]
                pwd = tempdat[2]
                if(condn == "UP"):
                    connect = True
                    for name in list(database["Username"].values):
                        if(username == name):
                            client.send('Error@0'.encode('ascii'))
                            connect = False
                    if connect == True:
                        client.send('-PERFECT-'.encode('ascii'))
                        memory["usernames"].append(username)
                        database =  database.append({"Username":username,"Password":pwd,"Muted":[False,"-"],"Banned":False},ignore_index=True)
                        sf.prnt(f'{username} connected with {str(add)}', "p")
                        sf.broadcast(f'{username} joined the chat!')
                        memory["clients"].append(client)
                        client.send('Connected to the server!'.encode('ascii'))
                        user = username
                        break
                elif(condn == "IN"):            
                    connect = False
                    correct_name = False
                    for name in list(database["Username"].values):
                        if(username == name):
                            correct_name = True
                            if(pwd == database["Password"][list(database["Username"].values).index(name)]):
                                connect = True
                            else:
                                client.send('Error@3'.encode('ascii'))
                    for name in memory["usernames"]:
                        if(name == username):
                            correct_name = True
                            connect = False
                            client.send('Error@1'.encode('ascii'))
                    if connect == True:
                        client.send('-PERFECT-'.encode('ascii'))
                        memory["usernames"].append(username)
                        sf.prnt(f'{username} connected with {str(add)}', "p")
                        sf.broadcast(f'{username} joined the chat!')
                        memory["clients"].append(client)
                        client.send('Connected to the server!'.encode('ascii'))
                        user = username
                        break
                    if correct_name == False:
                        client.send('Error@2'.encode('ascii'))
            kick = False
            is_banned = False
            for banned_user in memory["banned"]:
                if user == banned_user:
                    is_banned = True
                    client.send(f"You are banned from the Chatroom!".encode('ascii'))
                    client.send(f"You can request to lift the ban by /request <msg>".encode('ascii'))
                    break
            while True:
                kick = sf.check(user) 
                try:
                    is_banned = False
                    is_muted = False
                    message = client.recv(1024)
                    inmsg = message.decode('ascii')
                    for muted_user in memory["muted"]:
                        if user == muted_user:
                            is_muted = True
                            break
                    for banned_user in memory["banned"]:
                        if user == banned_user:
                            is_banned = True
                            break
                    words = inmsg.split()
                    if words[0] == "@DM":
                        words = inmsg.split(' ', 2)
                        trgt = words[1]
                        msg = words[2]
                        sf.dm(user, trgt, msg)
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
                    if memory["kicked"] == True:
                        if kick == True:
                            memory["kicked"] = False
                            break
                    else:
                        memory["clients"].remove(client)
                        client.close()
                        sf.prnt(f'{user} left the chat', "o")
                        sf.broadcast(f'{user} left the chat')
                        memory["usernames"].remove(user)
                        break
        except:
            pass

    #Check the username
    def check(user=""):
        kick = 0
        for name in memory["usernames"]:
            if user == name:
                kick += 1 
            else:
                pass
        if kick == 1:
            return True
        else:
            return False

    #Shutdown the Server
    def shtdwn(tmr=0):
        global memory
        memory["saving"] = True
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
        global memory
        memory["saving"] = True
        t.sleep(1)
        for user in list(database["Username"].values):
            if user in memory["banned"]:
                database.at[list(database["Username"].values).index(user),"Banned"] = True
            else:
                database.at[list(database["Username"].values).index(user),"Banned"] = False
        database.to_excel(data_path,index=False)
        memory["saving"] = False
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
        global memory
        while seconds > 0:
            if(memory["saving"] == True):
                database.at[list(database["Username"].values).index(trgt),"Muted"] = [True,seconds]
            t.sleep(1)
            seconds -= 1
        database.at[list(database["Username"].values).index(trgt),"Muted"] = [False,0]
        if trgt in memory["muted"]:
            memory["muted"] = sf.dlt(trgt=trgt,list=memory["muted"])

    #Delete
    def dlt(trgt="",list=[]):
        for l in list:
            if(l == trgt):
                idx = list.index(l)
                del list[idx]
                return list

    #Basic Animation
    def load_animation(inp,animation=[],counttime=0):
        ls_len = len(inp)
        anicount = 0
        i = 0                     
        while (counttime != 0):
            t.sleep(0.25) 
            load_str_list = list(inp) 
            x = ord(load_str_list[i])
            y = 0
            if x != 32 and x != 46:             
                if x>90:
                    y = x-32
                else:
                    y = x + 32
                load_str_list[i]= chr(y)
            res =''             
            for j in range(ls_len):
                res = res + load_str_list[j]
            sys.stdout.write("\r"+res + animation[anicount])
            sys.stdout.flush()
            inp = res
            anicount = (anicount + 1)% (len(animation))
            i =(i + 1)% ls_len
            counttime -= 1

#Run Server main 
main()