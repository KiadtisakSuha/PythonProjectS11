"""import socket
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
        self.buttonLogin = tk.Button(self, text="Submit", command=self.server_program)
        self.buttonLogin.configure(font=("Arial", 30))
        self.buttonLogin.configure(justify="center", foreground="green")
        self.buttonLogin.place(x=20, y=80)

        self.Received = tk.Label(self,text="Received",foreground="green")
        self.Received.configure(font=("Arial", 20))
        self.Received.place(x=280,y=10)
        self.client_socket = socket.socket()
        self.client_socket.connect((host, port))

    def server_program(self):
        self.client_socket.send(self.Data.get().encode())
        self.xxx = self.client_socket.recv(1024).decode()
        self.Received.configure(text=self.xxx)"""

"""if __name__ == '__main__':
    app = App()
    app.mainloop()"""


import socket
def server_program():
    # get the hostname
    host = "192.168.140.84"
    port = 9005

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.settimeout(1)
    server_socket.listen(2)
    conn, address = server_socket.accept()
    while True:
            data = conn.recv(128).decode()
            print("from connected user: " + str(data))
            data = input(' -> ')
            conn.send(data.encode())

    conn.close()  # close the connection



if __name__ == '__main__':
    server_program()
