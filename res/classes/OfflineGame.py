import tkinter as tk
import random
import time


from tkinter import Label, Button, PhotoImage, StringVar, Entry, Tk, Frame
from PIL import ImageTk, Image


class OfflineGame:
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

        
        self.deck_order = self._setHandOrder(self.players) #deck_order


        self.base_colour = "PaleGreen1" # debug set to: "medium sea green" 
        self.center_colour = "forest green"
        self.colour_text    = "DarkGreen"
        self.colour_widget  = "DarkSeaGreen2"

        self.suits = ["h", "s", "d", "c"]
        self.suit_names = ["Hearts", "Spades", "Dimonds", "Clubs"]
        self.trump_suit = ""
        self.round_number = 0


        self.options_frame = self._makeOptionsFrame()#._makeFrame(self.parent, 1, 0.05, 0.5, 0, "green", "n")
        self.left_frame = self._makeLeftFrame() #_makeFrame(self.parent, 0.11, 0.6, 0.1, 0.42, "pink", "center")
        self.top_frame = self._makeTopFrame()#_makeFrame(self.parent, 0.48, 0.15, 0.5, 0.21, "blue", "center")
        self.right_frame = self._makeRightFrame()#_makeFrame(self.parent, 0.11, 0.6, 0.9, 0.42, "yellow", "center")
        self.center_frame = self._makeCenterFrame() #_makeFrame(self.parent, 0.6, 0.35, 0.5, 0.49, "orange", "center")
        self.player_hand_frame = self._makePlayerHandFrame()#._makeFrame(self.parent, 0.9, 0.21, 0.5, 0.84, "red", "center")

        self.player_hand_frame.update_idletasks()

        self.frame_dims = self._getFrameDims(self.top_frame, self.left_frame, self.right_frame, self.player_hand_frame)

        self.current_player = 0#random.randint(0, self.players-1)
        self.center_cards = 0
        self.results = []

        self.predictions = [0]*self.players
        self.subRoundsWon = [0]*self.players
        self.scores = [0]*self.players

        self.center_state = []#stores player and their card in center

        self.game_active = True
        self.peek = False
        self.pause_user = False


        self.user_score_label = self._makeLabel(self.parent, "", 0.3, 0.695, "black", self.base_colour, "center")
        self.score_top_label = self._makeLabel(self.parent, "", 0.5, 0.1, "black", self.base_colour, "center")
        self.score_left_label = self._makeLabel(self.parent, "", 0.1, 0.1, "black", self.base_colour, "center")
        self.score_right_label = self._makeLabel(self.parent, "", 0.9, 0.1, "black", self.base_colour, "center")
        
        self.game = tk.Label(self.parent)
        self.game.pack()

        self.Player_turn_label = self._makeLabel(self.parent, "", 0.5, 0.695, "black", self.base_colour, "center")

        peek_button = Button(self.parent, text="Peek", width=8, bg=self.colour_widget, fg=self.colour_text, command= lambda x=None: self._peekOpponents())
        peek_button.place(relx=0.2, rely=0.025, anchor="center")
    
        home_button = Button(self.parent, text="End Game", width=8, bg=self.colour_widget, fg=self.colour_text, command= lambda x=None: parent_frame.destroy())#createHomePage(userConfig))
        home_button.place(relx=0.05, rely=0.025, anchor="center")

        #self._placeNames()
        #self._placePredictionsWon()
        #self._setupRound()
        #self.startGame()

        #TODO -
        #   self.subRoundsWon is being updated after round end so final win carrys over
        #   add prediction input for user and bots
        #   exit game destroys all, user selects and some hand frames come through
        

    def _getFrameDims(self, *args):
        dimentions = []
        for frame in args:
            dimentions.append(frame.winfo_width())
            dimentions.append(frame.winfo_height())
        return dimentions


    def _makeOptionsFrame(self):
        return self._makeFrame(self.parent, 1, 0.05, 0.5, 0, "green", "n")


    def _makeLeftFrame(self):
        return self._makeFrame(self.parent, 0.11, 0.6, 0.1, 0.42, self.base_colour, "center")


    def _makeTopFrame(self):
        return self._makeFrame(self.parent, 0.48, 0.15, 0.5, 0.21, self.base_colour, "center")


    def _makeRightFrame(self):
        return self._makeFrame(self.parent, 0.11, 0.6, 0.9, 0.42, self.base_colour, "center")


    def _makeCenterFrame(self):
        return self._makeFrame(self.parent, 0.6, 0.35, 0.5, 0.49, self.center_colour, "center")


    def _makePlayerHandFrame(self):
        return self._makeFrame(self.parent, 0.9, 0.21, 0.5, 0.84, self.base_colour, "center")


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
            name_top_label = self._makeLabel(self.parent, self.names[1], 0.5, 0.07, "black", self.base_colour, "center")
        elif self.players == 3:
            name_left_label = self._makeLabel(self.parent, self.names[1], 0.1, 0.07, "black", self.base_colour, "center")
            name_right_label = self._makeLabel(self.parent, self.names[2], 0.9, 0.07, "black", self.base_colour, "center")
        elif self.players == 4:
            name_left_label = self._makeLabel(self.parent, self.names[1], 0.1, 0.07, "black", self.base_colour, "center")
            name_top_label = self._makeLabel(self.parent, self.names[2], 0.5, 0.07, "black", self.base_colour, "center")
            name_right_label = self._makeLabel(self.parent, self.names[3], 0.9, 0.07, "black", self.base_colour, "center")


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
        self.pause_user = False
        self._placeCardCenter(0, card)
        #delete card
        del self.hands[0][int(card)]

        self.round_size -= 1

        self.player_hand_frame = self.player_hand_frame.destroy()
        self.player_hand_frame = self._makePlayerHandFrame()#self._makeFrame(self.parent, 0.9, 0.21, 0.5, 0.84, "red", "center")
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
        self.center_frame = self._makeCenterFrame() #self._makeFrame(self.parent, 0.6, 0.35, 0.5, 0.49, "orange", "center")
        self.center_cards = 0

        #self._setupRound()
        #update center info
        self.populateCenter()


    def _showResults(self):

        self.results_frame = self._makeFrame(self.parent, 1, 0.93, 0.5, 0.07, "orange", "n")

      #  self.results = [[0, True, 1, True, 2, False, 3, False],
      #                  [0, True, 1, True, 2, False, 3, False],
      #                  [0, True, 1, True, 2, False, 3, False],
      #                  [0, True, 1, True, 2, False, 3, False],
      #                  [0, True, 1, True, 2, False, 3, False],
      #                  [0, True, 1, True, 2, False, 3, False],
       #                 [0, True, 1, True, 2, False, 3, False],
       #                 [0, True, 1, True, 2, False, 3, False],
       #                 [0, True, 1, True, 2, False, 3, False],
       #                 [100, True, 101, True, 102, False, 103, False]]
        
        self.results_title_label = self._makeLabel(self.parent, "Results", 0.5, 0.15, "white", self.base_colour, "center")

        self.round_title_label = self._makeLabel(self.parent, "Round", 0.08, 0.3, "white", self.base_colour, "center")
    
        
        for col, name in enumerate(self.names):
            self.name_label = self._makeLabel(self.parent, name, 0.25+(0.2*col), 0.3, "white", self.base_colour, "w")
            for r in range(len(self.results)):
                if col == 0:
                    self.round_number_label = self._makeLabel(self.parent, str(r+1), 0.08+(0.2*col), 0.32+((r+1)*0.05), "white", self.base_colour, "center")
                self.score_label = self._makeLabel(self.parent, str(self.results[r][col*2]), 0.24+(0.2*col), 0.32+((r+1)*0.05), "white", self.base_colour, "center")
                self.score_label = self._makeLabel(self.parent, str(self.results[r][col*2+1]), 0.28+(0.2*col), 0.32+((r+1)*0.05), "white", self.base_colour, "center")

        self.winner_label = self._makeLabel(self.parent, "PLAYER won the game!", 0.5, 0.88, "white", self.base_colour, "center")

        close_game_button = Button(self.parent, text="Finish", width=8, command= lambda x=None: closeOfflineGame())
        close_game_button.place(relx=0.5, rely=0.95, anchor="center")

 
    def startGame(self):
       
        #if center is full
        if self.center_cards == self.players:
            
                #pause to show winner for each round

                #self.Player_turn_label['text'] = f'{self.names[self.current_player]} won the round!' #fixxx #move to win round code
                #self.Player_turn_label['fg'] = "yellow"
                
                time.sleep(1)

                #if there are still cards left to be played
                if len(self.hands[0]) != 0:
                    print("next sub round")
                    self._startNextRound()
                    
                else:
                    print("next round")                    
                    
                    #update scores and clear rounds one and TODO redo redictions
                    new_results = []
                    
                    for player in range(self.players):

                        self.scores[player] += self.subRoundsWon[player]

                        new_results.append(self.scores[player])
                        new_results.append(False)
                        
                        self.predictions[player] = 0
                        self.subRoundsWon[player] = 0


                    self.results.append(new_results)
                    print(self.results)

                    self.round_size -= 1

                    self.round_number += 1

                    if self.round_number == self.total_rounds:
                        print("end game 2")
                        self.game_active = False
                        #results page
                        self._showResults()
                            
                    else:
                        self._startNextRound()

                        self.round_size_two -= 1
                        self.round_size = self.round_size_two
                        self._setupRound()

                
        if self.game_active:

            #if players turn
            if (self.current_player == self.players) or (self.current_player == 0):

                #if player not already given choice options
                if not self.pause_user:
                    self.pause_user = True
                    self.current_player = 0

                    self.Player_turn_label["text"] = "Your Turn!"
                    self.Player_turn_label['fg'] = "red"

                    #show player hand
                    self.showPlayerCards()

                    #get valid player options
                    hand = self.hands[0]
                    if self.center_cards != 0:
                        first_card_suit = self.center_state[0][1][-1]
                        hand = self._getValidCards(hand, first_card_suit)
                    valid_indexes = []
                    for card in hand:
                        valid_indexes.append(self.hands[0].index(card))
                
                    #show valid player options
                    self.playerOptions = self._makeFrame(self.parent, 0.9, 0.05, 0.5, 0.95, self.base_colour, "n")
                    for card in range(self.round_size):
                        if card in valid_indexes:
                            test = Button(self.playerOptions, text="Select", width=8, command= lambda x=card: self.playerMadeTurn(str(x)))
                            test.place(relx=0.09*(card+1), rely=0.5, anchor="center")

            #else bots turn
            elif self.current_player != 0:
                self.Player_turn_label['text'] = f'{self.names[self.current_player]}\'s turn!'
                self.Player_turn_label['fg'] = "black"

                #botMakeTurn function?
                
                hand = self.hands[self.current_player]
                #get valid cards from bot hand
                if self.center_cards != 0:
                    first_card_suit = self.center_state[0][1][-1]
                    hand = self._getValidCards(hand, first_card_suit)
                    
                #randomly pick index from valid cards
                card_choice = hand[random.randint(0, len(hand)-1)]
                choice_index = self.hands[self.current_player].index(card_choice)
                
                #place card in center
                self._placeCardCenter(self.current_player, choice_index)

                #delete card from bot hand            
                del self.hands[self.current_player][choice_index]

                #reload bot hand
                self._placeOpponentCards(self.current_player)
                
                self.current_player += 1


            self.game.after(1000, self.startGame)


    @staticmethod
    def _getValidCards(full_hand, first_card_suit):
        valid_hand = []
        
        for card in full_hand:
            if first_card_suit in card:
                valid_hand.append(card)
                
        if len(valid_hand) == 0:
            valid_hand = full_hand

        return valid_hand


    def _placeOpponentCards(self, opponent):
            card = "bk"
            #self.player_hand_frame.winfo_height()
            #TOP
            if ((self.players == 2) & (opponent == 1)) or ((self.players == 4) & (opponent == 2)):
                self.top_frame = self.top_frame.destroy()
                self.top_frame = self._makeTopFrame()#self._makeFrame(self.parent, 0.48, 0.15, 0.5, 0.21, "blue", "center")

                h = self.frame_dims[1]
                for x in range(len(self.hands[opponent])):#TOP
                    if self.peek == True:
                        card = self.hands[opponent][x]
                    image = Image.open("res/images/card_packs/" + self.colour_scheme + "/" + card + ".png")
                    image = image.resize((int(h*0.6887), h))
                    image = ImageTk.PhotoImage(image)
                    image_label = Label(self.top_frame, image=image)
                    image_label.image = image
                    image_label.place(relx=0.09*(x+1), rely=0.5, anchor="center")

            #LEFT
            elif (self.players != 2) & (opponent == 1):
                self.left_frame = self.left_frame.destroy()
                self.left_frame = self._makeLeftFrame() #self._makeFrame(self.parent, 0.11, 0.6, 0.1, 0.42, "pink", "center")

                w = self.frame_dims[2]
                for x in range(len(self.hands[opponent])):#LEFT
                    if self.peek == True:
                        card = self.hands[self.deck_order[0]][x]
                    image = Image.open("res/images/card_packs/" + self.colour_scheme + "/" + card + ".png")
                    image = image.resize((int(w*0.6887), w))
                    image = image.transpose(Image.ROTATE_270) 
                    image = ImageTk.PhotoImage(image)
                    image_label = Label(self.left_frame, image=image)
                    image_label.image = image
                    image_label.place(relx=0.5, rely=0.09*(x+1), anchor="center")

            #RIGHT
            elif ((self.players == 3) & (opponent == 2)) or ((self.players == 4) & (opponent == 3)):
                self.right_frame = self.right_frame.destroy()
                self.right_frame = self._makeRightFrame()#self._makeFrame(self.parent, 0.11, 0.6, 0.9, 0.42, "yellow", "center")

                w = self.frame_dims[4]
                for x in range(len(self.hands[opponent])):#RIGHT
                    if self.peek == True:
                        card = self.hands[self.deck_order[2]][x]
                    image = Image.open("res/images/card_packs/" + self.colour_scheme + "/" + card + ".png")
                    image = image.resize((int(w*0.6887), w))
                    image = image.transpose(Image.ROTATE_90)
                    image = ImageTk.PhotoImage(image)
                    image_label = Label(self.right_frame, image=image)
                    image_label.image = image
                    image_label.place(relx=0.5, rely=1-(0.09*(x+1)), anchor="center")


    def _setTrumpSuit(self):
         self.trump_suit = self.suits[self.round_number%4]

        
    def populateCenter(self):
        #trump suit center info
        self._setTrumpSuit()
        h = self.frame_dims[7]//2
        trump_suit_label = Label(self.center_frame, text="Trump: " + self.suit_names[self.suits.index(self.trump_suit)], bg=self.center_colour, fg="white")
        trump_suit_label.place(relx=0.15, rely=0.12, anchor="center")
        image = Image.open("res/images/icons/" + self.trump_suit + "_icon.png")
        image = image.resize((h, h))
        image = ImageTk.PhotoImage(image)

       # cardImg = PhotoImage(file = "res/images/icons/" + self.trump_suit + "_icon.png")
        image_label = Label(self.center_frame, image=image)
        image_label.image = image
        image_label.place(relx=0.15, rely=0.32, anchor="center")

        scores = ""
        for index, name in enumerate(self.names):
            scores += "\n" + name + ": " + str(self.scores[index])
            
        self.scores_label = self._makeLabel(self.center_frame, "SCORES" + scores, 0.15, 0.75, "white", self.center_colour, "center")

        round_label = Label(self.center_frame, text="Round: " + str(self.round_number+1) + " of " + str(self.total_rounds), bg=self.center_colour, fg="white")
        round_label.place(relx=0.5, rely=0.05, anchor="center")


    @staticmethod
    def _makeFrame(parent, relw, relh, relx, rely, col, anchor):
        frame = Frame(parent, bg=col)
        frame.place(relwidth=relw, relheight=relh, relx=relx, rely=rely, anchor=anchor)
        return frame


    @staticmethod
    def _makeLabel(parent, text, relx, rely, fg_colour, bg_colour, anchor):
        label = Label(parent, text=text, fg=fg_colour, bg=bg_colour)
        label.place(relx=relx, rely=rely, anchor=anchor)
        return label
