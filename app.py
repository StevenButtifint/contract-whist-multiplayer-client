#python 3.9.4


import os
import time
import queue
import random
import asyncio
import warnings
import threading
import tkinter as tk

from threading import Thread
from PIL import ImageTk, Image
from UserConfig import UserConfig
from OfflineGame import OfflineGame
from SheetsConnection import SheetsConnection

from constants import *
from interface import *



class contractWhistClient:
    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(width=False, height=False)
        self.window.title("Contract Whist Client - 1.2")
        self.window.iconbitmap("res/icon.ico")
        self.windowSize = list(WINDOW_SIZES.keys())[0]
        self._resize(self.window, self.windowSize)

        self.lobby_active = False
        self.online_connect = SheetsConnection()
        self.colour_schemes = self._getColourSchemes()
        self.user_config = UserConfig()
        self.makeHomePage()


    @staticmethod
    def _getColourSchemes():
        colour_schemes = []
        for file in os.listdir(CARD_PACKS_DIR):
            d = os.path.join(CARD_PACKS_DIR, file)
            if os.path.isdir(d):
                colour_schemes.append(os.path.basename(d))
        return colour_schemes
    

    def _resize(self, frame, dimentions):
        try: self.settings_frame.destroy()
        except: pass
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
        h = WINDOW_SIZES[self.windowSize][1]//2
        w = int(h*0.6887)
        self.placeImage(frame, CARD_PACKS_DIR + colour_scheme + "/zas.png", 0.8, 0.5, w, h, COLOUR_PRIME)
        self.placeImage(frame, CARD_PACKS_DIR + colour_scheme + "/bk.png", 0.2, 0.5, w, h, COLOUR_PRIME)
        colour_string.set("Colour Scheme: " + str(colour_scheme))


    def makeHomePage(self):
        home_frame = makeFrame(self.window, COLOUR_PRIME, 1, 1, 0, 0, "nw")
        self.window.update_idletasks()
        canvas, self.home_BG = placeImage(home_frame, TEXTURES_DIR+"home.png", WINDOW_SIZES[self.windowSize][0], WINDOW_SIZES[self.windowSize][1], 0, 0, "nw")
        makeButton(home_frame, "Offline With Bots", 15, COLOUR_BUTTON, COLOUR_TEXT_D, 0.5, 0.55, "center", lambda: self.setupOfflineGame("You"), 16)       
        makeButton(home_frame, "Online Multiplayer", 15, COLOUR_BUTTON, COLOUR_TEXT_D, 0.5, 0.65, "center", lambda: self.makeMultiplayerPage(), 16)
        makeButton(home_frame, "Options", 15, COLOUR_BUTTON, COLOUR_TEXT_D, 0.5, 0.75, "center", lambda: self.makeSettingsPage(), 16)  
        makeButton(home_frame, "Exit", 8, COLOUR_BUTTON, COLOUR_TEXT_D, 0.5, 0.85, "center", lambda: quit(), 16)


    def makeSettingsPage(self):
        try:
            self.settings_frame.destroy()
        except:
            pass
            
        self.settings_frame = makeFrame(self.window, COLOUR_PRIME, 1, 1, 0, 0, "nw")
        canvas, self.settings_BG = placeImage(self.settings_frame, TEXTURES_DIR+"background.png", WINDOW_SIZES[self.windowSize][0], WINDOW_SIZES[self.windowSize][1], 0, 0, "nw")
        resize_string = makeStringVar(self.settings_frame, self.windowSize)
        resize_option_menu = makeOptionMenu(self.settings_frame, resize_string, list(WINDOW_SIZES.keys()), 21, COLOUR_BUTTON, COLOUR_TEXT_D, 0.5, 0.59, "center", lambda x=None: self.updateLayout(resize_string.get()))

        colour_string = makeStringVar(self.settings_frame, self.user_config.getColourScheme())
        colour_option_menu = makeOptionMenu(self.settings_frame, colour_string, self.colour_schemes, 21, COLOUR_BUTTON, COLOUR_TEXT_D, 0.5, 0.52, "center", lambda x=None: self.updateColourScheme(self.settings_frame, colour_string))
        self.showColourScheme(self.settings_frame, colour_string)

        makeButton(self.settings_frame, "Done", 8, COLOUR_BUTTON, COLOUR_TEXT_D, 0.5, 0.7, "center", lambda: self.settings_frame.destroy(), 12)        


    def makeMultiplayerPage(self):
        lobby_frame = makeFrame(self.window, COLOUR_PRIME, 1, 1, 0, 0, "nw")
        canvasBG, self.photoimageBG = placeImage(lobby_frame, TEXTURES_DIR+"background2.png", WINDOW_SIZES[self.windowSize][0], WINDOW_SIZES[self.windowSize][1], 0, 0, "nw")

        makeLabel(lobby_frame, "Online Multiplayer", "black", COLOUR_BUTTON, 0.5, 0.1, "center", 20)
        self.showPlayerIcon(lobby_frame)
        makeButton(lobby_frame, "Change Icon", 10, COLOUR_BUTTON, COLOUR_TEXT_D, 0.5, 0.48, "center", lambda: self.showPlayerIcon(lobby_frame),9)
        
        makeLabel(lobby_frame, "Username:", "black", COLOUR_BUTTON, 0.5, 0.55, "e", 12)
        username = tk.StringVar()
        username.trace("w", lambda name, index, mode, username=username: self.user_config.setUsername(username.get()))
        username_entry = makeEntry(lobby_frame, 18, COLOUR_BUTTON, COLOUR_TEXT_D, username, 0.5, 0.55, "w")
        username_entry.insert(0, self.user_config.getUsername())
        makeLabel(lobby_frame, "Lobby Code:", "black", COLOUR_BUTTON, 0.5, 0.6, "e", 12)
        lobby_entry = makeEntry(lobby_frame, 18, COLOUR_BUTTON, COLOUR_TEXT_D, "", 0.5, 0.6, "w")
        lobby_entry.config(show="•")


        self.notice = makeLabel(lobby_frame, "", "black", COLOUR_ERROR, 0.5, 0.9, "center", 12)
        makeButton(lobby_frame, "Back", 8, COLOUR_BUTTON, COLOUR_TEXT_D, 0.49, 0.7, "ne", lambda: lobby_frame.destroy(), 10)
        makeButton(lobby_frame, "Join", 8, COLOUR_BUTTON, COLOUR_TEXT_D, 0.51, 0.7, "nw", lambda: self.checkOnlineLobby(lobby_entry.get(), username_entry.get()), 10)


    def makeLobbyPage(self):
        self.lobby_frame = makeFrame(self.window, COLOUR_PRIME, 1, 1, 0, 0, "nw")
        canvasBG, self.lobbyBG = placeImage(self.lobby_frame, TEXTURES_DIR+"background2.png", WINDOW_SIZES[self.windowSize][0], WINDOW_SIZES[self.windowSize][1], 0, 0, "nw")

        self.slot_one_frame = makeFrame(self.lobby_frame, COLOUR_WIDGET_D, 0.16, 0.25, 0.2, 0.40, "center")
        self.slot_two_frame = makeFrame(self.lobby_frame, COLOUR_WIDGET_D, 0.16, 0.25, 0.4, 0.40, "center")
        self.slot_three_frame = makeFrame(self.lobby_frame, COLOUR_WIDGET_D, 0.16, 0.25, 0.6, 0.40, "center")
        self.slot_four_frame = makeFrame(self.lobby_frame, COLOUR_WIDGET_D, 0.16, 0.25, 0.8, 0.40, "center")

        canvas, self.playerOneImage = placeImage(self.slot_one_frame, EMPTY_ICON_DIR, WINDOW_SIZES[self.windowSize][0]//5, WINDOW_SIZES[self.windowSize][1]//3, 0.5, 0.5, "center")
        canvas, self.playerTwoImage = placeImage(self.slot_two_frame, EMPTY_ICON_DIR, WINDOW_SIZES[self.windowSize][0]//5, WINDOW_SIZES[self.windowSize][1]//3, 0.5, 0.5, "center")
        canvas, self.playerThreeImage = placeImage(self.slot_three_frame, EMPTY_ICON_DIR, WINDOW_SIZES[self.windowSize][0]//5, WINDOW_SIZES[self.windowSize][1]//3, 0.5, 0.5, "center")
        canvas, self.playerFourImage = placeImage(self.slot_four_frame, EMPTY_ICON_DIR, WINDOW_SIZES[self.windowSize][0]//5, WINDOW_SIZES[self.windowSize][1]//3, 0.5, 0.5, "center")

        self.slot_one_label = makeLabel(self.lobby_frame, "Empty", COLOUR_PRIME, COLOUR_WIDGET_D, 0.2, 0.56, "center", 12)
        self.slot_two_label = makeLabel(self.lobby_frame, "Empty", COLOUR_PRIME, COLOUR_WIDGET_D, 0.4, 0.56, "center", 12)
        self.slot_three_label = makeLabel(self.lobby_frame, "Empty", COLOUR_PRIME, COLOUR_WIDGET_D, 0.6, 0.56, "center", 12)
        self.slot_four_label = makeLabel(self.lobby_frame, "Empty", COLOUR_PRIME, COLOUR_WIDGET_D, 0.8, 0.56, "center", 12)
        
        makeButton(self.lobby_frame, "Leave", 8, COLOUR_BUTTON, COLOUR_TEXT_D, 0.3, 0.9, "center", lambda: self.leaveLobby(), 11)

        # host is given to player in slot one
        if self.online_connect.player_host:
            self.host_frame_edge = makeFrame(self.lobby_frame, COLOUR_WIDGET_D, 0.36, 0.22, 0.5, 0.73, "center")
            self.host_frame = makeFrame(self.lobby_frame, COLOUR_PRIME, 0.35, 0.21, 0.5, 0.73, "center")
            makeLabel(self.host_frame, "Host Options:", COLOUR_PRIME, COLOUR_WIDGET_L, 0.5, 0, "n", 16)
            makeLabel(self.host_frame, "Starting Round Size:", COLOUR_PRIME, COLOUR_WIDGET_L, 0.5, 0.4, "ne", 12)
            self.roundSizeString = makeStringVar(self.host_frame, str(ROUND_SIZE[-1]))
            self.roundSizeOption = makeOptionMenu(self.host_frame, self.roundSizeString, ROUND_SIZE, 4, COLOUR_BUTTON, COLOUR_TEXT_D, 0.5, 0.4, "nw", lambda x=None: self.setRoundSize())
            makeLabel(self.host_frame, "Cheats:", COLOUR_PRIME, COLOUR_WIDGET_L, 0.5, 0.64, "ne", 12)
            self.cheatsString = makeStringVar(self.host_frame, "No")
            self.roundSizeOption = makeOptionMenu(self.host_frame, self.cheatsString, ["Yes","No"], 4, COLOUR_BUTTON, COLOUR_TEXT_D, 0.5, 0.64, "nw", None)

            makeButton(self.lobby_frame, "Start", 8, COLOUR_BUTTON, COLOUR_TEXT_D, 0.7, 0.9, "center", lambda: lobby_frame.destroy(), 12)
        else:
            self.host_label = makeLabel(self.lobby_frame, "Waiting for host...", COLOUR_PRIME, COLOUR_WIDGET_D, 0.5, 0.7, "center", 12)
            
        self.lobby_active = True
        self.the_queue = queue.Queue()
        self.threadTest()

        


    def showPlayerIcon(self, lobby_frame):
        self.user_config.updateUserIconID()
        try:
            self.icon_frame.destroy()
        except: pass
        self.icon_frame = makeFrame(lobby_frame, COLOUR_PRIME, 0.15, 0.28, 0.5, 0.30, "center")
        canvas, self.playerIcon = placeImage(self.icon_frame, CHAR_ICONS_DIR+"player_"+str(self.user_config.getUserIconID())+".png", WINDOW_SIZES[self.windowSize][0]//5, WINDOW_SIZES[self.windowSize][1]//3, 0.5, 0.5, "center")


    def checkOnlineLobby(self, lobbyCode, username):

        session_ID, lobby_ID, page_ID = self.getSessionIDLobbyID(lobbyCode)
        self.online_connect.initialiseConnection()
        self.online_connect.setPlayerName(username)
        self.online_connect.setPlayerIcon("player_"+str(self.user_config.getUserIconID())+".png")
        
        if self.online_connect.link_status:
            if self.validateLobbyCode(session_ID, lobby_ID, page_ID):
                if self.online_connect.joinLobby():
                    self.notice["text"] = self.online_connect.notice
                    #create loading page
                    #~destroy lobby page
                    #create online lobby page
                    self.makeLobbyPage()
                else:
                    self.notice["text"] = self.online_connect.notice
            else:
                self.notice["text"] = L01
        else:
            self.notice["text"] = self.online_connect.notice
        

    @staticmethod
    def getSessionIDLobbyID(entryCode):
        session_ID = entryCode[:44]
        lobby_ID = entryCode[-6:]
        return session_ID, lobby_ID


    def validateLobbyCode(self, session_ID, lobby_ID):
        self.online_connect.setSessionID(session_ID)
        self.online_connect.setLobbyID(lobby_ID)
        return self.online_connect.checkForLobby()


    def setupOfflineGame(self, username):
        config_frame = makeFrame(self.window, COLOUR_PRIME, 1, 1, 0, 0, "nw")
        canvasBG, photoimageBG = placeImage(config_frame, TEXTURES_DIR+"background2.png", WINDOW_SIZES[self.windowSize][0], WINDOW_SIZES[self.windowSize][1], 0, 0, "nw")

        makeLabel(config_frame, "Offline With Bots", "black", COLOUR_BUTTON, 0.5, 0.1, "center", 20)
        canvas, photoimage = placeImage(config_frame, TEXTURES_DIR+"bot_1.png", WINDOW_SIZES[self.windowSize][0]//7, WINDOW_SIZES[self.windowSize][1]//4, 0.5, 0.15, "n")
        
        makeLabel(config_frame, "Number of Bots:", "black", COLOUR_BUTTON, 0.5, 0.43, "e", 12)
        bots_string = makeStringVar(config_frame, BOT_COUNT[-1])
        bots_option_menu = makeOptionMenu(config_frame, bots_string, BOT_COUNT, 3, COLOUR_BUTTON, COLOUR_TEXT_D, 0.5, 0.43, "w", None)

        makeLabel(config_frame, "Playstyle description:", "black", COLOUR_BUTTON, 0.5, 0.55, "e", 12)
        playstyle_desc = makeLabel(config_frame, "", "black", COLOUR_BUTTON, 0.5, 0.56, "w", 10)
        
        makeLabel(config_frame, "Bot playstyle:", "black", COLOUR_BUTTON, 0.5, 0.48, "e", 12)
        playstyle_string = makeStringVar(config_frame, BOT_PLAYSTYLE[2])
        playstyle_option_menu = makeOptionMenu(config_frame, playstyle_string, BOT_PLAYSTYLE, 6, COLOUR_BUTTON, COLOUR_TEXT_D, 0.5, 0.48, "w", lambda x=None: self.showPlaystyleDesc(playstyle_desc, playstyle_string.get()))
        self.showPlaystyleDesc(playstyle_desc, playstyle_string.get())

        makeLabel(config_frame, "Starting amount of cards:", "black", COLOUR_BUTTON, 0.5, 0.66, "e", 12)
        card_count_string = makeStringVar(config_frame, ROUND_SIZE[-1])
        card_count_option_menu = makeOptionMenu(config_frame, card_count_string, ROUND_SIZE, 3, COLOUR_BUTTON, COLOUR_TEXT_D, 0.5, 0.66, "w", None)

        makeButton(config_frame, "Start", 8, COLOUR_BUTTON, COLOUR_TEXT_D, 0.55, 0.78, "center", lambda: self.startOfflineGame(username, int(bots_string.get()), int(card_count_string.get()), self.user_config.getColourScheme()), 12)
        makeButton(config_frame, "Back", 8, COLOUR_BUTTON, COLOUR_TEXT_D, 0.45, 0.78, "center", lambda: config_frame.destroy(), 12)
        tk.mainloop()


    def showBotIcon(self, config_frame, bot_count):
        self.bot_frame.destroy()
        self.bot_frame = makeFrame(config_frame, COLOUR_PRIME, 0.15, 0.24, 0.5, 0.26, "center")
        canvas, self.bot_Icon = placeImage(self.bot_frame, "res/textures/bot_"+bot_count+".png", WINDOW_SIZES[self.windowSize][0]//7, WINDOW_SIZES[self.windowSize][1]//4, 0.5, 0.5, "center")

    
    @staticmethod
    def showPlaystyleDesc(playstyle_desc, selection):
        playstyle_desc["text"] = PLAYSTYLE_DESC[selection]
        

    def startOfflineGame(self, username, bot_count, start_round_size, col_scheme):
        print("offline with bots")
        offline_frame = makeFrame(self.window, COLOUR_PRIME, 1, 1, 0, 0, "nw")
        loading_frame = makeFrame(self.window, COLOUR_PRIME, 1, 1, 0, 0, "nw")
        canvasBG, photoimageBG = placeImage(loading_frame, TEXTURES_DIR+"background.png", WINDOW_SIZES[self.windowSize][0], WINDOW_SIZES[self.windowSize][1], 0, 0, "nw")
        makeLabel(loading_frame, "Loading...", "black", COLOUR_BUTTON, 0.5, 0.5, "center", 25)
        offline_game = OfflineGame(offline_frame, username, bot_count, col_scheme, start_round_size)
        offline_game.offlineStart()
        loading_frame.destroy()
        offline_game.startGame()


    @staticmethod
    def placeImage(frame, directory, relx, rely, w, h, bg):
        image = Image.open(directory)   
        image = image.resize((w, h))
        img = ImageTk.PhotoImage(image)   
        label = tk.Label(frame, image=img, bg=bg)
        label.config(borderwidth =0, highlightthickness=0)
        label.image = img
        label.place(relx=relx, rely=rely, anchor="center")
        

        
        
if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    contractWhistClient()


