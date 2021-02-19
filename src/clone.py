import os
import re

if __name__=='__main__':
    filename = 'ScrapedRepos/GithubRepositoriesExtended1234.txt'
    repos = open(filename, 'r', encoding='utf-8')
    cloneName = ''
    languages = ['Java', 'Python', 'C++']
    for langToParse in languages:
        for line in repos:
            match = re.search('^\"' + langToParse + '\".*$', line)
            if(match != None):
                cloneName =line[len(langToParse) + 4:-1] + '.git'
                if(cloneName[-12:-5] == 'members'):
                    print('skipped')
                    continue;
                repoName = cloneName.rsplit('/', 1)[-1][:-4]
                print(cloneName)
                print('cmd /c "cd resources/outputCode/' + langToParse + ' && git clone ' + cloneName + '"')
                os.system('cmd /c "cd resources/outputCode/' + langToParse + ' && git clone ' + cloneName + '"')

    
