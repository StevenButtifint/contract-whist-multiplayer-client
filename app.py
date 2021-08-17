import tkinter as tk
from tkinter import Label, Button
from PIL import ImageTk, Image

APP_TITLE   = "Contract Whist Client - 1.0"
APP_ICON    = "res/images/icon.ico"

COL_PRIME   = "PaleGreen1"
COL_SECND   = "PaleGreen2"
COL_THIRD   = "PaleGreen4"
COL_TEXT    = "DarkGreen"

COL_WIDGET  = "DarkSeaGreen2"


WINDOW_SIZES = ["800x600", "900x700", "1200x700", "1600x1100", "2100x1300"]
COL_SCHEMES = ["Default", "test"]


USERNAME    = ""
IDENTIFIER  = ""
COL_SCHEME  = "default"

WINDOW_W = 900
WINDOW_H = 600


def resize(dimentions):
    global WINDOW_W, WINDOW_H
    dimentions = str(dimentions).split("x")
    WINDOW_W, WINDOW_H = int(dimentions[0]), int(dimentions[1])
    root.geometry(f"{WINDOW_W}x{WINDOW_H}")


def updateLayout(dimentions, build_frame, user, identify):
    global USERNAME, IDENTIFIER
    USERNAME = user
    IDENTIFIER = identify
    resize(dimentions)
    build_frame()
    

def main():
    createHomePage()




if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=False, height=False)
    resize(WINDOW_SIZES[0])
    root.title(APP_TITLE)
    root.iconbitmap(APP_ICON)
    canvas = tk.Canvas(root, height=2000, width=2000, bg=COL_SECND).pack()
    main()
