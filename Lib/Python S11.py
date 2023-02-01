import time
import os
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter
from tkinter.ttk import Notebook, Style
#import pyvisa
import cv2 as cv
from PIL import ImageTk
from PIL import Image
import json
import urllib.request
from threading import Timer
import urllib.request
import logging
from tkinter import messagebox
import customtkinter



API = "http://192.168.1.48:89/RobotAPI/GetPart?machineId=E09"


font = "arial"
Camera_Qutity = 2
if Camera_Qutity == 1:
    frame0 = cv.VideoCapture(0,cv.CAP_DSHOW)
    frame0.set(cv.CAP_PROP_FRAME_WIDTH, 1980)
    frame0.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
elif Camera_Qutity ==2:
    frame0 = cv.VideoCapture(0, cv.CAP_DSHOW)
    frame1 = cv.VideoCapture(1, cv.CAP_DSHOW)
    frame0.set(cv.CAP_PROP_FRAME_WIDTH, 1980)
    frame0.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    frame1.set(cv.CAP_PROP_FRAME_WIDTH, 1980)
    frame1.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)


class GetEmp():
    def __int__(self):
        dirName = 'Information'
        try:
            os.mkdir(dirName)
        except FileExistsError:
            pass

        try:
            with urllib.request.urlopen("http://192.168.1.48:89/RobotAPI/GetEmp") as response:
                json_Emp = json.loads(response.read())
            with open('Information/Operator.json', 'w') as Operator:
                json.dump(json_Emp, Operator, indent=6)
        except:
            pass


class GetAPI():
    def __init__(self):
        """""""""
        try:
            with urllib.request.urlopen(API, timeout=1) as response:
                json_API = json.loads(response.read())
            self.Sever = "Connected"
            with open('Part.json', 'w') as Keep_Part:
                json.dump(json_API, Keep_Part)
        except:
            with open('Part.json', 'r') as json_Part:
                json_API = json.loads(json_Part.read())
            self.Sever = "Disconnect"
        self.PartNumber = json_API[0]["PartNumber"]
        self.BatchNumber = json_API[0]["BatchNumber"]
        self.PartName = json_API[0]["PartName"]
        self.CustomerPartNumber = json_API[0]["CustomerPartNumber"]
        self.MachineName = json_API[0]["MachineName"]
        self.MoldId = json_API[0]["MoldId"]
        self.Packing = json_API[0]["PackingStd"]
        """""""""
        with open('Parttest.json', 'r') as json_Part:
            json_API = json.loads(json_Part.read())
        self.Sever = "Connected"
        self.PartNumber_R = json_API[0]["Rigth"][0]["PartNumber"]
        self.BatchNumber_R = json_API[0]["Rigth"][0]["BatchNumber"]
        self.PartName_R = json_API[0]["Rigth"][0]["PartName"]
        self.CustomerPartNumber_R = json_API[0]["Rigth"][0]["CustomerPartNumber"]
        self.MachineName_R = json_API[0]["Rigth"][0]["MachineName"]
        self.MoldId_R = json_API[0]["Rigth"][0]["MoldId"]
        self.Packing_R = json_API[0]["Rigth"][0]["PackingStd"]

        self.PartNumber_L = json_API[1]["Left"][0]["PartNumber"]
        self.BatchNumber_L = json_API[1]["Left"][0]["BatchNumber"]
        self.PartName_L = json_API[1]["Left"][0]["PartName"]
        self.CustomerPartNumber_L = json_API[1]["Left"][0]["CustomerPartNumber"]
        self.MachineName_L = json_API[1]["Left"][0]["MachineName"]
        self.MoldId_L = json_API[1]["Left"][0]["MoldId"]
        self.Packing_L = json_API[1]["Left"][0]["PackingStd"]

class GetImage():
    def __init__(self):
        self.BKFImage = Image.open(r"BKF.png")
        self.BKFImage = self.BKFImage.resize((140, 55))
        self.BKFImage = ImageTk.PhotoImage(self.BKFImage)

        self.ExitImage = Image.open(r"Exit.PNG")
        self.ExitImage = self.ExitImage.resize((140, 55))
        self.ExitImage = ImageTk.PhotoImage(self.ExitImage)

