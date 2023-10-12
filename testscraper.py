import bs4
import requests 
import csv
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


link = "https://www.futbin.com/popular"
#url = "https://stackoverflow.com/questions/13779526/finding-a-substring-within-a-list-in-python"

def soup(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=headers)
    response = urlopen(req)
    html = response.read()
    return BeautifulSoup(html, 'html.parser')

site = soup(link)

players = []

for link in site.find_all('a'):
    players.append(link.get('href'))
#print(soup.prettify())

sub = "24/player/"
links = []

for player in players:
    if player is None:
        players.remove(player)
    elif sub in player:
        #print(player)
        links.append("https://www.futbin.com" + player)

# this code works and gets all of the popular players and their links
# need to now open each of those links - get the price and store that in a dictionary with their price and the player name

playerandprices = {}
listofplayers = []

for link in links:
    s = ""
    count = 0
    for letter in link:
        if letter == '/':
            count += 1
        if count == 6:
            s += letter
    listofplayers.append(s[1:])

playerprices = []

def flatten_list(list_):
    output = []
    for sublist in list_:
        output.extend(sublist)
        
    return output

def scrapeplayerdata(soup):
    output = []
    example = soup.find_all("tr")[0] # Mbappé
    attributes = [td.get_text() for td in example.find_all("td")]
    attributes = [i.strip() for i in attributes]
    attributes = flatten_list([i.split("\n") for i in attributes])
    attributes = flatten_list([i.split("\\") for i in attributes])
    attributes = [item.strip() for item in attributes if item.strip() != ""]
    output.append(attributes)
    return output


def prices(players):
    s = ""
    for player in players:
        if(len(player) != 0 and ord(player[5][0]) < 65 and len(player[5]) != 0):
            s = (player[5] + ' ' + player[6])        #print(player[0] + '\t' + player[6])
        elif (len(player) != 0 and len(player[6]) != 0):
            s = (player[6])
    
    return s

for count, player in enumerate(listofplayers):
    while count < 10:
        site = soup("https://www.futbin.com/players?page=1&search=" + player)
        #print("https://www.futbin.com/players?page=1&search=" + player)
        players = scrapeplayerdata(site)
        print(prices(players))