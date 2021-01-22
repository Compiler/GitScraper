import requests
from bs4 import BeautifulSoup

LANG = 'java'
GIT_URL_START = "https://github.com/trending/" + LANG + "?since=daily&spoken_language_code=en"
GIT_URL_TOPICS= "https://github.com/topics/" + LANG

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
    print("Beginning scrape")
    getTrendingRepositoriesLinks(GIT_URL_START)




