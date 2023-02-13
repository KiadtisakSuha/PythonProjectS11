import time
import os
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter
from tkinter.ttk import Notebook, Style
# import pyvisa
import cv2 as cv
from PIL import ImageTk
from PIL import Image
import json
import urllib.request
from threading import Timer
import logging
from tkinter import messagebox
import customtkinter
import socket

#API = "https://api.bkf.co.th/APIGateway_DB_BKF/GetCurrentMachineStatus?machineNickName=S11"

font = "arial"
Camera_Qutity = 2
if Camera_Qutity == 1:
    frame0 = cv.VideoCapture(0, cv.CAP_DSHOW)
    frame0.set(cv.CAP_PROP_FRAME_WIDTH, 1024)
    frame0.set(cv.CAP_PROP_FRAME_HEIGHT, 768)
elif Camera_Qutity == 2:
    frame0 = cv.VideoCapture(0, cv.CAP_DSHOW)
    frame1 = cv.VideoCapture(1, cv.CAP_DSHOW)
    frame0.set(cv.CAP_PROP_FRAME_WIDTH, 1024)
    frame0.set(cv.CAP_PROP_FRAME_HEIGHT, 768)
    frame1.set(cv.CAP_PROP_FRAME_WIDTH, 1024)
    frame1.set(cv.CAP_PROP_FRAME_HEIGHT, 768)


class GetEmp:
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


class GetAPI:
    @staticmethod
    def API():
        method = ["PartNumber", "BatchNumber", "PartName", "CustomerPartNumber", "PackingStd"]
        side = []
        data = []
        api_url = "https://api.bkf.co.th/APIGateway_DB_BKF/GetCurrentMachineStatus?machineNickName=E15"
        data_file = 'Part.json'

        try:
            with urllib.request.urlopen(api_url, timeout=1) as response:
                json_api = json.loads(response.read())
            status = "Connected"
            with open(data_file, 'w') as f:
                json.dump(json_api, f, indent=6)
        except:
            with open(data_file, 'r') as f:
                json_api = json.loads(f.read())
            status = "Disconnected"

        for s in json_api:
            side.append(s)
            for key in method:
                data.append(json_api[s][key])

        return status, side, data


class GetImage:
    def __init__(self):
        self.BKFImage = Image.open(r"BKF.png")
        self.BKFImage = self.BKFImage.resize((140, 55))
        self.BKFImage = ImageTk.PhotoImage(self.BKFImage)

        self.ExitImage = Image.open(r"Exit.PNG")
        self.ExitImage = self.ExitImage.resize((140, 55))
        self.ExitImage = ImageTk.PhotoImage(self.ExitImage)

class InfiniteTimer():
    def __init__(self, seconds, target):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target
        self.thread = None

    def _handle_target(self):
        self.is_running = True
        self.target()
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        if self._should_continue:
            self.thread = Timer(self.seconds, self._handle_target)
            self.thread.start()

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()
        else:
            pass

    def cancel(self):
        if self.thread is not None:
            self._should_continue = False
            self.thread.cancel()
        else:
            pass

class Main:
    @staticmethod
    def Main(Partnumber ,FileImage,Counter,Mode,Left,Top,Right,Bottom,Score_Set,Color_Data):
            Color = []
            ImageSave = []
            ColorView = []
            Color_Save_Image = []
            Result = []
            Score = []
            if Counter != 0:
                for x in range(Counter):
                    ImageSave.append(cv.imread(FileImage))
                    Template = r"" + Partnumber + "\Master""\\""Point" + str(x + 1) + "_Template.bmp"
                    (template, top_left, scale, val, w, h) = Shape.Process_Outline(FileImage, Template, Left[x], Top[x], Right[x], Bottom[x])
                    Master_Image = CropImage.Crop_Image(FileImage, Left[x], Top[x], Right[x], Bottom[x], Mode[x])
                    if scale == 1 and (val * 1000) >= Score_Set[x]:
                        if Mode[x] == "Shape":
                            Template_View = cv.imread(Template, 0)
                            Score_Area_Data = Shape.Process_Area(Shape.Rule_Of_Thirds(Master_Image), Shape.Rule_Of_Thirds(Template_View))
                            Score.append(Score_Area_Data)
                            if Score_Area_Data >= Score_Set[x]:
                                ColorView.append((0, 255, 0))
                                Color_Save_Image.append((0, 255, 0))
                                Result.append(1)
                            else:
                                ColorView.append((255, 0, 0))
                                Color_Save_Image.append((0, 0, 255))
                                Result.append(0)
                        elif Mode[x] == "Color":
                            Score_Color = Color.ColorScore(Color_Data[x], Color.ReadRBG(Master_Image))
                            Score.append(Score_Color)
                            if Score_Color >= Score_Set[x]:
                                ColorView.append((0, 255, 0))
                                Result.append(1)
                                Color_Save_Image.append((0, 255, 0))
                            else:
                                ColorView.append((255, 0, 0))
                                Result.append(0)
                                Color_Save_Image.append((0, 0, 255))
                    else:
                        ColorView.append((255, 0, 0))
                        Score.append(0)
                        Result.append(0)
                        Color_Save_Image.append((0, 0, 255))
                return ImageSave, ColorView, Color_Save_Image, Result, Score

    @staticmethod
    def ViewImage_Snap(Filename,Counter,Left,Top,Right,Bottom,Score,Color):
            image = cv.imread(Filename)
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            for s in range(Counter):
                cv.rectangle(image, (Left[s], Top[s]), (Right[s], Bottom[s]), Color[s], 2)
                cv.putText(image, "P:" + str(s + 1) + " S:" + str(Score[s]), (Left[s], Top[s]), cv.FONT_HERSHEY_SIMPLEX, 0.7, Color[s], 2)
            im = Image.fromarray(image)
            im = im.resize((950, 520))
            image = ImageTk.PhotoImage(image=im)
            return image

    @staticmethod
    def ShowResult(Result):
            for i in range(len(Result)):
                if Result[i] == 1:
                    if i == len(Result) - 1:
                        return True
                else:
                    return False
                    break



