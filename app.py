import tkinter as tk
import random
import threading


from tkinter import Label, Button, PhotoImage, StringVar, Entry, Tk
from PIL import ImageTk, Image

from APIs.sheets_API import getSheetData, setSheetData

from res.classes.UserConfig import UserConfig
from res.classes.OfflineGame import OfflineGame


class contractWhistClient:
    def __init__(self, parent):
        self.window = parent
        self.window.resizable(width=False, height=False)
        self.window.title = "Contract Whist Client - 1.0"
        self.window.iconbitmap("res/images/icon.ico")
        self.window_sizes = ["800x600", "900x700", "1200x700", "1600x1100", "2100x1300"]

        self.colour_schemes = ["Default", "test"]

        self.colour_prime   = "PaleGreen1"
        self.colour_second  = "PaleGreen2"
        self.colour_text    = "DarkGreen"
        self.colour_widget  = "DarkSeaGreen2"

        self.cards_deck = ["2c", "2d", "2h", "2s", "3c", "3d", "3h", "3s", "4c", "4d", "4h", "4s",
                           "5c", "5d", "5h", "5s", "6c", "6d", "6h", "6s", "7c", "7d", "7h", "7s",
                           "8c", "8d", "8h", "8s", "9c", "9d", "9h", "9s", "vc", "vd", "vh", "vs",
                           "wjc", "wjd", "wjh", "wjs", "xqc", "xqd", "xqh", "xqs", "ykc", "ykd",
                           "ykh", "yks", "zac", "zad", "zah", "zas"]

        self._resize(self.window, self.window_sizes[0])
        
        self.user_config = UserConfig()


    @staticmethod
    def _resize(frame, dimentions):
        dimentions = str(dimentions).split("x")
        w, h = int(dimentions[0]), int(dimentions[1])
        frame.geometry(f"{w}x{h}")

    
    def updateColourScheme(self, home_frame, colour_string):
        self.user_config.setColourScheme(colour_string.get())
        self.showColourScheme(home_frame, colour_string)


    def updateLayout(self, dimentions):
        self._resize(self.window, dimentions)
        self.makeHomePage()
    






        
        

        
        








        
        















if __name__ == "__main__":
