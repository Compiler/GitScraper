import os, re

if __name__=='__main__':
    filename = 'D:\\Projects\\gitscraper\\ScrapedRepos\\GithubRepositoriesExtended1234.txt'
    dir_to_setup = 'D:\\Projects\\gitscraper\\resources\\Tester_Setup'
    repos = open(filename, 'r', encoding='utf-8')
    matches = {}    
    for line in repos:
        match = re.search('^\".*\":', line)
        if(match != None):
            language = match[0][1:-2]
            result = 0
            if(language in matches): result = matches[language] + 1
            matches[language] = result


    top_100 = []
    count = 0
    exception_list = ['Archived', 'Other', "The", "1"]
    for k,v in sorted(matches.items(), key=lambda p:p[1], reverse=True):
        print(k, '=', v)
        if(count < 100 and k not in exception_list): top_100.append(k); count = count + 1

    print(top_100)   
    for lang in top_100:
        directory = dir_to_setup + "\\"+lang
        if not os.path.exists(directory):
            os.makedirs(directory)
    
     