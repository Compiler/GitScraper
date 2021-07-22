import os
import re
from glob import glob
import dev_utils, file_utils
def clone_it(path):
    print(path)
    os.system(path)
if __name__=='__main__':
    root = 'D:\\Projects\\gitscraper'
    filename = 'D:\\Projects\\gitscraper\\ScrapedRepos\\GithubRepositoriesExtended1234.txt'
    repos = open(filename, 'r', encoding='utf-8')
    cloneName = ''
    #print([x[0] for x in os.walk(root + "\\resources\\outputCode\\")])
    languages = glob(root + "\\resources\\outputCode\\*")
    exceptions = ["Java", "Python"]
    count = 0;
    for exception in exceptions:
        languages.remove("D:\\Projects\\gitscraper\\resources\\outputCode\\" + exception)

    languages = ["D:\\Projects\\gitscraper\\resources\\outputCode\\Python"]
    last_line = '"Python":"https://github.com/K8H/dopavision"'
    resume = False
    for line in repos:
        if(not resume):
            if(line != last_line+"\n"):print("Skipped:", line); continue;
            else: resume = True;
        else:
            for langToParse in languages:
                if(langToParse in exceptions): exit();
                langToParse = langToParse[len("D:\\Projects\\gitscraper\\resources\\outputCode\\"):]
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
                    user_name = cloneName[len("https://github.com/"):-len(repoName) - 1 - len(".git")]
                    print(user_name)
                    path = 'cmd /c "cd ' + root + '\\resources\\outputCode\\' + langToParse + ' && git clone ' + cloneName + '"'
                    path = ' git clone git@github.com:' + user_name + '/' + repoName + " "+ root + '\\resources\\outputCode\\' + langToParse + "\\" + user_name + "\\" + repoName
                    timed_func = dev_utils.timeout(timeout=60*30)(clone_it)
                    try:
                        timed_func(path)
                    except:
                        print("Skipping");

    
