#This file contains functions to setup the program.

#python imports
import json
import configparser
import os

def clearConsole(): #if open, clears the console
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

