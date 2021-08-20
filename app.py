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
def peek(left_frame, top_frame, right_frame, deck_order):
    global PEEK
    left_frame.destroy()
    top_frame.destroy()
    right_frame.destroy()
    PEEK = not PEEK
    placeOpponentCards(deck_order)
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
