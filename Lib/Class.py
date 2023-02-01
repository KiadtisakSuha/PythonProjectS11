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

with open('Parttest.json', 'r') as json_Part:
    json_API = json.loads(json_Part.read())

PartNumber_R = json_API[0]["Rigth"][0]["PartNumber"]
BatchNumber_R = json_API[0]["Rigth"][0]["BatchNumber"]
PartName_R = json_API[0]["Rigth"][0]["PartName"]
CustomerPartNumber_R = json_API[0]["Rigth"][0]["CustomerPartNumber"]
MachineName_R = json_API[0]["Rigth"][0]["MachineName"]
MoldId_R = json_API[0]["Rigth"][0]["MoldId"]
Packing_R = json_API[0]["Rigth"][0]["PackingStd"]

PartNumber_L = json_API[1]["Left"][0]["PartNumber"]
BatchNumber_L = json_API[0]["Left"][0]["BatchNumber"]
PartName_L = json_API[0]["Left"][0]["PartName"]
CustomerPartNumber_L = json_API[0]["Left"][0]["CustomerPartNumber"]
MachineName_L = json_API[0]["Left"][0]["MachineName"]
MoldId_L = json_API[0]["Left"][0]["MoldId"]
Packing_L = json_API[0]["Left"][0]["PackingStd"]