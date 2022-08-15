#standard library imports
from colorama import init, Fore, Back
import configparser  # to read from config file
import logging
import threading #  to set up threads

#local application imports
from backend import setup  # for setup and os-related functions

from frontend.consoleDisplay import ConsoleDisplay

if __name__ == "__main__":
    #set up logging
    logging.basicConfig(filename = 'logs/logfile.log', level = logging.WARNING)

    logging.info("Initializing program...")
    setup.updateItemData()
    program = ConsoleDisplay()
    program.run()       
