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
        self.client_ID = self.setClientID()




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
        found_lobby = self.getSheetData("p1", "a"+str(self.game_row), "a1"+str(self.game_row))
        print("looking for:", self.lobby_ID)
        print("found:", found_lobby[0][0])
        return found_lobby[0][0] == self.lobby_ID
        

 
    
    def setSessionID(self, session_ID):
        self.session_ID = session_ID


    def setLobbyID(self, lobby_ID):
        self.lobby_ID = lobby_ID


    def setPlayerName(self, player_name):
        self.player_name = player_name
        