class App(customtkinter.CTk):
    customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
    def __init__(self):
        super().__init__()
        self.title('Machine Vision Inspection 1.0.0')
        self.geometry("1920x1020+0+0")
        #self.state('zoomed')
        self.attributes('-fullscreen', True)
        self.CouterPacking_Left = 0
        self.CouterPacking_Rigth = 0
        self.CouterOK_Left = 0
        self.CouterNG_Left = 0
        self.CouterOK_Rigth = 0
        self.CouterNG_Rigth = 0
        self.CouterPoint_Rigth = 0
        self.Image_logo = GetImage()

        self.ReadFile()
        self.View()
        self.TCP()
        #self.Reorder()
        self.AddMaster()

        customtkinter.CTkLabel(master=self, text="Vision Inspection", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=50, weight="bold"), corner_radius=10).place(x=140, y=10)
        customtkinter.CTkLabel(master=self, text="v 1.0.0", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=15, weight="bold"), corner_radius=10).place(x=490, y=10)
        self.ImageRealTime_1 = tk.Label(self, bg="White")
        self.ImageRealTime_1.place(x=0, y=280)
        self.ImageRealTime_2 = tk.Label(self, bg="White")
        self.ImageRealTime_2.place(x=960, y=280)
        self.image_logo = tk.Button(self, bg="#232323",image=self.Image_logo.BKFImage,command=self.Destory,bd=0)
        self.image_logo.place(x=1755, y=10)
        self.image_logo.bind("<Enter>", self.on_enter)
        self.image_logo.bind("<Leave>", self.on_leave)
        self.Camera()
        #self.scaling_optionemenu = customtkinter.CTkOptionMenu(master=self, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        #self.scaling_optionemenu.place(x=1000, y=80)


        customtkinter.CTkButton(master=self, text="Reorder", text_color="#00B400", hover_color="#B4F0B4", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("#353535"),command=lambda :[self.ReadFile(),self.View()]).place(x=1570, y=10)
    def ReadFile(self):
        try:
            self.CouterPoint_Left = 0
            self.dir_path = r"" + GetAPI().PartNumber_L + "\Master"
            for path in os.listdir(self.dir_path):
                if os.path.isfile(os.path.join(self.dir_path, path)):
                    if path.endswith('.bmp'):
                        self.CouterPoint_Left += 1
        except FileNotFoundError as ex:
            self.CouterPoint_Left = 0

    def View(self):
        self.API = GetAPI()
        if self.API.Sever == "Connected":
            color = "#00B400"
        else:
            color = "#D8D874"
       # customtkinter.CTkButton(master=self, text="NG : 000"+str(self.CouterNG_Left), text_color="#FFFFFF", hover_color="#C80000", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=50, weight="bold"), corner_radius=10, fg_color=("#FF0000"),command=self.Destory).place(x=680, y=180)
        customtkinter.CTkLabel(master=self, text="S11", text_color=color, font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=65, weight="bold")).place(x=10, y=0)
        #customtkinter.CTkLabel(master=self, text="Server : "+self.API.Sever, text_color=color, font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=30, weight="bold"), corner_radius=10).place(x=1250, y=20)
        #Left
        customtkinter.CTkLabel(master=self, text="BKF Part :" , text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold")).place(x=10, y=100)
        customtkinter.CTkLabel(master=self, text=self.API.PartNumber_L,text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa",size=25,weight="bold"),fg_color=("#00B400"),corner_radius=10).place(x=150,y=100)
        customtkinter.CTkLabel(master=self, text="Customer :",text_color="#00B400",font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25,weight="bold")).place(x=10,y=140)
        customtkinter.CTkLabel(master=self, text=self.API.CustomerPartNumber_L, text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"),fg_color=("#00B400"),corner_radius=10).place(x=150, y=140)
        customtkinter.CTkLabel(master=self, text="Batch :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold")).place(x=10, y=180)
        customtkinter.CTkLabel(master=self, text=self.API.BatchNumber_L, text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"),fg_color=("#00B400"),corner_radius=10).place(x=150, y=180)
        customtkinter.CTkLabel(master=self, text="Part Name :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold")).place(x=10, y=220)
        customtkinter.CTkLabel(master=self, text=self.API.PartName_L[:30], text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"),fg_color=("#00B400"),corner_radius=10).place(x=150, y=220)
        customtkinter.CTkButton(master=self, text="NG : "+str(self.CouterNG_Left), text_color="#FFFFFF", hover_color="#C80000", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=50, weight="bold"), corner_radius=10, fg_color=("#FF0000"),command=lambda:self.ViewNG("NG_Left")).place(x=620, y=180)
        customtkinter.CTkLabel(master=self, text="OK : "+str(self.CouterOK_Left), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=52, weight="bold"), corner_radius=10,fg_color=("#00B400")).place(x=620, y=100)
        customtkinter.CTkLabel(master=self, text="Packing :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), corner_radius=10).place(x=400, y=100)
        customtkinter.CTkLabel(master=self, text=str(self.CouterPacking_Left) +"/"+str(self.API.Packing_L), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), corner_radius=10,fg_color=("#00B400")).place(x=530, y=100)

        #Right
        customtkinter.CTkLabel(master=self, text="BKF Part :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold")).place(x=960, y=100)
        customtkinter.CTkLabel(master=self, text=self.API.PartNumber_R, text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), fg_color=("#00B400"), corner_radius=10).place(x=1100, y=100)
        customtkinter.CTkLabel(master=self, text="Customer :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold")).place(x=960, y=140)
        customtkinter.CTkLabel(master=self, text=self.API.CustomerPartNumber_R, text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), fg_color=("#00B400"), corner_radius=10).place(x=1100, y=140)
        customtkinter.CTkLabel(master=self, text="Batch :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold")).place(x=960, y=180)
        customtkinter.CTkLabel(master=self, text=self.API.BatchNumber_R, text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), fg_color=("#00B400"), corner_radius=10).place(x=1100, y=180)
        customtkinter.CTkLabel(master=self, text="Part Name :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold")).place(x=960, y=220)
        customtkinter.CTkLabel(master=self, text=self.API.PartName_R[:30], text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), fg_color=("#00B400"), corner_radius=10).place(x=1100, y=220)
        customtkinter.CTkButton(master=self, text="NG : " + str(self.CouterNG_Left), text_color="#FFFFFF", hover_color="#C80000", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=50, weight="bold"), corner_radius=10, fg_color=("#FF0000"), command=lambda:self.ViewNG("NG_Rigth")).place(x=1590, y=180)
        customtkinter.CTkLabel(master=self, text="OK : " + str(self.CouterOK_Left), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=52, weight="bold"), corner_radius=10, fg_color=("#00B400")).place(x=1590, y=100)
        customtkinter.CTkLabel(master=self, text="Packing :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), corner_radius=10).place(x=1360, y=100)
        customtkinter.CTkLabel(master=self, text=str(self.CouterPacking_Left) + "/" + str(self.API.Packing_R), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), corner_radius=10, fg_color=("#00B400")).place(x=1490, y=100)
        for Point_Left in range(self.CouterPoint_Left):
            if Point_Left <= 4:
                LablePoint_Left = customtkinter.CTkLabel(master=self, text="Point:"+str(Point_Left+1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10,fg_color=("#A9A9A9")).place(x=190*(Point_Left), y=850)
            elif Point_Left <= 9:
                LablePoint_Left = customtkinter.CTkLabel(master=self, text="Point:"+str(Point_Left+1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10,fg_color=("#A9A9A9")).place(x=190*(Point_Left-5), y=930)
            elif Point_Left <= 15:
                LablePoint_Left = customtkinter.CTkLabel(master=self, text="Point:"+str(Point_Left+1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10,fg_color=("#A9A9A9")).place(x=190*(Point_Left-10), y=1010)
        for Point_Rigth in range(self.CouterPoint_Rigth):
            if Point_Rigth <= 4:
                LablePoint_Rigth = customtkinter.CTkLabel(master=self, text="Point:" + str(Point_Rigth + 1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("#A9A9A9")).place(x=960+(Point_Rigth*190), y=850)
            elif Point_Rigth <= 9:
                LablePoint_Rigth = customtkinter.CTkLabel(master=self, text="Point:" + str(Point_Rigth + 1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("#A9A9A9")).place(x=960+((Point_Rigth-5)*190), y=930)
            elif Point_Rigth <= 15:
                LablePoint_Rigth = customtkinter.CTkLabel(master=self, text="Point:" + str(Point_Rigth + 1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("#A9A9A9")).place(x=960+((Point_Rigth-10)*190), y=1010)
        #customtkinter.CTkLabel(master=self, text="Point:1", text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("red")).place(x=0, y=850)
    def ViewNG(self,Side):
        ViewNG = Toplevel(self)
        ViewNG.title(Side)
        PointNG = []
        if Side == "NG_Left":
            Counter = self.CouterPoint_Left
        elif Side == "NG_Rigth":
            Counter = self.CouterPoint_Rigth
        for i in range(Counter):
            PointNG.append("Point"+str(i+1))
        PointNG_value = customtkinter.StringVar()
        customtkinter.CTkComboBox(ViewNG, variable=PointNG_value, values=PointNG,
                                         corner_radius=10, border_color="#C5C5C5", text_color="#FF3939", border_width=5, width=200, height=50, font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), button_hover_color="#B4F0B4", button_color="#C5C5C5",
                                         dropdown_hover_color="#B4F0B4", dropdown_text_color="#FF3939", dropdown_font=("Microsoft PhagsPa", 20)).place(x=10, y=10)
        customtkinter.CTkButton(ViewNG, text="Commit", text_color="#FF3939", hover_color="#FF9797", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=35, weight="bold"), corner_radius=10, fg_color=("#353535")).place(x=35, y=70)
        ViewNG.configure(background='#232323')
        ViewNG.geometry('220x120')
    def on_enter(self, event):
        self.image_logo.configure(image=self.Image_logo.ExitImage)

    def on_leave(self, enter):
        self.image_logo.configure(image=self.Image_logo.BKFImage)

    def Destory(self):
        app.destroy()

    def Camera(self):
        self.Camera_1 = cv.cvtColor(frame0.read()[1], cv.COLOR_BGR2RGB)
        img_1 = Image.fromarray(self.Camera_1)
        resize_img_1 = img_1.resize((950, 520))
        imgtk_1 = ImageTk.PhotoImage(image=resize_img_1)
        self.ImageRealTime_1.imgtk = imgtk_1
        self.ImageRealTime_1.configure(image=imgtk_1)

        self.Camera_2 = cv.cvtColor(frame1.read()[1], cv.COLOR_BGR2RGB)
        img_2 = Image.fromarray(self.Camera_2)
        resize_img_2 = img_2.resize((950, 520))
        imgtk_2 = ImageTk.PhotoImage(image=resize_img_2)
        self.ImageRealTime_2.imgtk = imgtk_2
        self.ImageRealTime_2.configure(image=imgtk_2)
        self.after(20, self.Camera)
    def AddMaster(self):
        customtkinter.CTkButton(master=self, text="Add-master", text_color="#00B400", hover_color="#B4F0B4", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("#353535"), command=self.SaveMasterNewWindow).place(x=1300, y=10)
    def TCP(self):
        customtkinter.CTkLabel(master=self, text="Read : ", text_color="#00B400",  font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold")).place(x=580, y=30)
        customtkinter.CTkLabel(master=self, text="TCP", text_color="#FFFFFF",  font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), corner_radius=10, fg_color=("#00B400")).place(x=660, y=30)

        customtkinter.CTkLabel(master=self, text="Write : ", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold")).place(x=850, y=30)
        customtkinter.CTkLabel(master=self, text="TCP", text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), corner_radius=10, fg_color=("#00B400")).place(x=940, y=30)

    def SaveMasterNewWindow(self):
        Login = Toplevel(self)
        Login.title("Login")
        Login.configure(background='#232323')
        Login.geometry('220x120')
        Password = tk.StringVar()
        Password.trace("w", lambda *args: character_limit())

        def Loginform():
            with urllib.request.urlopen("http://192.168.1.48:89/RobotAPI/GetEmp") as response:
                json_object = json.loads(response.read())
                id_Emp = []
                for d in json_object:
                    id_Emp.append(d['id_Emp'])
            for i in range(len(id_Emp)):
                if id_Emp[i] == Password.get():
                    return True
            messagebox.showwarning("Password", "Wrong password did not match")
            return False

        def Search():
            if Loginform():
                Login.destroy()
                SaveMaster = Toplevel(self)
                SaveMaster.title("Save Master")
                SaveMaster.configure(background='#232323')
                SaveMaster.geometry('330x450')
                Score_Data_Area = tk.StringVar()
                Score_Data_Area.trace("w", lambda *args: score_limit(Score_Data_Area))
                Score_Data_Outline = tk.StringVar()
                Score_Data_Outline.trace("w", lambda *args: score_limit(Score_Data_Outline))

                def Save_Master():
                    Point = Point_value.get()
                    Emp_ID = Password.get()
                    Score = Score_value.get()
                    if str.isdigit(Score) and int(Score) >= 500:
                        if Side.get() == 1:
                            Partnumber = self.API.PartNumber_R
                            Imagesave = Image.fromarray(self.Camera_1)
                        else:
                            Partnumber = self.API.PartNumber_L
                            Imagesave = Image.fromarray(self.Camera_2)
                        Imagesave.save("Current.png")
                        Create = Partnumber + '/Master'
                        if not os.path.exists(Create):
                            os.makedirs(Create)
                        else:
                            print("")
                        refPt = []
                        cropping = False

                        def click_and_crop(event, x, y, flags, param):
                            global refPt, cropping
                            image = clone.copy()

                            if event == cv.EVENT_LBUTTONDOWN:
                                refPt = [(x, y)]
                                # print(refPt)
                                cropping = True
                            elif event == cv.EVENT_LBUTTONUP:
                                refPt.append((x, y))
                                # print(refPt)
                                cropping = False
                                cv.rectangle(image, refPt[0], refPt[1], (85, 255, 51), 2)
                                cv.imshow(Point, image)
                                if len(refPt) == 2:
                                    roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
                                    x = cv.cvtColor(roi, cv.COLOR_BGR2RGB)
                                    Left = refPt[0][0]
                                    Top = refPt[0][1]
                                    Right = refPt[1][0]
                                    Bottom = refPt[1][1]
                                    img = Image.fromarray(x)
                                    Showtext = cv.putText(image, "Save image " + Point + "", (10, 25),
                                                          cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                                    cv.imshow(Point, Showtext)
                                    img.save('' + Create + '/' + Point + '_Template.bmp')
                                    if Left and Top and Right and Bottom != 0:
                                        self.Master(Left, Top, Right, Bottom, Score, Point, Emp_ID, Partnumber)
                        path = r'Current.png'
                        image = cv.imread(path)
                        clone = image.copy()
                        cv.namedWindow(Point)
                        cv.setMouseCallback(Point, click_and_crop)
                        cv.imshow(Point, image)
                    else:
                        messagebox.showwarning("Score", "Minumun Score 500")

                customtkinter.CTkLabel(SaveMaster, text="Point:", text_color="#00B400",  font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold")).place(x=5, y=26)
                Point_value = customtkinter.StringVar()
                Point_value.set("Point1")
                Point = customtkinter.CTkComboBox(SaveMaster, variable=Point_value, values=['Point1', 'Point2', 'Point3', 'Point4', 'Point5', 'Point6', 'Point7', 'Point8', 'Point9', 'Point10', 'Point11', 'Point12', 'Point13', 'Point14', 'Point15'],
                                                  corner_radius=10, border_color="#C5C5C5", text_color="#00B400", border_width=5, width=200, height=50, font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), button_hover_color="#B4F0B4", button_color="#C5C5C5",
                                                  dropdown_hover_color="#B4F0B4", dropdown_text_color="#00B400", dropdown_font=("Microsoft PhagsPa", 20)).place(x=120, y=20)

                customtkinter.CTkLabel(SaveMaster, text="Mode:", text_color="#00B400",  font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold")).place(x=5, y=102)
                Mode_value = customtkinter.StringVar()
                Mode_value.set("Shape")
                Mode = customtkinter.CTkComboBox(SaveMaster, variable=Mode_value, values=['Shape', 'Color'],
                                                 corner_radius=10, border_color="#C5C5C5", text_color="#00B400", border_width=5, width=200, height=50, font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), button_hover_color="#B4F0B4", button_color="#C5C5C5",
                                                 dropdown_hover_color="#B4F0B4", dropdown_text_color="#00B400", dropdown_font=("Microsoft PhagsPa", 20)).place(x=120, y=100)

                customtkinter.CTkLabel(SaveMaster, text="Side:", text_color="#00B400",  font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold")).place(x=5, y=182)
                #Side_value = customtkinter.StringVar()
                #Side = customtkinter.CTkComboBox(SaveMaster, variable=Side_value, values=['Left', 'Right'],
                                                 #corner_radius=10, border_color="#C5C5C5", text_color="#00B400", border_width=5, width=200, height=50, font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), button_hover_color="#B4F0B4", button_color="#C5C5C5",
                                                 #dropdown_hover_color="#B4F0B4", dropdown_text_color="#00B400", dropdown_font=("Microsoft PhagsPa", 20)).place(x=120, y=180)
                Side = tkinter.IntVar(value=0)
                Side_Left = customtkinter.CTkRadioButton(SaveMaster, variable=Side, value=0 ,text="Left ",font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=30, weight="bold"), text_color="#00B400")
                Side_Left.place(x=120, y=180)
                Side_Rigth = customtkinter.CTkRadioButton(SaveMaster, variable=Side, value=1,text="Rigth",font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=30, weight="bold"), text_color="#00B400")
                Side_Rigth.place(x=120, y=220)

                customtkinter.CTkLabel(SaveMaster, text="Score:", text_color="#00B400",  font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold")).place(x=5, y=290)
                Score_value = customtkinter.StringVar()
                Score_value.set("800")
                customtkinter.CTkEntry(SaveMaster, width=200, height=50, placeholder_text="Score", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=30, weight="bold"), textvariable=Score_value, text_color="#00B400").place(x=120, y=285)
                Save = customtkinter.CTkButton(SaveMaster, text="Save", text_color="#00B400", hover_color="#B4F0B4", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=60, weight="bold"), corner_radius=10, fg_color=("#353535"), command=Save_Master).place(x=100, y=360)

                def score_limit(*args):
                    s = Score_value.get()
                    if str.isdigit(s):
                        if len(s) > 3:
                            Score_value.set(s[:3])
                    else:
                        Score_value.set(s[:0])

                Score_value.trace("w", score_limit)
                SaveMaster.mainloop()

        def character_limit():
            try:
                if len(Password.get()) > 0:
                    Password.set(Password.get()[6])
            except:
                pass
        #text_color="#00B400", hover_color="#B4F0B4", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("#353535")
        customtkinter.CTkEntry(Login, width=200, height=50, corner_radius=10, placeholder_text="Password", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), show='*', textvariable=Password).place(x=10, y=5)
        customtkinter.CTkButton(Login, text="Login", text_color="#00B400", hover_color="#B4F0B4", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=30, weight="bold"), corner_radius=10, fg_color=("#353535"), command=Search).place(x=40, y=70)
        Login.mainloop()

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def Master(self, Left, Top, Right, Bottom, Score, Point, Emp_ID, Partnumber):
        Score = int(Score)
        try:
            with open(Partnumber+'/'+Partnumber+'.json', 'r') as json_file:
                item = json.loads(json_file.read())
                for i in range(16):
                    str_ = str(i)
                    try:
                        if Point == "Point" + str_:
                            i = i - 1
                            item[i]["Point" + str_][0]["Emp ID"] = Emp_ID
                            item[i]["Point" + str_][0]["Left"] = Left
                            item[i]["Point" + str_][0]["Top"] = Top
                            item[i]["Point" + str_][0]["Right"] = Right
                            item[i]["Point" + str_][0]["Bottom"] = Bottom
                            item[i]["Point" + str_][0]["Score"] = Score
                            with open(Partnumber+'/'+Partnumber+'.json', 'w') as json_file:
                                json.dump(item, json_file, indent=6)
                    except:
                        # item.append({''+Point+'': [{"Camera": "",'Left': "",'Top': "","Rigth": "","Bottom": "",'Score': ""}]}
                        with open(Partnumber+'/'+Partnumber+'.json', 'r') as json_file:
                            item = json.loads(json_file.read())
                        try:
                            logging.debug(item[i - 1])
                            item.append({'' + Point + '': [
                                {"Emp ID": Emp_ID, 'Left': Left, 'Top': Top, "Right": Right, "Bottom": Bottom, 'Score': Score}]})
                            with open(Partnumber+'/'+Partnumber+'.json', 'w') as json_file:
                                json.dump(item, json_file, indent=6)
                        except:
                            pass
        except FileNotFoundError as exc:
            if Point == "Point1":
                item = [
                    {'' + Point + '': [
                        {"Emp ID": Emp_ID, 'Left': Left, 'Top': Top, "Right": Right, "Bottom": Bottom, 'Score': Score}]}]
                with open(Partnumber+'/'+Partnumber+'.json', 'w') as json_file:
                    json.dump(item, json_file, indent=6)



if __name__ == "__main__":
    app = App()
    app.mainloop()
