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




class Requester_Instance:
    def __init__(self):
        self.proxies = set();
        self.proxyPool = cycle({'81.12.119.189'})
        self.counter = 0
    
    # def getProxies(self):
    #     #url = 'https://free-proxy-list.net/'
    #     response = requests.get(url)
    #     parser = fromstring(response.text)
    #     self.proxies = set()
    #     self.proxyPool
    #     for i in parser.xpath('//tbody/tr')[:10]:
    #         if i.xpath('.//td[7][contains(text(),"yes")]'):
    #             #Grabbing IP and corresponding PORT
    #             proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
    #             self.proxies.add(proxy)
    #     self.proxyPool = cycle(self.proxies);
                


    def validateUser(self, git_username):
        try:
            res = requests.get('http://github.com/'+str(git_username), headers= {'User-Agent' : "Mozilla/5.0"})
            if(res.status_code != 200):
                print ("Failed to load '" + 'http://github.com/'+str(git_username) + "' -- response code : " + str(res.status_code))
                if(res.status_code == 429):
                    print("Sleeping --", end='')
                    time.sleep(5)
                    print("Reattempting connection!")
                    return self.validateUser(git_username)
                return -1
            print(".", end='')
            return 1
        except requests.exceptions.ConnectionError:
            print("Connection Exception caught")
            return self.validateUser(git_username)


if __name__ == '__main__':
    filename = "ScrapedUsers/GithubUsernames.txt"
    startKey = ''
    inst = Requester_Instance()
    if(os.stat(filename).st_size != 0):
        with open(filename, 'r') as f:
            line = f.readlines()[-1]
        
        startKey = re.findall("/[A-Z0-9_]*$", line)[0][1:]
        print("Resuming from",startKey)
    f = open(filename, "a", encoding='utf-8')
    flag = True
    if(startKey == ''):
        flag = False
    for i in range(4):
        for username in map(''.join, itertools.product('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', repeat=i)):
            if(flag):
                if(username == startKey):
                    flag = False
                print(username,'skipped')
                continue
            
            if(inst.validateUser(username) == 1):
                f.write('https://github.com/' + username + '\n')
    f.close()