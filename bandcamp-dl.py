#!/usr/bin/python3
import requests
import json
import argparse
from pathlib import Path
from getpass import getpass
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from io import StringIO
import sys, getopt
from bs4 import BeautifulSoup
import re
import os

links=[]
outpath='/'

try:
    opts, args = getopt.getopt(sys.argv[1:],"hl:o:",["help","url=","output="])
except getopt.GetoptError:
    print("Usage: bandcamp-dl.py -l <URL> -o <OUTPUT_FOLDER>")
    sys.exit(2)

for opt, arg in opts:
    if(opt == '-h'):
        print("Usage: bandcamp-dl.py -l <URL> -o <OUTPUT_FOLDER>")
        sys.exit()
        
    elif(opt == '-o'):
        outpath=arg
        if(outpath[len(outpath)-1] != '/'):
            outpath=outpath+'/'
    else:
        url=arg

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
page=downloader.get(url+'music', verify=False)

soup = BeautifulSoup(page.text)
for link in soup.findAll('a', attrs={'href': re.compile("^/track")}):
    links.append(url[:len(url)-1]+link.get('href'))
for link in soup.findAll('a', attrs={'href': re.compile("^/album")}):
    links.append(url[:len(url)-1]+link.get('href'))

for i in links:
    os.system('youtube-dl -o "'+outpath+'%(album)s/%(title)s.%(ext)s" ' + '"'+i+'"')
