import tkinter as tk
import random
import threading
import time

from tkinter import Label, Button, PhotoImage, StringVar
from PIL import ImageTk, Image

from APIs.sheets_API import getSheetData, setSheetData

APP_TITLE   = "Contract Whist Client - 1.0"
APP_ICON    = "res/images/icon.ico"

COL_PRIME   = "PaleGreen1"
COL_SECND   = "PaleGreen2"
COL_THIRD   = "PaleGreen4"
COL_TEXT    = "DarkGreen"
COL_WIDGET  = "DarkSeaGreen2"


WINDOW_SIZES    = ["800x600", "900x700", "1200x700", "1600x1100", "2100x1300"]
CARDS_SCALES    = [9, 8, 7, 4, 2]

CARDS_DECK      = ["2c", "2d", "2h", "2s", "3c", "3d", "3h", "3s",
                   "4c", "4d", "4h", "4s", "5c", "5d", "5h", "5s",
                   "6c", "6d", "6h", "6s", "7c", "7d", "7h", "7s",
                   "8c", "8d", "8h", "8s", "9c", "9d", "9h", "9s",
                   "vc", "vd", "vh", "vs", "wjc", "wjd", "wjh", "wjs",
                   "xqc", "xqd", "xqh", "xqs", "ykc", "ykd", "ykh", "yks",
                   "zac", "zad", "zah", "zas"]

CARDS_SCALE = 9


def resize(dimentions):
    global CARDS_SCALE
    CARDS_SCALE = CARDS_SCALES[WINDOW_SIZES.index(dimentions)]
    dimentions = str(dimentions).split("x")
    w, h = int(dimentions[0]), int(dimentions[1])
    root.geometry(f"{w}x{h}")


def updateLayout(dimentions, build_frame):
    resize(dimentions)
    build_frame()
    

def showColourScheme(frame, colour_string):
    colour_scheme = colour_string.get()
    placeImage(frame, "res/images/card_packs/" + colour_scheme + "/zas.png", 0.8, 0.5)
    placeImage(frame, "res/images/card_packs/" + colour_scheme + "/bk.png", 0.2, 0.5)
    colour_string.set("Colour Scheme: " + str(colour_scheme))


