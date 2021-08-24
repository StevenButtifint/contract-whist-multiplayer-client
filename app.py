import tkinter as tk
from tkinter import Label, Button
from PIL import ImageTk, Image

from APIs.sheets_API import getSheetData, setSheetData

APP_TITLE   = "Contract Whist Client - 1.0"
APP_ICON    = "res/images/icon.ico"

COL_PRIME   = "PaleGreen1"
COL_SECND   = "PaleGreen2"
COL_THIRD   = "PaleGreen4"
COL_TEXT    = "DarkGreen"

COL_WIDGET  = "DarkSeaGreen2"


WINDOW_SIZES = ["800x600", "900x700", "1200x700", "1600x1100", "2100x1300"]
COL_SCHEMES = ["Default", "test"]
WINDOW_SIZES    = ["800x600", "900x700", "1200x700", "1600x1100", "2100x1300"]
COL_SCHEMES     = ["Default", "test"]

CARDS_DECK      = ["2c", "2d", "2h", "2s", "3c", "3d", "3h", "3s",
                   "4c", "4d", "4h", "4s", "5c", "5d", "5h", "5s",
                   "6c", "6d", "6h", "6s", "7c", "7d", "7h", "7s",
                   "8c", "8d", "8h", "8s", "9c", "9d", "9h", "9s",
                   "vc", "vd", "vh", "vs", "wjc", "wjd", "wjh", "wjs",
                   "xqc", "xqd", "xqh", "xqs", "ykc", "ykd", "ykh", "yks",
                   "zac", "zad", "zah", "zas"]
SUITS       = ["h", "s", "d", "c"]
SUIT_NAMES  = ["Hearts", "Spades", "Dimonds", "Clubs"]

USERNAME    = ""
IDENTIFIER  = ""
COL_SCHEME  = "default"

WINDOW_W = 900
WINDOW_H = 600
WINDOW_W    = 900
WINDOW_H    = 600


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
    

