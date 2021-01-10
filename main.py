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

path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__, static_folder=path + "/www/static")

sys.maxsize = 2018302999999

# Current year, month, day, hour, minute (needed to request data from Twelve)
dy, dm, dd, dh, dn = time.localtime(time.time())[0:5]
dh = dh - 6
statistiekenaan = 1
turfdictalcohol = turflijst()
turfdictfris = turflijst()
testing = 1


@app.route('/index/spotify/')
def spotifyding():
    informatie = info()
    if informatie is None:
        return "<h1>Er ging iets mis met het laden van Spotify</h1> <h3><i>Sippe fluit begint met spelen</i></h3>"
    sequence = "<table><tr><th width=30% style='padding: 0px;' rowspan = 2><img src='" + informatie[
        'plaatje'] + "' width=100px></th><th id='CurrPlay'>Currently Playing:</th></tr>"
    sequence += "<tr>"
    sequence += "<th id='MusicInfo'>" + informatie['artiest'] + "<br>" + informatie['nummer'] + "</th>"
    return sequence  # "Artiest: " + informatie['artiest'] + "<br>Nummer: " + informatie['nummer'] + "<br><img src='"
    # + informatie['plaatje'] + "'>"


@app.route('/index/daemon/')
def statistiekendeamon():
    global dy, dm, dd, dh, dn, turfdictalcohol, turfdictfris, testing, rawdata
    commissiedict = commissielijst()
    commissiedict[''] = ''
    if testing == 0:
        py, pm, pd, ph, pn = dy, dm, dd, dh, dn
        dy, dm, dd, dh, dn = time.localtime(time.time())[0:5]
        # Fetch raw transaction data from Twelve
        rawdata = list(
            map(lambda x: x.decode('utf-8'),
                pakdata(dy, dm, dd, dh, dn, py, pm, pd, ph, pn))
        )

    if testing == 1:
        rawdata = list(
            map(lambda x: x.decode('utf-8'),
                pakdata(2020, 1, 9, 23, 59, 2020, 1, 9, 14, 0))
        )

    foundstart = 0
    teller = -1

    for i in rawdata:
        if foundstart == 0:
            # rawdata is in bytes here
            if '<tr class="row_even">' in i:
                foundstart = 1
            teller += 1

    # startpos is the first instance of the table row with data (<tr>)
    startpos = teller

    running = 1
    if foundstart == 0:  # geen data
        running = 0
        print("Laf gezopen!")
    i = 0
    while running:
        if "</table>" in rawdata[startpos + 25 * i]:
            # end of table is reached
            running = 0
        else:
            rekeningnummer = rawdata[startpos + 6 + 25 * i].strip("\t<td>").strip("</td>\n")
            aantal = rawdata[startpos + 16 + 25 * i].strip('\t<td align="right">').strip("</td>\n")
            product = rawdata[startpos + 23 + 25 * i].strip("\t<td>").strip(
                "</td>\n")  # print naam + " en die kocht " + hoeveel + " " + product
            if '2018302' in rekeningnummer:
                rekeningnummer = int(rekeningnummer) - 2018302000000 + 4302000
            if rekeningnummer == '':  # Make sure pin or cash doesnt crash the system
                pass
            elif int(rekeningnummer) in commissiedict and commissiedict[int(rekeningnummer)] != '':
                if commissiedict[int(rekeningnummer)] not in turfdictalcohol:
                    turfdictalcohol[commissiedict[int(rekeningnummer)]] = 0
                    turfdictfris[commissiedict[int(rekeningnummer)]] = 0
                if int(product) == 8010:
                    turfdictalcohol[commissiedict[int(rekeningnummer)]] += int(aantal)
                if int(product) == 8020:
                    turfdictfris[commissiedict[int(rekeningnummer)]] += int(aantal)
            i += 1

    lijstalcohol = sorted(turfdictalcohol.items(), key=None, reverse=True)
    lijstfris = sorted(turfdictfris.items(), key=None, reverse=True)

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
    page = open(path + '/www/page.html')
    return page.read()


@app.route('/prijslijst/')
def prijslijstpage():
    page = open(path + '/www/geenstatistiek.html')
    return page.read()


@app.route('/index/refresher.js')
def refresher():
    page = open(path + '/www/refresher.js')
    return page.read()


@app.route('/index/stylesheet.css')
def stylesheet():
    page = open(path + '/www/stylesheet.css')
    return page.read()


# var blnResult; en die kocht TD TABLE


app.run(port=9999)
