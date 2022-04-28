import tkinter as tk
import random
import threading
import os


from tkinter import Label, Button, PhotoImage, StringVar, Entry, Tk
from PIL import ImageTk, Image

from APIs.sheets_API import getSheetData, setSheetData

from res.classes.UserConfig import UserConfig
from res.classes.OfflineGame import OfflineGame
from constants import *


class contractWhistClient:
    def __init__(self, parent):
        self.window = parent
        self.window.resizable(width=False, height=False)
        self.window.title = "Contract Whist Client - 1.0"
        self.window.iconbitmap("res/images/icon.ico")

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
        self._resize(self.window, WINDOW_SIZES[0])
        
        self.colour_schemes = self._getColourSchemes()

        self.user_config = UserConfig()

    @staticmethod
    def _getColourSchemes():
        colour_schemes = []
        for file in os.listdir(CARD_PACKS_LOC):
            d = os.path.join(CARD_PACKS_LOC, file)
            if os.path.isdir(d):
                colour_schemes.append(os.path.basename(d))
        return colour_schemes
    

    @staticmethod
    def _resize(frame, dimentions):
        dimentions = dimentions.split("x")
        frame.geometry(str(int(dimentions[0]))+"x"+str(int(dimentions[1])))

    
    def updateColourScheme(self, home_frame, colour_string):
        self.user_config.setColourScheme(colour_string.get())
        self.showColourScheme(home_frame, colour_string)


    def updateLayout(self, dimentions):
        self._resize(self.window, dimentions)
        self.makeHomePage()
    

    def showColourScheme(self, frame, colour_string):
        colour_scheme = colour_string.get()
        h = root.winfo_height()//2
        w = int(h*0.6887)
        self.placeImage(frame, "res/images/card_packs/" + colour_scheme + "/zas.png", 0.8, 0.5, w, h)
        self.placeImage(frame, "res/images/card_packs/" + colour_scheme + "/bk.png", 0.2, 0.5, w, h)
        colour_string.set("Colour Scheme: " + str(colour_scheme))


    @staticmethod
    def placeImage(frame, directory, relx, rely, w, h):
        image = Image.open(directory)   
        image = image.resize((w, h))
        img = ImageTk.PhotoImage(image)
        label = Label(frame, image=img)
        label.image = img
        label.place(relx=relx, rely=rely, anchor="center")   


    def makeHomePage(self):

        home_frame = tk.Frame(self.window, bg=self.colour_prime).place(relwidth=1, relheight=1, relx=0, rely=0)
        self.window.update_idletasks()   
        
        username_label = Label(home_frame, text="Username:", bg=self.colour_prime, fg=self.colour_text)
        username_label.place(relx=0.46, rely=0.4, anchor="e")
        username = StringVar()
        username.trace("w", lambda name, index, mode, username=username: self.user_config.setUsername(username.get()))
        username_entry = Entry(home_frame, width=18, bg=self.colour_widget, fg=self.colour_text, textvariable=username)
        username_entry.place(relx=0.48, rely=0.4, anchor="w")
        username_entry.insert(0, self.user_config.getUsername())

        identifier_label = Label(home_frame, text="Identifier:", bg=self.colour_prime, fg=self.colour_text)
        identifier_label.place(relx=0.46, rely=0.45, anchor="e")
        identifier_code_label = Label(home_frame, text=self.user_config.getIdentifier(), bg=self.colour_prime, fg=self.colour_text)
        identifier_code_label.place(relx=0.48, rely=0.45, anchor="w")
        #identifier_entry = tk.Entry(home_frame, width=18, bg=COL_WIDGET, fg=COL_TEXT)
        #identifier_entry.config(state="disabled")
        #identifier_entry.place(relx=0.48, rely=0.45, anchor="w")
        #identifier_entry.insert(0, self.user_config.getIdentifier())
        #identifier_entry.config(state="disabled")

        colour_string = tk.StringVar(home_frame)
        colour_string.set(self.user_config.getColourScheme())
        colour_option_menu = tk.OptionMenu(home_frame, colour_string, *self.colour_schemes, command= lambda x=None: self.updateColourScheme(home_frame, colour_string))
        colour_option_menu.config(width=21, bg=self.colour_widget, fg=self.colour_text)
        colour_option_menu["menu"].config(bg=self.colour_widget, fg=self.colour_text)
        colour_option_menu.place(relx=0.5, rely=0.52, anchor="center")
        
        self.showColourScheme(home_frame, colour_string)

        resolution = str(root.winfo_width()) + "x" + str(root.winfo_height())
        
        resize_string = tk.StringVar(home_frame)
        resize_string.set("Resolution: " + resolution)
        resize_option_menu = tk.OptionMenu(home_frame, resize_string, *self.window_sizes, command= lambda x=None: self.updateLayout(resize_string.get()))
        resize_option_menu.config(width=21, bg=self.colour_widget, fg=self.colour_text)
        resize_option_menu["menu"].config(bg=self.colour_widget, fg=self.colour_text)
        resize_option_menu.place(relx=0.5, rely=0.59, anchor="center")
        
        offline_button = Button(home_frame, text="Offline With Bots", width=15, bg=self.colour_widget, fg=self.colour_text, command= lambda x=None: self.setupOfflineGame(username_entry.get()))
        offline_button.place(relx=0.5, rely=0.7, anchor="center")

        online_button = Button(home_frame, text="Multiplayer", width=15, bg=self.colour_widget, fg=self.colour_text, command= lambda x=None: self.joinOnlineGame())
        online_button.place(relx=0.5, rely=0.75, anchor="center")

        quit_button = Button(home_frame, text="Exit", width=8, bg=self.colour_widget, fg=self.colour_text, command=root.destroy)
        quit_button.place(relx=0.5, rely=0.96, anchor="center")

        #config_button = Button(home_frame, text="config", bg=self.colour_widget, fg=self.colour_text, command= lambda x=None: createConfigPage())
        #config_button.place(relx=0.01, rely=0.99, anchor="sw")


    def joinOnlineGame(self):
        print("join online game")
        lobby_frame = tk.Frame(self.window, bg=self.colour_prime).place(relwidth=1, relheight=1, relx=0, rely=0)

        home_button = Button(lobby_frame, text="Back", width=8, bg=self.colour_widget, fg=self.colour_text, command= lambda x=None: self.makeHomePage())
        home_button.place(relx=0.01, rely=0.01, anchor="nw")


    def setupOfflineGame(self, username):
        bot_count       = ["1", "2", "3"]
        start_round_size = [1,2,3,4,5,6,7,8,9,10]
        round_size = 10
        
        config_frame = tk.Frame(self.window, bg=self.colour_prime)
        config_frame.place(relwidth=1, relheight=1, relx=0, rely=0)

        bots_label = Label(config_frame, text="Number of Bots:", bg=self.colour_prime, fg=self.colour_text)
        bots_label.place(relx=0.5, rely=0.42, anchor="e")
        bots_string = tk.StringVar(config_frame)
        bots_string.set(bot_count[-1])

        bots_option_menu = tk.OptionMenu(config_frame, bots_string, *bot_count)#, command= lambda x=None: setBotCount(bots_string.get()))
        bots_option_menu.config(width=6, bg=self.colour_widget, fg=self.colour_text)
        bots_option_menu["menu"].config(bg=self.colour_widget, fg=self.colour_text)
        bots_option_menu.place(relx=0.5, rely=0.42, anchor="w")

        card_count_label = Label(config_frame, text="Starting amount of cards:", bg=self.colour_prime, fg=self.colour_text)
        card_count_label.place(relx=0.5, rely=0.48, anchor="e")
        card_count_string = tk.StringVar(config_frame)
        card_count_string.set(round_size)
        card_count_option_menu = tk.OptionMenu(config_frame, card_count_string, *start_round_size)
        card_count_option_menu.config(width=6, bg=self.colour_widget, fg=self.colour_text)
        card_count_option_menu["menu"].config(bg=self.colour_widget, fg=self.colour_text)
        card_count_option_menu.place(relx=0.5, rely=0.48, anchor="w")

        start_button = Button(config_frame, text="Start", width=8, bg=self.colour_widget, fg=self.colour_text, command= lambda x=None: self.startOfflineGame(username, int(bots_string.get()), int(card_count_string.get()), self.user_config.getColourScheme()))
        start_button.place(relx=0.5, rely=0.7, anchor="center")
        
        home_button = Button(config_frame, text="Back", width=8, bg=self.colour_widget, fg=self.colour_text, command= lambda x=None: config_frame.destroy())
        home_button.place(relx=0.02, rely=0.02, anchor="nw")


    def startOfflineGame(self, username, bot_count, start_round_size, col_scheme):
        print("offline with bots")

        #frame for all to go in instead of root to destroy if back to main menu or game over
        offline_frame = tk.Frame(self.window, bg=self.colour_prime)
        offline_frame.place(relwidth=1, relheight=1, relx=0, rely=0)

        bot_names = ["Leon", "Napoleon", "Jesse", "Mr. Blonde", "Falcon", "Vulture", "Banshee", "Nova",
                     "Voyager", "Zoe", "Arya", "Lab Rat", "Katie"]

        player_names = [username]

        #pick random names for bots
        for bot in range(bot_count):
            pick = random.randint(0, len(bot_names)-1)
            player_names.append(bot_names[pick])
            del bot_names[pick]

        home_button = Button(offline_frame, text="End Game", width=8, bg=self.colour_widget, fg=self.colour_text, command= lambda x=None: createHomePage(userConfig))
        home_button.place(relx=0.8, rely=0.025, anchor="center")

        offline_game = OfflineGame(offline_frame, player_names, col_scheme, start_round_size, self.cards_deck)
        offline_game.offlineStart()







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


