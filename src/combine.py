from datetime import date
from os import listdir
from os.path import isfile, join

#this file will concatenate all links inside all files of scrapedprojects and remove duplicates.

if __name__ == "__main__":
    #f = open("ScrapedProjects/SJP-"+str(date.today())+".txt", "a", encoding='utf-8')
    combinedSet = set({})
    onlyfiles = [f for f in listdir('ScrapedProjects/') if isfile(join('ScrapedProjects/', f))]
    for file in onlyfiles:
        f = open('ScrapedProjects/' + file, "r", encoding='utf-8')
        for x in f:
            combinedSet.add(x.rstrip('\n'))
    f.close() 
    f = open("ScrapedProjects/Combined-SJP-"+str(date.today())+".txt", "a", encoding='utf-8')
    for item in combinedSet:
        f.write(item+'\n')
    f.close()