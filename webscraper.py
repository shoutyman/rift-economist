#This script fetches item data from the League of Legends wiki
# and turns it into a format usable by the data parser.
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import re

def FetchItemData(filename):
    response = requests.get("https://leagueoflegends.fandom.com/wiki/Module:ItemData/data?action=view")
    status_code = response.status_code
    if (status_code == 200):
        outputfile = open(filename, "w", encoding = "utf-8")
        logfile = open("test.html", "w", encoding = "utf-8")
        content = response.text
        pre_tags = SoupStrainer("pre")
        soup = BeautifulSoup(content, 'lxml', parse_only = pre_tags)

        #item data is contained in second <pre> tag
        data = soup.find_all("pre")[1]
        text = data.text

        #clean up the data a little
        head_pattern = r"return {"
        tail_pattern = r"-- </pre>"

        logfile.write(text)
        header = re.search(r"return {", text, re.DOTALL|re.MULTILINE)
        footer = re.search(r",\n}\n-- </pre>", text, re.DOTALL|re.MULTILINE)
        if (header and footer):
            print("found header and footer")
            text = text[header.end():] + text[:footer.start()]
            if (text):
                print("found item data")
                outputfile.write(text)
        else:
            print("could not find item data")
    else:
        print("Error connecting to League of Legends Wiki")


FetchItemData("datafile.html")