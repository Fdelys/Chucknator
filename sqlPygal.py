# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 13:54:29 2020

@author: frand
"""

import psycopg2, config
import pandas as pd
import pygal
from pygal.style import RedBlueStyle

conn = psycopg2.connect(database="bdd_fdelys", user=config.user,password=config.passw, host='127.0.0.1') 
cur = conn.cursor()
sql = 'SELECT * FROM "factChuck"'
dfAll = pd.read_sql(sql,conn)
print(len(dfAll))

#requêtes pour chaque répartition
rateUn = '''SELECT DISTINCT * FROM "factChuck" INNER JOIN "rateChuck" ON ("factChuck".id="rateChuck".id) WHERE date = '2020-12-16' AND rating BETWEEN 0.00 AND 2.50 ORDER BY rating'''
dfUn = pd.read_sql(rateUn,conn)
lenUn = (len(dfUn))

rateDeux = '''SELECT DISTINCT * FROM "factChuck" INNER JOIN "rateChuck" ON ("factChuck".id="rateChuck".id) WHERE date = '2020-12-16' AND rating BETWEEN 2.51 AND 3.50 ORDER BY rating'''
dfDeux = pd.read_sql(rateDeux,conn)
lenDeux = (len(dfDeux))

rateTrois = '''SELECT DISTINCT * FROM "factChuck" INNER JOIN "rateChuck" ON ("factChuck".id="rateChuck".id) WHERE date = '2020-12-16' AND rating BETWEEN 3.51 AND 4.00 ORDER BY rating'''
dfTrois = pd.read_sql(rateTrois,conn)
lenTrois = (len(dfTrois))

rateQuatre = '''SELECT DISTINCT * FROM "factChuck" INNER JOIN "rateChuck" ON ("factChuck".id="rateChuck".id) WHERE date = '2020-12-16' AND rating BETWEEN 4.01 AND 5.00 ORDER BY rating'''
dfQuatre = pd.read_sql(rateQuatre,conn)
lenQuatre = (len(dfQuatre))

#Graph de répartion par moyenne
pie_chart = pygal.Pie(style=RedBlueStyle)
pie_chart.title = 'Repartition des facts par moyenne - 5308 facts'
pie_chart.add('0.00-2.50 : 11%', lenUn)
pie_chart.add('2.51-3.50 : 31%', lenDeux)
pie_chart.add('3.51-4.00 : 52%', lenTrois)
pie_chart.add('4.01-5.00 : 6%', lenQuatre)
pie_chart.render_in_browser()



#requêtes pour nb de votes alt : SELECT DISTINCT * FROM "factChuck" INNER JOIN "rateChuck" ON ("factChuck".id="rateChuck".id) WHERE date = '2020-12-16' AND nbvotes BETWEEN 0 AND 500 ORDER BY nbvotes
voteUno = '''SELECT SUM(nbvotes) FROM "rateChuck" WHERE nbvotes BETWEEN 0 AND 500'''
dfUno = pd.read_sql(voteUno,conn)
Uno = dfUno.loc[:, "sum"]

voteDos = '''SELECT SUM(nbvotes) FROM "rateChuck" WHERE nbvotes BETWEEN 501 AND 2000'''
dfDos = pd.read_sql(voteDos,conn)
Dos = dfDos.loc[:, "sum"]

voteTres = '''SELECT SUM(nbvotes) FROM "rateChuck" WHERE nbvotes BETWEEN 2001 AND 4000'''
dfTres = pd.read_sql(voteTres,conn)
Tres = dfTres.loc[:, "sum"]

voteQuattro = '''SELECT SUM(nbvotes) FROM "rateChuck" WHERE nbvotes BETWEEN 4001 AND 6000'''
dfQuattro = pd.read_sql(voteQuattro,conn)
Quattro = dfQuattro.loc[:, "sum"]

voteCinqo = '''SELECT SUM(nbvotes) FROM "rateChuck" WHERE nbvotes BETWEEN 6001 AND 10000'''
dfCinqo = pd.read_sql(voteCinqo,conn)
Cinqo = dfCinqo.loc[:, "sum"]

voteTotal = '''SELECT SUM(nbvotes) FROM "rateChuck"'''
dfTotal = pd.read_sql(voteTotal,conn)
Total = dfTotal.loc[:, "sum"]
#Graph pour les votes
line_chart = pygal.HorizontalBar()
line_chart.title = 'nombre de votes totaux : 2.600.099'
line_chart.add('0-500 : 35%', Uno)
line_chart.add('501-2000 : 8%', Dos)
line_chart.add('2001-4000 : 26%', Tres)
line_chart.add('4001-6000 : 24%', Quattro)
line_chart.add('6001-10000 : 7%', Cinqo)
line_chart.render_in_browser()