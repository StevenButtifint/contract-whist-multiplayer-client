from googleapiclient.discovery import build
from google.oauth2 import service_account
from constants import *

import string
import random


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
        self.player_icon = None
        self.client_ID = self.setClientID()


    def initialiseConnection(self):
        try:
            self._initialiseCredentials()
            try:
                self._initialiseSheet()
                self.notice = C00
                self.link_status = True
            except:
                self.notice = C02
        except:
            self.notice = C01


    def _initialiseCredentials(self):
        self.credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)


    def _initialiseSheet(self):
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.sheet = self.service.spreadsheets()


    def getSheetData(self, page, cell_start, cell_end):
        result = self.sheet.values().get(spreadsheetId=self.session_ID, range=page+"!"+cell_start+":"+cell_end).execute()
        values = result.get('values', [])
        return values


    def setSheetData(self, cell, data):
        request = self.sheet.values().update(spreadsheetId=self.session_ID,
                                range="p1!"+str(cell), valueInputOption="USER_ENTERED",
                                body={"values":data}).execute()


    def setClientID(self):
        self.client_ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


        
    def checkForLobby(self):
        try:
            found_lobby = self.getSheetData("p1", "a"+str(self.game_row), "a1"+str(self.game_row))
            print("looking for:", self.lobby_ID)
            print("found:", found_lobby[0][0])
            return found_lobby[0][0] == self.lobby_ID
        except:
            return False
            
        

    def joinLobby(self):
        player_slots = ["c", "d", "e", "f"]
        icon_slots = ["g", "h", "i", "j"]

        try:
            self.current_players = self.getSheetData("p1", "c"+str(self.game_row), "f"+str(self.game_row))[0]
        except:
            self.current_players = []

        try:
            self.current_players_icons = self.getSheetData("p1", "g"+str(self.game_row), "j"+str(self.game_row))[0]
        except:
            self.current_players_icons = []
            
        if len(self.current_players) < 4:
            print(player_slots[len(self.current_players)]+str(self.game_row))
            print(self.player_name)
            self.setSheetData(player_slots[len(self.current_players)]+str(self.game_row), [[self.player_name]])
            self.setSheetData(icon_slots[len(self.current_players)]+str(self.game_row), [[self.player_icon]])
            self.player_ID = len(self.current_players)
            self.notice = L00
            print(self.player_name)
            return True
        
        elif '' in self.current_players:
            self.setSheetData(player_slots[self.current_players.index('')]+str(self.game_row), [[self.player_name]])
            self.player_ID = player_slots[self.current_players.index('')]+str(self.game_row)
            self.notice = L00
            return True
        else:
            self.notice = L02
            return False
 
    
    def setSessionID(self, session_ID):
        self.session_ID = session_ID


    def setLobbyID(self, lobby_ID):
        self.lobby_ID = lobby_ID


    def setPlayerName(self, player_name):
        self.player_name = player_name
        
