import itertools
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import date
import os
import re
from itertools import cycle
import traceback
from lxml.html import fromstring
import sys, getopt

filename = "ScrapedUsers/GithubRepositories.txt"
f = open(filename, "a", encoding='utf-8')

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    prox = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            prox.add(proxy)
    return prox


repos = dict()

def parseContent(htmlData):
    domStruct = BeautifulSoup(htmlData, 'html.parser')

    allRepos = domStruct.select('li.col-12.d-flex.width-full.py-4.border-bottom.color-border-secondary.public.source')
    for eachRepo in allRepos:
        href = 'https://github.com' + eachRepo.a.attrs["href"]
        lang = eachRepo.span
        if(lang != None):
            print(lang.text.split()[0],'-',href)
            repos[lang.text.split()[0]] =  href
            f.write('\"'+lang.text.split()[0]+'\":\"' + href+'\"\n')
    print('done')
    

def scrapeRepos(startURL):
    try:
        res = requests.get('http://github.com/'+str(startURL)+'?tab=repositories', headers= {'User-Agent' : "Mozilla/5.0"})
        if(res.status_code != 200):
            print ("Failed to load '" + startURL + "' -- response code : " + str(res.status_code))
            if(res.status_code == 429):
                print("Sleeping --", end='')
                time.sleep(5)
                
                print("Reattempting connection!")
                return scrapeRepos(startURL)
            return -1
        parseContent(res.content)
        return 1
    except requests.exceptions.ConnectionError:
        print("Connection Exception caught")
        return scrapeRepos(startURL)



if __name__ == '__main__':
    flag = True
    usernameToContinueFrom = ''
    if(usernameToContinueFrom == ''):
        flag = False
    for i in range(5):
        for username in map(''.join, itertools.product('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', repeat=i)):
            if(flag):
                if(username == usernameToContinueFrom):
                    flag = False
                print('x',end='')
                continue
            scrapeRepos(username)
    f.close()