import customtkinter
from PIL import ImageTk, Image, ImageDraw
import cv2 as cv
customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("400x780")
app.title("CustomTkinter simple_example.py")

def button_callback():
    print("Button click")


def slider_callback(value):
    progressbar_1.set(value)



x = cv.imread("Current_Right.png")
import customtkinter
from PIL import Image, ImageTk



button = customtkinter.CTkButton(master=app,
                                    width=120,
                                    height=32,
                                    border_width=0,
                                    corner_radius=8,
                                    text="CTkButton",

                                    image=ImageTk.PhotoImage(file="Current_Right.png")
                                    )
app.mainloop()