def placeImage(frame, directory, relx, rely):
    image = Image.open(directory)   
    image = image.resize((500//3, 726//3))
    img = ImageTk.PhotoImage(image)
    label = Label(frame, image=img)
    label.image = img
    label.place(relx=relx, rely=rely, anchor="center")      





def offlineConfigFrame(username, col_scheme):
    global config_frame
    try:
        config_frame.destroy()
    except:
        pass

    #offline game setup
    BOT_COUNT       = ["1", "2", "3"]
    BOTS    = 3
    start_round_size = [1,2,3,4,5,6,7,8,9,10]
    round_size = 10
    
    config_frame = tk.Frame(root, bg=COL_PRIME).place(relwidth=1, relheight=1, relx=0, rely=0)

    bots_label = Label(home_frame, text="Number of Bots:", bg=COL_PRIME, fg=COL_TEXT)
    bots_label.place(relx=0.5, rely=0.42, anchor="e")#x=WINDOW_W//2-40, y=WINDOW_H*0.4, anchor="center")
    bots_string = tk.StringVar(config_frame)
    bots_string.set(BOTS)
    #######change to horizontal slider?? as seperate function
    bots_option_menu = tk.OptionMenu(home_frame, bots_string, *BOT_COUNT)#, command= lambda x=None: setBotCount(bots_string.get()))
    bots_option_menu.config(width=6, bg=COL_WIDGET, fg=COL_TEXT)
    bots_option_menu["menu"].config(bg=COL_WIDGET, fg=COL_TEXT)
    bots_option_menu.place(relx=0.5, rely=0.42, anchor="w")#x=WINDOW_W//2+40, y=WINDOW_H*0.4, anchor="center")

    #slider = tk.Scale(home_frame, from_=0, to=10, orient='horizontal')
    #slider.place(relx=0.2, rely=0.2)

    card_count_label = Label(home_frame, text="Starting amount of cards:", bg=COL_PRIME, fg=COL_TEXT)
    card_count_label.place(relx=0.5, rely=0.48, anchor="e")
    card_count_string = tk.StringVar(config_frame)
    card_count_string.set(round_size)
    card_count_option_menu = tk.OptionMenu(home_frame, card_count_string, *start_round_size)#, command= lambda x=None: setRoundSize(card_count_string.get()))
    card_count_option_menu.config(width=6, bg=COL_WIDGET, fg=COL_TEXT)
    card_count_option_menu["menu"].config(bg=COL_WIDGET, fg=COL_TEXT)
    card_count_option_menu.place(relx=0.5, rely=0.48, anchor="w")

    start_button = Button(home_frame, text="Start", width=8, bg=COL_WIDGET, fg=COL_TEXT, command= lambda x=None: offlinePlay(username, int(bots_string.get()), int(card_count_string.get()), col_scheme))
    start_button.place(relx=0.5, rely=0.7, anchor="center")
    
    home_button = Button(home_frame, text="Back", width=8, bg=COL_WIDGET, fg=COL_TEXT, command= lambda x=None: createHomePage())
    home_button.place(relx=0.02, rely=0.02, anchor="nw")


def offlinePlay(username, bot_count, start_round_size, col_scheme):
    print("offline with bots")

    #frame for all to go in instead of root to destroy if back to main menu or game over
    offline_frame = tk.Frame(root, bg=COL_PRIME).place(relwidth=1, relheight=1, relx=0, rely=0)

    bot_names = ["Leon", "Napoleon", "Jesse", "Mr. Blonde", "Falcon", "Vulture", "Banshee", "Nova",
                 "Voyager", "Zoe", "Arya", "Lab Rat", "Katie"]

    if len(username) > 15:
        username = username[0:15]

    player_names = [username]

    #pick random names for bots
    for bot in range(bot_count):
        pick = random.randint(0, len(bot_names)-1)
        player_names.append(bot_names[pick])
        del bot_names[pick]

    ##################################################################################################################
    offlineGame(offline_frame, player_names, col_scheme, start_round_size, CARDS_DECK)



class offlineGame:
    def __init__(self, parent_frame, names, colour_scheme, round_size, cards_deck):# +difficulty/bot playstyles, bot amount, colour scheme all in game config class object?
        
        self.parent = parent_frame
        self.names = names
        self.colour_scheme = colour_scheme
        self.round_size = round_size # start_round_size
        self.cards_deck = cards_deck
        
        
        self.players = len(names)
        
        self.hands = [[]] * self.players#store all lists of players cards


        self.round_size_two = round_size#to organise
        self.total_rounds = round_size

        
        self.deck_order = self._setHandOrder() #deck_order

        

        self.suits = ["h", "s", "d", "c"]
        self.suit_names = ["Hearts", "Spades", "Dimonds", "Clubs"]
        self.trump_suit = ""
        self.round_number = 0


        self.options_frame = self._makeFrame(self.parent, 1, 0.05, 0.5, 0, "green", "n")
        self.left_frame = self._makeFrame(self.parent, 0.11, 0.6, 0.1, 0.42, "pink", "center")
        self.top_frame = self._makeFrame(self.parent, 0.48, 0.15, 0.5, 0.21, "blue", "center")
        self.right_frame = self._makeFrame(self.parent, 0.11, 0.6, 0.9, 0.42, "yellow", "center")
        self.center_frame = self._makeFrame(self.parent, 0.6, 0.35, 0.5, 0.49, "orange", "center")
        self.player_hand_frame = self._makeFrame(self.parent, 0.9, 0.21, 0.5, 0.84, "red", "center")

        self.player_hand_frame.update_idletasks()

        self.frame_dims = self._getFrameDims(self.top_frame, self.left_frame, self.right_frame,
                                             self.player_hand_frame)

        self.current_player = 2#random.randint(0, self.players-1)
        self.center_cards = 0
        self.results = []

        self.predictions = [0]*self.players
        self.subRoundsWon = [0]*self.players
        self.scores = [0]*self.players

        self.center_state = []#stores player and their card in center

        self.game_active = True
        self.peek = False

        self.user_score_label = self._makeLabel(self.parent, "", 0.3, 0.695, "center")
        self.score_top_label = self._makeLabel(self.parent, "", 0.5, 0.1, "center")
        self.score_left_label = self._makeLabel(self.parent, "", 0.1, 0.1, "center")
        self.score_right_label = self._makeLabel(self.parent, "", 0.9, 0.1, "center")


        
        self.game = tk.Label(self.parent)
        self.game.pack()


        self.Player_turn_label = self._makeLabel(self.parent, "", 0.5, 0.695, "center")

        peek_button = Button(self.parent, text="Peek", width=8, bg=COL_WIDGET, fg=COL_TEXT, command= lambda x=None: self._peekOpponents())
        peek_button.place(relx=0.2, rely=0.025, anchor="center")
    
        home_button = Button(self.parent, text="Exit Game", width=8, bg=COL_WIDGET, fg=COL_TEXT, command= lambda x=None: createHomePage())
        home_button.place(relx=0.05, rely=0.025, anchor="center")

        #self._placeNames()
        #self._placePredictionsWon()
        #self._setupRound()
        #self.startGame()

        #TODO -
        #   self.subRoundsWon is being updated after round end so final win carry over sometimes?
        #   add prediction input for user and bots
        #   exit game destroys all, user selects and some hand frames come through
        #   peek is broken


    def _getFrameDims(self, *args):
        dimentions = []
        for frame in args:
            dimentions.append(frame.winfo_width())
            dimentions.append(frame.winfo_height())
        return dimentions
        

    def offlineStart(self):
        self._placeNames()
        self._placePredictionsWon()
        self._setupRound()
        self.startGame()


    @staticmethod
    def _setHandOrder(player_count):
        deck_order = [1, 1, 2]  #left, top, right
        if player_count == 4:
            deck_order[1] = 2
            deck_order[2] = 3
        return deck_order


    def _placeNames(self):#place names and predicted/achieved
        if self.players == 2:
            name_top_label = self._makeLabel(self.parent, self.names[1], 0.5, 0.07, "center")
        elif self.players == 3:
            name_left_label = self._makeLabel(self.parent, self.names[1], 0.1, 0.07, "center")
            name_right_label = self._makeLabel(self.parent, self.names[2], 0.9, 0.07, "center")
        elif self.players == 4:
            name_left_label = self._makeLabel(self.parent, self.names[1], 0.1, 0.07, "center")
            name_top_label = self._makeLabel(self.parent, self.names[2], 0.5, 0.07, "center")
            name_right_label = self._makeLabel(self.parent, self.names[3], 0.9, 0.07, "center")


    def _placePredictionsWon(self):
        self.user_score_label["text"] = "Predicted: " + str(self.predictions[0]) + ", Won: " + str(self.subRoundsWon[0])
        if self.players == 2:
            self.score_top_label["text"] = "Predicted: " + str(self.predictions[1]) + ", Won: " + str(self.subRoundsWon[1])
        elif self.players == 3:
            self.score_left_label["text"] = "Predicted: " + str(self.predictions[1]) + ", Won: " + str(self.subRoundsWon[1])
            self.score_right_label["text"] = "Predicted: " + str(self.predictions[2]) + ", Won: " + str(self.subRoundsWon[2])
        elif self.players == 4:
            self.score_left_label["text"] = "Predicted: " + str(self.predictions[1]) + ", Won: " + str(self.subRoundsWon[1])
            self.score_top_label["text"] = "Predicted: " + str(self.predictions[2]) + ", Won: " + str(self.subRoundsWon[2])
            self.score_right_label["text"] = "Predicted: " + str(self.predictions[3]) + ", Won: " + str(self.subRoundsWon[3])


    def _peekOpponents(self):
        self.peek = not self.peek
        self._placeAllHands()


    def _setupRound(self):
        self._shuffleDeck()
        for x in range(self.players):
            self.hands[x] = self.cards_deck[x*self.round_size_two:x*self.round_size_two+self.round_size_two]
        self._setTrumpSuit()
        self._orderHands()
        self.showPlayerCards()
        self.populateCenter()
        #place all opponent cards
        self._placeAllHands()


    def _shuffleDeck(self):
        random.shuffle(self.cards_deck)
def createHomePage():


    def _orderHands(self):
        for index, hand in enumerate(self.hands):
            h, s, d, c = [], [], [], []
            for card in hand:
                if "h" in card:
                    h.append(card)
                elif "s" in card:
                    s.append(card)
                elif "d" in card:
                    d.append(card)
                elif "c" in card:
                    c.append(card)

            h = sorted(h)
            s = sorted(s)
            d = sorted(d)
            c = sorted(c)
            ordered_hand = []
            
            if self.trump_suit == "h":
                ordered_hand = s + d + c + h
            if self.trump_suit == "s":
                ordered_hand = d + c + h + s
            if self.trump_suit == "d":
                ordered_hand = c + h + s + d
            if self.trump_suit == "c":
                ordered_hand = h + s + d + c
            
            for card in range(len(hand)):
                self.hands[index][card] = ordered_hand[card]


    def playerMadeTurn(self, card):
        self.playerOptions = self.playerOptions.destroy()
        self.current_player = 1

        self._placeCardCenter(0, card)
        #delete card
        del self.hands[0][int(card)]

        self.round_size -= 1

        self.player_hand_frame = self.player_hand_frame.destroy()
        self.player_hand_frame = self._makeFrame(self.parent, 0.9, 0.21, 0.5, 0.84, "red", "center")
        self.showPlayerCards()


    def showPlayerCards(self):
        for x in range(len(self.hands[0])):
            img_loc = "res/images/card_packs/" + self.colour_scheme + "/" + self.hands[0][x] + ".png"
            h = self.frame_dims[7]
            w = int(0.6887*h)
            relx = 0.09*(x+1)
            self._placeImage(self.player_hand_frame, img_loc, w, h, relx, 0, "n")
            

    @staticmethod
    def _placeImage(frame, img_location, width, height, relx, rely, anchor):
            image = Image.open(img_location)
            image = image.resize((width, height))
            image = ImageTk.PhotoImage(image)
            image_label = Label(frame, image=image)
            image_label.image = image
            image_label.place(relx=relx, rely=rely, anchor=anchor)


    def _placeCardCenter(self, player, card_index):
        self.center_state.append([player, self.hands[player][int(card_index)]])
        img_loc = "res/images/card_packs/" + self.colour_scheme + "/" + self.hands[player][int(card_index)] + ".png"
        h = self.frame_dims[7]
        w = int(h/1.452)
        relx = 0.4+(self.center_cards*0.14)
        self._placeImage(self.center_frame, img_loc, w, h, relx, 0.5, "center")
            
        self.center_cards += 1


    def _placeAllHands(self):
        for p in range(1, self.players):
            self._placeOpponentCards(p)


    def _calculateRoundWinner(self):
        card_order = ["2", "3", "4", "5", "6", "7", "8", "9", "v", "w", "x", "y", "z"]
        card_values = []
        round_suit = self.center_state[0][1][-1]

        #calculate card values
        for pair in self.center_state:
            card = pair[1]
            value = 0
            if self.trump_suit in card:
                value += 13
            if round_suit in card:
                value += card_order.index(card[0])
            card_values.append(value)

        #calc winning player index
        winner = self.center_state[card_values.index(max(card_values))][0]
        return winner
      

    def _startNextRound(self):
        #calc winner for round

        winner_index = self._calculateRoundWinner()
        self.subRoundsWon[winner_index] += 1
        print(self.subRoundsWon)

        self.current_player = winner_index

        self._placePredictionsWon()

        #clear center
        self.center_state = []
        self.center_frame = self.center_frame.destroy()
        self.center_frame = self._makeFrame(self.parent, 0.6, 0.35, 0.5, 0.49, "orange", "center")
        self.center_cards = 0

        #self._setupRound()
        #update center info
        self.populateCenter()


            

    @staticmethod
    def _getValidCards(full_hand, first_card_suit):
        valid_hand = []
        
        for card in full_hand:
            if first_card_suit in card:
                valid_hand.append(card)
                
        if len(valid_hand) == 0:
            valid_hand = full_hand

        return valid_hand




    def _setTrumpSuit(self):
         self.trump_suit = self.suits[self.round_number%4]
    @staticmethod
    def _makeFrame(parent, relw, relh, relx, rely, col, anchor):
        frame = tk.Frame(parent, bg=col)
        frame.place(relwidth=relw, relheight=relh, relx=relx, rely=rely, anchor=anchor)
        return frame


    @staticmethod
    def _makeLabel(parent, text, relx, rely, anchor):
        label = Label(parent, text=text)
        label.place(relx=relx, rely=rely, anchor=anchor)
        return label


    global home_frame
    try:
        home_frame.destroy()
        lobby_frame.destroy()
    except:
        pass
    home_frame = tk.Frame(root, bg=COL_PRIME).place(relwidth=1, relheight=1, relx=0, rely=0)
    
    image = Image.open("res/images/card_packs/" + COL_SCHEME + "/as.png")
    image = image.resize((500//3, 726//3))
    img = ImageTk.PhotoImage(image)
    label1 = Label(image=img)
    label1.image = img
    label1.place(x=(WINDOW_W//4)*3, y=WINDOW_H//2, anchor="center")

    imaget = Image.open("res/images/card_packs/" + COL_SCHEME + "/bk.png")
    imaget = imaget.resize((500//3, 726//3))
    imgt = ImageTk.PhotoImage(imaget)
    label1t = Label(image=imgt)
    label1t.image = imgt
    label1t.place(x=(WINDOW_W//4)*1, y=WINDOW_H//2, anchor="center")
    
    username_label = Label(home_frame, text="Username:", bg=COL_PRIME, fg=COL_TEXT)
    username_label.place(x=WINDOW_W//2-60, y=WINDOW_H*0.4, anchor="center")

    username_entry = tk.Entry(home_frame, width=18, bg=COL_WIDGET, fg=COL_TEXT)
    username_entry.place(x=WINDOW_W//2+40, y=WINDOW_H*0.4, anchor="center")
    username_entry.insert(0, USERNAME)

    identifier_label = Label(home_frame, text="Identifier:", bg=COL_PRIME, fg=COL_TEXT)
    identifier_label.place(x=WINDOW_W//2-60, y=WINDOW_H*0.4+30, anchor="center")
    identifier_entry = tk.Entry(home_frame, width=18, bg=COL_WIDGET, fg=COL_TEXT)
    identifier_entry.place(x=WINDOW_W//2+40, y=WINDOW_H*0.4+30, anchor="center")
    identifier_entry.insert(0, IDENTIFIER)

    colour_string = tk.StringVar(home_frame)
    colour_string.set("Colour Scheme: " + str(COL_SCHEME))
    colour_option_menu = tk.OptionMenu(home_frame, colour_string, *COL_SCHEMES, command= lambda x=None: setColourScheme(home_frame, colour_string))
    colour_option_menu.config(width=21, bg=COL_WIDGET, fg=COL_TEXT)
    colour_option_menu["menu"].config(bg=COL_WIDGET, fg=COL_TEXT)
    colour_option_menu.place(x=WINDOW_W//2, y=WINDOW_H*0.4+70, anchor="center")

    resize_string = tk.StringVar(home_frame)
    resize_string.set("Resolution: " + str(WINDOW_W) + "x" + str(WINDOW_H))
    resize_option_menu = tk.OptionMenu(home_frame, resize_string, *WINDOW_SIZES, command= lambda x=None: updateLayout(resize_string.get(), createHomePage, username_entry.get(), identifier_entry.get()))
    resize_option_menu.config(width=21, bg=COL_WIDGET, fg=COL_TEXT)
    resize_option_menu["menu"].config(bg=COL_WIDGET, fg=COL_TEXT)
    resize_option_menu.place(x=WINDOW_W//2, y=WINDOW_H*0.4+110, anchor="center")

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