class Shape:

    @staticmethod
    def Process_Area(Data1, Data2):
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

    @staticmethod
    def Rule_Of_Thirds(ROT):
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

    @staticmethod
    def Process_Outline(imgframe, imgTemplate, Left, Top, Right, Bottom):
        global curMaxLoc
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
                return 0, (0, 0), 0, 0, 0, 0
            else:
                # print((curMaxTemplate % 3, curMaxLoc, 1 - int(curMaxTemplate / 3) * 0.2, curMaxVal, w, h))
                return curMaxTemplate % 3, curMaxLoc, 1 - int(curMaxTemplate / 3) * 0.2, curMaxVal, w, h
        except:
            return 0, (0, 0), 0, 0, 0, 0


class CropImage:
    @staticmethod
    def Crop_Image(Imageframe, Left, Top, Right, Bottom, Mode):
        if Mode == "Color":
            image = cv.imread(Imageframe, cv.COLOR_BGR2RGB)
        elif Mode == "Shape":
            image = cv.imread(Imageframe, 0)
        crop_image = image[Top:Bottom, Left:Right]
        return crop_image

    @staticmethod
    def Crop_Image_Color(Imageframe, Left, Top, Right, Bottom):
        image = cv.imread(Imageframe, cv.COLOR_BGR2RGB)
        crop_image = image[Top:Bottom, Left:Right]
        return crop_image


class Color:
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
        return int(min(total))

class Save_Data:
    @staticmethod
    def Save_Score(Partnumber, Batch, Machine, Couter, Score, Result):
        named_tuple = time.localtime()
        Time = time.strftime("%Y%m%d%H%M%S", named_tuple)
        parent_dir = 'Transaction/'
        path = os.path.join(parent_dir)
        try:
            os.makedirs(path, exist_ok=True)
        except OSError as error:
            pass
        Transition = [dict(PartNumber=Partnumber, BatchNumber=Batch, MachineName=Machine, Details=[])]
        for s in range(Couter):
            Transition[0]["Details"].append([dict(Score=int(Score[s]),
                                                  Result=Result[s], Point=s + 1)])
        with open('Transaction/' + Time + '.json', 'w') as json_file:
            json.dump(Transition, json_file, indent=6)

    @staticmethod
    def Save_Image(Partnumber,Counter,Image,Mode,Left,Top,Right,Bottom,Color,Score,Score_Set,Result):
        named_tuple = time.localtime()
        Time = time.strftime("%Y%m%d%H%M%S", named_tuple)
        for s in range(Counter):
                cv.rectangle(Image[s], (Left[s], Top[s]), (Right[s], Bottom[s]), Color[s], 3)
                cv.putText(Image[s], "Mode : " + Mode[s], (10, 25), cv.FONT_HERSHEY_SIMPLEX, 1, Color[s], 2)
                cv.putText(Image[s], "Score : " + str(Score[s]) + " / " + str(Score_Set[s]), (10, 55), cv.FONT_HERSHEY_SIMPLEX, 1, Color[s], 2)
                cv.putText(Image[s], "Time : " + str(Time) + "", (10, 85), cv.FONT_HERSHEY_SIMPLEX, 1, Color[s], 2)
                if s <= 8:
                    Point = "0"
                else:
                    Point = ""
                if Result[s] == 1:
                    cv.imwrite('Record/' + Partnumber +'/OK/Point' + str(s + 1)+'/'+Time + '_P' + Point + str(s + 1) + '.jpg', Image[s])
                else:
                    cv.imwrite('Record/' + Partnumber +'/NG/Point' + str(s + 1)+'/'+Time + '_P' + Point + str(s + 1) + '.jpg', Image[s])

    @staticmethod
    def Master(Left, Top, Right, Bottom, Score, Point, Emp_ID, Mode, Partnumber):
        Score = int(Score)
        image = r'Current.png'
        Master_Image = CropImage.Crop_Image_Color(image, Left, Top, Right, Bottom)
        try:
            with open(Partnumber + '/' + Partnumber + '.json', 'r') as json_file:
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
                            item[i]["Point" + str_][0]["Color"] = Color.ReadRBG(Master_Image)
                            with open(Partnumber + '/' + Partnumber + '.json', 'w') as json_file:
                                json.dump(item, json_file, indent=6)
                    except:
                        # item.append({''+Point+'': [{"Camera": "",'Left': "",'Top': "","Right": "","Bottom": "",'Score': ""}]}
                        with open(Partnumber + '/' + Partnumber + '.json', 'r') as json_file:
                            item = json.loads(json_file.read())
                        try:
                            logging.debug(item[i - 1])
                            item.append({'' + Point + '': [
                                {"Emp ID": Emp_ID, "Mode": Mode, 'Left': Left, 'Top': Top, "Right": Right, "Bottom": Bottom, 'Score': Score, 'Color': Color.ReadRBG(Master_Image)}]})
                            with open(Partnumber + '/' + Partnumber + '.json', 'w') as json_file:
                                json.dump(item, json_file, indent=6)
                        except:
                            pass
        except FileNotFoundError as exc:
            if Point == "Point1":
                item = [
                    {'' + Point + '': [
                        {"Emp ID": Emp_ID, "Mode": Mode, 'Left': Left, 'Top': Top, "Right": Right, "Bottom": Bottom, 'Score': Score, 'Color': Color.ReadRBG(Master_Image)}]}]
                with open(Partnumber + '/' + Partnumber + '.json', 'w') as json_file:
                    json.dump(item, json_file, indent=6)

class Packing:
    @staticmethod
    def Check_Priter(Partnumber,Packing):
        try:
            Check_File = os.path.isfile(Partnumber + '\Couter_Printer.json')
            if Check_File is False:
                item = {"Partnumber": Partnumber, "Counter": 0, 'Packing': Packing}
                with open(Partnumber + '\Couter_Printer.json', 'w') as json_file:
                    json.dump(item, json_file, indent=6)
        except:
            pass
    @staticmethod
    def Read_Priter(Partnumber):
            try:
                with open(Partnumber + '\Couter_Printer.json', 'r') as json_file:
                    Data = json.loads(json_file.read())
                return  Data["Counter"]
            except:
                return 0

    @staticmethod
    def Couter_Printer(Partnumber,Packing):
        with open(Partnumber+'\Couter_Printer.json', 'r') as json_file:
            Data = json.loads(json_file.read())
        Packing_Couter = Data["Counter"]+1
        PackPart = Data["Partnumber"]
        if PackPart != Partnumber:
            Printer = {"Partnumber": Partnumber, "Counter": 1, "Packing": Packing}
            with open(Partnumber+'\Couter_Printer.json', 'w') as json_file:
                json.dump(Printer, json_file, indent=6)
        else:
            Printer = {"Partnumber": Partnumber, "Counter": Packing_Couter, "Packing": Packing}
            with open(Partnumber+'\Couter_Printer.json', 'w') as json_file:
                json.dump(Printer, json_file, indent=6)
            if Packing == Packing_Couter:
                Printer = {"Partnumber": Partnumber, "Counter": 0, "Packing": Packing}
                with open(Partnumber+'\Couter_Printer.json', 'w') as json_file:
                    json.dump(Printer, json_file, indent=6)
                with open('Printer.txt', 'w') as f:
                    f.write('Printer')

