#!/usr/bin/python

import tkinter
import os
import platform
import wget

from tkinter import END, HORIZONTAL, INSERT, W, Button, PhotoImage, StringVar, Tk, Canvas, Label, filedialog
from tkinter import messagebox
from tkinter.ttk import Progressbar

#Variables
os_system = platform.system()
path = 'none'
downloading = False

#Functions

def writePath():
    showdir['state'] = 'normal'
    showdir.insert(INSERT, path)
    showdir['state'] = 'disabled'

def clearPath():
    showdir['state'] = 'normal'
    showdir.delete('1.0', END)
    showdir['state'] = 'disabled'

def getFolderPath():
    global path
    global downloading
    if (downloading == True):
        messagebox.showinfo("Attenzione", "È già in corso l'installlazione del modpack")
    else:
        path = filedialog.askdirectory(initialdir=path, title="Example")
    clearPath()
    if (path == ''):
        getOs()
        messagebox.showerror("Errore", "Nessuna cartella selezionate, usando il percorso predefinito")
    writePath()

def getOs():
    global path
    if (os_system == "Windows"):
        path = os.path.join("C:/Users",os.getlogin(),"AppData/Roaming/.minecraft").replace("\\","/")
    elif(os_system == "Darwin"):
        path = os.path.join(os.getlogin(),"/Library/Application Support/minecraft").replace("\\","/")
    elif(os_system == "Linux"):
        path = os.path.join(os.getlogin(),"/.minecraft").replace("\\","/")
    else:
         messagebox.showerror("Errore", "Sistema operativo non riconosciuto!")
         screen.destroy()

def setDownloadStart():
    global downloading
    if (downloading == False):
        downloading = True
        putDownloadBar()
        setProgress()
        wget.download()
    else:
        messagebox.showinfo("Attenzione", "Download già avviato!")

def setDownloadStop():
    global downloading
    downloading = False

def setProgress():
    global my_progress
    if my_progress['value'] < 100:
        my_progress['value'] += 10

def putDownloadBar():
    global my_progress
    my_progress = Progressbar(screen, orient= HORIZONTAL, length= 1000, mode= "determinate")
    my_progress.pack()

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

#Version

getOs()

#Open
screen = tkinter.Tk()
screen.title("TheBigWolf Pixelmon Installer")

#Resolution
screen.geometry("1000x606")
screen.resizable(False,False)

#Icon
icon_img = tkinter.PhotoImage(file="icon.png")
screen.iconphoto(True, icon_img)

#Background
background_img = tkinter.PhotoImage(file="background.png")
canvas = tkinter.Canvas(screen, bg="white", height=1000	, width=1000, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

background = canvas.create_image(500, 303, anchor='c', image=background_img)

#Buttons
install_button = CanvasButton(canvas, 501, 304, BUTTON_IMG_PATH, command=setDownloadStart)
selectdir_button = Button(text="...", bg="white", highlightcolor="white", command=getFolderPath)
selectdir_button.place(x=753, y=410)
#Text

showdir = tkinter.Text(screen, height=1, width=63)
showdir['state'] = 'disabled'
writePath()
showdir.place(x=246, y=413)

#End
screen.mainloop()
