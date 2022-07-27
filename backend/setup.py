#This file contains functions to setup the program.

#python imports
import json
import configparser
import os

#local imports
from webscraper import FetchItemData

def clearConsole(): #if open, clears the console
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def updateItemData():
    config = configparser.ConfigParser()
    config.read("config.ini")
    outputfilename = config["PATH"]["ITEMDATAPATH"]
    print(f"Sending item data to {outputfilename}")
    FetchItemData(outputfilename)

if __name__ == "__main__":
    updateItemData()