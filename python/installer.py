#!/usr/bin/python


import tkinter
import os
import platform
import threading
import zipfile
import wget
import json

from multiprocessing.connection import wait
from time import sleep
from zipfile import ZipFile
from unicodedata import name
from tkinter import END, HORIZONTAL, INSERT, Button, PhotoImage, StringVar, Tk, Canvas, Label, filedialog
from tkinter import messagebox
from tkinter.ttk import Progressbar

#Variables
os_system = platform.system()
path = 'none'
downloading = False
url = "https://www.dropbox.com/s/ls6u78p6wv0e0hy/thebigwolf-pixelmon.zip?dl=1"


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

def setDownloadStart():
    global downloading
    global path
    global url
    global progress
    if (downloading == False):
        downloading = True
        putDownloadBar()
        checkIfAlreadyExisting()
        background_thread= threading.Thread(target=startDownload, args=(path, url))
        background_thread.start()
    else:
        messagebox.showinfo("Attenzione", "Download già avviato!")


def setDownloadStop():
    global downloading
    downloading = False

def checkIfAlreadyExisting():
    global path
    global url
    tempfile = os.path.join(path, wget.filename_from_url(url)).replace("\\","/")
    if (os.path.exists(tempfile) == True):
        os.remove(tempfile)

def progressionBarUpdater(current, total, width=80):
    setProgress(current, total)

def startDownload(path, url):
    wget.download(url, path, bar=progressionBarUpdater)
    startUnzip(path)

def startUnzip(path):
    filepath = os.path.join(path, wget.filename_from_url(url)).replace("\\","/")
    zf = zipfile.ZipFile(filepath)

    uncompress_size = sum((file.file_size for file in zf.infolist()))

    extracted_size = 0

    for file in zf.infolist():
        extracted_size += file.file_size
        setFinalProgress(extracted_size, uncompress_size)
        zf.extract(file, path=path)
    zf.close()
    sleep(3)
    insertProfile(path)
    deleteDownloadZip(filepath)

def deleteDownloadZip(filepath):
    if (os.path.exists(filepath) == True):
        os.remove(filepath)
    finishedPrompt()

