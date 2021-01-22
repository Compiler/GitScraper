import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time




LANG = 'java'
PAGE_COUNT = 30
GIT_URL_START = "https://github.com/trending/" + LANG + "?since=daily&spoken_language_code=en"
GIT_URL_TOPICS= "https://github.com/topics/" + LANG + "?l=" + LANG


def seleniumScrapeTopics(startURL):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome(chrome_options=options)
    driver.get(startURL)
    html = driver.page_source.encode('utf-8')

    currentPageNum = 1
    while(driver.find_element_by_xpath("/html/body/div[4]/main/div[2]/div[2]/div/div[1]/form/button") and currentPageNum < PAGE_COUNT):
        print("On page " + str(currentPageNum))
        currentPageNum += 1
        driver.find_element_by_xpath("/html/body/div[4]/main/div[2]/div[2]/div/div[1]/form/button").click();
        time.sleep(3)
                #if loading new page, uncomment
        #element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div/div[1]/form/button")))
        #element.click();

    html = driver.page_source.encode('utf-8')


    domStruct = BeautifulSoup(html, 'html.parser')
    print("Parsing DOM Structure")
    allRepos = domStruct.select('article.border.rounded-1.box-shadow.bg-gray-light.my-4 div.d-flex.flex-items-start.ml-3 a')
    endStr = ""
    for eachRepo in allRepos:
        repre = str(eachRepo.attrs['href'] + '\n')
        if('/login' in repre):
            continue
        endStr += 'github.com'+str(eachRepo.attrs['href'])[0:-10] + '\n'
    
    f = open("HTMLDump.txt", "a", encoding='utf-8')
    f.write(endStr)
    f.close() 



def getTrendingRepositoriesLinks(startURL):
    res = requests.get(startURL, headers= {'User-Agent' : "Mozilla/5.0"})
    if(res.status_code != 200):
        print ("Failed to load " + startURL + ' -- response code : ' + res.status_code)
        return

    htmlData = res.content
    domStruct = BeautifulSoup(htmlData, 'html.parser')

    allRepos = domStruct.select('article.Box-row h1')
    for eachRepo in allRepos:
        href = eachRepo.a.attrs["href"]
        print('github.com/'+href) 
    
if __name__ == "__main__":
    print("Starting selenium")
    seleniumScrapeTopics(GIT_URL_TOPICS)





