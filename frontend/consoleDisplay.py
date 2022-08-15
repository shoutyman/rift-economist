#standard library imports
from colorama import init, Fore, Back
import configparser
import logging
import time

#local imports
from backend.clientConnection import ClientConnection
from backend.gameStates import GameStates as game
import backend.setup as setup

class ConsoleDisplay:
    def __init__(self):
        self.client = ClientConnection()
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

        #import information from config file
        self.UPDATE_INTERVAL = self.config.getint("SETTINGS", "UPDATEINTERVAL")
        self.DISPLAY_TYPE = self.config["CONSOLEDISPLAYSETTINGS"]["DISPLAYTYPE"]
        
        #setup colorama for text styles
        init(autoreset = True)
        self.ORDER_PLAYER_STYLE = Fore.WHITE + Back.BLUE
        self.CHAOS_PLAYER_STYLE = Fore.WHITE + Back.RED
        self.ORDER_HEADER_STYLE = Fore.CYAN
        self.CHAOS_HEADER_STYLE = Fore.RED
        self.UNSPENT_GOLD_STYLE = Fore.GREEN

    def run(self):
        running = True
        while (running):
            self.client.updateGameInfo()
            setup.clearConsole()
            match(self.client.currentGameState):
                case game.NO_GAME_DETECTED:
                    print("No game detected")
                case game.LOADING:
                    print("Game is loading...")
                case game.RUNNING:
                    self.displayGameTime()
                    if (self.DISPLAY_TYPE == "team"):
                        self.displayTeamGold()
                    elif (self.DISPLAY_TYPE == "value"):
                        self.displayRichestFirst()
                    else:
                        logging.error(f"config error: {self.DISPLAY_TYPE} is not a valid display type")
                        print(f"config error: {self.DISPLAY_TYPE} is not a valid display type")
                case _:
                    print("Unknown game state")
                
            time.sleep(self.UPDATE_INTERVAL)

    def displayGameTime(self):
        gameTimeInteger = int(self.client.currentGameTime)
        hours = gameTimeInteger // 3600
        gameTimeInteger = gameTimeInteger % 3600
        minutes = gameTimeInteger // 60
        gameTimeInteger = gameTimeInteger % 60
        seconds = gameTimeInteger
        print(f"Last updated: {hours}:{minutes}:{seconds}")

    def displayTeamGold(self):
        print(self.ORDER_HEADER_STYLE + f"Order team: {len(self.client.team_order)} players, {self.client.getTeamOrderValue()} gold value")
        for player in self.client.team_order.values():
            print(self.ORDER_PLAYER_STYLE + f"{player.championName}: {player.getSpentGold()} gold value")
        print(self.CHAOS_HEADER_STYLE + f"Chaos team: {len(self.client.team_chaos)} players, {self.client.getTeamChaosValue()} gold value")
        for player in self.client.team_chaos.values():
            print(self.CHAOS_PLAYER_STYLE + f"{player.championName}: {player.getSpentGold()} gold value")

    def displayRichestFirst(self):
        players = self.client.team_order
        players.update(self.client.team_chaos)
        sorted(players, lambda x: x.currentGold)
        for player in players.values():
            if (player.team == "ORDER"):
                print(self.ORDER_PLAYER_STYLE + f"{player.championName}: {player.getSpentGold()} gold value")
            elif (player.team == "CHAOS"):
                print(self.CHAOS_PLAYER_STYLE + f"{player.championName}: {player.getSpentGold()} gold value")