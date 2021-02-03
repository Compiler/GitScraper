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
                print("Sleeping")
                time.sleep(10)
                print("re-attempting")
                return validateUser(startURL)
            return -1
        print(".", end='')
        return 1
    except:
        print("Exception caught: sleeping...")
        time.sleep(15*60)
        return validateUser(startURL)


if __name__ == '__main__':
    f = open("ScrapedUsers/Github_Usernames_Scrape.txt", "w", encoding='utf-8')
    for i in range(5):
        for username in map(''.join, itertools.product('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', repeat=i+2)):
            if(validateUser(username) == 1):
                f.write('https://github.com/' + username + '\n')
    f.close()