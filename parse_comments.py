import sys,os,string
import re
import json
import ntpath
JAVA_EXT = 'java'
CPLUSPLUS_EXT = 'cpp'
PYTHON_EXT = 'py'


language = 'Java'
#outDir = "resources\ResultingJSON\\"+language+'\code.json'
outDir = "code.json"
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

start_comment_types = ['/\*', '/\*\*']
end_comment_types = ['\*/'] #'//.*\n']
def check_comment(test_str):
    allowed = set('\t\n ')
    return set(test_str) <= allowed
def getJavaComments(methodNames, filename, methodCode):
    classname =ntpath.basename(filename).split('.')[0]
    ####print(classname)
    ####print(filename)
    ####print(methodNames)
    ####print(methodCode[methodNames[0]])
    methodHeaders = get_method_headers(methodCode, methodNames)
    source = open(filename, encoding="utf-8").read()
    source = re.sub("//.*\n", "/*removed comment*/", source) #removes single-line comments
    constructorHeaders = getConstructorHeaders(source, classname)
    comments = getConstructorComments(source, constructorHeaders + methodHeaders)

    ####print("Final:\n", comments)
def get_method_headers(methodCode, methodNames):
    method_headers = []
    for method_name in methodNames:
        ####print(method_name)
        code = methodCode[method_name]
        header_pos = code.find(method_name)
        matches = re.findall("^.*"+method_name+ "[^{]*", code)
        method_headers = method_headers + matches
    return method_headers

#returns the constructor comments given their headers and source code
def getConstructorComments(source, headers):
    if(len(headers) == 0): return [];
    start_comment_positions = []
    end_comment_locations = []
    for comment_type in end_comment_types: end_comment_locations = end_comment_locations + ([m.start() for m in re.finditer(comment_type, source)]);
    for comment_type in start_comment_types: start_comment_positions = start_comment_positions + ([m.start() for m in re.finditer(comment_type, source)]);
    if(len(end_comment_locations) == 0): return [];
    ####print("End comment locations: ", end_comment_locations)
    count = 0
    comment_header_relations={}
    for header in headers:
        position_of_header = source.find(header)
        ####print("header pos:", position_of_header)
        min_distance = -1
        #find minimum distance
        working_end_comment_pos = end_comment_locations[0]
        for end_comment in end_comment_locations:
            distance = position_of_header - end_comment
            if distance < 0: continue;
            minmin_distance_pos = max(min_distance, distance)
            working_end_comment_pos = end_comment
        #validate that there is a comment above and nothing else
        data_between_header_and_comment = source[working_end_comment_pos+2:position_of_header]
        ####print('\'',data_between_header_and_comment,'\'')
        comment_pertains_to_header = check_comment(data_between_header_and_comment)
        ####print("Comment pertains to header?", comment_pertains_to_header)
        if(comment_pertains_to_header):
            #extract the comment for header
            header_comment = extract_constructor_comment(source, header, working_end_comment_pos, start_comment_positions)
            #extract source code for header
            header_body = extract_body_source(source, header)
            comment_header_relations["code"] = {"body" : header_body, "comment" : header_comment}
            ####print("Header:", header)
            ####print("Body:", header_body)
            if(len(header_body) < 25 or len(header_comment) < 2): continue;
            ####print("Comment:", header_comment)
            #outFile.write("{\n")
            json.dump(comment_header_relations, outFile)
            outFile.write('\n')
            #outFile.write('\n}')
    ####print("Headers:", headers)
    return comment_header_relations



def extract_constructor_comment(source, header, comment_end_position, start_comment_positions):
    header_position = source.find(header)
    ##print("Start comment locations:", start_comment_positions)
    min_distance = -1
    #find minimum distance
    working_start_comment_pos = start_comment_positions[0]
    for start_comment in start_comment_positions:
        distance = header_position - start_comment
        if distance < 0: break;
        minmin_distance_pos = max(min_distance, distance)
        working_start_comment_pos = start_comment
    data_between_end_and_start = source[working_start_comment_pos:comment_end_position+2]
    #print('Comment:\'',data_between_end_and_start,'\'')
    return data_between_end_and_start



#TODO: rewrite this 
def remove_comments(text):
    return text
    #return re.compile(r'(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',re.DOTALL | re.MULTILINE).sub(comment_replacer, text)


