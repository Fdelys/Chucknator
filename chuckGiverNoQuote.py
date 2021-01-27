# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 14:24:09 2020

@author: frand
"""


import requests
import re
from bs4 import BeautifulSoup
import psycopg2, config

conn = psycopg2.connect(database="bdd_fdelys", user=config.user,password=config.passw, host='127.0.0.1') 
cur = conn.cursor()

# Traitement de chaque ligne: affichage & enregistrement
def traiteInfo(id, rate, vote, fact):
    print("%4d : %.2f %5d %s" % (id, rate, vote, fact))
    cur.execute("""INSERT INTO public."factChuck" VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;""", (id, fact))
    cur.execute("""INSERT INTO public."rateChuck" VALUES (NOW()::Date, %s, %s, %s) ON CONFLICT DO NOTHING;""", (id, rate, vote))

# Definition de la procédure qui traite 1 page
def recupPage(page):
    url = "https://chucknorrisfacts.net/facts.php?page=%d" % (page)
    print("\nRécupération de %s" %(url))
    r = requests.get(url, headers={"User-Agent": "Mon navigateur perso d'ici"})
    soup = BeautifulSoup(r.content, 'html.parser')
    blocks = soup.select("#content > div:nth-of-type(n+2)")
    for block in blocks: 
        fact = block.select_one("p")
        if fact is not None:
            id = block.select_one("ul.star-rating").attrs['id']
            rate = block.select_one("span.out5Class")
            vote = block.select_one("span.votesClass")
            
            traiteInfo(int(id[6:]), float(rate.text), int(vote.text[:-6]), fact.text)

def lastPage():
    url = "https://chucknorrisfacts.net/facts"
    r = requests.get(url, headers={"User-Agent": "Mon navigateur perso d'ici"})
    soup = BeautifulSoup(r.content, 'html.parser')
    lastPage = soup.select("#content a:link")
    lastPageToStr = str(lastPage[-1].get('href'))   
    numPage = re.findall(r'\d+', lastPageToStr)
    return(int(numPage[0]))

for p in range(1, lastPage()+1):
    recupPage(page = p)

cur.execute("""SELECT COUNT(*) FROM "factChuck";""")
print(cur.fetchall())
conn.commit()
conn.close()