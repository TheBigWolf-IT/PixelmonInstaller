#!/usr/bin/python

import tkinter
import os
import platform
import threading
from xml.dom.expatbuilder import FragmentBuilderNS
import zipfile
import wget
import json
import sys
import requests

from multiprocessing.connection import wait
from time import sleep
from zipfile import ZipFile
from unicodedata import name
from tkinter import END, HORIZONTAL, INSERT, Button, PhotoImage, StringVar, Tk, Canvas, Label, filedialog, messagebox
from tkinter.ttk import Progressbar

#Variables
os_system = platform.system()
path = 'none'
downloading = False
global_urls = "https://raw.githubusercontent.com/TheBigWolf-IT/PixelmonInstaller/main/urls/urls.json"

urls = requests.get(global_urls)
urls_json = json.loads(urls.text)
#This is so that if i need to change links i don't have to recompile a new version
profile_url = urls_json['profiles']
pack_url = urls_json['pack']

#Functions

#Necessary only for py-to-exe
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

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

def putDownloadBar():
    global progress

    progress = Progressbar(screen, orient= HORIZONTAL, length= 1000, mode= "determinate")
    progress.pack()

def setProgress(current, total):
    global progress

    size = (current / total * 100)
    progress['value'] = size / 2

def setFinalProgress(current, total):
    global progress

    size = (current / total * 100)
    progress['value'] = size

def setDownloadStart():
    global downloading
    global path
    global pack_url
    global profile_url
    global progress

    if (downloading == False):
        downloading = True
        putDownloadBar()
        checkIfAlreadyExisting()
        background_thread= threading.Thread(target=startDownload, args=(path, pack_url))
        background_thread.start()
        if (os.path.exists(os.path.join(path, "launcher_profiles.json").replace("\\", "/"))):
            insertProfile(path, profile_url)

    else:
        messagebox.showinfo("Attenzione", "Download già avviato!")

def startDownload(path, pack_url):
    wget.download(pack_url, path, bar=progressionBarUpdater)
    startUnzip(path)

def startUnzip(path):
    filepath = os.path.join(path, wget.filename_from_url(pack_url)).replace("\\","/")
    pack_file = zipfile.ZipFile(filepath)

    uncompress_size = sum((file.file_size for file in pack_file.infolist()))

    extracted_size = 0

    for file in pack_file.infolist():
        extracted_size += file.file_size
        setFinalProgress(extracted_size, uncompress_size)
        pack_file.extract(file, path=path)
    pack_file.close()
    sleep(3)
    deleteDownloadZip(filepath)

def setDownloadStop():
    global downloading

    downloading = False

def checkIfAlreadyExisting():
    global path
    global pack_url

    tempfile = os.path.join(path, wget.filename_from_url(pack_url)).replace("\\","/")
    if (os.path.exists(tempfile) == True):
        os.remove(tempfile)

def progressionBarUpdater(current, total, width=80):
    setProgress(current, total)

def deleteDownloadZip(filepath):
    if (os.path.exists(filepath) == True):
        os.remove(filepath)
    finishedPrompt()

def insertProfile(path, profile_url):
    filepath = os.path.join(path, "launcher_profiles.json").replace("\\","/")
    value = os.path.join(path, "versions/1.16.5-TheBigWolf-Pixelmon").replace("/", "//").replace("\\", "//")
    folder_profile = {}
    folder_profile['gameDir'] = value
    profile_json = requests.get(profile_url)
    data = json.loads(profile_json.text)
    data['thebigwolf-pixelmon'].update(folder_profile)

    with open((filepath), 'r+') as file:
        file_data = json.load(file)
        file_data['profiles'].update(data)
        file.seek(0)
        json.dump(file_data, file, indent = 2)

def finishedPrompt():
    global downloading

    messagebox.showinfo("Successo!", "Pixelmon installata, ora ti basterà avviare il launcher e se non hai mai avviato la 1.16.5 dovrai prima avviare la 1.16.5 e poi potrai avviare la pixelmon!")
    downloading = False


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

BUTTON_IMG_PATH = resource_path("install.png")

#Version

getOs()

#Open
screen = tkinter.Tk()
screen.title("TheBigWolf Pixelmon Installer")

#Resolution
screen.geometry("1000x606")
screen.resizable(False,False)

#Icon
icon_path = resource_path("icon.png")
icon_img = tkinter.PhotoImage(file=icon_path)
screen.iconphoto(True, icon_img)

#Background
background_path = resource_path("background.png")
background_img = tkinter.PhotoImage(file=background_path)
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
