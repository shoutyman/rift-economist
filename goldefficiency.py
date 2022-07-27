#import python modules
import asyncio  # for timing
import configparser  # to read from config file
import time  # for timing
import requests  # to query the client

#local application imports
from backend import iteminfo as items  # to calculate item values & efficiency
from backend import setup  # for setup and os-related functions


class ClientConnection:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

        # create an HTTP session and prepare requests
        self.session = requests.Session()
        self.session.verify = self.config["PATH"]["TLSCERTIFICATEPATH"]

        #   set variables to default
        self.playerInfo = {"summonerName" : ""}
        self.itemInfo = {}
    
    #re-reads the config file and updates variables
    def updateConfig(self):
        self.config.read("config.ini")

    #connects to the client and displays info
    async def run(self):
        while (True):
            self.updateGameInfo()
            await asyncio.sleep(self.config["SETTINGS"]["UPDATEINTERVAL"])
        
    #retrieves current game info from the client
    def updateGameInfo(self):
        try: 
            playerInfoRequest = requests.Request("GET", self.config["API"]["PLAYERDATAURL"])
            #champion info is required before fetching item info
            preparedPlayerInfoRequest = self.session.prepare_request(playerInfoRequest)
            playerInfoResponse = self.session.send(preparedPlayerInfoRequest)
            self.playerInfo = playerInfoResponse.json()
            playerName = self.playerInfo["summonerName"]
            #fetch item info
            itemInfoRequest = requests.Request("GET", self.config["API"]["ITEMDATAURL"], params = {"summonerName" : playerName})
            preparedItemInfoRequest = self.session.prepare_request(itemInfoRequest)
            itemInfoResponse = self.session.send(preparedItemInfoRequest)
            self.itemInfo = itemInfoResponse.json()
            self.connected = True
        except requests.ConnectionError as err: # no game detected
            self.connected = False
            self.playerInfo = {}
            self.itemInfo = {}
            self.playerInfo["currentGold"] = 0

    def getPlayerInfo(self):
        return self.playerInfo
    
    def getItemInfo(self):
        return self.itemInfo

    #returns the sum of the purchase values of all owned items
    def getAssetValue(self):
        sum = 0
        for item in self.itemInfo:
            sum += items.getBuyPrice(item["itemID"])
        return sum

    #returns a dictionary containing the total stats gained from items
    def getTotalItemStats(self):
        totalStats = {}
        for item in self.itemInfo:
            itemStats = items.getItemStats(item["itemID"])
            for statName in itemStats.keys():
                if (statName in totalStats):
                    totalStats[statName] += itemStats[statName]
                else:
                    totalStats[statName] = itemStats[statName]
        return totalStats

    #returns current spendable gold
    def getLiquidValue(self):
        return self.playerInfo["currentGold"]

    def getTotalValue(self):
        return self.getAssetValue() + self.getLiquidValue()

class ConsoleDisplay:
    def __init__(self):
        self.client = ClientConnection()

    def run(self):
        while (running):
            self.client.updateGameInfo()
            setup.clearConsole()
            if (self.client.connected):
                print(f"Current market value: {self.client.getAssetValue()}")
                print(f"Current gold: {int(self.client.getLiquidValue())}")
                print(f"Net Worth: {int(self.client.getTotalValue())}")
                print()
                print("Total stats from items:")
                print(self.client.getTotalItemStats())
            else:
                print("No game detected")
            time.sleep(self.client.config.getint("SETTINGS", "UPDATEINTERVAL"))
            
    

""" #get live game data and write to logfile
#fetching champ stats and abilities
r = requests.get('https://127.0.0.1:2999/liveclientdata/activeplayer', verify = 'datadragon/riotgames.pem')
playerdata = r.json() 
champStatInfo = playerdata["championStats"]
championlogfile = open('logs\champion.json', "w")
championlogfile.write(json.dumps(playerdata, indent=4))

#get item data from champion data
summonerName = playerdata["summonerName"]
print("Summoner Name: " + summonerName)
r = requests.get(f'https://127.0.0.1:2999/liveclientdata/playeritems?summonerName={summonerName}', verify = 'datadragon/riotgames.pem')
currentItems = r.json()
itemlogfile = open('logs\currentitems.json', 'w')
itemlogfile.write(json.dumps(currentItems, indent = 4)) """
 
if __name__ == "__main__":
    print("Initializing program...")
    setup.updateItemData()
    program = ConsoleDisplay()
    running = True
    program.run()
