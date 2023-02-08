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
import logging
from tkinter import messagebox
import customtkinter



API = "https://api.bkf.co.th/APIGateway_DB_BKF/GetCurrentMachineStatus?machineNickName=S11"


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

        try:
            with urllib.request.urlopen(API, timeout=3) as response:
                json_API = json.loads(response.read())
            self.Sever = "Connected"
            with open('Part.json', 'w') as Keep_Part:
                json.dump(json_API, Keep_Part, indent=6)
        except:
            with open('Part.json', 'r') as json_Part:
                json_API = json.loads(json_Part.read())
            self.Sever = "Disconnect"
        self.PartNumber_R = json_API["Right"]["PartNumber"]
        self.BatchNumber_R = json_API["Right"]["BatchNumber"]
        self.PartName_R = json_API["Right"]["PartName"]
        self.CustomerPartNumber_R = json_API["Right"]["CustomerPartNumber"]
        self.MachineName_R = json_API["Right"]["MachineName"]
        self.MoldId_R = json_API["Right"]["MoldId"]
        self.Packing_R = json_API["Right"]["PackingStd"]

        self.PartNumber_L = json_API["Left"]["PartNumber"]
        self.BatchNumber_L = json_API["Left"]["BatchNumber"]
        self.PartName_L = json_API["Left"]["PartName"]
        self.CustomerPartNumber_L = json_API["Left"]["CustomerPartNumber"]
        self.MachineName_L = json_API["Left"]["MachineName"]
        self.MoldId_L = json_API["Left"]["MoldId"]
        self.Packing_L = json_API["Left"]["PackingStd"]

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
        self.CouterPacking_Right = 0
        self.CouterOK_Left = 0
        self.CouterNG_Left = 0
        self.CouterOK_Right = 0
        self.CouterNG_Right = 0
        self.Run_Left = False
        self.Run_Right = False
        self.Image_logo = GetImage()

        self.Color_L = []
        self.ImageSave_L = []
        self.ColorView_L = []
        self.Color_Save_Image_L = []
        self.Result_L = []
        self.Score_L = []

        self.ReadFile()
        self.ReadFileScore()
        self.View()
        self.TCP()
        #self.Reorder()
        self.AddMaster()
        customtkinter.CTkLabel(master=self, text="Vision Inspection", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=50, weight="bold"), corner_radius=10).place(x=140, y=10)
        customtkinter.CTkLabel(master=self, text="v 1.0.0", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=15, weight="bold"), corner_radius=10).place(x=490, y=10)
        self.ImageReal_Left = tk.Button(self, bg="White",command=lambda :self.ViewImagePart(self.API.PartNumber_L))
        self.ImageReal_Left.place(x=0, y=280)
        self.ImageReal_Right = tk.Button(self, bg="White",command=lambda :self.ViewImagePart(self.API.PartNumber_R))
        self.ImageReal_Right.place(x=960, y=280)
        self.image_logo = tk.Button(self, bg="#232323",image=self.Image_logo.BKFImage,command=self.Destory,bd=0)
        self.image_logo.place(x=1755, y=10)
        self.image_logo.bind("<Enter>", self.on_enter)
        self.image_logo.bind("<Leave>", self.on_leave)
        self.Camera()
        #self.scaling_optionemenu = customtkinter.CTkOptionMenu(master=self, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        #self.scaling_optionemenu.place(x=1000, y=80)
        customtkinter.CTkButton(master=self, text="Reorder", text_color="#00B400", hover_color="#B4F0B4", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("#353535"),command=lambda :[self.ReadFile(),self.ReadFileScore(),self.View()]).place(x=1570, y=10)
    def ViewImagePart(self,Partnumber):
        try:
            View = r"Image_Partnumber/" + Partnumber + ".png"
            img = cv.imread(View, cv.COLOR_BGR2RGB)
            cv.imshow(Partnumber, img)
            cv.waitKey(0)
        except:
            View = r"BKF.png"
            img = cv.imread(View, cv.COLOR_BGR2RGB)
            cv.imshow(Partnumber, img)
            cv.waitKey(0)
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
        try:
            self.CouterPoint_Right = 0
            self.dir_path = r"" + GetAPI().PartNumber_R + "\Master"
            for path in os.listdir(self.dir_path):
                if os.path.isfile(os.path.join(self.dir_path, path)):
                    if path.endswith('.bmp'):
                        self.CouterPoint_Right += 1
        except FileNotFoundError as ex:
            self.CouterPoint_Right = 0

    def ReadFileScore(self):
        try:
            with open(GetAPI().PartNumber_L+'/'+ GetAPI().PartNumber_L + '.json', 'r') as json_file:
                Master_Left = json.loads(json_file.read())
            if self.CouterPoint_Left != 0:
                self.Point_Left_L = []
                self.Point_Top_L = []
                self.Point_Right_L = []
                self.Point_Bottom_L = []
                self.Point_Score_L = []
                self.Point_Mode_L = []
                self.Point_Color_L = []
                for L in range(self.CouterPoint_Left):
                    FileFolder_Ok = 'Record/' + GetAPI().PartNumber_L + '/Point' + str(L + 1) + '/OK'
                    path = os.path.join(FileFolder_Ok)
                    try:
                        os.makedirs(path, exist_ok=True)
                    except OSError as error:
                        pass
                    FileFolder_NG = 'Record/' + GetAPI().PartNumber_L + '/Point' + str(L + 1) + '/NG'
                    path = os.path.join(FileFolder_NG)
                    try:
                        os.makedirs(path, exist_ok=True)
                    except OSError as error:
                        pass
                    self.Point_Mode_L.append(Master_Left[L]["Point" + str(L + 1)][0]["Mode"])
                    self.Point_Left_L.append(Master_Left[L]["Point" + str(L + 1)][0]["Left"])
                    self.Point_Top_L.append(Master_Left[L]["Point" + str(L + 1)][0]["Top"])
                    self.Point_Right_L.append(Master_Left[L]["Point" + str(L + 1)][0]["Right"])
                    self.Point_Bottom_L.append(Master_Left[L]["Point" + str(L + 1)][0]["Bottom"])
                    self.Point_Score_L.append(Master_Left[L]["Point" + str(L + 1)][0]["Score"])
                    self.Point_Color_L.append(Master_Left[L]["Point" + str(L + 1)][0]["Color"])
                #print(self.Point_Color_L)
        except:
            pass

        try:
            with open(GetAPI().PartNumber_R + '/' + GetAPI().PartNumber_R + '.json', 'r') as json_file:
                Master_Right = json.loads(json_file.read())
            if self.CouterPoint_Right != 0:
                self.Point_Left_R = []
                self.Point_Top_R = []
                self.Point_Right_R = []
                self.Point_Bottom_R = []
                self.Point_Score_R = []
                self.Point_Mode_R = []
                self.Point_Color_R = []
                for R in range(self.CouterPoint_Right):
                    FileFolder_Ok = 'Record/' + GetAPI().PartNumber_R + '/OK'
                    path = os.path.join(FileFolder_Ok)
                    try:
                        os.makedirs(path, exist_ok=True)
                    except OSError as error:
                        pass
                    FileFolder_NG = 'Record/' + GetAPI().PartNumber_R + '/NG'
                    path = os.path.join(FileFolder_NG)
                    try:
                        os.makedirs(path, exist_ok=True)
                    except OSError as error:
                        pass
                    self.Point_Mode_R.append(Master_Right[R]["Point" + str(R + 1)][0]["Mode"])
                    self.Point_Left_R.append(Master_Right[R]["Point" + str(R + 1)][0]["Left"])
                    self.Point_Top_R.append(Master_Right[R]["Point" + str(R + 1)][0]["Top"])
                    self.Point_Right_R.append(Master_Right[R]["Point" + str(R + 1)][0]["Right"])
                    self.Point_Bottom_R.append(Master_Right[R]["Point" + str(R + 1)][0]["Bottom"])
                    self.Point_Score_R.append(Master_Right[R]["Point" + str(R + 1)][0]["Score"])
                    self.Point_Color_R.append(Master_Right[R]["Point" + str(R + 1)][0]["Color"])
        except:
            pass

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
        customtkinter.CTkButton(master=self, text="NG : " + str(self.CouterNG_Left), text_color="#FFFFFF", hover_color="#C80000", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=50, weight="bold"), corner_radius=10, fg_color=("#FF0000"), command=lambda:self.ViewNG("NG_Right")).place(x=1590, y=180)
        customtkinter.CTkLabel(master=self, text="OK : " + str(self.CouterOK_Left), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=52, weight="bold"), corner_radius=10, fg_color=("#00B400")).place(x=1590, y=100)
        customtkinter.CTkLabel(master=self, text="Packing :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), corner_radius=10).place(x=1360, y=100)
        customtkinter.CTkLabel(master=self, text=str(self.CouterPacking_Left) + "/" + str(self.API.Packing_R), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), corner_radius=10, fg_color=("#00B400")).place(x=1490, y=100)
        #,command=lambda :self.ViewNG_RealTime()
        for Point_Left in range(self.CouterPoint_Left):
            if Point_Left <= 4:
                self.LablePoint_Left = customtkinter.CTkLabel(master=self, text="Point:"+str(Point_Left+1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10,fg_color=("#A9A9A9")).place(x=190*(Point_Left), y=850)
            elif Point_Left <= 9:
                self.LablePoint_Left = customtkinter.CTkLabel(master=self, text="Point:"+str(Point_Left+1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10,fg_color=("#A9A9A9")).place(x=190*(Point_Left-5), y=930)
            elif Point_Left <= 15:
                self.LablePoint_Left = customtkinter.CTkLabel(master=self, text="Point:"+str(Point_Left+1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10,fg_color=("#A9A9A9")).place(x=190 * (Point_Left - 10), y=1010)
        for Point_Right in range(self.CouterPoint_Right):
            if Point_Right <= 4:
                LablePoint_Right = customtkinter.CTkLabel(master=self, text="Point:" + str(Point_Right + 1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("#A9A9A9")).place(x=960+(Point_Right*190), y=850)
            elif Point_Right <= 9:
                LablePoint_Right = customtkinter.CTkLabel(master=self, text="Point:" + str(Point_Right + 1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("#A9A9A9")).place(x=960+((Point_Right-5)*190), y=930)
            elif Point_Right <= 15:
                LablePoint_Right = customtkinter.CTkLabel(master=self, text="Point:" + str(Point_Right + 1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("#A9A9A9")).place(x=960+((Point_Right-10)*190), y=1010)
        #customtkinter.CTkLabel(master=self, text="Point:1", text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("red")).place(x=0, y=850)

        customtkinter.CTkButton(master=self, text="Test Left", text_color="#FFFFFF", hover_color="#C80000", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=20, weight="bold"), corner_radius=10, fg_color=("#FF0000"), command=lambda:self.Processing(1)).place(x=1000, y=20)
        customtkinter.CTkButton(master=self, text="Test Right", text_color="#FFFFFF", hover_color="#C80000", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=20, weight="bold"), corner_radius=10, fg_color=("#FF0000"), command=lambda:self.Processing(2)).place(x=1150, y=20)

    def ViewNG(self,Side):
        ViewNG = Toplevel(self)
        ViewNG.title(Side)
        PointNG = []
        if Side == "NG_Left":
            Counter = self.CouterPoint_Left
        elif Side == "NG_Right":
            Counter = self.CouterPoint_Right
        for i in range(Counter):
            PointNG.append("Point"+str(i+1))
        PointNG_value = customtkinter.StringVar()
        customtkinter.CTkComboBox(ViewNG, variable=PointNG_value, values=PointNG,
                                         corner_radius=10, border_color="#C5C5C5", text_color="#FF3939", border_width=5, width=200, height=50, font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), button_hover_color="#B4F0B4", button_color="#C5C5C5",
                                         dropdown_hover_color="#B4F0B4", dropdown_text_color="#FF3939", dropdown_font=("Microsoft PhagsPa", 20)).place(x=10, y=10)
        customtkinter.CTkButton(ViewNG, text="Commit", text_color="#FF3939", hover_color="#FF9797", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=35, weight="bold"), corner_radius=10, fg_color=("#353535")).place(x=35, y=70)
        ViewNG.configure(background='#232323')
        ViewNG.geometry('220x120')
    """""""""
    def ViewNG_RealTime(self):
        if self.LablePoint_Left.winfo_pointerx() < 155:
            print("Point1")
        if self.LablePoint_Left.winfo_pointerx() > 155 and self.LablePoint_Left.winfo_pointerx() > 155:
            print("Point2")
    print(self.LablePoint_Left.winfo_pointerx())
    """""""""

    def Processing(self,x):
        if x == 1:
            if self.CouterPoint_Left != 0:
                self.Run_Left = True
                Partnumber = self.API.PartNumber_L
                Imagesave = Image.fromarray(self.Camera_Left)
                Imagesave.save("Current_Left.png")
                self.Main(Partnumber)
                self.ViewImage_Snap(Partnumber)
                self.Save_Image(Partnumber)
                self.Clear_Data(Partnumber)
        elif x == 2:
            if self.CouterPoint_Right != 0:
                self.Run_Right = True
                Partnumber = self.API.PartNumber_R
                Imagesave = Image.fromarray(self.Camera_Right)
                Imagesave.save("Current_Right.png")
                self.Main(Partnumber)
                self.ViewImage_Snap(Partnumber)

    def ReadRBG(self,image):
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
        return (int(r_total / count), int(g_total / count), int(b_total / count))

    def ColorScore(self,Data1, Data2):
        total = []
        for i in range(len(Data1)):
            if Data1[i] >= Data2[i]:
                total.append((Data2[i] / Data1[i]) * 1000)
            elif Data2[i] >= Data1[i]:
                total.append((Data1[i] / Data2[i]) * 1000)
        return int(min(total))


    def Process_Outline(self, imgframe, imgTemplate, Left, Top, Right, Bottom):
        img = cv.imread(imgframe, 0)
        template = cv.imread(imgTemplate, 0)
        w, h = template.shape[::-1]
        TemplateThreshold = 0.45
        curMaxVal = 0
        c = 0
        for meth in ['cv.TM_CCOEFF_NORMED']:
            method = eval(meth)
            try:
                crop_image_ = img[(Top - 45):(Bottom + 45), (Left - 45):(Right + 45)]
                res = cv.matchTemplate(crop_image_, template, method)
            except:
                crop_image = img[Top:Bottom, Left:Right]
                res = cv.matchTemplate(crop_image, template, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            if max_val > TemplateThreshold and max_val > curMaxVal:
                curMaxVal = max_val
                curMaxTemplate = c
                curMaxLoc = max_loc
            c = c + 1

        try:
            if curMaxTemplate == -1:
                return (0, (0, 0), 0, 0, 0, 0)
            else:
                # print((curMaxTemplate % 3, curMaxLoc, 1 - int(curMaxTemplate / 3) * 0.2, curMaxVal, w, h))
                return (curMaxTemplate % 3, curMaxLoc, 1 - int(curMaxTemplate / 3) * 0.2, curMaxVal, w, h)
        except:
            return (0, (0, 0), 0, 0, 0, 0)

    def Crop_image_Area(self, imgframe, Left, Top, Right, Bottom,Mode):
        if Mode == "Color":
            image = cv.imread(imgframe,cv.COLOR_BGR2RGB)
        elif Mode == "Shape":
            image = cv.imread(imgframe, 0)
        crop_image = image[Top:Bottom, Left:Right]
        return crop_image

    def Rule_Of_Thirds(self, ROT):
        total = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mod = len(ROT) % 9
        if mod != 0:
            for i in range(mod):
                total[9] += sum(ROT[len(ROT) - mod + i])
        layout = int(len(ROT) / 9)
        for i in range(9):
            i = i + 1
            for j in range(layout * i):
                total[i - 1] += sum(ROT[j])
        point = [total[0]]
        for k in range(8):
            point.append(total[k + 1] - total[k])
        if mod != 0:
            point.append(total[9])
        return point

    def Process_Area(self, Data1, Data2):
            Score_Ture = []
            Chack = []
            swapped = False
            Result_Score = 0
            for i in range(len(Data1)):
                total = (((Data1[i] + Data2[i]) / 2) / Data2[i])
                if total < 1.99:
                    score_out = int(total * 1000)
                    if score_out > 1000:
                        score_out = 1000 - (score_out - 1000)
                        Chack.append(1)
                    else:
                        Chack.append(0)
                    Score_Ture.append(score_out)
                else:
                    Score_Ture.append(0)
                    Chack.append(0)
            return int(min(Score_Ture))


    def Main(self):
        if Partnumber == self.API.PartNumber_L:
            if self.CouterPoint_Left != 0:
                for x in range(self.CouterPoint_Left):
                    image = r'Current_Left.png'
                    self.ImageSave_L.append(cv.imread(image))
                    Template = r"" + GetAPI().PartNumber_L + "\Master""\\""Point" + str(x + 1) + "_Template.bmp"
                    (template, top_left, scale, val, w, h) = self.Process_Outline(image, Template, self.Point_Left_L[x], self.Point_Top_L[x], self.Point_Right_L[x], self.Point_Bottom_L[x])
                    Master_Image = self.Crop_image_Area(image, self.Point_Left_L[x], self.Point_Top_L[x], self.Point_Right_L[x], self.Point_Bottom_L[x],self.Point_Mode_L[x])
                    if scale == 1 and (val * 1000) >= self.Point_Score_L[x]:
                        if self.Point_Mode_L[x] == "Shape":
                            Template_View = cv.imread(Template, 0)
                            Score_Area_Data = self.Process_Area(self.Rule_Of_Thirds(Master_Image), self.Rule_Of_Thirds(Template_View))
                            self.Score_L.append(Score_Area_Data)
                            if Score_Area_Data >= self.Point_Score_L[x]:
                                    color = "Green"
                                    self.ColorView_L.append((0, 255, 0))
                                    self.Color_Save_Image_L.append((0, 255, 0))
                                    self.Result_L.append(1)
                            else:
                                    color = "Red"
                                    self.ColorView_L.append((255, 0, 0))
                                    self.Color_Save_Image_L.append((0, 0, 255))
                                    self.Result_L.append(0)
                        elif self.Point_Mode_L[x] == "Color":
                            Template = cv.imread(Template,cv.COLOR_BGR2RGB)
                            Score_Color = self.ColorScore(self.Point_Color_L[x],self.ReadRBG(Master_Image))
                            self.Score_L.append(Score_Color)
                            if Score_Color >= self.Point_Score_L[x]:
                                color = "Green"
                                self.ColorView_L.append((0, 255, 0))
                                self.Result_L.append(1)
                                self.Color_Save_Image_L.append((0, 255, 0))
                            else:
                                color = "Red"
                                self.ColorView_L.append((255, 0, 0))
                                self.Result_L.append(0)
                                self.Color_Save_Image_L.append((0, 0, 255))
                    else:
                        color = "Red"
                        self.ColorView_L.append((255, 0, 0))
                        self.Score_L.append(0)
                        self.Result_L.append(0)
                        self.Color_Save_Image_L.append((0, 0, 255))
                    if x <= 4:
                               customtkinter.CTkLabel(master=self, text="Point:" + str(x + 1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=(color)).place(x=190 * (x), y=850)
                    elif x <= 9:
                              customtkinter.CTkLabel(master=self, text="Point:" + str(x + 1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=(color)).place(x=190 * (x - 5), y=930)
                    elif x <= 15:
                              customtkinter.CTkLabel(master=self, text="Point:" + str(x + 1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=(color)).place(x=190 * (x - 10), y=1010)

        elif Partnumber == self.API.PartNumber_R:
            if self.CouterPoint_Right != 0:
                self.Color_R = []
                self.ImageSave_R = []
                self.ColorView_R = []
                self.Color_Save_Image_R = []
                self.Result_R = []
                self.Score_R = []
                for x in range(self.CouterPoint_Right):
                    image = r'Current_Right.png'
                    self.ImageSave_R.append(cv.imread(image))
                    Template = r"" + GetAPI().PartNumber_R + "\Master""\\""Point" + str(x + 1) + "_Template.bmp"
                    (template, top_left, scale, val, w, h) = self.Process_Outline(image, Template, self.Point_Left_R[x], self.Point_Top_R[x], self.Point_Right_R[x], self.Point_Bottom_R[x])
                    Master_Image = self.Crop_image_Area(image, self.Point_Left_R[x], self.Point_Top_R[x], self.Point_Right_R[x], self.Point_Bottom_R[x], self.Point_Mode_R[x])
                    if scale == 1 and (val * 1000) >= self.Point_Score_R[x]:
                        if self.Point_Mode_R[x] == "Shape":
                            Template_View = cv.imread(Template, 0)
                            Score_Area_Data = self.Process_Area(self.Rule_Of_Thirds(Master_Image), self.Rule_Of_Thirds(Template_View))
                            self.Score_R.append(Score_Area_Data)
                            if Score_Area_Data >= self.Point_Score_R[x]:
                                color = "Green"
                                self.ColorView_R.append((0, 255, 0))
                                self.Color_Save_Image_R.append((0,255,0))
                                self.Result_R.append(1)
                            else:
                                color = "Red"
                                self.ColorView_R.append((255, 0, 0))
                                self.Color_Save_Image_R.append((0, 0, 255))
                                self.Result_R.append(0)
                        elif self.Point_Mode_R[x] == "Color":
                            Template = cv.imread(Template, cv.COLOR_BGR2RGB)
                            Score_Color = self.ColorScore(self.Point_Color_R[x], self.ReadRBG(Master_Image))
                            self.Score_R.append(Score_Color)
                            if Score_Color >= self.Point_Score_R[x]:
                                color = "Green"
                                self.ColorView_R.append((0, 255, 0))
                                self.Result_R.append(1)
                                self.Color_Save_Image_R.append((0, 255, 0))
                            else:
                                color = "Red"
                                self.ColorView_R.append((255, 0, 0))
                                self.Result_R.append(0)
                                self.Color_Save_Image_R.append((0, 0, 255))
                    else:
                        color = "Red"
                        self.ColorView_R.append((255, 0, 0))
                        self.Score_R.append(0)
                        self.Result_R.append(0)
                        self.Color_Save_Image_R.append((0, 0, 255))
                    if x <= 4:
                        customtkinter.CTkLabel(master=self, text="Point:" + str(x + 1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=(color)).place(x=960 + (x * 190), y=850)
                    elif x <= 9:
                        customtkinter.CTkLabel(master=self, text="Point:" + str(x + 1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=(color)).place(x=960 + ((x - 5) * 190), y=930)
                    elif x <= 15:
                        customtkinter.CTkLabel(master=self, text="Point:" + str(x + 1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=(color)).place(x=960 + ((x - 10) * 190), y=1010)

    def Save_Image(self,Partnumber):
        named_tuple = time.localtime()
        Date = time.strftime("%Y%m%d", named_tuple)
        Time = time.strftime("%Y%m%d%H%M%S", named_tuple)
        if Partnumber == self.API.PartNumber_L:
            for L in range(self.CouterPoint_Left):
                cv.rectangle(self.ImageSave_L[L], (self.Point_Left_L[L], self.Point_Top_L[L]), (self.Point_Right_L[L], self.Point_Bottom_L[L]), self.Color_Save_Image_L[L], 3)
                cv.putText(self.ImageSave_L[L], "Mode : " + self.Point_Mode_L[L], (10, 25), cv.FONT_HERSHEY_SIMPLEX, 1, self.Color_Save_Image_L[L], 2)
                cv.putText(self.ImageSave_L[L], "Score : " + str(self.Score_L[L]) + " / " + str(self.Point_Score_L[L]), (10, 55), cv.FONT_HERSHEY_SIMPLEX, 1, self.Color_Save_Image_L[L], 2)
                cv.putText(self.ImageSave_L[L], "Time : " + str(Time) + "", (10, 85), cv.FONT_HERSHEY_SIMPLEX, 1, self.Color_Save_Image_L[L], 2)
                if L <= 8 :
                    Point = "0"
                else :
                    Point = ""
                if self.Result_L[L] == 1:
                        cv.imwrite('Record/'+ Partnumber + '/OK/' + Time + '_P' +Point+str(L + 1) + '.jpg', self.ImageSave_L[L])
                else:
                        cv.imwrite('Record/'+ Partnumber + '/NG/' + Time + '_P' +Point+str(L + 1) + '.jpg', self.ImageSave_L[L])

        elif Partnumber == self.API.PartNumber_R:
            for R in range(self.CouterPoint_Right):
                cv.rectangle(self.ImageSave_R[R], (self.Point_Left_R[R], self.Point_Top_R[R]), (self.Point_Right_R[R], self.Point_Bottom_R[R]), self.Color_Save_Image_R[R], 3)
                cv.putText(self.ImageSave_R[R], "Mode : " + self.Point_Mode_R[R], (10, 25), cv.FONT_HERSHEY_SIMPLEX, 1, self.Color_Save_Image_R[R], 2)
                cv.putText(self.ImageSave_R[R], "Score : " + str(self.Score_R[R]) + " / " + str(self.Point_Score_R[R]), (10, 55), cv.FONT_HERSHEY_SIMPLEX, 1, self.Color_Save_Image_R[R], 2)
                cv.putText(self.ImageSave_R[R], "Time : " + str(Time) + "", (10, 85), cv.FONT_HERSHEY_SIMPLEX, 1, self.Color_Save_Image_R[R], 2)
                if R <= 8 :
                    Point = "0"
                else :
                    Point = ""
                if self.Result_R[R] == 1:
                    cv.imwrite('Record/' + Partnumber + '/OK/' + Time + '_P'+Point+str(s + 1) + '.jpg', self.ImageSave_R[R])
                else:
                    cv.imwrite('Record/' + Partnumber + '/NG/' + Time + '_P'+Point+ str(s + 1) + '.jpg', self.ImageSave_R[R])



    def ViewImage_Snap(self,Partnumber):
        if Partnumber == self.API.PartNumber_L:
            image = cv.imread("Current_Left.png")
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            for s in range(self.CouterPoint_Left):
                cv.rectangle(image, (self.Point_Left_L[s], self.Point_Top_L[s]), (self.Point_Right_L[s], self.Point_Bottom_L[s]), self.ColorView_L[s], 2)
                cv.putText(image, "P:" + str(s + 1)+" S:"+str(self.Score_L[s]), (self.Point_Left_L[s], self.Point_Top_L[s]), cv.FONT_HERSHEY_SIMPLEX, 0.7, self.ColorView_L[s], 2)
            im = Image.fromarray(image)
            im = im.resize((950, 520))
            image = ImageTk.PhotoImage(image=im)
            self.ImageReal_Left.imgtk = image
            self.ImageReal_Left.configure(image=image)
        elif Partnumber == self.API.PartNumber_R:
            image = cv.imread("Current_Right.png")
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            for s in range(self.CouterPoint_Right):
                cv.rectangle(image, (self.Point_Left_R[s], self.Point_Top_R[s]), (self.Point_Right_R[s], self.Point_Bottom_R[s]), self.ColorView_R[s], 2)
                cv.putText(image, "P:" + str(s + 1)+" S:"+str(self.Score_R[s]), (self.Point_Left_R[s], self.Point_Top_R[s]), cv.FONT_HERSHEY_SIMPLEX, 0.7, self.ColorView_R[s], 2)
            im = Image.fromarray(image)
            im = im.resize((950, 520))
            image = ImageTk.PhotoImage(image=im)
            self.ImageReal_Right.imgtk = image
            self.ImageReal_Right.configure(image=image)

    def Clear_Data(self,Partnumber):
        self.Color_L.clear()
        self.ImageSave_L.clear()
        self.ColorView_L.clear()
        self.Color_Save_Image_L.clear()
        self.Result_L.clear()
        self.Score_L.clear()

    def on_enter(self, event):  
        self.image_logo.configure(image=self.Image_logo.ExitImage)

    def on_leave(self, enter):
        self.image_logo.configure(image=self.Image_logo.BKFImage)

    def Destory(self):
        app.destroy()

    def Camera(self):
        self.Camera_Left = cv.cvtColor(frame0.read()[1], cv.COLOR_BGR2RGB)
        Left = Image.fromarray(self.Camera_Left)
        Resize_Left = Left.resize((950, 520))
        self.LeftCommit = ImageTk.PhotoImage(image=Resize_Left)
        self.Camera_Right = cv.cvtColor(frame1.read()[1], cv.COLOR_BGR2RGB)
        Right = Image.fromarray(self.Camera_Right)
        Resize_Right = Right.resize((950, 520))
        self.RightCommit = ImageTk.PhotoImage(image=Resize_Right)
        if self.Run_Left == False and self.Run_Right == False:
            self.ImageReal_Left.imgtk = self.LeftCommit
            self.ImageReal_Left.configure(image=self.LeftCommit)
            self.ImageReal_Right.imgtk = self.RightCommit
            self.ImageReal_Right.configure(image=self.RightCommit)
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
                    Mode = Mode_value.get()
                    if str.isdigit(Score) and int(Score) >= 500:
                        if Side.get() == 1:
                            Partnumber = self.API.PartNumber_R
                            Imagesave = Image.fromarray(self.Camera_Right)
                        else:
                            Partnumber = self.API.PartNumber_L
                            Imagesave = Image.fromarray(self.Camera_Left)
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
                                        self.Master(Left, Top, Right, Bottom, Score, Point, Emp_ID,Mode,Partnumber)
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
                Side_Right = customtkinter.CTkRadioButton(SaveMaster, variable=Side, value=1,text="Right",font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=30, weight="bold"), text_color="#00B400")
                Side_Right.place(x=120, y=220)

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

    def Crop_image(self, imgframe, Left, Top, Right, Bottom):
        image = cv.imread(imgframe,cv.COLOR_BGR2RGB)
        crop_image = image[Top:Bottom, Left:Right]
        return crop_image


    def Master(self, Left, Top, Right, Bottom, Score, Point, Emp_ID,Mode ,Partnumber):
        Score = int(Score)
        image = r'Current.png'
        Master_Image = self.Crop_image(image, Left, Top, Right, Bottom)
        try:
            with open(Partnumber+'/'+Partnumber+'.json', 'r') as json_file:
                item = json.loads(json_file.read())
                for i in range(16):
                    str_ = str(i)
                    try:
                        if Point == "Point" + str_:
                            i = i - 1
                            item[i]["Point" + str_][0]["Mode"] = Mode
                            item[i]["Point" + str_][0]["Emp ID"] = Emp_ID
                            item[i]["Point" + str_][0]["Left"] = Left
                            item[i]["Point" + str_][0]["Top"] = Top
                            item[i]["Point" + str_][0]["Right"] = Right
                            item[i]["Point" + str_][0]["Bottom"] = Bottom
                            item[i]["Point" + str_][0]["Score"] = Score
                            item[i]["Point" + str_][0]["Color"] = self.ReadRBG(Master_Image)
                            with open(Partnumber+'/'+Partnumber+'.json', 'w') as json_file:
                                json.dump(item, json_file, indent=6)
                    except:
                        # item.append({''+Point+'': [{"Camera": "",'Left': "",'Top': "","Right": "","Bottom": "",'Score': ""}]}
                        with open(Partnumber+'/'+Partnumber+'.json', 'r') as json_file:
                            item = json.loads(json_file.read())
                        try:
                            logging.debug(item[i - 1])
                            item.append({'' + Point + '': [
                                {"Emp ID": Emp_ID, "Mode":Mode, 'Left': Left, 'Top': Top, "Right": Right, "Bottom": Bottom, 'Score': Score,'Color': self.ReadRBG(Master_Image)}]})
                            with open(Partnumber+'/'+Partnumber+'.json', 'w') as json_file:
                                json.dump(item, json_file, indent=6)
                        except:
                            pass
        except FileNotFoundError as exc:
            if Point == "Point1":
                item = [
                    {'' + Point + '': [
                        {"Emp ID": Emp_ID, "Mode":Mode, 'Left': Left, 'Top': Top, "Right": Right, "Bottom": Bottom, 'Score': Score, 'Color': self.ReadRBG(Master_Image)}]}]
                with open(Partnumber+'/'+Partnumber+'.json', 'w') as json_file:
                    json.dump(item, json_file, indent=6)



if __name__ == "__main__":
    app = App()
    app.mainloop()
