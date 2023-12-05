import socket
import threading
import time
import tkinter as tk
from tkinter import ttk

import customtkinter as ctk

# Paths
config_path = r"H:\Datcord\New\Development Build\config.txt"

# Client-side setup
server_ip = "127.0.0.1"
server_port = 55555

client = None

username = ""
error_codes = ["Username already in use!","Already logged in!","Invalid username!","Incorrect password!"]
wh, ht = 720, 460

app = tk.Tk()
app.geometry("720x460")
app.minsize(width=wh, height=ht)
app.title("Datcord")

app.tk.call("source", r"H:\Datcord\Gui\theme\forest.tcl")
app.tk.call("set_theme", "light")

#===============================================================================================================>ConnectionErrorpage
CEpage =ttk.Frame(app)

errorlabel0 = ttk.Label(CEpage,text="Could not connect to server!",font=('Helvetica', 16))
errorlabel1 = ttk.Label(CEpage,text="Try again after a few mins",font=('Helvetica', 16))
errorlabel0.place(x=220, y=180)
errorlabel1.place(x=230, y=220)

# Receive messages from the server
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if(message=='-offline-'):
                add_to_terminal("Server went offline!")
                _input.configure(state="disabled")
                break
            elif(message=='-shutdown-'):
                _input.configure(state="disabled")
                add_to_terminal("Server is shutting down!")
                break
            else:
                add_to_terminal(message)
        except socket.error as e:
            add_to_terminal("An error occurred while receiving messages from the server!")
            _input.configure(state="disabled")
            break

# Send messages to the server
def send_messages(sentence = ""):
    global username
    try:
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
    except:
        pass

def timer():
    time.sleep(3)
    error.configure(text="")

def send():
    global username
    dat = _input.get()
    if len(dat) != 0:
        _input.delete(first=0,last=len(dat))
        add_to_terminal(f'{username}: {dat}')
        send_messages(dat)

def add_to_terminal(data):
    data += "\n"
    terminal.configure(state="normal")
    terminal.insert("end", data)  # Insert the new data at the end
    terminal.configure(state="disabled")
    terminal.yview("end")

def change_theme():
    # NOTE: The theme's real name is azure-<mode>
    if app.tk.call("ttk::style", "theme", "use") == "forest-dark":
        # Set light theme
        app.tk.call("set_theme", "light")
        ctk.set_appearance_mode("light")
        terminal.configure(bg_color="#ffffff",fg_color="#ffffff")
    else:
        # Set dark theme
        app.tk.call("set_theme", "dark")
        ctk.set_appearance_mode("dark")
        terminal.configure(bg_color="#333333",fg_color="#3e3e3e")

    button_style = ttk.Style()
    button_style.configure("Accent.TButton", font=("TkDefaultFont", 12))

def sign(command="",usr="",pwsd="",direct=False):
    global username
    _userinput.delete(first=0,last=len(usr))
    _pwdinput.delete(first=0,last=len(pwsd))
    while True:
        message = client.recv(1024).decode('ascii')
        if message == '-CHOOSE-':
            if command == "in":
                client.send(f"-IN-{usr}-{pwsd}-".encode('ascii'))
            elif command == "up":
                client.send(f"-UP-{usr}-{pwsd}-".encode('ascii'))
        elif message == "-PERFECT-":
            username = usr
            signpage.pack_forget()
            notebook.pack(expand=True, fill="both")
            receive = threading.Thread(target=receive_messages)
            receive.start()
            break
        elif (msg:=message.split("@"))[0] == "Error":
            code = int(msg[1])
            error.configure(text=error_codes[code])
            tim = threading.Thread(target=timer)
            tim.start()
            break
    terminal.configure(state="normal")
    terminal.delete("1.0","end")
    terminal.configure(state="disabled")
    terminal.yview("end")
    if direct == False:
        with open(config_path, 'w') as file:
            if Remember.get() == 1:
                data = f'True\n{usr}${pwsd}'
                file.write(data)
            else:
                data = f'False\n $ '
                file.write(data)
    
def logout():
    global username,client
    notebook.pack_forget()
    username = ""
    client.close()
    Remember.set(0)
    with open(config_path, 'w') as file:
            data = f'False\n $ '
            file.write(data)
    connect()

#===============================================================================================================>Signpage
signpage =ttk.Frame(app)
user = ttk.Label(signpage,text="Username:",font=('Helvetica', 12))
pwd = ttk.Label(signpage,text= "Password:",font=('Helvetica', 12))

user.place(x=230, y=130)
pwd.place(x=230, y=190)

_userinput = ttk.Entry(signpage)
_pwdinput = ttk.Entry(signpage)

_userinput.place(x=310, y=125, w=180)
_pwdinput.place(x=310, y=185, w=180)

button_style = ttk.Style()
button_style.configure("Accent.TButton", font=('Helvetica bold', 12))

signin_but = ttk.Button(signpage, text="Sign-in", style="Accent.TButton", command= lambda: sign("in",_userinput.get(),_pwdinput.get()))
signin_but.place(x=250, y=250, w=100, h=40)

signup_but = ttk.Button(signpage, text="Sign-up", style="Accent.TButton", command= lambda: sign("up",_userinput.get(),_pwdinput.get()))
signup_but.place(x=360, y=250, w=100, h=40)

Remember = tk.IntVar()
check = ttk.Checkbutton(signpage, text="Remember me", variable=Remember,onvalue = 1, offvalue = 0)
check.place(x=320, y=310)

error = ttk.Label(signpage,font=('Helvetica', 10))
error.place(x=320, y=350)

# Notebook
notebook = ttk.Notebook(app)
#===============================================================================================================>Tab 1
tab_1 = ttk.Frame(notebook)
notebook.add(tab_1, text="Home")
terminal = ctk.CTkTextbox(tab_1,border_color="#247f4c",border_width=2,font=ctk.CTkFont(size=14),fg_color="#ffffff")
terminal.configure(state="disabled")
terminal.place(x=30, y=30, w=640, h=300)

_input = ttk.Entry(tab_1)
_input.bind("<Return>", lambda event: send())
_input.place(x=30, y=340, w=640)
#===============================================================================================================>Tab 2
tab_2 = ttk.Frame(notebook)
notebook.add(tab_2, text="Settings")

switch = ttk.Checkbutton(tab_2, text="Mode", style="Switch", command=change_theme)
switch.place(x=100, y=100)

logout_but = ttk.Button(tab_2, text="Log out", style="Accent.TButton", command= lambda: logout())
logout_but.place(x=250, y=250, w=100, h=40)

change_theme()

def connect():
    global client
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_ip,server_port))
        with open(config_path, 'r') as file:
            data = file.read().split("\n")
            if data[0] == "True":
                details = data[1].split("$")
                sign("in",details[0],details[1],direct=True)
            else:
                signpage.pack(expand=True, fill="both")
    except:
        signpage.pack_forget()
        notebook.pack_forget()
        CEpage.pack(expand=True, fill="both")
        
connect()

app.mainloop()