def insertProfile(path):
    filepath = os.path.join(path, "launcher_profiles.json").replace("\\","/")
    data = {
        "thebigwolf-pixelmon": {
            "created": "2022-09-12T00:42:09.620Z",
            "icon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAABiGSURBVHhe7Z15kBzVfcenZ3dnT90X0kpCICxhBwEWwmAggLkU41Ql5TImduKkYsr5hyQ4laqkUklclarYLgLYBSZGEgZxmMQGBYIhMSJOxbhSxBhs2dyH0LXSarUraS9pV5rdmUn/jm/39K/nbc+OdiWZ6Q/89OvjdU937/v93u+9fu+1d/sDe0sZosj/ZjJZ1QDbM56okiQP1lWF24HswG5LKZbegNN7ep6s6FJRjgsOt+dxnRbnE+UTLkXQ412nsejlBZSC85od9udiu80G+3eIncBF0nmiJOxO+aDj3b5xD2d2a0hhzpaFUuAJBJvz40gCmyxuWdEtsARsdf1OcJQ9oaZ3HFaBiVN6mWOsS6UW1jGc12d3VH9FRJDaeViV50tIlnqAOsf7p/vUA/Cqm/6uA7pkspTDArEQpk7IiiCWzJ6nMqUgQXW/s37dYdYlvYGWZrHwO+74DmtQVNd4221fYP38KwtYx1wmcPy8LePjHgJUd/0hldPPWTZXlyYm9QB1jnfHhmgMAItAzhoILD+KKwfHotkA2V5t7FAt7R1NrC+7bAnrNefPYT1vNqsYj2/4ni4JixYv1CX53RnZUdGeaEt3QSzr+Z/PZx3gcAhucJ/2fmUdz8nlaKolyROkHqDO8e5UD6DV6wBXmW/za+gxJC/Z/eGG2B6l8nZsvfVPz2a9+IyZrGvFWr7FeoLOhkOsATxerinH+q0B8Tz/+8ZS1hZcf7UWbGtdeJ7h4bpU5fksLk+QeoA6x7trQxfnKVjy4T29rGNoxgwyqgNYSpgOS0lHCp2dHazXXjDGGsehBfDSKz7Mulqe2PR91jjexab7n2I9b77EEIMDg6xd4GyeJzZ08Q1/wzrAFezY6wiSyYIrhgpjLjk+5lnM73nBFUaxniD1AHWO942N6gE0Sx3ucngAgzPa180lrZgH6YLk5jiTUf/4iytY9/V0swYNDY2sZ84WD7Fq9WLW4NYv/B3rDd+VevzTj2xkPXK0cjQPcs1Slm/YsIU1OHp0WJcmZuz4OOsbPn8X61rJaktrKaGaVNmuqyf1ACkRvG+qB0DR5GzxM8QNWhay+tbui186j/XypWK5Lu68403WZ585xLpz6SzWAJYPCgWxuGxWy95LV7MG9319E+t5cyauNbS3Scvft/5ZYgQwPISyXx6IfQdibfD635us5U/8XANO1NQdzFk2T5eE1APUOYEHQI5LigFclv+5P/gQ63NXSxltKage1+B+DDovC30H+ln3H4rWv5MY2LeL9ZnLJHpHtP/6q3tYh+0UUR7c/LQuCQOHbb1f0djI9l+48ffvloX4AzlB9DzWNOGiK9+Of5jjuADZP0efE0g9QJ3j3R2LAVztAJVzOLb+15a/1yXhx288y3p0RGw/f1wsfWwszxrr0IcPigcAhXEpfBsaG1gD9BA63LWdNWIBWMbypeoJ1GJ/uW0H64YGOY+1/EN9EvOgPg9wfKkk14/13/mjb7MO77wy7rd9yrSZ3sS/m3qAlAiBB1ADquABojnKlb+e3/IVXcKZhMd/9Bjr4aEjrMfHJIqHPn5cPEI2K9E+LDx//DjrhkbJo6gN5DV9/siA6BGpPQB4hE7z7uDLf3EPa1z/6KjU80eOSDsBfje0fNHFoniAJ5/6JuvRY3JdW7ZGayvuJxOldMImV93vuJideoCUcgIPAEIPMLmchha/rVukRc5yz8NiQeNaDUC07mWlbEYZDQsPLV9a6uBZ7P7BbqkFwPKLxWjFfXlnNCa47csSvR8+KPeZV4s+b+0a1n/5lb9mvXjpWay9rOwPYg3lmX+XlsqefSOsayX0CCdm2e7DoztmaYwEoneVUnd439ok4wLQ922gq4+1xZ0/dY9J8NwTlT3BXfffzhqGmmtuZo0WvtAzsHIy3LuXdXFcjnNxwVWflIWSeB5b1hfGpYxHbcPuB0iXyUgL4uaNb7F2mpBtQTTpcPbwsUUfYPTXK2Ced4UNFZmdeoCUcrx71QMgx/U7+gPEM1xSjpP9P3zib1mDf7znH1g3ay9clOUAtYFi0Vo2fk+vVF3E4D6p56PsR1l93mVi+Q2NE1t+rll6+BQK6glMLAKQbtM977CerOkkWrTeX/ypmi26mny+yqQeICUCv7srl6xvKeUS7KPlcik7JiryH+Uskk999qss2NvW3sZCll9u/VTPJ/FPzWIhyyShFkJuJaTXdL6QRdvymiDLJyFLJ8F1N/plPUlTrpGF6vmo6xMUi5CQxZNQbEBy/z1vs5DjYfHTTkbwPMJt1FYo7YUVRa+XnkVEdD/OF0q1/9HfplxS6hrv2yYGcNUCEqFsychCsBogW66+Tsr4bEM0Ber7hYKU2XgX0JSTshdh9VheYgNE7f1732dty/6MjulDOpTtKOuBrQWQdyDy+pYS5918n7x7iBO/0wie8U66an0WWbsuqQZTa6Ozl0YHTKQeoM7xNtyPdgBej3sAzZBUrkeJ5WHVluh2rF29Hi18Fklho3RE5WHULp4ALYFg7SfWs7aWDuItjrJuQVzxyEbxMHH0Tqp9DAZ7GA4MD58a27S/k3qAlAjeRvUAyCnxGCAhSwdZSNPBlTiOC7fK0lWBJ5Djwn4A0byJ7dYD4C3hinNWsq62jB/X7RYUxTjvg/e+zRpUvqsy9LJLxaSUdn+Ntug8rPLvz9Y+l/gr1firKR8UvE06RxB6v4YewJGDgywj+935XPcEHkExx4MrrxeLc2H7A+AdAnrsLD9bxhACa/kWVyyA7Q/fpy1+k8b1RPA8RIVMzgZL2uu6VmaZXtepB6hzAg+AnDnQdVAWlPhbuYQcriTnU6SAh5D1KwJPEPUcaCdATyHEAsvOkpFEwNb3raW7ahVYf/HH0jt4z45oTyMQrw0lUV36UqItJpzH7jaOF/tnpbWAlHK87yAG4FW/Xm08gMVtAdXl0GQLkv2XXRfNm7Z2sHK1jAga0wEGOW0xHNf+AdYTuGICu314UDzMs9/vYp14XzFMenu4wzJjthikq/z7CbsDwuctR6QxQEoE74EqPUCS5cf2Jm9gsPXCK8TCi4VomNzWLtF+mFKuFB7ARvGJeBJLjGiv4lxOzo+2eHgYjBPAdujWVtn+wDe0fSBow6+Vam2wyt9JSDYz9QAp5Xibq44BolkrXNOlxAwqCZavlP76Czolyi6iD6AeX0BnQb2gxiapFTQ1SV6F5dsWP7zT7+2WHk25FokJGhvl+Macaq1NoK0f++FB0LOoqUnSzZ9X2Ubu/Wqt7QQ1Wnzi850Y/H3TGCAlgvcw2gGU/pgHqJz1wvfXE3Pdp2U8ev8hGfsHi4flwRKD0+kCZgfPalmc1ageWbkpJxba0CD7sY7zoX7f2Cjb8Q4AHgVlPNLjvX9bu2rH1MDg9Z/LiKKfPCejkJOR8wY4H191z7Va7BjFNAZIieA98sA+tSlRg3vFAyDnqIGEFhpQOade/skZrMfGpD4N0NsXh+FoG2Wj/g6LR1mfg8WrJSNdUGYHHkHL9OA8ksfjHid6/QvmS/rJct/XXLFA1Laiv1ZO5T362DO3/NU5rDWEcYJpFR539l8QUg+QEqHMAwhD6gFALH+aL3cgxbU3ySzax0elXh6Ot5d0sES4koKODoblBvuVBrVYzDkEi0VZDUsH2I6+hlh3xRwLFySYVJVsDDxA9PpdVPsu4dyL9Pk2SaxxyW+ez1onNXPSc0BaRp9+sHJsknqAlAjeo9V6AMd7aGzNzjQ9Z9Rir/3UdawL2kZvy15E+yizsR8eBPV7tNjBU2B+AXgQgNPDAxS0ZXHRwgTTqZH7v/aeLrmI3i+ovNVHd6xaG/UAloWLF7GePbfyHMDPbNZ3GZG/LnmA6LwJqQeoc7zH1AMgo8ADBDk0wfJBY4uUOYWcjJe3b+NAW7tUsK+64RrWocWLRlQf1tej+1HvxxWEbwPFwufNPTV5+oGvO8YNGAtMNH3lQ2u1RdThAcCq36g8d/J/PIi3mYqefkbqAVLK8R7bHI0BhoMYIJoj4xnXkZVn6rh5BWUy2hNcfO6Wm1iPHBWLhsUDrNuePm3tottbWZ0yHlQPEF614/kETOwaVp6gB/ghYgBD6gFSInj/ajxAWAswFqjalbNRvy3Nkrl/bf3bWi7WXR4CFv+7n/8M64z2/q21xW66eQgxgPVcqifLWR9VDwAcnsDlAbZaD6DXNaMz9QApZdAUAJw5KH+I4D9ZpxxCEu6Pbsc4c5wne7yNhVrcygWQ5ZfXDKiejro6QR6CBMc99dgTLC88/z8spytUWWKh5TKhZ0Vit8fFjNvPtrDUip3nwf17KXUN1/JZ/H9Igpys4v9fWfx/yiXIWcdXsDT59XgSqtejbk/AsmHpAOs2PaD+BOhTcDoCvxlaWJXiPzwRWg6lWDzGUivx34LFQ8J9KXVMkAH8TFdZ/NxJEs+p0XXgb2KhYp/EWjTOB6jNnqTE8/2Ec/7AI+B8NlY43YA10Z2RYN1ux/1DbDpIAEX/FWoA9C4E70PKwfMk31ou/hOOin8xLP6+lDrGe/wh2xIoXUsotwrhEkHWGEU2YLOfr3VJGG1/nTWsHuU+2vDteH2KGwRJj3QAvXVvufXTrE81u3fILOgvPhH9xnL0KRDxLYQr3RnrpNe063mvXC1faEG/CfCTh2QGVcfPZTrSdoCUcrj4riSAcmC5AFqsJFhAemoJRGsggXaAMOovsZBli3XLCWx7Aco2u/1k090zyLJv3wBLU0uBpdG/WRKU4foYgnWXxNNJGQ0QS0H8f1nI8q31E55XEvHTVJJIHMCSUtf4HgC5A7lR1zUnWZAOBOl0B44H1LMn7B8YAotG1A+shdP7fxJ4FNQqNt3+A5bphj4MStJzYIiF51Eoq4wUiv71+nLpZxexUJdEkkYVrDf4z4gEzwuSVbHb8Vzs86HFstUYOJ9L8BzTWkAKE5qW/3+5hIvFqHgQza3G4kNoWymTG1zFYoEloz5sLR+XhRyPdgDEFA0d4yzTRe/BEZaBw0dZaIYSErkr36K1DMb1zJiTY4l5QCPwBHERTzHn/AEWGiVNYj3BkmWdLJag3UR/vwGi5230f4MEvxd4BT0+pU7x/u2R6NhAtANYKPeKxhIOw7pg2wHCNclrHefILGQjR4+qlvZuWD/aCcq9QTl2/5/8ufQkOlF6Dkh9HuMQ2P2Q0jtAewXaM8a0Fa65Recv0MMa/LiG2HrvxL2FNXkA1jvO028X64ZwbKRsOHeNfJPZ8tKj0RlT9TJjtHemcwSllOE9qR4A9ow+gbEMZLJUuObaLsCCsH3WuTIzB74ZjNN6nljY0SPSq3h4aOLv99sc/qU/m5wngMXbcQnhiCehpRXzEcp2qrkQWG9uxjqrQOug5MwP7sTIoeh5zeVnWj8slo/t+B3o89d9lLX1jPBILz1aeUygjc/a9StqIPUAdY735KMaA2hGGd6rM4UGWdTm1SjYa8t+7AksXNfnfkQsbywvYwhDy5GFXIuYzrERKWNhmd17pY0bFjHZWODIiFTej+nYRYw4Ct5R+JE8o9eD625tk3kGrMfB0MTw/gQ4EC2yMzqFUeY/7za9pVXPXCNv+vJ5GU2N68F9Yn3NRReytrz8Xdd3DAT8Dky9fUl0JFHqAeocb8dBNT0xKD8nirbo7sQsE+x2pNv5s1dYj45Izvd0pE+pIJeBsX7542Kh8Azj41JbaG2TAQANxXbWu/a8y9rlAXr7JKbwa9GsG9V0wz4Ksh19DXD+ppzcsToavxYgGh4LlYVqLWiXdmbSD5Vm9m6T55A3D9yDhzNlvwVvRf/vYemFXS0dqQdIKcfbDg+gaFE05YwMSJQ73C3f+Rsd0W/6qAfAOIJmnd1LPzEcMDwkx7d3iIWibIS+/saPsQb9AyjrxbJxfpSt6Gcw2C/nHdHah39G/nfJ8sWs584XT6OTlE2ayMP1eeFH21gfG5UHjetCYU29rIgLP3YRaxev/It4Pid6PlUB7YtTD5BSxvR7AM1iQzukPjw0gFm4YZFSyFJ/QAIta54nhS4sfKD/MOtmnf0L22FB1994MWvL0BGJJTAnMOjtkdpOb4/MK1gqBlHOhFxwsczUMUumQqoaPGRoWObzz77EGnMcX/TxqCcDiIW6firX3adBBZ5DtbQvkVnbcCWpB6hzTtwDVJmFDr71GmtE//TVTtYazaKsRu+h1rYO1rCV/n7J+UWdNRzzB8AyPnH9WtYWrfYHFjfQL+0QXTtlPgO0PGaz4lmSuPIa8QBTBfxSn87tYxksaZOiRW/o/e9Jn8skcP9tgQcQUg9Q50zeA9SYZRADDA9KGz/a2NGih5Y5zP41Z/581rDwgwek123YmzgaI1xx9RrWLsbEcWT269vOPTtk9GyxWN0N1Wr5+F1XLQIPHxba3S1/gOGsvmVMQl3I+1vEw+JE9h0AaF8szxWkHqDOoWFikmsglCUmkhppae1gwVfDqT7O0iCCvoMYIUTtASQ05y/m/SWC41TQIycJ+gwAycjRURb0SJpuyPInakPAYweDhRxL1ZAD9WXlzWsiEuvJFUjYi4vkBP6kKR8ETloGOO7X10lC6/VUGlRkOzxBU1OOBRYeHidCtQASeJQknn78BZb8sTxLtZ5juiDfU8n/ZJv8Z+JLzVDR78tZN1/I4pv5hJJ6gDrnpGWAtvlnsNgsSDOIYhbRcmhWcBJqLyCBx8C8AxT8SwWAbiH5NuiLISTb39nFks8XWU4V9qrf6RGZMuAJbvI9gS/YoJuDP8FJywAppyfe9kOmHcDRH2Cq6HvzVdbN2vMH2O8CrjhH5skHO9+t3PNFO81mLrms8mxZb7+1j/WO96TlD+0KM2bIWz4xBTcYg3/N+sotjV1d0pK4bFkb6xOFRiERu6JTNk8ZOuVypuu/tYcV/5tSt0y7B7D21ZvgASjCJ85aFfUAu7aLB9CXhoHlA5cHeO4ZeduGlsfxMWk6yyVNvK8ktQBifn7LvAVy/lr7Eby6U87b3FrddVYLPMBkezSlfECZtgygQeYJE0b7Alk+CXkMEvII8AqVmDGzgwXtCu0d7SzTzaG+MZb9PXmWyVL0b4rFvzdusMQDTRIXZj91oyBJPUCdw0XBRBknCRxvJQn6iph8SSx6BCy82pY6GtmD0T2VaMzlWNra21laWltYpore7i4Wql2ghlEOva0koVjBFS+U8/KbAyyARiqR4Cm5JKDSThLFbk49QJ0z6Qxgc9BUgTb9YBy+WhTeFbiAhbhoa2sV6VDx6/8kU8XCJQtZ+g/2sOzv2sVCzqCCQwg8AXVECjoilzFz3mwW+mo6SWOTx5KE/bu4xJJ6gDrnlGUAvPenHkDl3wBE1B8vUyvn4YZGj8XF4HgzS6bUxjJ4+DDLiUJXRrJoUQfL0hWdLLPnzWLp7d7DsnfXdhbL8FCehXoAkbx7IMOCu8T5IdNF6gHqHO/9k/wu4MAbv2Ldqp/nRvleKEgjOCL/zjOXs875ETzx9mtvsMa7ArQYrrt0NWvrA0a0b+Mv34zOeDLWv5819Y6pBldLIHrz2uhkXJ9m/yEp4N/f3s262BYdl4/R0i2tMtKpfebJ+eiRPs6A1APUOSc9A8yaPYclLONFaORO+egdzJJ1sLeXBaCWQDOKsPjbrPUTv3ijj8XS5HsQkiRcs3GD3TsOsbz7Th8LwPyA8+e3sRRb57CQxdN/QY8mbZ/INvq1HJ1/6FSQeoA656THAIO7dC6borSKYVxAXqfSoF5AxIpzVrJ+7035JjHK/CYtxPB+YN0lMmu25cVtlWc72/Pqy6wXnrGQdWMTrC/qR1xl//4eGds4rDOOHBwUr1UYk+v/yCr5pu/uPglC2vBBQzU1XHf0104eaQyQEuGke4BjQ2JBO3WGDIC5fi7QuXAG+iVdqSTlMMUDrLUvP8YKTNYDdL0W/V0XN//hetaweEvvgFzXiDbv4yveZU0apyWpB0iJcNIzwMD+bhYXCxYtYAFoMbRv/chj2DnzoqCGMT2MjIyz5JpbWMjyT3frr0TqAeqcWAwApisW8I2ZyffI6Nwd70Xn1D3z7LNZw7r37t7NGsycJd+8ufa31rEGuIljWiZvMy2AoOtX1cUAv/0ZiQGGNGaxdPfLL86YO4v16Y4t+0HqAeocpwcA010rQKle0Eb0YzqL+DGdUO/A2/LuAMAzXHol5gTC5cuZ9vRp653J2njnQCORiZ2v/JS1iytv+LguKZ70+x/O/HoV9C7LB6kHqHMSPQCYrCeouaXLHJgflUJ99y9+xnpsTDzDxZdHZ9BEC2LvqHR8px7ARFb7CqAFzgV2b9u6lfVV6y9nPZiRuYpqvp9TRJLlg9QD1DlVe4BamTLLMSfCVSdZdq38ull8raQeoM7hqWmn0oroVOUyaewJIIapvu56JfUAdU0m8/+4ajjhQPg9lQAAAABJRU5ErkJggg\u003d\u003d",
            "lastUsed": "2022-09-12T00:45:47.991Z",
            "lastVersionId": "1.16.5-TheBigWolf-Pixelmon",
            "name": "TheBigWolf-Pixelmon",
            "type": "custom"
            }
    }
    if (os.path.exists(filepath) == True):
        with open((filepath), 'r+') as file:
            file_data = json.load(file)
            file_data['profiles'].update(data)
            file.seek(0)
            json.dump(file_data, file, indent = 2)


def finishedPrompt():
    messagebox.showinfo("Successo!", "Pixelmon installata, ora ti basterà avviare il launcher e se non hai mai avviato la 1.16.5 dovrai prima avviare la 1.16.5 e poi potrai avviare la pixelmon!")

def setProgress(current, total):
    global progress
    size = (current / total * 100)
    progress['value'] = size / 2

def setFinalProgress(current, total):
    global progress
    size = (current / total * 100)
    progress['value'] = size

def putDownloadBar():
    global progress
    progress = Progressbar(screen, orient= HORIZONTAL, length= 1000, mode= "determinate")
    progress.pack()

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