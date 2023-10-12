#this is just a test file to learn about web scrapingimport bs4
import requests 
import csv
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

link = "https://www.futbin.com/popular"
#url = "https://stackoverflow.com/questions/13779526/finding-a-substring-within-a-list-in-python"

def soup (url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=headers)
    response = urlopen(req)
    html = response.read()
    return BeautifulSoup(html, 'html.parser')

site = soup(link)

players = []

#print("The href links are :")
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

#print(listofplayers)

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

def prices(player):
    s = ""
    for card in players:
        if(len(card) != 0 and ord(card[5][0]) < 65 and len(card[5]) != 0):
            s = (card[5] + ' ' + card[6])        #print(card[0] + '\t' + card[6])
        elif (len(card) != 0 and len(card[6]) != 0):
            s = (card[6])
    return s

for player in listofplayers:
    print(player)
    playerurl = "https://www.futbin.com/24/players?page=1&search=" + player
    playerdata = scrapeplayerdata(soup(playerurl))
    print(prices(playerdata))



#for link in links:
 #   currentsite = soup(link)
  #  for price in currentsite.find_all('span id'):
   #     print(price)
#currentsite = soup(links[0])
#print(currentsite.find_all(id="pslowest"))
#for price in currentsite.find_all('span', class_='price_big_right'):
 #   print(price)
#print("done")