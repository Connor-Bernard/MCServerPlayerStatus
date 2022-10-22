import threading
import requests
import rumps
import json

class MCUserChecker(rumps.App):
    def __init__(self):
        super(MCUserChecker, self).__init__(name="MCUserChecker")
        self.serverIp = "brimwat.apexmc.co"
        self.serverPort = "25565"
        self.players = []
        self.numPlayers = 0

    @rumps.timer(5)
    def userCheckThread(self, sender):
        thread = threading.Thread(target=self.updateNumUsers)
        thread.start()

    def updateNumUsers(self):
        res = requests.get(f"https://mcapi.us/server/status?ip={self.serverIp}&port={self.serverPort}")
        numPlayers = json.loads(res.text)["players"]["now"]
        for user in json.loads(res.text)["players"]["sample"]:
            if user["name"] not in self.players:
                self.players.append(user["name"])
                self.menu.add(user["name"])
                rumps.MenuItem.update()
            if self.numPlayers != numPlayers:
                self.players = []
                self.numPlayers = numPlayers
                self.menu.clear()
        self.title = f"Players: {numPlayers}"


if __name__ == '__main__':
    MCUserChecker().run()
