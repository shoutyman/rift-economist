#standard library imports
import configparser  # to read from config file
import logging

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
