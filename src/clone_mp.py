import multiprocessing as mp
import os
import re
from glob import glob


filename = 'D:\\Projects\\gitscraper\\ScrapedRepos\\GithubRepositoriesExtended1234.txt'
root = 'D:\\Projects\\gitscraper'


def download(language):
    repos = open(filename, 'r', encoding='utf-8')
    langToParse = language[len("D:\\Projects\\gitscraper\\resources\\outputCode\\"):];
    for line in repos:
        #match = re.search('^\"' + langToParse + '\".*$', line)
        if(line[1:len(langToParse)+1] == langToParse):
            print("\tFound match")
            cloneName =line[len(langToParse) + 4:-1] + '.git'
            if(cloneName[-12:-5] == 'members'):
                print('\tSkipped')
                continue;
            repoName = cloneName.rsplit('/', 1)[-1][:-5]
            print(repoName)
            cloneName = cloneName[0:-5] + cloneName[-4:]
            print(cloneName)
            path = 'cmd /c "cd ' + root + '\\resources\\outputCode\\' + langToParse + ' && git clone ' + cloneName + '"'
            path = ' git clone ' + cloneName + ' ' + root + '\\resources\\outputCode\\' + langToParse + "\\" + repoName
            print(path)
            os.system(path)


def run_driver(root_filename, exceptions):
    languages = glob(root_filename + "\\*")
    for exception in exceptions:
        languages.remove("D:\\Projects\\gitscraper\\resources\\outputCode\\" + exception)
    cpu_count = mp.cpu_count()
    pool = mp.Pool(cpu_count)
    result = pool.map(download, languages)
if __name__=='__main__':
    run_driver(root + "\\resources\\outputCode", ["Java", "Python"])
    
    

    
