import string
import random



class UserConfig:
    def __init__(self):
        self.username = ""
        self.identifier = ""
        self.colour_scheme = "Default"


    def getUsername(self):
        if self.username == "":
            self.username = "new Player"
        elif len(self.username) > 15:
            self.username = self.username[0:15]
        return self.username


    def getIdentifier(self):
        if self.identifier == "":
            self.setIdentifier()
        return self.identifier


    def getColourScheme(self):
        return self.colour_scheme

    
    def setUsername(self, username):
        self.username = username
    

    def setIdentifier(self):
        self.identifier = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))


    def setColourScheme(self, colour_scheme):
        self.colour_scheme = colour_scheme



