import requests 
import csv
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import time

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
listofplayers = [] #list of strings of all of the players
playerprices = [] #list of strings of all of the player prices
cardrarity = [] #list of strings of all of the player card rarities

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
    listofplayers.append(s[1:])

for count, player in enumerate(listofplayers):
    if count < 10:
        site = soup("https://www.futbin.com/players?page=1&search=" + player)
        players = scrapeplayerdata(site)
        playerprices.append((prices(players)))
        time.sleep(0.1) # to not annoy futbin and get banned (add a delay to act as a real person)
        cardrarity.append(getRarity(links[count]))

listofpercentages = []
for price in playerprices:
    index = price.find(' ')
    if index != -1:
        listofpercentages.append(price[index + 1:])
        price = price[:index]
    else:
        listofpercentages.append(0)

#print(cardrarity)

#for count, price in enumerate(playerprices):
#    print(listofplayers[count] + "\t" + price)

#Need to make a way to find what card is actually popular

csv_file_name = "spreadsheet-of-popular-players.csv"
    
with open(csv_file_name, mode="w", newline='') as file:
    writer = csv.writer(file) # Create a CSV writer object (idk what this means)
    writer.writerow(["Player", "Price", "Percentage", "Rarity", "Max Buy", "Min Profit"])
    for count, price in enumerate(playerprices):
        writer.writerow([listofplayers[count], price, listofpercentages[count], cardrarity[count], float(price[:-1]) * 0.9, float(price[:-1]) * 0.05])

print("Done.")