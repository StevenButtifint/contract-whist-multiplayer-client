import random



class UserConfig:
    def __init__(self):
        self.username = ""
        self.colour_scheme = "Default"
        self.userIconID = random.randint(1, 17)


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


    def getUserIconID(self):
        return self.userIconID


