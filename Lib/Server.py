"""import socket
print(socket.gethostname())
import tkinter as tk

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print(screen_width,screen_height)"""
import socket
def server_program():
    # get the hostname
    host = "192.168.140.84"
    port = 9005

    server_socket = socket.socket()
    server_socket.bind((host, port))
    try:
        server_socket.settimeout(1)
        server_socket.listen(2)
        conn, address = server_socket.accept()  # accept new connection
        while True:
            data = conn.recv(128).decode()
            print("from connected user: " + str(data))
            data = input(' -> ')
            conn.send(data.encode())

        conn.close()  # close the connection
    except:
        print("ผมชอบเงี่ยนครับ")


if __name__ == '__main__':
    server_program()
