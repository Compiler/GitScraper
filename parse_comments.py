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
    print(classname)
    print(filename)
    print(methodNames)
    methodHeaders = get_method_headers(methodCode, methodNames)
    source = open(filename, encoding="utf-8").read()
    constructorHeaders = getConstructorHeaders(source, classname)
    comments = getMethodComments(source, constructorHeaders + methodHeaders)

    print("Final:\n", comments)
def get_method_headers(methodCode, methodNames):
    method_headers = []
    for method_name in methodNames:
        print(method_name)
        code = methodCode[method_name]
        header_pos = code.find(method_name)
        matches = re.findall("^.*"+method_name+ "[^{]*", code)
        method_headers = method_headers + matches
    return method_headers

#returns the constructor comments given their headers and source code
def getMethodComments(source, headers):
    if(len(headers) == 0): return [];
    start_comment_positions = []
    end_comment_locations = []
    for comment_type in end_comment_types: end_comment_locations = end_comment_locations + ([m.start() for m in re.finditer(comment_type, source)]);
    for comment_type in start_comment_types: start_comment_positions = start_comment_positions + ([m.start() for m in re.finditer(comment_type, source)]);

    if(len(end_comment_locations) == 0): return [];
    end_comment_locations = sorted(end_comment_locations)
    start_comment_positions = sorted(start_comment_positions)
    print("End comment locations: ", end_comment_locations)
    count = 0
    comment_header_relations={}
    for header in headers:
        position_of_header = source.find(header)
        print("header pos:", position_of_header)
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
        print('\'',data_between_header_and_comment,'\'')
        comment_pertains_to_header = check_comment(data_between_header_and_comment)
        print("Comment pertains to header?", comment_pertains_to_header)
        if(comment_pertains_to_header):
            #extract the comment for header
            header_comment = extract_comment(source, header, working_end_comment_pos, start_comment_positions)
            #extract source code for header
            header_body = extract_body_source(source, header)
            comment_header_relations["code"] = {"body" : header_body, "comment" : header_comment}
            print("Header:", header)
            print("Body:", header_body)
            if(len(header_body) < 25 or len(header_comment) < 2): continue;
            print("Comment:", header_comment)
            #outFile.write("{\n")
            json.dump(comment_header_relations, outFile)
            outFile.write('\n')
            #outFile.write('\n}')
    print("Headers:", headers)
    return comment_header_relations



def extract_comment(source, header, comment_end_position, start_comment_positions):
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
    pos = 0
    while(pos < len(text) - 2):
        moved_index = False
        #this section handles skipping past single-quotes
        if text[pos: pos +1] == '\'':
            pos = pos + 1
            moved_index = True

            inside_single_quotes = True
            start_single_quote_pos = pos
            while(inside_single_quotes and len(text) - 2 > pos):
                if(text[pos: pos +1] == "\'"):
                    inside_single_quotes = False
                pos = pos + 1
            print("Skipped:'",text[start_single_quote_pos : pos-1],"'")
            print("1:",pos)

        #this section handles skipping past quotes
        if text[pos: pos +1] == '\"': #first quote wont have anything behind it
            pos = pos + 1
            moved_index = True
            inside_quotes = True
            start_quote_pos = pos
            while(inside_quotes and len(text) - 2 > pos):
                if(text[pos: pos +1] == "\""):
                    inside_quotes = False
                    if(text[pos-2: pos] == "\\\\"):
                        inside_quotes = True
                pos = pos + 1
            pos = pos + 1
            print("2:",pos)
            print("Skipped:'",text[start_quote_pos : pos],"'")
        #now we know we aren't in a quote and can look for comments outside of quotes
        #first we will check for single line comments
        else:
            if text[pos: pos+2] == '//' : 
                skip_pos_start = pos;
                pos = pos + 2
                moved_index = True
                while(pos < len(text) - 2 and text[pos: pos+1] != '\n'):
                    pos = pos + 1
                print("1: Skipping: '", text[skip_pos_start : pos], "'")
                text = text[0:skip_pos_start] + text[pos:]
                distance_removed = pos - skip_pos_start
                #print("Distance moved: ", distance_removed)
                pos = pos - distance_removed + 1
                print("3:",pos)

            #now we check for multiline ones
            if  text[pos: pos+2] == '/*':
                skip_pos_start = pos;
                pos = pos + 2
                moved_index = True
                while(pos < len(text) - 2 and text[pos: pos+2] != '*/'):
                    pos = pos + 1
                print("2: Skipping: '", text[skip_pos_start : pos], "'")
                text = text[0:skip_pos_start] + text[pos+2:]
                distance_removed = pos - skip_pos_start
                #print("Distance moved: ", distance_removed)
                pos = pos - distance_removed + 1
                print("4:",pos)
        if not moved_index: pos = pos + 1;
    return text
    #return re.compile(r'(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',re.DOTALL | re.MULTILINE).sub(comment_replacer, text)


