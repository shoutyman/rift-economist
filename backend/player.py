#player.py
#This file describes the the Player class, which stores relevant information for a player in game.

#local imports
import backend.iteminfo as items

class Player():
    def __init__(self, attributes):
        self.championName = attributes.get("championName")
        self.summonerName = attributes.get("summonerName")
        self.team = attributes.get("team")
        self.currentGold = attributes.get("currentGold")
        self.items = attributes.get("items")
        self.position = attributes.get("position")
        self.dead = attributes.get("isDead")

    def getSpentGold(self):
        value = 0
        for item in self.items:
            value += items.getBuyPrice(item["itemID"])
        return value

    def getGoldValue(self):
        value = 0
        for item in self.items:
            itemid = item["id"]
            value += items.getItemValue(itemid)
        return value
