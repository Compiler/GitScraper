import os
import re

if __name__=='__main__':
    langToParse = 'Java'
    repos = open('ScrapedUsers/GithubRepositories.txt', 'r', encoding='utf-8')
    cloneName = ''
    for line in repos:
        match = re.search('^\"' + langToParse + '\".*$', line)
        if(match != None):
            cloneName =line[len(langToParse) + 4:-2] + '.git'
            repoName = cloneName.rsplit('/', 1)[-1][:-4]
            print(cloneName)

            os.system('cmd /c "git clone ' + cloneName + ' resources/outputCode/' + repoName + '"')
