#This file contains functions to setup the program.

#standard library imports
import configparser
import logging
import os

#local imports
from backend.webscraper import FetchItemData

def clearConsole(): #clears the console to make way for the next frame
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def updateItemData():
    config = configparser.ConfigParser()
    config.read("config.ini")
    outputfilename = config["PATH"]["ITEMDATAPATH"]
    logging.info(f"Sending item data to {outputfilename}")
    FetchItemData(outputfilename)

if __name__ == "__main__":
    updateItemData()