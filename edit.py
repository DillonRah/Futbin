import requests 
import csv
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import time

class Player:
    def __init__(self, name, price, rarity, percentage, fullname):
        self.name = name
        self.price = price
        self.rarity = rarity
        self.percentage = percentage
        self.fullname = fullname

def soup(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=headers)
    response = urlopen(req)
    html = response.read()
    return BeautifulSoup(html, 'html.parser')

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

def getRarity(site):
    site = soup(site)
    names = (site.find_all(class_="header_name full-name"))
    name = str(names[0])
    name = name[36:] # just parsing the string
    index = name.find('-')
    if index != -1:
        rarity = name[index + 1:]
        rarity = rarity[1:-37]
    else:
        rarity = "Rare Gold" # unless its a bronze or something or a gold non rare but realistically this is an edge case so we can try validate it later
    return rarity

popularlink = "https://www.futbin.com/popular" # The main site I will be scraping from (just the list of the most popular players on fifa) - equivilant to liquidity?
popularsite = soup(popularlink) # The soup object of the popular site
hrefs = [] #href links of the players
substring = "24/player/" #substring to differentiate the players from the random links
links = [] #parsed href links of the players
playernames = [] #list of strings of  names of all of the players
nonparsedplayerprices = [] #list of strings of all of the unparsed player prices
playerprices = [] #list of strings of all of the parsed player prices
cardrarity = [] #list of strings of all of the player card rarities
listofpercentages = []
listofplayers = []

for link in popularsite.find_all('a'):
    hrefs.append(link.get('href'))

for link in hrefs:
    if link is None:
        hrefs.remove(link)
    elif substring in link:
        #print(player)
        links.append("https://www.futbin.com" + link)

#print(links)

for link in links:
    s = ""
    count = 0
    for letter in link:
        if letter == '/':
            count += 1
        if count == 6:
            s += letter
    playernames.append(s[1:])

for count, player in enumerate(playernames):
    if count < 10:
        site = soup("https://www.futbin.com/players?page=1&search=" + player)
        players = scrapeplayerdata(site)
        nonparsedplayerprices.append((prices(players)))
        time.sleep(0.1) # to not annoy futbin and get banned (add a delay to act as a real person)
        cardrarity.append(getRarity(links[count]))


for count, price in enumerate(nonparsedplayerprices):
    index = price.find(' ')
    if index != -1:
        listofpercentages.append(price[index + 1:])
        nonparsedplayerprices[count] = price[:index]
    else:
        listofpercentages.append(0)

for price in nonparsedplayerprices:
    s.replace(" ", "")
    if price[-1] == 'K':
        playerprices.append(float(price[:-1]) * 1000)
    elif price[-1] == 'M':
        playerprices.append(float(price[:-1]) * 1000000)
    else:
        playerprices.append(float(price))

for count, price in enumerate(playerprices):
    index = playernames[count].find('-')
    if index != -1:
        x = Player(playernames[count][index + 1:], price, cardrarity[count], listofpercentages[count], playernames[count])
    else:
        x = Player(playernames[count], price, cardrarity[count], listofpercentages[count], playernames[count])
    listofplayers.append(x)

csv_file_name = "spreadsheet-of-popular-players.csv"

def makingcsv(spreadsheetname, players):
    with open(spreadsheetname, mode="w", newline='') as file:
        writer = csv.writer(file) # Create a CSV writer object (idk what this means)
        writer.writerow(["Card Name", "Price", "Rarity", "Percentage", "Max Buy", "Min Profit", "Full Name"])
        for player in players:
            writer.writerow([player.name, player.price, player.rarity, player.percentage, price * 0.9, price * 0.05, player.fullname])


makingcsv(csv_file_name, listofplayers)

print("Done.")