def setColourScheme(frame, colour_string):
    global COL_SCHEME
    COL_SCHEME = colour_string.get()
    print(COL_SCHEME)
    colour_string.set("Colour Scheme: " + str(COL_SCHEME))
    
    image = Image.open("res/images/card_packs/" + COL_SCHEME + "/as.png")
    image = image.resize((500//3, 726//3))
    img = ImageTk.PhotoImage(image)
    label1 = Label(frame, image=img)
    label1.image = img
    label1.place(x=(WINDOW_W//4)*3, y=WINDOW_H//2, anchor="center")

    imaget = Image.open("res/images/card_packs/" + COL_SCHEME + "/bk.png")
    imaget = imaget.resize((500//3, 726//3))
    imgt = ImageTk.PhotoImage(imaget)
    label1t = Label(image=imgt)
    label1t.image = imgt
    label1t.place(x=(WINDOW_W//4)*1, y=WINDOW_H//2, anchor="center")
def setUsername(userName):
    global USERNAME
    USERNAME = userName
def setBotCount(botCount):
    global BOTS
    BOTS = int(botCount)
def setRoundSize(roundSize):
    global ROUND_SIZE
    ROUND_SIZE = int(roundSize)
def peek(left_frame, top_frame, right_frame, deck_order):
    global PEEK
    left_frame.destroy()
    top_frame.destroy()
    right_frame.destroy()
    PEEK = not PEEK
    placeOpponentCards(deck_order)
def shuffle(array):
    random.shuffle(array)
def orderHands(allHands):
    
    for index, hand in enumerate(allHands):
        
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
        
        if TRUMP_SUIT == "h":
            ordered_hand = s + d + c + h
        if TRUMP_SUIT == "s":
            ordered_hand = d + c + h + s
        if TRUMP_SUIT == "d":
            ordered_hand = c + h + s + d
        if TRUMP_SUIT == "c":
            ordered_hand = h + s + d + c
        
        for card in range(len(hand)):
            allHands[index][card] = ordered_hand[card]
def offlinePlay():
    print("offline with bots")
    global bot_left_frame, bot_top_frame, bot_right_frame, ALL_HANDS, ROUND_NUMBER, OFFLINE_GAME, player_select_frame, ROUND_SIZE
    
    #frame for all to go in instead of root to destroy if back to main menu or game over
    offline_frame = tk.Frame(root, bg=COL_PRIME).place(relwidth=1, relheight=1, relx=0, rely=0)

    #Player_hand_frame = tk.Frame(root, bg="red").place(relwidth=0.9, relheight=0.3, relx=0.5, rely=0.85, anchor="center")

    #player_select_frame = tk.Frame(root, bg="purple")
    #player_select_frame.place(relwidth=0.95, relheight=0.06, relx=0.5, rely=0.92, anchor="n")


    options_frame = tk.Frame(root, bg="green")
    options_frame.place(relwidth=1, relheight=0.07, relx=0.5, rely=0, anchor="n")

    
   # bot_left_frame = tk.Frame(root, bg="red")
   # bot_left_frame.place(relwidth=0.15, relheight=0.6, relx=0.1, rely=0.38, anchor="center")
    
  #  bot_top_frame = tk.Frame(root, bg="blue")
  #  bot_top_frame.place(relwidth=0.48, relheight=0.18, relx=0.5, rely=0.18, anchor="center")
    
  #  bot_right_frame = tk.Frame(root, bg="yellow")
  #  bot_right_frame.place(relwidth=0.15, relheight=0.6, relx=0.9, rely=0.38, anchor="center")
    
    #center_frame = tk.Frame(root, bg="orange")
    #center_frame.place(relwidth=0.5, relheight=0.35, relx=0.5, rely=0.47, anchor="center")

    OFFLINE_GAME = True
    #threading.Thread(target=checkPlayersGo).start()
    #threading.Thread(target=setCurrentPlayer).start()
    
    #randonly shuffle deck and pick out cards for player and each bot



    #ALL_HANDS = []
    #shuffle(CARDS_DECK)

    #for x in range(BOTS+1):
    #    ALL_HANDS.append(CARDS_DECK[x*ROUND_SIZE:x*ROUND_SIZE+ROUND_SIZE])

    #orderHands(ALL_HANDS)

    

    deck_order = [1, 1, 2]  #left, top, right
    
    if BOTS == 3:
        deck_order[1] = 2
        deck_order[2] = 3
        
    #placeOpponentCards(deck_order)

    USERNAME = "temp user"
    player_names = [USERNAME, "bot1", "bot2", "bot3"]
    print("here class start")##################################################################################################################


    offlineGame(offline_frame, player_names, COL_SCHEME, ROUND_SIZE, deck_order, CARDS_DECK)

    #ChangeText(offline_frame, WINDOW_W, WINDOW_H, BOTS, ALL_HANDS, ROUND_SIZE, player_names, bot_left_frame, bot_top_frame, bot_right_frame, deck_order)


    #show player cards
  #  for x in range(ROUND_SIZE):
  #      image = Image.open("res/images/card_packs/" + COL_SCHEME + "/" + ALL_HANDS[0][x] + ".png")
  #      image = image.resize((500//(CARDS_SCALE-3), 726//(CARDS_SCALE-3)))
   #     image = ImageTk.PhotoImage(image)
   #     image_label = Label(Player_hand_frame, image=image)
   #     image_label.image = image
   #     image_label.place(x=(int(WINDOW_W*0.09)*(x+1)), y=int(WINDOW_H*0.8), anchor="center")
        
        #test = Button(player_select_frame, text="Select", width=8, command= lambda x=x: testingTwo(str(x)))
        #test.place(x=int(WINDOW_W*0.09)*(x+1), y=WINDOW_H*0.95, anchor="center")


  #  #trump suit center info
  #  trump_suit_label = Label(center_frame, text="Trump: " + SUIT_NAMES[SUITS.index(TRUMP_SUIT)], bg=COL_PRIME, fg=COL_TEXT)
  #  trump_suit_label.place(relx=0.1, rely=0.05, anchor="center")
  #  image = Image.open("res/images/icons/" + TRUMP_SUIT + "_icon.png")
  #  image = image.resize((400//(CARDS_SCALE), 400//(CARDS_SCALE)))
  #  image = ImageTk.PhotoImage(image)
  #  image_label = Label(center_frame, image=image)
  #  image_label.image = image
  #  image_label.place(relx=0.1, rely=0.22, anchor="center")


    peek_button = Button(options_frame, text="Peek", width=8, bg=COL_WIDGET, fg=COL_TEXT, command= lambda x=None: peek(bot_left_frame, bot_top_frame, bot_right_frame, deck_order))
    peek_button.place(relx=0.2, rely=0.5, anchor="center")
    
    home_button = Button(options_frame, text="Exit Game", width=8, bg=COL_WIDGET, fg=COL_TEXT, command= lambda x=None: createHomePage())
    home_button.place(relx=0.05, rely=0.5, anchor="center")
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
        self.left_frame = self._makeFrame(self.parent, 0.15, 0.6, 0.1, 0.42, "pink", "center")
        self.top_frame = self._makeFrame(self.parent, 0.48, 0.16, 0.5, 0.21, "blue", "center")
        self.right_frame = self._makeFrame(self.parent, 0.15, 0.6, 0.9, 0.42, "yellow", "center")
        self.center_frame = self._makeFrame(self.parent, 0.6, 0.35, 0.5, 0.49, "orange", "center")
        self.player_hand_frame = self._makeFrame(self.parent, 0.9, 0.25, 0.5, 0.85, "red", "center")


        self.current_player = 2#random.randint(0, self.players-1)
        self.center_cards = 0
        self.results = []

        self.predictions = [0]*self.players
        self.subRoundsWon = [0]*self.players

        self.center_state = []#stores player and their card in center

        self.game_active = True
        self.peek = False
        
        self.game = tk.Label(self.parent)
        self.game.pack()


        self.Player_turn_label = self._makeLabel(self.parent, "", 0.5, 0.695, "center")

        peek_button = Button(self.parent, text="Peek", width=8, bg=COL_WIDGET, fg=COL_TEXT, command= lambda x=None: self._peekOpponents())
        peek_button.place(relx=0.2, rely=0.025, anchor="center")
    
        home_button = Button(self.parent, text="Exit Game", width=8, bg=COL_WIDGET, fg=COL_TEXT, command= lambda x=None: createHomePage())
        home_button.place(relx=0.05, rely=0.025, anchor="center")

        self._placeNames()
        self._placePredictionsWon()
        self._setupRound()
        self.startGame()

        #TODO -
        #   self.subRoundsWon is being updated after round end so final win carry over sometimes?
        #   add prediction input for user and bots
        #   exit game destroys all, user selects and some hand frames come through

        
    def _setHandOrder(self):
        self.deck_order = [1, 1, 2]  #left, top, right
    
        if BOTS == 3:
            self.deck_order[1] = 2
            self.deck_order[2] = 3


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
        try:#improve so dont distroy and remake, change ["text"] param like self.Player_turn_label
            self.user_score_label = self.user_score_label.destroy()
            self.score_top_label = self.score_top_label.destroy()
        except:
            try:
                self.score_left_label = self.score_left_label.destroy()
                self.score_right_label = self.score_right_label.destroy()
            except:
                try:
                    self.score_left_label = self.score_left_label.destroy()
                    self.score_top_label = self.score_top_label.destroy()
                    self.score_right_label = self.score_right_label.destroy()
                except:
                    print("passed preds")


        self.user_score_label = self._makeLabel(self.parent, "Predicted: " + str(self.predictions[0]) + ", Won: " + str(self.subRoundsWon[0]), 0.3, 0.695, "center")

        
        if self.players == 2:
            self.score_top_label = self._makeLabel(self.parent, "Predicted: " + str(self.predictions[1]) + ", Won: " + str(self.subRoundsWon[1]), 0.5, 0.1, "center")

        elif self.players == 3:
            self.score_left_label = self._makeLabel(self.parent, "Predicted: " + str(self.predictions[1]) + ", Won: " + str(self.subRoundsWon[1]), 0.1, 0.1, "center")
            self.score_right_label = self._makeLabel(self.parent, "Predicted: " + str(self.predictions[2]) + ", Won: " + str(self.subRoundsWon[2]), 0.9, 0.1, "center")

        elif self.players == 4:
            self.score_left_label = self._makeLabel(self.parent, "Predicted: " + str(self.predictions[1]) + ", Won: " + str(self.subRoundsWon[1]), 0.1, 0.1, "center")
            self.score_top_label = self._makeLabel(self.parent, "Predicted: " + str(self.predictions[2]) + ", Won: " + str(self.subRoundsWon[2]), 0.5, 0.1, "center")
            self.score_right_label = self._makeLabel(self.parent, "Predicted: " + str(self.predictions[3]) + ", Won: " + str(self.subRoundsWon[3]), 0.9, 0.1, "center")


        #place all opponent cards
        #self._placeAllHands()

        self._setupRound()
        self.startGame()
    def _shuffleDeck(self):
        random.shuffle(self.cards_deck)
def createHomePage():
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
