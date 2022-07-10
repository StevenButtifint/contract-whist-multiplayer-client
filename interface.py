import tkinter as tk
import tkinter.font as font
from PIL import Image, ImageTk
from constants import *



def makeFrame(frame, bg, rw, rh, rx, ry, anchor):
    new_frame = tk.Frame(frame, bg=bg)
    new_frame.place(relwidth=rw, relheight=rh, relx=rx, rely=ry, anchor=anchor)
    return new_frame


def makeLabel(frame, text, bg, fg, rx, ry, anchor, size):
    label = tk.Label(frame, text=text, bg=bg, fg=fg)
    label.place(relx=rx, rely=ry, anchor=anchor)
    label['font'] = font.Font(family='Helvetica', size=size)
    return label


def makeButton(frame, text, width, bg, fg, rx, ry, anchor, command, size):
    button = tk.Button(frame, text=text, width=width, bg=bg, fg=fg, command=command)
    button['font'] = font.Font(family='Helvetica', size=size)
    button['borderwidth'] = 2
    button.place(relx=rx, rely=ry, anchor=anchor)
    return button


def makeStringVar(frame, default_value):
    stringVar = tk.StringVar(frame)
    stringVar.set(default_value)
    return stringVar

                     
def makeOptionMenu(frame, displayed, choices, width, bg, fg, rx, ry, anchor, command):
    option_menu = tk.OptionMenu(frame, displayed, *choices, command=command)
    option_menu.config(width=width, bg=bg, fg=fg)
    option_menu["menu"].config(bg=bg, fg=fg)
    option_menu["borderwidth"]=0
    option_menu["highlightthickness"]=0
    option_menu.place(relx=rx, rely=ry, anchor=anchor)
    return option_menu


def placeImage(parent, file, w, h, x, y, anchor):
    canvas = tk.Canvas(parent, bg=COLOUR_SECOND, width=w, height=h)
    canvas.place(relx=x, rely=y, anchor=anchor)
    canvas["highlightthickness"]=0
    img = Image.open(file)
    img = img.resize((w,h), Image.ANTIALIAS)
    photoimage = ImageTk.PhotoImage(img)
    canvas.create_image(w//2, h//2, image=photoimage)
    return canvas, photoimage


def makeEntry(frame, width, bg, fg, textvariable, rx, ry, anchor):
    entry = tk.Entry(frame, width=width, bg=bg, fg=fg, textvariable=textvariable)
    entry.place(relx=rx, rely=ry, anchor=anchor)
    return entry



    
