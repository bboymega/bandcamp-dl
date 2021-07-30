#!/usr/local/bin/python3
import requests
import json
import argparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from io import StringIO
from bs4 import BeautifulSoup
import re
import os
import urllib

links=[]

parser = argparse.ArgumentParser()
parser.add_argument("url", help="URL of Video Page", type=str)
parser.add_argument("-o", "--output", default='./',dest="output", help="Set Output Location", action="store")
args=parser.parse_args()
outpath=args.output
url=args.url
if(url[len(url)-1]!='/'):
    url=url+'/'

downloader=requests.session()
header={
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'dnt': '1',
    'origin': 'https://www.google.com',
    'pragma': 'no-cache',
    'referer': 'https://www.google.com/',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
}

downloader.headers.update(header)
if(url[len(url)-4:len(url)-1] == 'com'):
    page=downloader.get(url+'music', verify=False)
else:
    page=downloader.get(url, verify=False)

soup = BeautifulSoup(page.text,features="html.parser")
for link in soup.findAll('a', attrs={'href': re.compile("^/track")}):
    if (url[-6:-1] != "music"):
        links.append(url[:-1]+link.get('href'))
    else:
        links.append(url[:-7]+link.get('href'))
for link in soup.findAll('a', attrs={'href': re.compile("^/album")}):
    if (url[-6:-1] != "music"):
        links.append(url[:-1]+link.get('href'))
    else:
        links.append(url[:-7]+link.get('href'))
    for i in links:
        os.system('youtube-dl -o "'+outpath+'%(album)s/%(title)s.%(ext)s" ' + '"'+i+'"')
