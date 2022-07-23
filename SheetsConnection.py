from googleapiclient.discovery import build
from google.oauth2 import service_account
from constants import *


class SheetsConnection:   
    def __init__(self):
        self.credentials = None
        self.service = None
        self.sheet = None
        self.link_status = False
        self.notice = ""
        self.session_ID = None
        self.lobby_ID = None
        self.game_row = 1
        self.current_players = []
        self.player_ID = None
        self.player_name = None


    def setLobbyID(self, lobby_ID):
        self.lobby_ID = lobby_ID


    def setPlayerName(self, player_name):
        self.player_name = player_name
        
