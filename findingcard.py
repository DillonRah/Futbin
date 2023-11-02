import bs4
import requests 
import csv
import time
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


link = "https://www.futbin.com/players?page=1&search=kolo-muani"
#url = "https://stackoverflow.com/questions/13779526/finding-a-substring-within-a-list-in-python"

def soup(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=headers)
    response = urlopen(req)
    html = response.read()
    return BeautifulSoup(html, 'html.parser')

site = soup(link)

def getplayerpagelink(site):
    temp = []
    for link in site.find_all('a'):
        temp.append(link.get('href'))

    sub = "24/player/"
    links = [] #parsed href links of the temp

    for player in temp:
        if player is None:
            temp.remove(player)
        elif sub in player:
            #print(player)
            links.append("https://www.futbin.com" + player)

    return(links[0])

def getRarity(site):
    names = (site.find_all(class_="header_name full-name"))
    name = str(names[0])
    name = name[36:] # just parsing the string
    index = name.find('-')
    if index != -1:
        temp = name[index + 1:]
        index = temp.find(' ')
        rarity = temp[:index]
    else:
        rarity = "Rare Gold" # unless its a bronze or something or a gold non rare but realistically this is an edge case so we can try validate it later
    return rarity

# now update the csv file?
# make a disctionary for futbin acronyms and the actual words e.g RTTK -> Road to the Knockout
