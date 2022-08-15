#This script fetches item data from the League of Legends wiki
# and turns it into a format usable by the data parser.
#Python library imports
import configparser
import logging
import re

#third party imports
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests



def FetchItemData(filename):
    logging.info("Updating item data...")
    config = configparser.ConfigParser()
    config.read("config.ini")
    item_data_url = config["API"]["ITEMDATAURL"]
    logging.info("Retrieving item data...")
    response = requests.get(item_data_url)
    status_code = response.status_code
    if (status_code == 200):
        logging.info("Retrieved item data")
        outputfile = open(filename, "w", encoding = "utf-8")
        content = response.text
        pre_tags = SoupStrainer("pre")
        soup = BeautifulSoup(content, 'lxml', parse_only = pre_tags)

        #item data is contained in second <pre> tag
        data = soup.find_all("pre")[1]
        text = data.text

        #clean up the data
        logging.info("Formatting item data...")
        text = re.sub(r"--.*\n", "", text, re.MULTILINE)
        text = re.sub(r".*return {", "{", text, re.DOTALL)  #remove the header
        text = re.sub(r",\n}\n-- </pre>", "}", text, re.DOTALL|re.MULTILINE)    #remove the footer
        text = re.sub("=", ":", text)   #replace all equals with colons
        text = re.sub("\[|\]", "", text)    #remove brackets around keys
        text = re.sub(r",(?=\n( |\t)*})", "", text)  #remove trailing commas
        text = re.sub(r",(?=})", "", text)
        text = re.sub(r"{(?=.*})", "[", text)  #replace braces around grouped values with brackets
        text = re.sub(r"(?<=\")}", "]", text)
        if (text):
            logging.info("Writing to item data file")
            outputfile.write(text)
    else:
        logging.warning(f"Could not connect to {item_data_url}; item data not updated")


if __name__ == "__main__":
    FetchItemData("datafile.json")