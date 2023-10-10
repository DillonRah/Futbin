import bs4
import requests 
import csv
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

url = "https://www.futbin.com/players?page=1&version=gold_rare&pos_type=all"
r = "https://www.futbin.com/popular"

headers = {'User-Agent': 'Mozilla/5.0'}
req = Request(url, headers=headers)
response = urlopen(req)
html = response.read()


soup = BeautifulSoup(html, 'html.parser')

players = []

def flatten_list(list_):
    output = []
    for sublist in list_:
        output.extend(sublist)
        
    return output

for i in range(62):
    example = soup.find_all("tr")[i] # Mbappé
    attributes = [td.get_text() for td in example.find_all("td")]
    attributes = [i.strip() for i in attributes]
    attributes = flatten_list([i.split("\n") for i in attributes])
    attributes = flatten_list([i.split("\\") for i in attributes])
    attributes = [item.strip() for item in attributes if item.strip() != ""]
    players.append(attributes)

#print(players)
#print(....,end=)
def printprices(players):
    for player in players:
        if(len(player) != 0 and ord(player[5][0]) < 65 and len(player[5]) != 0):
            print(player[5] + ' ' + player[6])        #print(player[0] + '\t' + player[6])
        elif (len(player) != 0 and len(player[6]) != 0):
            print(player[6])

printprices(players)