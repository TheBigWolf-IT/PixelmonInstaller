#!/usr/bin/python

from msilib.schema import Dialog
import tkinter
import os
import platform

from tkinter import Button, PhotoImage, Tk, Canvas, Label
from os import getlogin
from tkinter import simpledialog
from tkinter import messagebox

#Hide the button (thx Isaac)
class CanvasButton:
    flash_delay = 100

    def __init__(self, canvas, x, y, image_path, command, state=tkinter.NORMAL):
        self.canvas = canvas
        self.btn_image = tkinter.PhotoImage(file=image_path)
        self.canvas_btn_img_obj = canvas.create_image(x, y, anchor='c', state=state,
                                                      image=self.btn_image)
        canvas.tag_bind(self.canvas_btn_img_obj, "<ButtonRelease-1>",
                        lambda event: (self.flash(), command()))
    def flash(self):
        self.set_state(tkinter.HIDDEN)
        self.canvas.after(self.flash_delay, self.set_state, tkinter.NORMAL)

    def set_state(self, state):
        self.canvas.itemconfigure(self.canvas_btn_img_obj, state=state)

BUTTON_IMG_PATH = "install.png"

#Open
screen = tkinter.Tk()
screen.title("TheBigWolf Pixelmon Installer")
#Resolution
screen.geometry("1000x606")
screen.resizable(False,False)
#Background
background_img = tkinter.PhotoImage(file="background.png")
canvas = tkinter.Canvas(screen, bg="white", height=1000	, width=1000, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

background = canvas.create_image(500, 303, anchor='c', image=background_img)

#Buttons
install_button = CanvasButton(canvas, 501, 304, BUTTON_IMG_PATH, command=exit)






#Version
os_system = platform.system()

path= "none"

if (os_system == "Windows"):
    path = os.path.join("C:\\Users",os.getlogin(),"AppData\\Roaming\\.minecraft")
elif(os_system == "Darwin"):
    path = os.path.join("~/Library/Application Support/minecraft")
elif(os_system == "Linux"):
    path = os.path.join("~/.minecraft")
else:
    messagebox.showerror("Errore", "Sistema operativo non riconosciuto!")
    screen.destroy()

print(path)
#End
screen.mainloop()
