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




def makeEntry(frame, width, bg, fg, textvariable, rx, ry, anchor):
    entry = tk.Entry(frame, width=width, bg=bg, fg=fg, textvariable=textvariable)
    entry.place(relx=rx, rely=ry, anchor=anchor)
    return entry



    