open_list = ["{"]
close_list = ["}"]
def is_balanced(myStr):
    print("Sent string:###############################################\n", myStr, "\n###############################################\n")
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
    print("Starting source:'\n",source,"'")
    cleaned_source = remove_comments(source)
    print("Removed comment source:'\n",cleaned_source,"'")
    header_pos = cleaned_source.find(header)
    #print("Header( ", header_pos,"):", header)
    #print(cleaned_source[header_pos:header_pos+len(header)])
    count = 0
    source_to_balance = cleaned_source
    print("Started balancing method for header: ", header)
    print("Starting source:", source_to_balance)
    amount_removed = 0
    x = 0
    while(not is_balanced(source_to_balance[header_pos:header_pos+len(header)+1 + count])):
        print("Source so far:________\n",source_to_balance[header_pos:header_pos+len(header)+1 + count], "\n__________")
        #find opening quote
        pos = header_pos+len(header) + count
        moved_index = False
        if source_to_balance[pos: pos +1] == '\'':
            print("Found first tick")
            amount_moved = 0
            pos = pos + 1
            moved_index = True

            inside_single_quotes = True
            start_single_quote_pos = pos
            while(inside_single_quotes):
                if(source_to_balance[pos: pos +1] == "\'"):
                    inside_single_quotes = False
                pos = pos + 1
                count = count + 1
                amount_moved = amount_moved + 1
            print("~~Skipping elements inside of ticks:_________________\n",source_to_balance[start_single_quote_pos : pos-1],"\n_________________")
            amount_removed = pos - start_single_quote_pos-1

#TODO SKIPPING SINGLE QUOTES AND DOUBLE QUOTES FAILS

            print("First 1/2:",  source_to_balance[header_pos:start_single_quote_pos-1]) 
            source_to_balance = source_to_balance[header_pos:start_single_quote_pos-1] + source_to_balance[start_single_quote_pos-1 + amount_moved:]
            print("Sent source:\"", source_to_balance,"\"")
        #this section handles skipping past quotes
        if source_to_balance[pos: pos +1] == '"': #first quote wont have anything behind it
            print("Found first quotation")
            print("Source before removal:________\n",source_to_balance[header_pos:header_pos+len(header)+1 + count], "\n__________")
            pos = pos + 1
            moved_index = True
            inside_quotes = True
            start_quote_pos = pos
            while(inside_quotes):
                if(source_to_balance[pos: pos +1] == "\""):
                    inside_quotes = False
                    if(source_to_balance[pos-2: pos] == "\\\\"):
                        inside_quotes = True
                pos = pos + 1
            end_quote_pos = pos - 1
            print("--Skipping elements inside of quotes:_________________\n",source_to_balance[start_quote_pos : end_quote_pos],"\n_________________")
            amount_removed = end_quote_pos - start_quote_pos
            print("Amount removed:", amount_removed)
            pos = pos - amount_removed
            header_pos = header_pos - amount_removed *4
            source_to_balance = source_to_balance[header_pos:start_quote_pos] + source_to_balance[end_quote_pos:]
            count = count - amount_removed
            print("Source after removal:________\n",source_to_balance[header_pos:header_pos+len(header)+1 + count], "\n__________")
            exit()

        if not moved_index: count = count + 1
        #print("Count:", count)
        #print("len(source_to_balance):", len(source_to_balance))
        if(count > len(source_to_balance)): return "NO";
    print("Balanced source:\n_______________\n", source_to_balance[header_pos:header_pos+len(header)+1 + count], "\n_________________")
    #print("balanced:\n", cleaned_source[header_pos:header_pos+len(header)+1 + count])
    #header_pos = cleaned_source.find(header)
    body_source = cleaned_source[header_pos:header_pos+len(header)+1 + count + amount_removed]
    print("Source code for header '", header, "':\n____________________\n", body_source, "\n____________________")
    return body_source

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
    try:
        f = open(source_directory, mode="r", encoding="utf-8")
        data = f.read()
    except:
        print("Failed to read data")
        return
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

    getJavaComments(methodNames, source_directory, methods)
    
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
    #parseSource("D:\\Projects\\gitscraper\\resources\\outputCode\\Java\\.emacs.d\\lib\\jdee-server\\src\\main\\java\\jde\\juci\\LispWriter.java")
    #test_file = open("D:\\Projects\\gitscraper\\resources\\outputCode\\Java\\02June2018\\src\\test\\java\\SeleniumGrid\\Grid_Practice_23March_2018.java")
    #print(remove_comments(test_file.read()))
    #print(remove_comments("/*hello*/\ncap.setBrowserName(\"chrome //this is cool\");"))
    #parseSource("D:\\Projects\\gitscraper\\resources\\outputCode\\Java\\02June2018\\src\\test\\java\\SeleniumGrid\\Grid_Practice_23March_2018.java")
    # test = open(filename + language + "/3d-renderer/src/matrix/Matrix.java").read()
    # print(test)
    # print(re.search("^(.+)\n\(", test))

    #parseSource("D:\\Projects\\gitscraper\\resources\\outputCode\\Java\\09-08-Projeto-Bicicleta\\src\\Bicicleta.java") #UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe1 in position 27: invalid continuation byte
    #parseSource("D:\\Projects\\gitscraper\\resources\\outputCode\\Java\\1.-Java-Basics-Homeworks\\3_Java_Loops_Methods_Classes\\lib\\joda-time-2.3\\src\\main\\java\\org\\joda\\time\convert\\StringConverter.java") 
    
    #parseSource("TestFile.java") 
    code = ''' 
      x){
        return x % 2 == 0 ? "" : "ODD";

    }
    '''
    #print(code, "\n is balanced : ", is_balanced(code))
    file = open("TestFile.java").read();
    extract_body_source(file, "public void sup1(int x)")
    #extract_body_source(file, "public void sup2()")

    #parseCode(filename + language)