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
#alternative solution : do not delete

#import requests
#from requests.adapters import HTTPAdapter
#from requests.packages.urllib3.util.retry import Retry
#
#
#session = requests.Session()
#retry = Retry(connect=3, backoff_factor=0.5)
#adapter = HTTPAdapter(max_retries=retry)
#session.mount('http://', adapter)
#session.mount('https://', adapter)
#
#session.get(url)

def validateUser(startURL):
    try:
        res = requests.get('http://github.com/'+str(startURL), headers= {'User-Agent' : "Mozilla/5.0"})
        if(res.status_code != 200):
            print ("Failed to load '" + startURL + "' -- response code : " + str(res.status_code))
            if(res.status_code == 429):
                print("Sleeping --", end='')
                time.sleep(5)
                print("Reattempting connection!")
                return validateUser(startURL)
            return -1
        print(".", end='')
        return 1
    except requests.exceptions.ConnectionError:
        print("Connection Exception caught: sleeping...")
        time.sleep(5)
        return validateUser(startURL)


if __name__ == '__main__':
    filename = "ScrapedUsers/GithubUsernames.txt"
    startKey = ''
    if(os.stat(filename).st_size != 0):
        with open(filename, 'r') as f:
            line = f.readlines()[-1]
        
        startKey = re.findall("/[A-Z0-9_]*$", line)[0][1:]
        print("Resuming from",startKey)
    f = open(filename, "a", encoding='utf-8')
    flag = True
    if(startKey == ''):
        flag = False
    for i in range(5):
        for username in map(''.join, itertools.product('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', repeat=i)):
            if(flag):
                if(username == startKey):
                    flag = False
                print(username,'skipped')
                continue
            
            if(validateUser(username) == 1):
                f.write('https://github.com/' + username + '\n')
    f.close()