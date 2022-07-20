#!/usr/bin/env python

import httpx
from bs4 import BeautifulSoup as bs
import base64
import json
from Cryptodome.Cipher import AES
import yarl
import os

#some stuffs
headers= {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"
}

s = b'25742532592138496744665879883281'
iv = b'9225679083961858'
ajax_url = "https://membed.net/encrypt-ajax.php"

client = httpx.Client(headers=headers)

def pad(data):
    return data + chr(len(data) % 16) * (16 - len(data) % 16)

def decrypt(data):
    return AES.new(s, AES.MODE_CBC, iv=iv).decrypt(base64.b64decode(data))

def get_embade_url_id(url):
    '''
    function to get id from embade url
    '''
    r=client.get(url).text
    soup = bs(r, 'html.parser')
    link = soup.select("ul a")[1]["href"]
    return yarl.URL(link).query.get('id')
    


url = f"https://database.gdriveplayer.us/player.php?imdb=tt10872600"

id = get_embade_url_id(url)
encrypted_ajax = base64.b64encode(
    AES.new(s,AES.MODE_CBC,iv=iv).encrypt(
        pad(id).encode()
    )
)

r=client.get(ajax_url,
             params={'id':encrypted_ajax.decode()},
             headers={'x-requested-with': 'XMLHttpRequest'})

j = json.loads(
    decrypt(r.json().get("data")).strip(
        b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10"))


video_link = j["source"][0]["file"]
sub_link = j["track"]["tracks"][0]["file"]

print(f"{video_link}")

with open("results", "a") as write_results:
    write_results.write(video_link)
