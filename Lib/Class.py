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

class GetAPI:
    @staticmethod
    def API():
        method = ["PartNumber", "BatchNumber", "PartName", "CustomerPartNumber", "PackingStd"]
        side = []
        data = []
        api_url = "https://api.bkf.co.th/APIGateway_DB_BKF/GetCurrentMachineStatus?machineNickName=S11"
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

print(GetAPI.API())