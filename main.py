# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 15:21:58 2018

@author: Arjan B'vomeulen
"""

import sys
import time

from flask import Flask

from commissielezer import *
from datapakker import *
from productenlezer import *
from spotifyunit import *

path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__, static_folder=path + "/www/static")

sys.maxsize = 2018302999999

# Current year, month, day, hour, minute (needed to request data from Twelve)
dy, dm, dd, dh, dn = time.localtime(time.time())[0:5]
dh = dh - 6
statistiekenaan = 1
# turfdictalcohol = turflijst()
# turfdictfris = turflijst()
turfdictalcohol = {}
turfdictfris = {}
totalData = {}
productDict = productenDict()

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
        # py pm etc are the dates from the previous data retrieval.
        # the new data is from the interval [previous_retrieval_date, current_date]
        # the daemon only adds the new data to existing data.
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
            aantal = rawdata[startpos + 15 + 25 * i].strip('\t<td align="right">').strip("</td>\n")
            productID = rawdata[startpos + 13 + 25 * i].strip("\t<td>").strip(
                "</td>\n")  # print naam + " en die kocht " + hoeveel + " " + product
            if '2018302' in rekeningnummer:
                rekeningnummer = int(rekeningnummer) - 2018302000000 + 4302000
            if rekeningnummer == '':  # Betaald met pin, niet op rekening
                pass
            else:
                if rekeningnummer not in totalData:
                    # if rekeningnummer not yet in dict -> set default values
                    totalData[rekeningnummer] = {}
                    totalData[rekeningnummer]["Bier"] = 0
                    totalData[rekeningnummer]["Wijn"] = 0
                    totalData[rekeningnummer]["Fris"] = 0
                    totalData[rekeningnummer]["Snacks"] = 0
                    totalData[rekeningnummer]["Overig"] = 0

                totalData[rekeningnummer][productDict[productID]] += int(aantal)

            i += 1

    alcoholDict = {}
    for rekeningnummer in totalData:
        alcoholDict[rekeningnummer] = totalData[rekeningnummer]["Bier"]

    # sort dict
    alcoholDict = dict(sorted(alcoholDict.items(), key=lambda item: item[1], reverse=True))

    # lijstalcohol = sorted(turfdictalcohol.items(), key=None, reverse=True)
    # lijstfris = sorted(turfdictfris.items(), key=None, reverse=True)

    sequence = "<table><tr><th width=40%>Alcoholic:</th><th width=10%></th><th width=40%>Non-alcoholic:</th><th " \
               "width=10%></th></tr>\n "
    for i in alcoholDict:
        sequence += "<tr>\n"
        if alcoholDict[i] != 0:
            sequence += "<td>" + i + "</td><td width=10%>" + str(alcoholDict[i]) + "</td>\n"
        else:
            sequence += "<td></td><td></td>\n"
        # if lijstfris[i][1] != 0:
        #     sequence += "<td>" + str(lijstfris[i][0]) + "</td><td width=10%>" + str(lijstfris[i][1]) + "</td>\n"
        # else:
        #     sequence += "<td></td><td></td>\n"
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
