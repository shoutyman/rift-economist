import tkinter as Tk
import configparser

#load settings from the config file
config = configparser.ConfigParser()
config.read("config.ini")

rowwidth = config["DISPLAY"]["ROWMAX"]
imgfolder = config["PATH"]["ITEMIMGPATH"]

