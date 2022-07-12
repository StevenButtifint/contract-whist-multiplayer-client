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


