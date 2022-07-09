#INTERFACE CONSTANTS
WINDOW_SIZES = {"900x506" : [900, 506],
                "1000x562" : [1000, 562],
                "1200x700":[1200, 675],
                "1400x787":[1400, 787],
                "1900x1125":[1900, 1069]}


#DIRECTORIES
CARD_PACKS_DIR = "res/card_packs/"
TEXTURES_DIR = "res/textures/"
CHAR_ICONS_DIR = "res/characters/"


#COLOURS
COLOUR_TEXT = "black"
COLOUR_WIDGET = "DarkSeaGreen2"
COLOUR_PRIME = "black"
COLOUR_SECOND = "red"
COLOUR_TEXT_L = "white"
COLOUR_TEXT_D = "Black"
COLOUR_WIDGET_D = "#494080"
COLOUR_WIDGET_L = "#958aff"
COLOUR_CENTER = "#494080"
COLOUR_ERROR = "red"
COLOUR_BUTTON = "#958aff"


#OFFLINE CONSTANTS
CARDS_DECK = ["2c", "2d", "2h", "2s", "3c", "3d", "3h", "3s", "4c", "4d", "4h", "4s",
              "5c", "5d", "5h", "5s", "6c", "6d", "6h", "6s", "7c", "7d", "7h", "7s",
              "8c", "8d", "8h", "8s", "9c", "9d", "9h", "9s", "vc", "vd", "vh", "vs",
              "wjc", "wjd", "wjh", "wjs", "xqc", "xqd", "xqh", "xqs", "ykc", "ykd",
              "ykh", "yks", "zac", "zad", "zah", "zas"]

BOT_NAMES = ["Leon", "Napoleon", "Jesse", "Dodo", "Brim", "Banshee",
             "Nova", "Voyager", "Zoe", "Arya", "Lab Rat"]

PLAYSTYLE_DESC = {"Potoo" : "Plays the game legitimately\n but doesnt know how to play.",
                  "Falcon" : "Plays aggressively to win as\n many rounds as it can regardless of predicts.",
                  "Raven" : "Plays tactically based on past\n events and its current situation.",
                  "Random" : "Random playstyle will be selected."}

CARD_ORDER = ["2", "3", "4", "5", "6", "7", "8", "9", "v", "w", "x", "y", "z"]
BOT_PLAYSTYLE = ["Potoo", "Falcon", "Raven", "Random"]
SUIT_LETTERS = ["h", "s", "d", "c"]
SUIT_NAMES = ["Hearts", "Spades", "Dimonds", "Clubs"]
BOT_COUNT = [1, 2, 3]
ROUND_SIZE = [1,2,3,4,5,6,7,8,9,10]


#ERROR CODES
L01 = "Lobby code is invalid."
L02 = "Lobby is full."
C00 = "Connection successful."
C01 = "Cannot find credentials."
C02 = "Invalid credentials."


#MULTIPLAYER CONSTANTS
SERVICE_ACCOUNT_FILE = 'keys/default_key.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
