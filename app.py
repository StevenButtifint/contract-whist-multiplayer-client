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







if __name__ == "__main__":
    root = Tk()
    window = contractWhistClient(root)
    window.makeHomePage()
    #root.mainloop()

