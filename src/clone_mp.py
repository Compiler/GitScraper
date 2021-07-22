import multiprocessing as mp
import os
import re
from glob import glob
import dev_utils


filename = 'D:\\Projects\\gitscraper\\ScrapedRepos\\GithubRepositoriesExtended1234.txt'
root = 'D:\\Projects\\gitscraper'
def clone_it(path):
    print(path)
    os.system(path)

def download(language):
    repos = open(filename, 'r', encoding='utf-8')
    langToParse = language[len("D:\\Projects\\gitscraper\\resources\\outputCode\\"):];
    last_line = '"Python":"https://github.com/K8H/dopavision"'
    resume = True
    for line in repos:
        if(not resume):
            if(line != last_line+"\n"):print("Skipped:", line); continue;
            else: resume = True;
        else:
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
                user_name = cloneName[len("https://github.com/"):-len(repoName) - 1 - len(".git")]
                path = ' git clone git@github.com:' + user_name + '/' + repoName + " "+ root + '\\resources\\outputCode\\' + langToParse + "\\" + user_name + "\\" + repoName
                timed_func = dev_utils.timeout(timeout=60*30)(clone_it)
                try:
                    timed_func(path)
                except:
                    print("Skipping");



def run_driver(root_filename, exceptions):
    languages = glob(root_filename + "\\*")
    for exception in exceptions:
        languages.remove("D:\\Projects\\gitscraper\\resources\\outputCode\\" + exception)
    cpu_count = mp.cpu_count()
    pool = mp.Pool(cpu_count)
    result = pool.map(download, languages)
if __name__=='__main__':
    run_driver(root + "\\resources\\outputCode", ["Java", "Python"])
    
    

    
