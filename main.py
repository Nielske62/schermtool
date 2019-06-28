# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 15:21:58 2018

@author: Arjan B'vomeulen
"""

from flask import Flask
import numpy as np
from datapakker import *
import time
import sys
import math

app = Flask(__name__)


sys.maxsize = 2018302999999

#Current year, month, day, hour, minute (needed to request data from Twelve)
dy, dm, dd, dh, dn = time.localtime(time.time())[0:5]
dh = dh-2
statistiekenaan = 1
sintzuipt = 1
kerstmanzuipt = 1
productsint = 788436
productkerstman = 788437	
testing = 0
hoevaak = 50

@app.route('/index/daemon/')
def statistiekendeamon():
    global dy, dm, dd, dh, dn, productsint, productkerstman, testing, sintzuipt, kerstmanzuipt, hoevaak
    hoevaak += 1
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
    modifier = hoevaak/50
    
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
            product = rawdata[teller+14 + 26*i].strip("\t<td>").strip("</td>\n") #print naam + " en die kocht " + hoeveel + " " + product
            if int(product) == productsint:
                sintzuipt += int(hoeveel)*modifier
            if int(product) == productkerstman:
                kerstmanzuipt += int(hoeveel)*modifier
        i += 1 
    omrekenfactor = 1200./(sintzuipt+kerstmanzuipt)
    kerstmanbalkje = math.floor(kerstmanzuipt*omrekenfactor)
    sintbalkje = math.ceil(sintzuipt*omrekenfactor)
	
    print "Sint: " + str(sintzuipt) +", Kerstman: " + str(kerstmanzuipt) + " Debug infomartie: " + str(hoevaak) + " " + str(modifier)
    
    sequence = '<table><tr width="1200px" height="120px"><td width='+ str(sintbalkje) +'px" style="background-color:rgba(193,13,0,0.85);"> </td><td width=' + str(kerstmanbalkje) + 'px" style="background-color:rgba(0,193,13,0.85);"> </td></tr></table>' 

    return sequence        
    
@app.route('/index/')
def indexpage():
    page = open('www/page.html')
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
    


