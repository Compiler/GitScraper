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

filename = "ScrapedRepos/GithubRepositories.txt"
f = open(filename, "a", encoding='utf-8')


repos = dict()

def parseContent(htmlData):
    domStruct = BeautifulSoup(htmlData, 'html.parser')

    allRepos = domStruct.select('li.col-12.d-flex.width-full.py-4.border-bottom.color-border-secondary.public.source')
    for eachRepo in allRepos:
        href = 'https://github.com' + eachRepo.a.attrs["href"]
        lang = eachRepo.span
        if(lang != None):
            repos[lang.text.split()[0]] =  href
            f.write('\"'+lang.text.split()[0]+'\":\"' + href+'\"\n')
    allForks = domStruct.select('li.col-12.d-flex.width-full.py-4.border-bottom.color-border-secondary.public.fork')
    for eachFork in allForks:
        href = 'https://github.com' + eachFork.a.attrs["href"]
        lang = eachFork.span
        if(lang != None):
            repos[lang.text.split()[0]] =  href
            f.write('\"'+lang.text.split()[0]+'\":\"' + href+'\"\n')

    buttons = domStruct.select('#user-repositories-list > div > div')
    buttonSel = domStruct.select('.paginate-container')
    
    # buttonSel = domStruct.select('.paginate-container')
    # for button in buttonSel:
    #     print("Select button:", button.a.attrs["href"])
    for button in buttons:
        bType = button.a.text;
        if(bType.upper() == 'Previous'.upper()):
            return [0,0]
        elif(bType.upper() == 'Next'.upper()):
            return [1, buttonSel[0].a.attrs["href"]]
    
    return [-1, -1]


    

# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# driver = webdriver.Chrome(chrome_options=options)
def scrapeRepos(startURL):
    try:

        #html = driver.page_source.encode('utf-8')
        res = requests.get('http://github.com/'+str(startURL)+'?tab=repositories', headers= {'User-Agent' : "Mozilla/5.0"})
        print('====\tParsing\t', startURL)
        if(res.status_code != 200):
            print ("Failed to load '" + startURL + "' -- response code : " + str(res.status_code))
            if(res.status_code == 429):
                print("Sleeping --", end='')
                time.sleep(5)
                
                print("Reattempting connection!")
                return scrapeRepos(startURL)
            return -1
        code = parseContent(res.content)
        if(code[0] == 1):
            print('Next\tNew url:',code[1])
            res = requests.get(code[1], headers= {'User-Agent' : "Mozilla/5.0"})
            parseContent(res.content)

        print('====\tParsed\t', startURL)

        return 1
    except requests.exceptions.ConnectionError:
        print("Connection Exception caught")
        return scrapeRepos(startURL)



if __name__ == '__main__':
    flag = True
    usernameToContinueFrom = ''
    if(os.stat(filename).st_size != 0):
        with open(filename, 'r') as fileRead:
            line = fileRead.readlines()[-1]
        usernameToContinueFrom = line.split('/')[3]
        print("Resuming from",usernameToContinueFrom)
    if(usernameToContinueFrom == ''):
        flag = False
    for i in range(5):
        for username in map(''.join, itertools.product('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', repeat=i)):
            if(flag):
                if(username == usernameToContinueFrom.upper()):
                    flag = False
                    print('\n')
                print('.',end='')
                continue
            scrapeRepos(username)
    print("Closing")
    f.close()

    