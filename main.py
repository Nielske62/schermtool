# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 15:21:58 2018

@author: Arjan B'vomeulen
"""

from flask import Flask
import numpy as np
from datapakker import *
import time
from commissielezer import *
import sys
from spotifyunit import *

app = Flask(__name__)


sys.maxsize = 2018302999999

#Current year, month, day, hour, minute (needed to request data from Twelve)
dy, dm, dd, dh, dn = time.localtime(time.time())[0:5]
dh = dh-6
statistiekenaan = 1
turfdictalcohol = turflijst()
turfdictfris = turflijst()
testing = 0

@app.route('/index/spotify/')
def spotifyding():
    informatie = info()
    sequence = "<table><tr><th width=30% style='padding: 0px;' rowspan = 2><img src='" + informatie['plaatje'] + "' width=100px></th><th id='CurrPlay'>Currently Playing:</th></tr>"
    sequence += "<tr>"
    sequence += "<th id='MusicInfo'>" + informatie['artiest'] + "<br>" + informatie['nummer'] + "</th>"
    return sequence#"Artiest: " + informatie['artiest'] + "<br>Nummer: " + informatie['nummer'] + "<br><img src='" + informatie['plaatje'] + "'>"

@app.route('/index/daemon/')
def statistiekendeamon():
    global dy, dm, dd, dh, dn, turfdictalcohol, turfdictfris, testing
    commissiedict = commissielijst()
    commissiedict[''] = ''
    if testing == 0:
        py, pm, pd, ph, pn = dy, dm, dd, dh, dn
        dy, dm, dd, dh, dn = time.localtime(time.time())[0:5]
        #Fetch raw transaction data from Twelve
        rawdata = pakdata(dy, dm, dd, dh, dn, py, pm, pd, ph, pn)
    
    if testing == 1:
        rawdata = open("TwelveTestInput.txt")
        rawdata = rawdata.readlines()
        statistiekenaan = 0
    
    foundstart = 0
    teller = -1
    
    for i in rawdata:
        if foundstart == 0:
            if '<tr class="row_even">' in i:
                foundstart = 1
            teller += 1
    
    startpos = teller
    
    running = 1
    if foundstart == 0:
        running = 0
        print "Laf gezopen!"
    i = 0
    while running:
        if "TABLE" in str(rawdata[teller+15 + 26*i]):
            running = 0
        else:
            naam = rawdata[teller+6 + 26*i].strip("\t<td>").strip("</td>\n")
            hoeveel = rawdata[teller+16 + 26*i].strip('\t<td align="right">').strip("</td>\n")
            product = rawdata[teller+23 + 26*i].strip("\t<td>").strip("</td>\n") #print naam + " en die kocht " + hoeveel + " " + product
            if '2018302' in naam:
                naam = long(naam) - 2018302000000 + 4302000
            if naam == '': #Make sure pin or cash doesnt crash the system
                pass
            elif int(naam) in commissiedict and commissiedict[int(naam)] != '':
		if commissiedict[int(naam)] not in turfdictalcohol:
                    turfdictalcohol[commissiedict[int(naam)]] = 0
                    turfdictfris[commissiedict[int(naam)]] = 0
                if int(product) == 8010:
                    turfdictalcohol[commissiedict[int(naam)]] += int(hoeveel)
                if int(product) == 8020:
                    turfdictfris[commissiedict[int(naam)]] += int(hoeveel)
            i += 1 
    
    lijstalcohol = sorted(turfdictalcohol.iteritems(), key=lambda (k,v): (v,k), reverse = True)
    lijstfris = sorted(turfdictfris.iteritems(), key=lambda (k,v): (v,k), reverse = True)

    sequence = "<table><tr><th width=40%>Alcoholic:</th><th width=10%></th><th width=40%>Non-alcoholic:</th><th width=10%></th></tr>\n"
    for i in range(len(lijstalcohol)):
        sequence += "<tr>\n"
        if lijstalcohol[i][1] != 0:
            sequence += "<td>" + str(lijstalcohol[i][0]) + "</td><td width=10%>" + str(lijstalcohol[i][1]) + "</td>\n"
        else:
            sequence += "<td></td><td></td>\n"
        if lijstfris[i][1] != 0:
            sequence += "<td>" + str(lijstfris[i][0]) + "</td><td width=10%>" + str(lijstfris[i][1]) + "</td>\n"
        else:
            sequence += "<td></td><td></td>\n"
        sequence += "</tr>\n"
    sequence += "</table>"
    return sequence        
    
@app.route('/index/')
def indexpage():
    page = open('www/page.html')
    return page.read()

@app.route('/prijslijst/')
def prijslijstpage():
    page = open('www/geenstatistiek.html')
    return page.read()
        
@app.route('/index/refresher.js')
def refresher():
    page = open('www/refresher.js')
    return page.read()

@app.route('/index/stylesheet.css')
def stylesheet():
    page = open('www/stylesheet.css')
    return page.read()

    
#var blnResult; en die kocht TD TABLE


app.run(port=9999)
    


