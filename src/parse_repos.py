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



def parseContent(htmlData):
    domStruct = BeautifulSoup(htmlData, 'html.parser')

    allRepos = domStruct.select('li.col-12.d-flex.width-full.py-4.border-bottom.color-border-secondary.public.source')
    langs = domStruct.select('ml-0.mr-3')
    for eachLanguage in langs:
        print(eachLanguage)
    for eachRepo in allRepos:
        href = eachRepo.a.attrs["href"]
        print(href) 
    
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
    filename = "ScrapedUsers/GithubUsernames.txt"
    flag = True
    startKey = ''
    f = open(filename, "a", encoding='utf-8')
    if(startKey == ''):
        flag = False
    for i in range(5):
        for username in map(''.join, itertools.product('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', repeat=i)):
            if(flag):
                if(username == startKey):
                    flag = False
                print(username,'x')
                continue
            
            if(scrapeRepos(username) == 1):
                f.write('https://github.com/' + username + '\n')
    f.close()