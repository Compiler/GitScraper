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

if __name__=='__main__':
    cloneName = ''
    languages = ['JavaScript', 'Python', 'Java', 'Ruby', 'HTML', 'C++', 'C', 'PHP', 'Go', 'Shell', 'C#', 'CSS', 'TypeScript', 'Jupyter', 'Objective-C', 'MIT', 'Swift', 'Rust', 'Perl', 'Vim', 'R', 'Scala', 'Vue', 'Haskell', 'Clojure', 'GNU', 'Kotlin', 'Lua', 'TeX', 'CoffeeScript', 'Emacs', 'Dockerfile', 'Apache', 'Makefile', 'Dart', 'Elixir', 'PowerShell', 'Erlang', 'MATLAB', 'Creative', 'Groovy', 'OCaml', 'Julia', 'Assembly', 'Arduino', 'Common', 'HCL', 'Puppet', 'Batchfile', 'CMake', 'ActionScript', 'Template', 'Visual', 'F#', 'Scheme', 'SCSS', 'Processing', 'Pascal', 'Smarty', 'Nix', 'BSD', 'Elm', 'D', 'Verilog', 'XSLT', 'Fortran', 'Crystal', 'Racket', 'TSQL', 'ASP', 'Nim', 'VHDL', 'QML', 'Roff', 'PLpgSQL', 'OpenSCAD', 'Haxe', 'Eagle', 'AutoHotkey', 'Prolog', 'Cuda', 'Tcl', 'ApacheConf', 'Objective-C++', 'GDScript', 'Mathematica', 'PureScript', 'GLSL', 'SaltStack', 'Smalltalk', 'Mozilla', 'Nginx', 'SourcePawn', 'Rich', 'ShaderLab', 'Vala', 'PLSQL', 'PostScript', 'Standard', 'Logos']
    #print([x[0] for x in os.walk(root + "\\resources\\outputCode\\")])
    languages = glob(root + "\\resources\\outputCode\\*")
    exceptions = ["Java", "Python"]
    count = 0;
    for exception in exceptions:
        languages.remove("D:\\Projects\\gitscraper\\resources\\outputCode\\" + exception)



    test_lang = languages[0][len("D:\\Projects\\gitscraper\\resources\\outputCode\\"):]
    print(test_lang)

    cpu_count = mp.cpu_count()
    pool = mp.Pool(cpu_count)
    result = pool.map(download, languages)
    

    
