#standard library imports
import configparser
import requests

#third party imports
import asyncio

#local imports
from backend.gameStates import GameStates as game
from backend.player import Player

class ClientConnection:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

        #   create an HTTP session and prepare requests
        self.session = requests.Session()
        self.session.verify = self.config["PATH"]["TLSCERTIFICATEPATH"]
        playerInfoRequest = requests.Request("GET", self.config["API"]["PLAYERDATAURL"])
        self.PREPARED_PLAYER_INFO_REQUEST = self.session.prepare_request(playerInfoRequest) #for player info
        gameStateRequest = requests.Request("GET", self.config["API"]["GAMEDATAURL"])
        self.GAME_INFO_REQUEST = self.session.prepare_request(gameStateRequest)    #for querying game info

        #   create variables
        self.team_order = {}
        self.team_chaos = {}
        self.itemInfo = {}
        self.currentGameTime = 0
        self.currentGameState = game.UNKNOWN
    
    #re-reads the config file and updates variables
    def updateConfig(self):
        self.config.read("config.ini")

    #connects to the client and displays info
    async def run(self):
        while (True):
            self.updateGameInfo()
            await asyncio.sleep(self.config["SETTINGS"]["UPDATEINTERVAL"])

    #queries the client for the current game state (no game, loading, running)
    def updateGameState(self):
        try:
            response = self.session.send(self.GAME_INFO_REQUEST)
            content = response.json()
            gameTime = content.get("gameTime")
            if (gameTime is None or gameTime <= 0):
                self.currentGameState = game.LOADING
                self.currentGameTime = 0
            else:
                self.currentGameState = game.RUNNING
                self.currentGameTime = gameTime

        except requests.ConnectionError: # no game detected
            self.currentGameState = game.NO_GAME_DETECTED
        
    #retrieves current game info from the client
    def updateGameInfo(self):
        self.updateGameState()
        #champion info is required before fetching item info
        if (self.currentGameState == game.RUNNING):
            playerInfoResponse = self.session.send(self.PREPARED_PLAYER_INFO_REQUEST)
            self.playerInfo = playerInfoResponse.json()
            self.team_order = {}
            self.team_chaos = {}
            for player in self.playerInfo:
                playerName = player["summonerName"]
                if player["team"] == "ORDER":
                    self.team_order[playerName] = Player(player)
                else:
                    self.team_chaos[playerName] = Player(player)

    #returns the total value of Order team
    def getTeamOrderValue(self):
        value = 0
        for player in self.team_order.values():
            value += player.getSpentGold()
        return value

    def getTeamChaosValue(self):
        value = 0
        for player in self.team_chaos.values():
            value += player.getSpentGold()
        return value