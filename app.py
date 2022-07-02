import tkinter as tk
import random
import threading
import os


from tkinter import Label, Button, PhotoImage, StringVar, Entry, Tk
from PIL import ImageTk, Image

from APIs.sheets_API import getSheetData, setSheetData

from UserConfig import UserConfig
from OfflineGame import OfflineGame
from constants import *
from interface import *


class contractWhistClient:
    def __init__(self, parent):
        self.window = parent
        self.window.resizable(width=False, height=False)
        self.window.title("Contract Whist Client - 1.2")
        self.window.iconbitmap("res/icon.ico")
        self.windowSize = list(WINDOW_SIZES.keys())[0]
        self._resize(self.window, self.windowSize)
        
        self.colour_schemes = self._getColourSchemes()
        self.user_config = UserConfig()
        self.makeHomePage()


    @staticmethod
    def _getColourSchemes():
        colour_schemes = []
        for file in os.listdir(CARD_PACKS_LOC):
            d = os.path.join(CARD_PACKS_LOC, file)
            if os.path.isdir(d):
                colour_schemes.append(os.path.basename(d))
        return colour_schemes
    

    def _resize(self, frame, dimentions):
        w, h = WINDOW_SIZES[dimentions]
        frame.geometry(str(w)+"x"+str(h))
        self.windowSize = dimentions

    
    def updateColourScheme(self, home_frame, colour_string):
        self.user_config.setColourScheme(colour_string.get())
        self.showColourScheme(home_frame, colour_string)


    def updateLayout(self, dimentions):
        self._resize(self.window, dimentions)
        self.makeSettingsPage()
    

    def showColourScheme(self, frame, colour_string):
        colour_scheme = colour_string.get()
        h = root.winfo_height()//2
        w = int(h*0.6887)
        self.placeImage(frame, "res/card_packs/" + colour_scheme + "/zas.png", 0.8, 0.5, w, h, COLOUR_PRIME)
        self.placeImage(frame, "res/card_packs/" + colour_scheme + "/bk.png", 0.2, 0.5, w, h, COLOUR_PRIME)
        colour_string.set("Colour Scheme: " + str(colour_scheme))


    def makeHomePage(self):
        home_frame = self._makeFrame(self.window, COLOUR_PRIME, 1, 1, 0, 0)
        self.window.update_idletasks()   

        self._makeLabel(home_frame, "Username:", COLOUR_PRIME, COLOUR_TEXT, 0.46, 0.4, "e")
        
        username = StringVar()
        username.trace("w", lambda name, index, mode, username=username: self.user_config.setUsername(username.get()))
        username_entry = Entry(home_frame, width=18, bg=COLOUR_WIDGET, fg=COLOUR_TEXT, textvariable=username)
        username_entry.place(relx=0.48, rely=0.4, anchor="w")
        username_entry.insert(0, self.user_config.getUsername())

        self._makeLabel(home_frame, "Identifier:", COLOUR_PRIME, COLOUR_TEXT, 0.46, 0.45, "e")
        self._makeLabel(home_frame, self.user_config.getIdentifier(), COLOUR_PRIME, COLOUR_TEXT, 0.48, 0.45, "w")

        #identifier_entry = tk.Entry(home_frame, width=18, bg=COLOUR_WIDGET, fg=COLOUR_TEXT)
        #identifier_entry.config(state="disabled")
        #identifier_entry.place(relx=0.48, rely=0.45, anchor="w")
        #identifier_entry.insert(0, self.user_config.getIdentifier())
        #identifier_entry.config(state="disabled")

        colour_string = self._makeStringVar(home_frame, self.user_config.getColourScheme())
        colour_option_menu = self._makeOptionMenu(home_frame, colour_string, self.colour_schemes, 21, COLOUR_WIDGET, COLOUR_TEXT, 0.5, 0.52, "center", lambda x=None: self.updateColourScheme(home_frame, colour_string))

        self.showColourScheme(home_frame, colour_string)

        resolution = str(root.winfo_width()) + "x" + str(root.winfo_height())
        resize_string = self._makeStringVar(home_frame, "Resolution: " + resolution)
        resize_option_menu = self._makeOptionMenu(home_frame, resize_string, WINDOW_SIZES, 21, COLOUR_WIDGET, COLOUR_TEXT, 0.5, 0.59, "center", lambda x=None: self.updateLayout(resize_string.get()))

        self._makeButton(home_frame, "Offline With Bots", 15, COLOUR_WIDGET, COLOUR_TEXT, 0.5, 0.7, "center", lambda: self.setupOfflineGame(username_entry.get()))
        self._makeButton(home_frame, "Multiplayer", 15, COLOUR_WIDGET, COLOUR_TEXT, 0.5, 0.75, "center", lambda: self.joinOnlineGame())
        self._makeButton(home_frame, "Exit", 8, COLOUR_WIDGET, COLOUR_TEXT, 0.5, 0.96, "center", lambda: quit())



    def joinOnlineGame(self):
        print("join online game")
        lobby_frame = self._makeFrame(self.window, COLOUR_PRIME, 1, 1, 0, 0)
        self._makeButton(lobby_frame, "Back", 8, COLOUR_WIDGET, COLOUR_TEXT, 0.01, 0.01, "nw", lambda: lobby_frame.destroy())#self.makeHomePage())


    def setupOfflineGame(self, username):
        bot_count       = ["1", "2", "3"]
        start_round_size = [1,2,3,4,5,6,7,8,9,10]
        round_size = 10
        
        config_frame = tk.Frame(self.window, bg=COLOUR_PRIME)
        config_frame.place(relwidth=1, relheight=1, relx=0, rely=0)

        self._makeLabel(config_frame, "Number of Bots:", COLOUR_PRIME, COLOUR_TEXT, 0.5, 0.42, "e")
        bots_string = self._makeStringVar(config_frame, bot_count[-1])
        bots_option_menu = self._makeOptionMenu(config_frame, bots_string, bot_count, 6, COLOUR_WIDGET, COLOUR_TEXT, 0.5, 0.42, "w", None)# x=None: setBotCount(bots_string.get()))

        self._makeLabel(config_frame, "Starting amount of cards:", COLOUR_PRIME, COLOUR_TEXT, 0.5, 0.48, "e")
        card_count_string = self._makeStringVar(config_frame, round_size)
        card_count_option_menu = self._makeOptionMenu(config_frame, card_count_string, start_round_size, 6, COLOUR_WIDGET, COLOUR_TEXT, 0.5, 0.48, "w", None)

        self._makeButton(config_frame, "Start", 8, COLOUR_WIDGET, COLOUR_TEXT, 0.5, 0.7, "center", lambda: self.startOfflineGame(username, int(bots_string.get()), int(card_count_string.get()), self.user_config.getColourScheme()))
        self._makeButton(config_frame, "Back", 8, COLOUR_WIDGET, COLOUR_TEXT, 0.02, 0.02, "nw", lambda: config_frame.destroy())





    def startOfflineGame(self, username, bot_count, start_round_size, col_scheme):
        print("offline with bots")

        offline_frame = self._makeFrame(self.window, COLOUR_PRIME, 1, 1, 0, 0)

        loading_frame = self._makeFrame(self.window, COLOUR_PRIME, 1, 1, 0, 0)
        self._makeLabel(loading_frame, "Loading...", COLOUR_PRIME, COLOUR_TEXT, 0.5, 0.5, "center")

        self._makeButton(offline_frame, "End Game", 8, COLOUR_WIDGET, COLOUR_TEXT, 0.8, 0.025, "center", lambda: offline_frame.destroy())


        offline_game = OfflineGame(offline_frame, player_names, col_scheme, start_round_size, self.cards_deck)
        offline_game.offlineStart()



    @staticmethod    
    def _makeFrame(frame, bg, rw, rh, rx, ry):
        new_frame = tk.Frame(frame, bg=bg)
        new_frame.place(relwidth=rw, relheight=rh, relx=rx, rely=ry)
        return new_frame


    @staticmethod
    def _makeLabel(frame, text, bg, fg, rx, ry, anchor):
        label = tk.Label(frame, text=text, bg=bg, fg=fg)
        label.place(relx=rx, rely=ry, anchor=anchor)
        return label


    @staticmethod
    def _makeButton(frame, text, width, bg, fg, rx, ry, anchor, command):
        button = Button(frame, text=text, width=width, bg=bg, fg=fg, command=command)
        button.place(relx=rx, rely=ry, anchor=anchor)
        return button


    @staticmethod
    def _makeStringVar(frame, default_value):
        stringVar = tk.StringVar(frame)
        stringVar.set(default_value)
        return stringVar

                         
    @staticmethod
    def _makeOptionMenu(frame, displayed, choices, width, bg, fg, rx, ry, anchor, command):
        optionMenu = tk.OptionMenu(frame, displayed, *choices, command=command)
        optionMenu.config(width=width, bg=bg, fg=fg)
        optionMenu["menu"].config(bg=bg, fg=fg)
        optionMenu.place(relx=rx, rely=ry, anchor=anchor)
        return optionMenu


    @staticmethod
    def placeImage(frame, directory, relx, rely, w, h, bg):
        image = Image.open(directory)   
        image = image.resize((w, h))
        img = ImageTk.PhotoImage(image)   
        label = tk.Label(frame, image=img, bg=bg)
        label.image = img
        label.place(relx=relx, rely=rely, anchor="center")
        

if __name__ == "__main__":
    root = tk.Tk()
    contractWhistClient(root)


