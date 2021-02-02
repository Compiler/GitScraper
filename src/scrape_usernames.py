import itertools
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import date

def validateUser(startURL):
    res = requests.get('http://github.com/'+str(startURL), headers= {'User-Agent' : "Mozilla/5.0"})
    if(res.status_code != 200):
        print ("Failed to load " + startURL + ' -- response code : ' + str(res.status_code))
        return -1
    return 1


if __name__ == '__main__':
    for username in map(''.join, itertools.product('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', repeat=2)):
        if(validateUser(username) == 1):
            print(username)
        else:
            print("Failed: ", username)