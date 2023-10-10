#this is just a test file to learn about web scrapingimport bs4
import requests 
import csv
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

#url = "https://www.futbin.com/popular"
url = "https://stackoverflow.com/questions/13779526/finding-a-substring-within-a-list-in-python"

headers = {'User-Agent': 'Mozilla/5.0'}
req = Request(url, headers=headers)
response = urlopen(req)
html = response.read()

soup = BeautifulSoup(html, 'html.parser')

players = []

print("The href links are :")
for link in soup.find_all('a'):
    players.append(link.get('href'))
#print(soup.prettify())

sub = "ea"

for player in players:
    if player is None:
        players.remove(player)
    elif sub in player:
        print(player)


