import sys,os
import json
JAVA_EXT = 'java'
CPLUSPLUS_EXT = 'cpp'
PYTHON_EXT = 'py'


language = 'Java'
outDir = "resources\ResultingJSON\\"+language+'\code4.json'
outFile = open(outDir, mode="a")

import javalang as jl
def __get_start_end_for_node(node_to_find, data, tree):
    start = None
    end = None
    for path, node in tree:
        if start is not None and node_to_find not in path:
            end = node.position
            return start, end
        if start is None and node == node_to_find:
            start = node.position
    return start, end


def __get_string(start, end, data, tree):
    if start is None:
        return ""

    # positions are all offset by 1. e.g. first line -> lines[0], start.line = 1
    end_pos = None

    if end is not None:
        end_pos = end.line - 1

    lines = data.splitlines(True)
    string = "".join(lines[start.line:end_pos])
    string = lines[start.line - 1] + string

    # When the method is the last one, it will contain a additional brace
    if end is None:
        left = string.count("{")
        right = string.count("}")
        if right - left == 1:
            p = string.rfind("}")
            string = string[:p]

    return string


   

def parseSource(source_directory):
    f = open(source_directory, mode="r", encoding="utf-8")
    try:
        data = f.read()
        methods = {}
        try:
            tree = jl.parse.parse(data)
            methods = {}
            for _, node in tree.filter(jl.tree.MethodDeclaration):
                start, end = __get_start_end_for_node(node, data, tree)
                methods[node.name] = __get_string(start, end, data, tree)     
        except:
            print("Error")

        #print(methods)
        for method in methods:
            #print(methods[method])
            data = {}
            data['code'] = methods[method]
            json.dump(data, outFile)
            outFile.write('\n')
            #print("Done")
    except:
        print("Couldn't encode data")
    
startFromName = ''#'\\resources\outputCode\Java\HabitatGUIJava\src\sample\Main.java'
def parseCode(root):
    print("Beginning")
    extension = ''
    if(language == 'Java'):
        extension = JAVA_EXT
    elif(language == "C++"):
        extension = CPLUSPLUS_EXT
    elif(language == "Python"):
        extension = PYTHON_EXT
    else:
        print("Default language -- Testing")
        extension = JAVA_EXT
    if(startFromName == ''):
        print("Starting from scratch...")
        for path, subdirs, files in os.walk(root):
            for name in files:
                if(name[-len(extension):] == extension):
                    print(os.path.join(path, name))
                    parseSource(os.path.join(path, name))
    else:
        print("Resuming...")
        for path, subdirs, files in os.walk(root):
            for name in files:
                if(name[-len(extension):] == extension):
                    if(name != startFromName):
                        print("Skipped",os.path.join(path, name))
                        continue
                    print(os.path.join(path, name))
                    parseSource(os.path.join(path, name))


if __name__ == '__main__':
    #parseSource('resources\outputCode\TestLang\\3D-Cal-Steps\CalSteps.java')
    filename = 'resources/outputCode/'
    parseCode(filename + language)