class App(customtkinter.CTk):
    customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

    def __init__(self):
        super().__init__()
        #self.PartNumber_R = self.BatchNumber_R = self.PartName_R = self.CustomerPartNumber_R = self.Packing_R = self.PartNumber_L = self.BatchNumber_L = self.PartName_L = self.CustomerPartNumber_L = self.Packing_L = ""
        self.title('Machine Vision Inspection 1.0.0')
        self.geometry("1920x1020+0+0")
        # self.state('zoomed')
        self.attributes('-fullscreen', True)
        self.MachineName = "S11"
        self.CouterOK_Left = 0
        self.CouterNG_Left = 0
        self.CouterOK_Right = 0
        self.CouterNG_Right = 0
        self.CouterOK_Single = 0
        self.CouterNG_Single = 0

        self.View()
        self.ReadFile()
        self.View_Point()

        self.Image_logo = GetImage()
        host = socket.gethostname()
        port = 10000
        #.client_socket = socket.socket()
        #self.client_socket.connect((host, port))
        self.Ready = False

        #self.Loop = InfiniteTimer(0.1, self.client_program)
        #self.Loop.start()
        #self.Keepdata = ""
        self.ReadFileScore()
        self.TCP()
        self.AddMaster()

        customtkinter.CTkLabel(master=self, text="Vision Inspection", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=50, weight="bold"), corner_radius=10).place(x=140, y=10)
        customtkinter.CTkLabel(master=self, text="v 1.0.0", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=15, weight="bold"), corner_radius=10).place(x=490, y=10)
        self.image_logo = tk.Button(self, bg="#232323", image=self.Image_logo.BKFImage, command=self.Destory, bd=0)
        self.image_logo.place(x=1755, y=10)
        self.image_logo.bind("<Enter>", self.on_enter)
        self.image_logo.bind("<Leave>", self.on_leave)
        self.Camera()
        #self.scaling_optionemenu = customtkinter.CTkOptionMenu(master=self, values=["50%", "60%", "70%","80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        #self.scaling_optionemenu.place(x=1000, y=80)
        customtkinter.CTkButton(master=self, text="Reorder", text_color="#00B400", hover_color="#B4F0B4", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("#353535"),
                                command=lambda: [self.ReadFile(), self.ReadFileScore(), self.View(),self.View_Point()]).place(x=1570, y=10)
    def ViewImagePart(self, Partnumber):
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
            self.dir_path = r"" + self.PartNumber_L + "\Master"
            for path in os.listdir(self.dir_path):
                if os.path.isfile(os.path.join(self.dir_path, path)):
                    if path.endswith('.bmp'):
                        self.CouterPoint_Left += 1
        except FileNotFoundError as ex:
            self.CouterPoint_Left = 0
        try:
            self.CouterPoint_Right = 0
            self.dir_path = r"" + self.PartNumber_R + "\Master"
            for path in os.listdir(self.dir_path):
                if os.path.isfile(os.path.join(self.dir_path, path)):
                    if path.endswith('.bmp'):
                        self.CouterPoint_Right += 1
        except FileNotFoundError as ex:
            self.CouterPoint_Right = 0

    def ReadFileScore(self):
        try:
            with open(self.PartNumber_L + '/' + self.PartNumber_L + '.json', 'r') as json_file:
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
                    FileFolder_Ok = 'Record/' + self.PartNumber_L +'/OK/Point' + str(L + 1)
                    path = os.path.join(FileFolder_Ok)
                    try:
                        os.makedirs(path, exist_ok=True)
                    except OSError as error:
                        pass
                    FileFolder_NG = 'Record/' + self.PartNumber_L +'/NG/Point' + str(L + 1)
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
        except:
            pass
        try:
            with open(self.PartNumber_R  + '/' + self.PartNumber_R  + '.json', 'r') as json_file:
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
                    FileFolder_Ok = 'Record/' + self.PartNumber_R  +'/OK/Point' + str(R + 1)
                    path = os.path.join(FileFolder_Ok)
                    try:
                        os.makedirs(path, exist_ok=True)
                    except OSError as error:
                        pass
                    FileFolder_NG = 'Record/' + self.PartNumber_R  +'/NG/Point' + str(R + 1)
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
        self.API = GetAPI.API()
        if self.API[0] == "Connected":
            color = "#00B400"
        else:
            color = "#D8D874"
        customtkinter.CTkLabel(master=self, text="S11", text_color=color, font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=65, weight="bold")).place(x=10, y=0)
        self.Run_Left = self.Run_Right =False
        self.ImageReal_Left = tk.Button(self, bg="White", command=lambda: self.ViewImagePart(self.PartNumber_L))
        self.ImageReal_Right = tk.Button(self, bg="White", command=lambda: self.ViewImagePart(self.PartNumber_R))



        self.CouterPacking_Left = 0
        self.CouterPacking_Right = 0
        self.CouterPacking_Single= 0
        self.PartNumber_R = self.BatchNumber_R = self.PartName_R = self.CustomerPartNumber_R = self.Packing_R = ""
        self.PartNumber_L = self.BatchNumber_L = self.PartName_L = self.CustomerPartNumber_L = self.Packing_L = ""
        self.PartNumber_S = self.BatchNumber_S = self.PartName_S = self.CustomerPartNumber_S = self.Packing_S = ""

        # Left
        self.BKF_Part_L_Lable = customtkinter.CTkLabel(master=self, text="BKF Part :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"))
        self.BKF_Part_L_Lable.place(x=10, y=100)
        self.PartNumber_L_Data = customtkinter.CTkLabel(master=self, text=self.PartNumber_L, text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), fg_color=("#00B400"), corner_radius=10)
        self.PartNumber_L_Data.place(x=150, y=100)
        self.Customer_L_Lable = customtkinter.CTkLabel(master=self, text="Customer :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"))
        self.Customer_L_Lable.place(x=10, y=140)
        self.CustomerPartNumber_L_Data = customtkinter.CTkLabel(master=self, text=self.CustomerPartNumber_L, text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), fg_color=("#00B400"), corner_radius=10)
        self.CustomerPartNumber_L_Data.place(x=150, y=140)
        self.Batch_L_Lable = customtkinter.CTkLabel(master=self, text="Batch :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"))
        self.Batch_L_Lable.place(x=10, y=180)
        self.BatchNumber_L_Data = customtkinter.CTkLabel(master=self, text=self.BatchNumber_L, text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), fg_color=("#00B400"), corner_radius=10)
        self.BatchNumber_L_Data.place(x=150, y=180)
        self.PartName_L_Lable = customtkinter.CTkLabel(master=self, text="Part Name :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"))
        self.PartName_L_Lable.place(x=10, y=220)
        self.PartName_L_Data = customtkinter.CTkLabel(master=self, text=self.PartName_L[:30], text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), fg_color=("#00B400"), corner_radius=10)
        self.PartName_L_Data.place(x=150, y=220)
        self.NG_L = customtkinter.CTkButton(master=self, text="NG : " + str(self.CouterNG_Left), text_color="#FFFFFF", hover_color="#C80000", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=50, weight="bold"), corner_radius=10, fg_color=("#FF0000"),
                                            command=lambda: self.ViewNG("NG_Left"))
        self.NG_L.place(x=620, y=180)
        self.OK_L = customtkinter.CTkLabel(master=self, text="OK : " + str(self.CouterOK_Left), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=52, weight="bold"), corner_radius=10, fg_color=("#00B400"))
        self.OK_L.place(x=620, y=100)
        self.Packing_L_Lable = customtkinter.CTkLabel(master=self, text="Packing :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), corner_radius=10)
        self.Packing_L_Lable.place(x=400, y=100)
        self.Packing_L_Show = customtkinter.CTkLabel(master=self, text=str(self.CouterPacking_Left) + "/" + str(self.Packing_L), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), corner_radius=10, fg_color=("#00B400"))
        self.Packing_L_Show.place(x=530, y=100)

        # Right
        self.BKF_Part_R_Lable = customtkinter.CTkLabel(master=self, text="BKF Part :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"))
        self.BKF_Part_R_Lable.place(x=960, y=100)
        self.PartNumber_R_Data = customtkinter.CTkLabel(master=self, text=self.PartNumber_R, text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), fg_color=("#00B400"), corner_radius=10)
        self.PartNumber_R_Data.place(x=1100, y=100)
        self.Customer_R_Lable = customtkinter.CTkLabel(master=self, text="Customer :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"))
        self.Customer_R_Lable.place(x=960, y=140)
        self.CustomerPartNumber_R_Data = customtkinter.CTkLabel(master=self, text=self.CustomerPartNumber_R, text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), fg_color=("#00B400"), corner_radius=10)
        self.CustomerPartNumber_R_Data.place(x=1100, y=140)
        self.Batch_R_Lable = customtkinter.CTkLabel(master=self, text="Batch :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"))
        self.Batch_R_Lable.place(x=960, y=180)
        self.BatchNumber_R_Data = customtkinter.CTkLabel(master=self, text=self.BatchNumber_R, text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), fg_color=("#00B400"), corner_radius=10)
        self.BatchNumber_R_Data.place(x=1100, y=180)
        self.PartName_R_Lable = customtkinter.CTkLabel(master=self, text="Part Name :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"))
        self.PartName_R_Lable.place(x=960, y=220)
        self.PartName_R_Data = customtkinter.CTkLabel(master=self, text=self.PartName_R[:30], text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), fg_color=("#00B400"), corner_radius=10)
        self.PartName_R_Data.place(x=1100, y=220)
        self.NG_R = customtkinter.CTkButton(master=self, text="NG : " + str(self.CouterNG_Left), text_color="#FFFFFF", hover_color="#C80000", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=50, weight="bold"), corner_radius=10, fg_color=("#FF0000"),
                                            command=lambda: self.ViewNG("NG_Right"))
        self.NG_R.place(x=1590, y=180)
        self.OK_R = customtkinter.CTkLabel(master=self, text="OK : " + str(self.CouterOK_Left), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=52, weight="bold"), corner_radius=10, fg_color=("#00B400"))
        self.OK_R.place(x=1590, y=100)
        self.Packing_R_Lable = customtkinter.CTkLabel(master=self, text="Packing :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), corner_radius=10)
        self.Packing_R_Lable.place(x=1360, y=100)
        self.Packing_R_Show = customtkinter.CTkLabel(master=self, text=str(self.CouterPacking_Right) + "/" + str(self.Packing_R), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), corner_radius=10, fg_color=("#00B400"))
        self.Packing_R_Show.place(x=1490, y=100)

        # Single
        self.BKF_Part_S_Lable = customtkinter.CTkLabel(master=self, text="BKF Part :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"))
        self.BKF_Part_S_Lable.place(x=450, y=100)
        self.PartNumber_S_Data = customtkinter.CTkLabel(master=self, text=self.PartNumber_S, text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), fg_color=("#00B400"), corner_radius=10)
        self.PartNumber_S_Data.place(x=590, y=100)
        self.Customer_S_Lable = customtkinter.CTkLabel(master=self, text="Customer :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"))
        self.Customer_S_Lable.place(x=450, y=140)
        self.CustomerPartNumber_S_Data = customtkinter.CTkLabel(master=self, text=self.CustomerPartNumber_S, text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), fg_color=("#00B400"), corner_radius=10)
        self.CustomerPartNumber_S_Data.place(x=590, y=140)
        self.Batch_S_Lable = customtkinter.CTkLabel(master=self, text="Batch :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"))
        self.Batch_S_Lable.place(x=450, y=180)
        self.BatchNumber_S_Data = customtkinter.CTkLabel(master=self, text=self.BatchNumber_S, text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), fg_color=("#00B400"), corner_radius=10)
        self.BatchNumber_S_Data.place(x=590, y=180)
        self.PartName_S_Lable = customtkinter.CTkLabel(master=self, text="Part Name :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"))
        self.PartName_S_Lable.place(x=450, y=220)
        self.PartName_S_Data = customtkinter.CTkLabel(master=self, text=self.PartName_S[:30], text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), fg_color=("#00B400"), corner_radius=10)
        self.PartName_S_Data.place(x=590, y=220)
        self.NG_S = customtkinter.CTkButton(master=self, text="NG : " + str(self.CouterNG_Single), text_color="#FFFFFF", hover_color="#C80000", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=50, weight="bold"), corner_radius=10, fg_color=("#FF0000"),
                                            command=lambda: self.ViewNG("NG_Right"))
        self.NG_S.place(x=1080, y=180)
        self.OK_S = customtkinter.CTkLabel(master=self, text="OK : " + str(self.CouterOK_Single), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=52, weight="bold"), corner_radius=10, fg_color=("#00B400"))
        self.OK_S.place(x=1080, y=100)
        self.Packing_S_Lable = customtkinter.CTkLabel(master=self, text="Packing :", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), corner_radius=10)
        self.Packing_S_Lable.place(x=850, y=100)
        self.Packing_S_Show = customtkinter.CTkLabel(master=self, text=str(self.CouterPacking_Single) + "/" + str(self.Packing_S), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), corner_radius=10, fg_color=("#00B400"))
        self.Packing_S_Show.place(x=980, y=100)

        if len(self.API[1]) == 2:
            self.ImageReal_Left.place(x=0, y=260)
            self.ImageReal_Right.place(x=960, y=260)
            self.PartNumber_R = self.API[2][0]
            self.BatchNumber_R = self.API[2][1]
            self.PartName_R = self.API[2][2]
            self.CustomerPartNumber_R = self.API[2][3]
            self.Packing_R = self.API[2][4]

            self.PartNumber_L = self.API[2][5]
            self.BatchNumber_L = self.API[2][6]
            self.PartName_L = self.API[2][7]
            self.CustomerPartNumber_L = self.API[2][8]
            self.Packing_L = self.API[2][9]

            self.PartNumber = "|"+self.PartNumber_R + "|" + self.PartNumber_L
            self.CouterPacking_Left = Packing.Read_Priter(self.PartNumber_L)
            self.CouterPacking_Right = Packing.Read_Priter(self.PartNumber_R)

            self.BKF_Part_S_Lable.place_forget()
            self.PartNumber_S_Data.place_forget()
            self.Customer_S_Lable.place_forget()
            self.CustomerPartNumber_S_Data.place_forget()
            self.Batch_S_Lable.place_forget()
            self.BatchNumber_S_Data.place_forget()
            self.PartName_S_Lable.place_forget()
            self.PartName_S_Data.place_forget()
            self.NG_S.place_forget()
            self.OK_S.place_forget()
            self.Packing_S_Lable.place_forget()
            self.Packing_S_Show.place_forget()

        elif len(self.API[1]) == 1:
            if self.API[1][0] == "Right":
                self.ImageReal_Left.place_forget()
                self.ImageReal_Right.place(x=960, y=260)
                self.PartNumber_R = self.API[2][0]
                self.BatchNumber_R = self.API[2][1]
                self.PartName_R = self.API[2][2]
                self.CustomerPartNumber_R = self.API[2][3]
                self.Packing_R = self.API[2][4]
                self.CouterPacking_Left = Packing.Read_Priter(self.PartNumber_L)
                self.CouterPacking_Right = Packing.Read_Priter(self.PartNumber_R)
                self.PartNumber = "|"+self.PartNumber_R+ "|"

                self.BKF_Part_S_Lable.place_forget()
                self.PartNumber_S_Data.place_forget()
                self.Customer_S_Lable.place_forget()
                self.CustomerPartNumber_S_Data.place_forget()
                self.Batch_S_Lable.place_forget()
                self.BatchNumber_S_Data.place_forget()
                self.PartName_S_Lable.place_forget()
                self.PartName_S_Data.place_forget()
                self.NG_S.place_forget()
                self.OK_S.place_forget()
                self.Packing_S_Lable.place_forget()
                self.Packing_S_Show.place_forget()

                self.BKF_Part_L_Lable.place_forget()
                self.PartNumber_L_Data.place_forget()
                self.Customer_L_Lable.place_forget()
                self.CustomerPartNumber_L_Data.place_forget()
                self.Batch_L_Lable.place_forget()
                self.BatchNumber_L_Data.place_forget()
                self.PartName_L_Lable.place_forget()
                self.PartName_L_Data.place_forget()
                self.NG_L.place_forget()
                self.OK_L.place_forget()
                self.Packing_L_Lable.place_forget()
                self.Packing_L_Show.place_forget()


            elif self.API[1][0] == "Left":
                self.ImageReal_Left.place(x=0, y=260)
                self.ImageReal_Right.place_forget()
                self.PartNumber_L = self.API[2][0]
                self.BatchNumber_L = self.API[2][1]
                self.PartName_L = self.API[2][2]
                self.CustomerPartNumber_L = self.API[2][3]
                self.Packing_L = self.API[2][4]
                self.CouterPacking_Left = Packing.Read_Priter(self.PartNumber_L)
                self.CouterPacking_Right = Packing.Read_Priter(self.PartNumber_R)
                self.PartNumber = "|"+"|"+self.PartNumber_L

                self.BKF_Part_S_Lable.place_forget()
                self.PartNumber_S_Data.place_forget()
                self.Customer_S_Lable.place_forget()
                self.CustomerPartNumber_S_Data.place_forget()
                self.Batch_S_Lable.place_forget()
                self.BatchNumber_S_Data.place_forget()
                self.PartName_S_Lable.place_forget()
                self.PartName_S_Data.place_forget()
                self.NG_S.place_forget()
                self.OK_S.place_forget()
                self.Packing_S_Lable.place_forget()
                self.Packing_S_Show.place_forget()

                self.BKF_Part_R_Lable.place_forget()
                self.PartNumber_R_Data.place_forget()
                self.Customer_R_Lable.place_forget()
                self.CustomerPartNumber_R_Data.place_forget()
                self.Batch_R_Lable.place_forget()
                self.BatchNumber_R_Data.place_forget()
                self.PartName_R_Lable.place_forget()
                self.PartName_R_Data.place_forget()
                self.NG_R.place_forget()
                self.OK_R.place_forget()
                self.Packing_R_Lable.place_forget()
                self.Packing_R_Show.place_forget()

            elif self.API[1][0] == "Single":
                self.ImageReal_Left.place(x=450, y=280)
                self.ImageReal_Right.place_forget()
                self.PartNumber_L = self.API[2][0]
                self.BatchNumber_L = self.API[2][1]
                self.PartName_L = self.API[2][2]
                self.CustomerPartNumber_L = self.API[2][3]
                self.Packing_L = self.API[2][4]
                self.CouterPacking_Left = Packing.Read_Priter(self.PartNumber_L)
                self.CouterPacking_Right = Packing.Read_Priter(self.PartNumber_R)
                self.PartNumber = self.PartNumber_L + "|"+ "|"




    def forget(self):
        try:
            self.BKF_Part_L_Lable.place_forget()
            self.PartNumber_L_Data.place_forget()
            self.Customer_L_Lable.place_forget()
            self.CustomerPartNumber_L_Data.place_forget()
            self.Batch_L_Lable.place_forget()
            self.BatchNumber_L_Data.place_forget()
            self.PartName_L_Lable.place_forget()
            self.PartName_L_Data.place_forget()
            self.NG_L.place_forget()
            self.OK_L.place_forget()
            self.Packing_L_Lable.place_forget()
            self.Packing_L_Show.place_forget()
        except:
            pass



    def View_Point(self):
        self.Frame_Point = customtkinter.CTkFrame(master=self, width=1980, height=270).place(x=0, y=810)
        if self.PartNumber_L != "":
            for Point_Left in range(self.CouterPoint_Left):
                if Point_Left <= 4:
                    customtkinter.CTkLabel(master=self.Frame_Point, text="Point:" + str(Point_Left + 1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("#A9A9A9")).place(x=190 * (Point_Left), y=850)
                elif Point_Left <= 9:
                    customtkinter.CTkLabel(master=self.Frame_Point, text="Point:" + str(Point_Left + 1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("#A9A9A9")).place(x=190 * (Point_Left - 5), y=930)
                elif Point_Left <= 15:
                    customtkinter.CTkLabel(master=self.Frame_Point, text="Point:" + str(Point_Left + 1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("#A9A9A9")).place(x=190 * (Point_Left - 10), y=1010)
        if self.PartNumber_R != "":
            for Point_Right in range(self.CouterPoint_Right):
                if Point_Right <= 4:
                    customtkinter.CTkLabel(master=self.Frame_Point, text="Point:" + str(Point_Right + 1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("#A9A9A9")).place(x=960 + (Point_Right * 190), y=850)
                elif Point_Right <= 9:
                    customtkinter.CTkLabel(master=self.Frame_Point, text="Point:" + str(Point_Right + 1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("#A9A9A9")).place(x=960 + ((Point_Right - 5) * 190), y=930)
                elif Point_Right <= 15:
                    customtkinter.CTkLabel(master=self.Frame_Point, text="Point:" + str(Point_Right + 1), text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("#A9A9A9")).place(x=960 + ((Point_Right - 10) * 190), y=1010)

    def ViewNG(self, Side):
        ViewNG = Toplevel(self)
        ViewNG.title(Side)
        PointNG = []
        if Side == "NG_Left":
            Counter = self.CouterPoint_Left
        elif Side == "NG_Right":
            Counter = self.CouterPoint_Right
        for i in range(Counter):
            PointNG.append("Point" + str(i + 1))
        PointNG_value = customtkinter.StringVar()
        customtkinter.CTkComboBox(ViewNG, variable=PointNG_value, values=PointNG,
                                  corner_radius=10, border_color="#C5C5C5", text_color="#FF3939", border_width=5, width=200, height=50, font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), button_hover_color="#B4F0B4", button_color="#C5C5C5",
                                  dropdown_hover_color="#B4F0B4", dropdown_text_color="#FF3939", dropdown_font=("Microsoft PhagsPa", 20)).place(x=10, y=10)
        customtkinter.CTkButton(ViewNG, text="Commit", text_color="#FF3939", hover_color="#FF9797", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=35, weight="bold"), corner_radius=10, fg_color=("#353535")).place(x=35, y=70)
        ViewNG.configure(background='#232323')
        ViewNG.geometry('220x120')


    def Processing(self):
        if self.data == "Snap1":
            print(self.PartNumber_L, self.Packing_L)
            if self.CouterPoint_Left != 0:
                self.Run_Left = True
                Filename = "Current_Left.png"
                cv.imwrite(Filename, frame0.read()[1])
                ImageSave, ColorView, Color_Save_Image, Result, Score = Main.Main(self.PartNumber_L, Filename, self.CouterPoint_Left, self.Point_Mode_L, self.Point_Left_L, self.Point_Top_L, self.Point_Right_L, self.Point_Bottom_L, self.Point_Score_L, self.Point_Color_L)
                # self.Ready = True
                image = Main.ViewImage_Snap(Filename, self.CouterPoint_Left, self.Point_Left_L, self.Point_Top_L, self.Point_Right_L, self.Point_Bottom_L, Score, ColorView)
                Save_Data.Save_Image(self.PartNumber_L, self.CouterPoint_Left, ImageSave, self.Point_Mode_L, self.Point_Left_L, self.Point_Top_L, self.Point_Right_L, self.Point_Bottom_L, Color_Save_Image, Score, self.Point_Score_L, Result)
                Save_Data.Save_Score(self.PartNumber_L, self.BatchNumber_L, self.MachineName, self.CouterPoint_Left, Score, Result)
                Data = Main.ShowResult(Result)
                if Data is True:
                    self.message = "OK"
                    self.CouterOK_Left = self.CouterOK_Left + 1
                    self.OK_L.configure(text="NG : " + str(self.CouterOK_Left))
                    #print(self.PartNumber_L, self.Packing_L)
                    Packing.Couter_Printer(self.PartNumber_L, self.Packing_L)
                    #CouterPacking = Packing.Read_Priter(self.PartNumber_L)
                    #self.Packing_L.configure(text=str(CouterPacking) + "/" + str(self.Packing_L))
                elif Data is False:
                    self.message = "NG"
                    self.CouterNG_Left = self.CouterNG_Left + 1
                    self.NG_L.configure(text="NG : " + str(self.CouterNG_Left))
                self.ImageReal_Left.imgtk = image
                self.ImageReal_Left.configure(image=image)

        elif self.data == "Snap2":
            if self.CouterPoint_Left != 0:
                self.Run_Left = True
                Filename = "Current_Left.png"
                cv.imwrite(Filename, frame0.read()[1])
                ImageSave, ColorView, Color_Save_Image, Result, Score = Main.Main(self.PartNumber_L,Filename,self.CouterPoint_Left,self.Point_Mode_L,self.Point_Left_L, self.Point_Top_L, self.Point_Right_L, self.Point_Bottom_L,self.Point_Score_L,self.Point_Color_L)
                #self.Ready = True
                image = Main.ViewImage_Snap(Filename, self.CouterPoint_Left,self.Point_Left_L, self.Point_Top_L, self.Point_Right_L, self.Point_Bottom_L, Score, ColorView)
                Save_Data.Save_Image(self.PartNumber_L,self.CouterPoint_Left,ImageSave,self.Point_Mode_L,self.Point_Left_L,self.Point_Top_L,self.Point_Right_L,self.Point_Bottom_L,Color_Save_Image,Score,self.Point_Score_L,Result)
                Save_Data.Save_Score(self.PartNumber_L, self.BatchNumber_L, self.MachineName,self.CouterPoint_Left,Score,Result)
                Data = Main.ShowResult(Result)
                if Data is True:
                    self.message = "OK"
                    self.CouterOK_Left = self.CouterOK_Left + 1
                    self.OK_L.configure(text="NG : " + str(self.CouterOK_Left))
                    Packing.Couter_Printer(self.PartNumber_L,self.Packing_L)
                    CouterPacking = Packing.Read_Priter(self.PartNumber_L)
                    self.Packing_L.configure(text=str(CouterPacking) + "/" + str(self.Packing_L))
                elif Data is False:
                    self.message = "NG"
                    self.CouterNG_Left = self.CouterNG_Left + 1
                    self.NG_L.configure(text="NG : " + str(self.CouterNG_Left))
                self.ImageReal_Left.imgtk = image
                self.ImageReal_Left.configure(image=image)
                #self.Ready = False
                #self.client_socket.send(self.message.encode())

        elif self.data == "Snap3":
            if self.CouterPoint_Right != 0:
                self.Run_Right = True
                Filename = "Current_Right.png"
                cv.imwrite(Filename, frame1.read()[1])
                ImageSave, ColorView, Color_Save_Image, Result, Score = Main.Main(self.PartNumber_R,Filename,self.CouterPoint_Right,self.Point_Mode_R,self.Point_Left_R, self.Point_Top_R, self.Point_Right_R, self.Point_Bottom_R,self.Point_Score_R,self.Point_Color_R)
                image = Main.ViewImage_Snap(Filename, self.CouterPoint_Right, self.Point_Left_R, self.Point_Top_R, self.Point_Right_R, self.Point_Bottom_R, Score, ColorView)
                Save_Data.Save_Image(self.PartNumber_R,self.CouterPoint_Right,ImageSave,self.Point_Mode_R,self.Point_Left_R,self.Point_Top_R,self.Point_Right_R,self.Point_Bottom_R,Color_Save_Image,Score,self.Point_Score_R,Result)
                Save_Data.Save_Score(self.PartNumber_R, self.BatchNumber_R, self.MachineName,self.CouterPoint_Right,Score,Result)
                Data = Main.ShowResult(Result)
                if Data is True:
                    self.message = "OK"
                    self.CouterOK_Right = self.CouterOK_Right + 1
                    self.OK_R.configure(text="NG : " + str(self.CouterOK_Right))
                    Packing.Couter_Printer(self.PartNumber_R, self.Packing_R)
                    CouterPacking = Packing.Read_Priter(self.PartNumber_R)
                    self.Packing_R.configure(text=str(CouterPacking) + "/" + str(self.Packing_R))
                elif Data is False:
                    self.message = "NG"
                    self.CouterNG_Right = self.CouterNG_Right + 1
                    self.NG_R.configure(text="NG : " + str(self.CouterNG_Right))
                self.ImageReal_Right.imgtk = image
                self.ImageReal_Right.configure(image=image)
                #self.client_socket.send(self.message.encode())
        #self.after(1000,self.Processing)

    def client_program(self):
        self.data = self.client_socket.recv(128).decode()
        if self.data != self.Keepdata:
            if self.data == "Vision":
                if self.API[0] == "Connected":
                    print(self.API[1])
                    if len(self.API[1]) == 1:
                        if self.API[1][0] == "Right" and self.CouterPoint_Right != 0:
                            self.message = "Ready"
                        elif self.API[1][0] == "Left" and self.CouterPoint_Left != 0:
                            self.message = "Ready"
                        elif self.API[1][0] == "Single" and self.CouterPoint_Left != 0:
                            self.message = "Ready"
                        else:
                            self.message = "Setup"
                    elif len(self.API[1]) == 2 and (self.CouterPoint_Right != 0 and self.CouterPoint_Left != 0):
                        self.message = "Ready"
                    else:
                        self.message = "Setup"
                else:
                    self.message = "Setup"
            elif self.data == "PartNumber":
                self.message = self.PartNumber
            elif self.data == "Snap1":#Single
                self.Processing()
            elif self.data == "Snap2":#Left
                self.Processing()
            elif self.data == "Snap3":#Right
                self.Processing()
            #else:
                #self.message = "NoOrder"
        elif self.data == self.Keepdata:
            self.message = "Wait"
        self.Keepdata = self.data
        self.client_socket.send(self.message.encode())
        self.message = ""
        #self.after(5000,self.client_program)

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
        if self.Run_Left == False:
            self.ImageReal_Left.imgtk = self.LeftCommit
            self.ImageReal_Left.configure(image=self.LeftCommit)
        if self.Run_Right == False:
            self.ImageReal_Right.imgtk = self.RightCommit
            self.ImageReal_Right.configure(image=self.RightCommit)
        self.after(20, self.Camera)

    def AddMaster(self):
        customtkinter.CTkButton(master=self, text="Add-master", text_color="#00B400", hover_color="#B4F0B4", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("#353535"), command=self.SaveMasterNewWindow).place(x=1300, y=10)

    def TCP(self):
        customtkinter.CTkLabel(master=self, text="Read : ", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold")).place(x=580, y=30)
        customtkinter.CTkLabel(master=self, text="TCP", text_color="#FFFFFF", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), corner_radius=10, fg_color=("#00B400")).place(x=660, y=30)
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
            with open('Information\Operator.json', 'r') as json_Part:
                json_object = json.loads(json_Part.read())
                id_Emp = []
                for d in json_object:
                    id_Emp.append(d['id_Emp'])
            for i in range(len(id_Emp)):
                if id_Emp[i] == Password.get():
                    return True
            messagebox.showwarning("Password", "Wrong password did not match")
            return False

            """""""""""
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
            """""""""""

        def Search():
            if Loginform():
                Login.destroy()
                SaveMaster = Toplevel(self)
                SaveMaster.title("Save Master")
                SaveMaster.configure(background='#232323')
                SaveMaster.geometry('330x470')
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
                            Partnumber = self.PartNumber_R
                            Imagesave = Image.fromarray(self.Camera_Right)
                        else:
                            Partnumber = self.PartNumber_L
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
                                        Save_Data.Master(Left, Top, Right, Bottom, Score, Point, Emp_ID, Mode, Partnumber)

                        path = r'Current.png'
                        image = cv.imread(path)
                        clone = image.copy()
                        cv.namedWindow(Point)
                        cv.setMouseCallback(Point, click_and_crop)
                        cv.imshow(Point, image)
                    else:
                        messagebox.showwarning("Score", "Minumun Score 500")

                customtkinter.CTkLabel(SaveMaster, text="Point:", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold")).place(x=5, y=26)
                Point_value = customtkinter.StringVar()
                Point_value.set("Point1")
                Point = customtkinter.CTkComboBox(SaveMaster, variable=Point_value, values=['Point1', 'Point2', 'Point3', 'Point4', 'Point5', 'Point6', 'Point7', 'Point8', 'Point9', 'Point10', 'Point11', 'Point12', 'Point13', 'Point14', 'Point15'],
                                                  corner_radius=10, border_color="#C5C5C5", text_color="#00B400", border_width=5, width=200, height=50, font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), button_hover_color="#B4F0B4", button_color="#C5C5C5",
                                                  dropdown_hover_color="#B4F0B4", dropdown_text_color="#00B400", dropdown_font=("Microsoft PhagsPa", 20)).place(x=120, y=20)

                customtkinter.CTkLabel(SaveMaster, text="Mode:", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold")).place(x=5, y=102)
                Mode_value = customtkinter.StringVar()
                Mode_value.set("Shape")
                Mode = customtkinter.CTkComboBox(SaveMaster, variable=Mode_value, values=['Shape', 'Color'],
                                                 corner_radius=10, border_color="#C5C5C5", text_color="#00B400", border_width=5, width=200, height=50, font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), button_hover_color="#B4F0B4", button_color="#C5C5C5",
                                                 dropdown_hover_color="#B4F0B4", dropdown_text_color="#00B400", dropdown_font=("Microsoft PhagsPa", 20)).place(x=120, y=100)

                customtkinter.CTkLabel(SaveMaster, text="Side:", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold")).place(x=5, y=182)
                # Side_value = customtkinter.StringVar()
                # Side = customtkinter.CTkComboBox(SaveMaster, variable=Side_value, values=['Left', 'Right'],
                # corner_radius=10, border_color="#C5C5C5", text_color="#00B400", border_width=5, width=200, height=50, font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold"), button_hover_color="#B4F0B4", button_color="#C5C5C5",
                # dropdown_hover_color="#B4F0B4", dropdown_text_color="#00B400", dropdown_font=("Microsoft PhagsPa", 20)).place(x=120, y=180)
                Side = tkinter.IntVar(value=0)
                if self.API[1][0] == "Single" :
                    Side = tkinter.IntVar(value=0)
                    Side_Single = customtkinter.CTkRadioButton(SaveMaster, variable=Side, value=0, text="Single", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=30, weight="bold"), text_color="#00B400")
                    Side_Single.place(x=120, y=180)
                else:
                    Side_Left = customtkinter.CTkRadioButton(SaveMaster, variable=Side, value=0, text="Left ", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=30, weight="bold"), text_color="#00B400")
                    Side_Left.place(x=120, y=180)
                    Side_Right = customtkinter.CTkRadioButton(SaveMaster, variable=Side, value=1, text="Right", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=30, weight="bold"), text_color="#00B400")
                    Side_Right.place(x=120, y=220)


                customtkinter.CTkLabel(SaveMaster, text="Score:", text_color="#00B400", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=25, weight="bold")).place(x=5, y=290)
                Score_value = customtkinter.StringVar()
                Score_value.set("800")
                customtkinter.CTkEntry(SaveMaster, width=200, height=50, placeholder_text="Score", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=30, weight="bold"), textvariable=Score_value, text_color="#00B400").place(x=120, y=285)
                Save = customtkinter.CTkButton(SaveMaster, text="Save", text_color="#00B400", hover_color="#B4F0B4", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=60, weight="bold"), corner_radius=10, fg_color=("#353535"), command=Save_Master).place(x=90, y=350)

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

        # text_color="#00B400", hover_color="#B4F0B4", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), corner_radius=10, fg_color=("#353535")
        customtkinter.CTkEntry(Login, width=200, height=50, corner_radius=10, placeholder_text="Password", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=40, weight="bold"), show='*', textvariable=Password).place(x=10, y=5)
        customtkinter.CTkButton(Login, text="Login", text_color="#00B400", hover_color="#B4F0B4", font=customtkinter.CTkFont(family="Microsoft PhagsPa", size=30, weight="bold"), corner_radius=10, fg_color=("#353535"), command=Search).place(x=40, y=70)
        Login.mainloop()

    def change_scaling_event(self,new_scaling: str):
        new_scaling_float = int(self.scaling_optionemenu.get().replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)





if __name__ == "__main__":
    app = App()
    app.mainloop()
