# -*- coding: utf-8 -*-
"""
Created on Fri Mar 01 15:50:43 2019

@author: Arjan Vermeulen
"""

import requests
'''
payload = {
'code': "AQBgjWCA34B9ydJGUA1iw1STbjPAN2CPBYM4OzHag3_3HAIAVU-vK2Kt0qHQPmw8X4jS1MZpNX38Woq7HG93_vSZqB5omjwXvT2-KrOOmdQRmUmk16DdJDu_kVYykoH6wdkIj3don1gO2uwwZt1GeMNo5O_ZzhEX52oLutQxvzsUr1kn7TPOtU02IOZHcyX7bjXDroRniXz-s1eDT1Si50CqoWAIl2LreswaPHDjOx_l",
'grant_type': "authorization_code",
'redirect_uri': "https://example.com/callback",
'client_id': "af8f34d639fa4e3dbbb7dd8d14d0f060",
'client_secret': "a0e9759a5f474d36a9e261e5052dbc91"
}

r = requests.post("https://accounts.spotify.com/api/token", data = payload)

payload2 = {
"authorization": r.json()['access_token']
}
'''
def refresher():
    payload = {
    'grant_type':'refresh_token',
    'refresh_token':'AQAy33h5np5S-vV6KBK-2EA99yVF4uP9Sudf9vzKT5e5KrHKq2HGI2tzsuJxTZ1ACbb4476D4Hin-xRkHj1DawHoGvdOOnZsTiQRHqDnpezusrU7g8kBF75ggBI5a_XmdZ_bCA',
    'client_id': "af8f34d639fa4e3dbbb7dd8d14d0f060",
    'client_secret': "a0e9759a5f474d36a9e261e5052dbc91"
    }
    rrefresh = requests.post("https://accounts.spotify.com/api/token", data = payload)
    return rrefresh.json()
    
def get_playing():
    token = str(refresher()['access_token'])
    r2 = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers={"Authorization": "Bearer " +token})
    return r2.json()
    
def info():
    obj = get_playing()
    artist = str(obj['item']['artists'][0]['name'])
    song = str(obj['item']['name'])
    image = str(obj['item']['album']['images'][1]['url'])
    result = {
        'artiest' : artist,
        'nummer' : song,
        'plaatje' : image
        }
    return result