open_list = ["{"]
close_list = ["}"]
def is_balanced(myStr):
    stack = []
    for i in myStr:
        if i in open_list:
            stack.append(i)
        elif i in close_list:
            pos = close_list.index(i)
            if ((len(stack) > 0) and
                (open_list[pos] == stack[len(stack)-1])):
                stack.pop()
            else:
                return False
    if len(stack) == 0:
        return True
    else:
        return False

#gets source code of method from the header and source
def extract_body_source(source, header):
    #first remove all data between strings and also remove all comments from source
    #cleaned_source = re.sub("\".*\"", "\"\"", source)#empties strings, maybe remove?
    cleaned_source = remove_comments(source)
    header_pos = cleaned_source.find(header)
    #print("Header( ", header_pos,"):", header)
    #print(cleaned_source[header_pos:header_pos+len(header)])
    count = 0
    while(not is_balanced(cleaned_source[header_pos:header_pos+len(header)+1 + count])):
        #find opening quote
        pos = header_pos+len(header) + count
        if cleaned_source[pos: pos +1] == '\"':
            start_pos = pos
            pos = pos + 1
            inside_quotes = True

            while(inside_quotes):
                if(cleaned_source[pos: pos +1] == "\""):
                    inside_quotes = False
                    if(cleaned_source[pos-1: pos] == "\\" and cleaned_source[pos-2: pos-1] != "\\"):
                        inside_quotes = True
                pos = pos + 1
            if(not inside_quotes): pass;#print("Skipped:'", cleaned_source[start_pos:pos],"'");
            count = count + (pos - start_pos);
        count = count + 1
        if(count > len(cleaned_source)): return "NO";
    #print("balanced:\n", cleaned_source[header_pos:header_pos+len(header)+1 + count])
    return cleaned_source[header_pos:header_pos+len(header)+1 + count]


    #right now we have cleaned source, now we need to use a stack to get the code from header to end of method.

#gets constuctor headers and returns those headers
def getConstructorHeaders(source, classname):
    headers = []
    while(source.find("public " + classname) != -1):
        posOfConstructor = source.find("public " + classname)
        posOfNewLine = source.find("\n", posOfConstructor)
        #print(source[posOfConstructor:posOfNewLine - 1])
        headers.append(source[posOfConstructor:posOfNewLine - 1])
        source = source[posOfNewLine:]
    
    return headers




def parseSource(source_directory):
    f = open(source_directory, mode="r", encoding="utf-8")
    data = f.read()
    search = re.findall("/\*", data)
    # if(len(search) == 0):
    #     search = re.findall("^[^\"]*//.*$", data)
    #     if(len(search) == 0): return
    methods = {}
    try:
        tree = jl.parse.parse(data)
        methods = {}
        for _, node in tree.filter(jl.tree.MethodDeclaration):
            start, end = __get_start_end_for_node(node, data, tree)
            methods[node.name] = __get_string(start, end, data, tree)     
    except:
        print("Error, couldn't parse javalang")
        return

    #print(methods)
    methodNames = []
    for method in methods:
        #print(methods[method])
        #data = {}
        #data['code'] = methods[method]
        methodNames.append(method)
        # json.dump(data, outFile)
        # outFile.write('\n')
        #print("Done")

    #print(methods[0])
    getJavaComments(methodNames, source_directory, methods)
    #print("Couldn't encode data")
    
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
    #filename = 'resources/outputCode/'
    #language = "TestLang"

    filename = 'D:\\Projects\\gitscraper\\resources\\outputCode\\'
    language = "Java"
    
    #parseSource(filename + language + "/3d-renderer/src/matrix/Matrix.java")
    #parseSource(filename + language + "/3d-renderer/src/matrix/MatrixException.java")
    #parseSource(filename + language + "/3d-renderer/src/render/Camera.java")
    #parseSource("D:\\Projects\\gitscraper\\resources\\outputCode\\Java\\.emacs.d\\lib\\jdee-server\\src\\main\\java\\jde\\parser\\ParseException.java")
    parseSource("D:\\Projects\\gitscraper\\resources\\outputCode\\Java\\02June2018\\src\\test\\java\\SeleniumGrid\\Grid_Practice_23March_2018.java")

    # test = open(filename + language + "/3d-renderer/src/matrix/Matrix.java").read()
    # print(test)
    # print(re.search("^(.+)\n\(", test))
    #parseCode(filename + language)