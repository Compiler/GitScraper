import sys,os,string
import re
import json
import ntpath
JAVA_EXT = 'java'
CPLUSPLUS_EXT = 'cpp'
PYTHON_EXT = 'py'


language = 'Java'
outDir = "resources\ResultingJSON\\"+language+'\code.json'
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

comment_types = ['//', '/*', '/**']
def check_comment(test_str):
    allowed = set('\t\n ')
    return set(test_str) <= allowed
def getJavaComments(methodNames, filename):
    classname =ntpath.basename(filename).split('.')[0]
    print(classname)
    print(filename)
    print(methodNames)
    source = open(filename).read()
    constructorHeaders = getConstructorHeaders(source, classname)
    comments = getConstructorComments(source, constructorHeaders)

#returns the constructor comments given their headers and source code
def getConstructorComments(source, headers):
    if(len(headers) == 0): return [];
    end_comment_locations = [m.start() for m in re.finditer('\*/', source)]
    if(len(end_comment_locations) == 0): return [];
    print("End comment locations: ", end_comment_locations)


    comment_header_relations={}
    for header in headers:
        position_of_header = source.find(header)
        print("header pos:", position_of_header)
        min_distance = -1
        #find minimum distance
        working_end_comment_pos = end_comment_locations[0]
        for end_comment in end_comment_locations:
            distance = position_of_header - end_comment
            #print("Current distance:", distance)
            if distance < 0: break;
            minmin_distance_pos = max(min_distance, distance)
            working_end_comment_pos = end_comment
        #validate that there is a comment above and nothing else
        data_between_header_and_comment = source[working_end_comment_pos+2:position_of_header]
        print('\'',data_between_header_and_comment,'\'')
        print("Comment pertains to header?",check_comment(data_between_header_and_comment))
    

#gets constuctor headers and returns those headers
def getConstructorHeaders(source, classname):
    headers = []
    while(source.find("public " + classname) != -1):
        posOfConstructor = source.find("public " + classname)
        posOfNewLine = source.find("\n", posOfConstructor)
        print(source[posOfConstructor:posOfNewLine - 1])
        headers.append(source[posOfConstructor:posOfNewLine - 1])
        source = source[posOfNewLine:]
    
    return headers




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
        methodNames = []
        for method in methods:
            #print(methods[method])
            data = {}
            data['code'] = methods[method]
            methodNames.append(method)
            # json.dump(data, outFile)
            # outFile.write('\n')
            #print("Done")

        #print(methods[0])
        getJavaComments(methodNames, source_directory)
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
    filename = 'resources/outputCode/'
    language = "TestLang"
    parseSource(filename + language + "/3d-renderer/src/matrix/Matrix.java")
    #parseSource(filename + language + "/3d-renderer/src/matrix/MatrixException.java")
    #parseSource(filename + language + "/3d-renderer/src/render/Camera.java")

    # test = open(filename + language + "/3d-renderer/src/matrix/Matrix.java").read()
    # print(test)
    # print(re.search("^(.+)\n\(", test))
#    parseCode(filename + language)