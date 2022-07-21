

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
