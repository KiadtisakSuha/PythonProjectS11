import socket
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import json
with open('Setting Paramiter.json', 'r') as json_file:
    Setting_Paramiter = json.loads(json_file.read())
Quantity_Cam = Setting_Paramiter[0]["Quantity_Cam"]
Board_Name = Setting_Paramiter[0]["Board_Name"]
Machine = Setting_Paramiter[0]["MachineName"]
Mode = Setting_Paramiter[0]["Mode"]
Port = Setting_Paramiter[0]["Port"]
IP = Setting_Paramiter[0]["IP"]


host = IP
port = Port
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Machine Vision Inspection Test TCP client')
        self.geometry("650x200+0+0")
        self.Data = tk.StringVar()  # string variable
        self.Entryclient_socket = ttk.Combobox(self, font="Arial",  textvariable=self.Data)
        self.Entryclient_socket.configure(font=("Arial", 30))
        self.Entryclient_socket.place(x=20, y=10, width=250, height=50)
        self.Entryclient_socket['values'] = ('Vision',
                                  'PartNumber',
                                  'Snap01',
                                  'Snap02',
                                  'Snap03',)
        self.buttonLogin = tk.Button(self, text="Submit", command=self.client_program)
        self.buttonLogin.configure(font=("Arial", 30))
        self.buttonLogin.configure(justify="center", foreground="green")
        self.buttonLogin.place(x=20, y=80)

        self.Received = tk.Label(self,text="Received",foreground="green")
        self.Received.configure(font=("Arial", 20))
        self.Received.place(x=280,y=10)
        self.client_socket = socket.socket()
        self.client_socket.connect((host, port))

    def client_program(self):
        self.client_socket.send(self.Data.get().encode())
        self.xxx = self.client_socket.recv(1024).decode()
        self.Received.configure(text=self.xxx)

if __name__ == '__main__':
    app = App()
    app.mainloop()


"""
def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 9000  # socket server port number
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    message = input(" -> ")  # take input
    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
        print('Received from server: ' + data)  # show in terminal
        message = input(" -> ")  # again take input
    client_socket.close()  # close the connection"""