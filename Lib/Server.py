"""import socket
print(socket.gethostname())
import tkinter as tk

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print(screen_width,screen_height)"""
"""def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 9000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        data = conn.recv(128).decode()
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()"""
import cv2 as cv
class ColorProcessing:
    @staticmethod
    def ReadRBG(image):
        r_total = 0
        g_total = 0
        b_total = 0
        count = 0
        for i in range(len(image)):
            for j in range(len(image[i])):
                r_total += image[i][j][0]
                g_total += image[i][j][1]
                b_total += image[i][j][2]
                count += 1
        return int(r_total / count), int(g_total / count), int(b_total / count)

    @staticmethod
    def ColorScore(Data1, Data2):
        total = []
        for i in range(len(Data1)):
            if Data1[i] >= Data2[i]:
                total.append((Data2[i] / Data1[i]) * 1000)
            elif Data2[i] >= Data1[i]:
                total.append((Data1[i] / Data2[i]) * 1000)
            print(total)
        return int(min(total))

Color = [156,153,155]
image = "Point1_Template.bmp"
image = cv.imread(image, 1)
Score_Color = ColorProcessing.ColorScore(Color, ColorProcessing.ReadRBG(image))
print(Score_Color)
cv.imshow("image",image)
cv.waitKey(0)