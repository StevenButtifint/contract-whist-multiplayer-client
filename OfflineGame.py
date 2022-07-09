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
        
