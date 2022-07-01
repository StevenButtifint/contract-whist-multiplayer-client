import tkinter as tk
import tkinter.font as font
from PIL import Image, ImageTk
from constants import *



def makeFrame(frame, bg, rw, rh, rx, ry, anchor):
    new_frame = tk.Frame(frame, bg=bg)
    new_frame.place(relwidth=rw, relheight=rh, relx=rx, rely=ry, anchor=anchor)
    return new_frame


def makeLabel(frame, text, bg, fg, rx, ry, anchor):
    label = tk.Label(frame, text=text, bg=bg, fg=fg)
    label.place(relx=rx, rely=ry, anchor=anchor)
    return label


