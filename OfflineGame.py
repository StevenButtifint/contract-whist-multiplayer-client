import tkinter as tk
import random
import time
from constants import *
from interface import *

from tkinter import Label, Button, PhotoImage, StringVar, Entry, Tk, Frame
from PIL import ImageTk, Image


class OfflineGame:
    def __init__(self, parent_frame, player_name, bot_count, colour_scheme, round_size):
        self.parent = parent_frame
        self.names = [player_name]
        self.names.extend(self._setBotNames(bot_count))
        self.colour_scheme = colour_scheme
        self.round_size = round_size # start_round_size
        
        self.cards_deck = CARDS_DECK
        self.player_count = len(self.names)
        self.hands = [[]] * self.player_count#store all lists of players cards
        self.round_size_two = round_size#to organise
        self.total_rounds = round_size
        self.deck_order = self._setHandOrder(self.player_count) #deck_order
        self.trump_suit = ""
        self.round_number = 0
        
        self._makeTopOptions()
        self._placeAreaFrames()
        self._placeAreaLabels()

        self.current_player = 0
        self.center_cards = 0
        self.results = []
        self.predictions = [0]*self.player_count
        self.subRoundsWon = [0]*self.player_count
        self.scores = [0]*self.player_count
        self.center_state = []#stores player and their card in center
        self.game_active = True
        self.peek = False
        self.pause_user = False

        self.frame_dims = self._getFrameDims(self.top_frame, self.left_frame, self.right_frame, self.player_hand_frame)
        self.game = makeLabel(self.parent, "", COLOUR_WIDGET_D, COLOUR_WIDGET_D, 0.5, 0, "center", 5)
        


    def _placeAreaFrames(self):
        self.left_frame = self._makeLeftFrame()
        self.top_frame = self._makeTopFrame()
        self.right_frame = self._makeRightFrame()
        self.center_frame = self._makeCenterFrame()
        self.player_hand_frame = self._makePlayerHandFrame()
        self.player_hand_frame.update_idletasks()


    def _placeAreaLabels(self):
        self.user_score_label = makeLabel(self.parent, "", COLOUR_PRIME, COLOUR_TEXT_L, 0.3, 0.71, "center", 10)
        self.score_top_label = makeLabel(self.parent, "", COLOUR_PRIME, COLOUR_TEXT_L, 0.5, 0.115, "center", 10)
        self.score_left_label = makeLabel(self.parent, "", COLOUR_PRIME, COLOUR_TEXT_L, 0.1, 0.115, "center", 10)
        self.score_right_label = makeLabel(self.parent, "", COLOUR_PRIME, COLOUR_TEXT_L, 0.9, 0.115, "center", 10)
        self.player_turn_label = makeLabel(self.parent, "", COLOUR_PRIME, COLOUR_TEXT_L, 0.5, 0.695, "center", 10)

    
    def _getFrameDims(self, *args):
        dimentions = []
        for frame in args:
            dimentions.append(frame.winfo_width())
            dimentions.append(frame.winfo_height())
        return dimentions


    def _makeTopOptions(self):
        self.options_frame = makeFrame(self.parent, COLOUR_WIDGET_D, 1, 0.05, 0.5, 0, "n")
        makeButton(self.options_frame, "Peek", 8, COLOUR_WIDGET_L, COLOUR_TEXT_L, 0.2, 0.5, "center",  lambda: self._peekOpponents(), 10)
        makeButton(self.options_frame, "End Game", 8, COLOUR_WIDGET_L, COLOUR_TEXT_L, 0.05, 0.5, "center",  lambda: self.parent.destroy(), 10)

        
    def _makeLeftFrame(self):
        return makeFrame(self.parent, COLOUR_PRIME, 0.0843, 0.6, 0.1, 0.428, "center")


    def _makeTopFrame(self):
        return makeFrame(self.parent, COLOUR_PRIME, 0.48, 0.15, 0.5, 0.21, "center")


    def _makeRightFrame(self):
        return makeFrame(self.parent, COLOUR_PRIME, 0.0843, 0.6, 0.9, 0.428, "center")


    def _makeCenterFrame(self):
        return makeFrame(self.parent, COLOUR_WIDGET_D, 0.6, 0.35, 0.5, 0.49, "center")


    def _makePlayerHandFrame(self):
        return makeFrame(self.parent, COLOUR_PRIME, 0.9, 0.21, 0.5, 0.84, "center")


    def offlineStart(self):
        self._placePredictionsWon()
        self._placeNames()
        self._setupRound()


    @staticmethod
    def _setHandOrder(player_count):
        deck_order = [1, 1, 2]  #left, top, right
        if player_count == 4:
            deck_order[1] = 2
            deck_order[2] = 3
        return deck_order


    def _placeNames(self):#place names and predicted/achieved
        if self.player_count == 2:
            name_top_label = makeLabel(self.parent, self.names[1], COLOUR_PRIME, COLOUR_TEXT_L, 0.5, 0.08, "center", 10)
        elif self.player_count == 3:
            name_left_label = makeLabel(self.parent, self.names[1], COLOUR_PRIME, COLOUR_TEXT_L, 0.1, 0.08, "center", 10)
            name_right_label = makeLabel(self.parent, self.names[2], COLOUR_PRIME, COLOUR_TEXT_L, 0.9, 0.08, "center", 10)
        elif self.player_count == 4:
            name_left_label = makeLabel(self.parent, self.names[1], COLOUR_PRIME, COLOUR_TEXT_L, 0.1, 0.08, "center", 10)
            name_top_label = makeLabel(self.parent, self.names[2], COLOUR_PRIME, COLOUR_TEXT_L, 0.5, 0.08, "center", 10)
            name_right_label = makeLabel(self.parent, self.names[3], COLOUR_PRIME, COLOUR_TEXT_L, 0.9, 0.08, "center", 10)


    def _placePredictionsWon(self):
        self.user_score_label["text"] = "Predicted: " + str(self.predictions[0]) + ", Won: " + str(self.subRoundsWon[0])
        if self.player_count == 2:
            self.score_top_label["text"] = "Predicted: " + str(self.predictions[1]) + ", Won: " + str(self.subRoundsWon[1])
        elif self.player_count == 3:
            self.score_left_label["text"] = "Predicted: " + str(self.predictions[1]) + ", Won: " + str(self.subRoundsWon[1])
            self.score_right_label["text"] = "Predicted: " + str(self.predictions[2]) + ", Won: " + str(self.subRoundsWon[2])
        elif self.player_count == 4:
            self.score_left_label["text"] = "Predicted: " + str(self.predictions[1]) + ", Won: " + str(self.subRoundsWon[1])
            self.score_top_label["text"] = "Predicted: " + str(self.predictions[2]) + ", Won: " + str(self.subRoundsWon[2])
            self.score_right_label["text"] = "Predicted: " + str(self.predictions[3]) + ", Won: " + str(self.subRoundsWon[3])


    def _peekOpponents(self):
        self.peek = not self.peek
        self._placeAllHands()


    def _setupRound(self):
        self._shuffleDeck()
        for x in range(self.player_count):
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
            elif self.trump_suit == "s":
                ordered_hand = d + c + h + s
            elif self.trump_suit == "d":
                ordered_hand = c + h + s + d
            elif self.trump_suit == "c":
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
        self.player_hand_frame = self._makePlayerHandFrame()
        self.showPlayerCards()


    def showPlayerCards(self):
        for x in range(len(self.hands[0])):
            img_loc = "res/card_packs/" + self.colour_scheme + "/" + self.hands[0][x] + ".png"
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
        img_loc = "res/card_packs/" + self.colour_scheme + "/" + self.hands[player][int(card_index)] + ".png"
        h = self.frame_dims[7]
        w = int(h/1.452)
        relx = 0.4+(self.center_cards*0.14)
        self._placeImage(self.center_frame, img_loc, w, h, relx, 0.5, "center")
        self.center_cards += 1


    def _placeAllHands(self):
        for p in range(1, self.player_count):
            self._placeOpponentCards(p)


    def _calculateRoundWinner(self):
        card_values = []
        round_suit = self.center_state[0][1][-1]

        #calculate card values
        for pair in self.center_state:
            card = pair[1]
            value = 0
            if self.trump_suit in card:
                value += 13
            if round_suit in card:
                value += CARD_ORDER.index(card[0])
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
        self.center_frame = self._makeCenterFrame()
        self.center_cards = 0

        #self._setupRound()
        #update center info
        self.populateCenter()


    def _showResults(self):
        self.results_frame = makeFrame(self.parent, COLOUR_WIDGET_D, 1, 0.93, 0.5, 0.07, "n")

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
        
        makeLabel(self.parent, "Results", COLOUR_WIDGET_D, "white", 0.5, 0.15, "center", 16)

        self.round_title_label = makeLabel(self.parent, "Round", COLOUR_WIDGET_D, "white", 0.08, 0.3, "center", 10)
        
        for col, name in enumerate(self.names):
            self.name_label = makeLabel(self.parent, name, COLOUR_WIDGET_D, "white", 0.25+(0.2*col), 0.3, "w", 10)
            for r in range(len(self.results)):
                if col == 0:
                    self.round_number_label = makeLabel(self.parent, str(r+1), COLOUR_WIDGET_D, "white", 0.08+(0.2*col), 0.32+((r+1)*0.05), "center", 10)

                self.score_label = makeLabel(self.parent, str(self.results[r][col*2]), COLOUR_WIDGET_D, "white", 0.24+(0.2*col), 0.32+((r+1)*0.05), "center", 10)
                self.score_label = makeLabel(self.parent, str(self.results[r][col*2+1]), COLOUR_WIDGET_D, "white", 0.28+(0.2*col), 0.32+((r+1)*0.05), "center", 10)

        makeLabel(self.parent, "PLAYER won the game!", COLOUR_WIDGET_D, "white", 0.5, 0.88, "center", 10)


 
    def startGame(self):
       
        #if center is full
        if self.center_cards == self.player_count:
            
                #pause to show winner for each round

                #self.player_turn_label['text'] = f'{self.names[self.current_player]} won the round!' #fixxx #move to win round code
                #self.player_turn_label['fg'] = "yellow"
                
                time.sleep(1)

                #if there are still cards left to be played
                if len(self.hands[0]) != 0:
                    print("next sub round")
                    self._startNextRound()
                    
                else:
                    print("next round")                    
                    
                    #update scores and clear rounds one and TODO redo redictions
                    new_results = []
                    
                    for player in range(self.player_count):

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
            if (self.current_player == self.player_count) or (self.current_player == 0):

                #if player not already given choice options
                if not self.pause_user:
                    self.pause_user = True
                    self.current_player = 0

                    self.player_turn_label["text"] = "Your Turn!"
                    self.player_turn_label['fg'] = "red"

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
                    self.playerOptions = makeFrame(self.parent, COLOUR_PRIME, 0.9, 0.05, 0.5, 0.95, "n")
                    for card in range(self.round_size):
                        if card in valid_indexes:
                            makeButton(self.playerOptions, "Select", 8, COLOUR_BUTTON, COLOUR_TEXT_L, 0.09*(card+1), 0.5, "center", lambda x=card: self.playerMadeTurn(str(x)), 9)

            #else bots turn
            elif self.current_player != 0:
                self.player_turn_label['text'] = f'{self.names[self.current_player]}\'s turn!'
                self.player_turn_label['fg'] = COLOUR_TEXT_L

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
            if ((self.player_count == 2) & (opponent == 1)) or ((self.player_count == 4) & (opponent == 2)):
                self.top_frame = self.top_frame.destroy()
                self.top_frame = self._makeTopFrame()#self._makeFrame(self.parent, 0.48, 0.15, 0.5, 0.21, "blue", "center")

                h = self.frame_dims[1]
                for x in range(len(self.hands[opponent])):
                    if self.peek == True:
                        card = self.hands[opponent][x]
                    image = makePhotoImage("res/card_packs/" + self.colour_scheme + "/" + card + ".png", int(h*0.6887), h, None)                    
                    makeLabelImage(self.top_frame, image, COLOUR_PRIME, 0.09*(x+1), 0.5, "center")

            #LEFT
            elif (self.player_count != 2) & (opponent == 1):
                self.left_frame = self.left_frame.destroy()
                self.left_frame = self._makeLeftFrame() #self._makeFrame(self.parent, 0.11, 0.6, 0.1, 0.42, "pink", "center")
                w = self.frame_dims[2]
                for x in range(len(self.hands[opponent])):
                    if self.peek == True:
                        card = self.hands[self.deck_order[0]][x]
                    image = makePhotoImage("res/card_packs/" + self.colour_scheme + "/" + card + ".png", int(w*0.6887), w, Image.ROTATE_270)                    
                    makeLabelImage(self.left_frame, image, COLOUR_PRIME, 0.5, 0.09*(x+1), "center")
    
            #RIGHT
            elif ((self.player_count == 3) & (opponent == 2)) or ((self.player_count == 4) & (opponent == 3)):
                self.right_frame = self.right_frame.destroy()
                self.right_frame = self._makeRightFrame()#self._makeFrame(self.parent, 0.11, 0.6, 0.9, 0.42, "yellow", "center")
                w = self.frame_dims[4]
                for x in range(len(self.hands[opponent])):
                    if self.peek == True:
                        card = self.hands[self.deck_order[2]][x]
                    image = makePhotoImage("res/card_packs/" + self.colour_scheme + "/" + card + ".png", int(w*0.6887), w, Image.ROTATE_90)                    
                    makeLabelImage(self.right_frame, image, COLOUR_PRIME, 0.5, 1-(0.09*(x+1)), "center")



    def _setTrumpSuit(self):
         self.trump_suit = SUIT_LETTERS[self.round_number%4]

        
    def populateCenter(self):
        #trump suit center info
        self._setTrumpSuit()
        h = self.frame_dims[7]//2
        trump_suit_label = Label(self.center_frame, text="Trump: " + SUIT_NAMES[SUIT_LETTERS.index(self.trump_suit)], bg=COLOUR_CENTER, fg="white")
        trump_suit_label.place(relx=0.01, rely=0.01, anchor="nw")
        image = Image.open("res/icons/" + self.trump_suit + "_icon.png")
        image = image.resize((h, h))
        image = ImageTk.PhotoImage(image)

       # cardImg = PhotoImage(file = "res/images/icons/" + self.trump_suit + "_icon.png")
        image_label = Label(self.center_frame, image=image)
        image_label.image = image
        image_label.place(relx=0.031, rely=0.14, anchor="nw")

        scores = ""
        for index, name in enumerate(self.names):
            scores += name + ": " + str(self.scores[index]) + "\n"
            
        makeLabel(self.center_frame, "Scores:", COLOUR_CENTER, COLOUR_TEXT_L, 0.08, 0.57, "center", 11)
        makeLabel(self.center_frame, scores, COLOUR_CENTER, COLOUR_TEXT_L, 0.08, 0.85, "center", 9)
        makeLabel(self.center_frame, "Round: " + str(self.round_number+1) + " of " + str(self.total_rounds), COLOUR_CENTER, "white", 0.5, 0.05, "center", 9)
        

