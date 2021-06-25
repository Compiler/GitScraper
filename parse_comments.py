import sys,os,string,logging
import re
import json
import ntpath
from typing import DefaultDict
JAVA_EXT = 'java'
CPLUSPLUS_EXT = 'cpp'
PYTHON_EXT = 'py'

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', stream=sys.stderr, level=logging.CRITICAL)### CRITICAL ERROR WARNING INFO DEBUG NOTSET
#logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', stream=sys.stderr, level=logging.ERROR)### CRITICAL ERROR WARNING INFO DEBUG NOTSET

language = 'Java'
outDir = "D:\\Projects\\gitscraper\\resources\\ResultingJSON\\"+language+'\\comment_code_data.json'
nameDir = "D:\\Projects\\gitscraper\\resources\\ResultingJSON\\"+language+'\\comment_code_data_names.txt'
#outDir = "code.json"
outFile = open(outDir, mode="a")
name_out_file = open(nameDir, mode="a", encoding="utf-8")

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
    logging.debug(classname)
    logging.debug(filename)
    logging.debug(methodNames)
    methodHeaders = get_method_headers(methodCode, methodNames)
    source = open(filename, encoding="utf-8").read()
    constructorHeaders = getConstructorHeaders(source, classname)
    comments = getMethodComments(source, constructorHeaders + methodHeaders)

    logging.debug("Final:\n%s", comments)
def get_method_headers(methodCode, methodNames):
    method_headers = []
    for method_name in methodNames:
        logging.debug(method_name)
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
    #logging.debug("End comment locations: ", end_comment_locations)
    count = 0
    comment_header_relations={}
    for header in headers:
        position_of_header = source.find(header)
        logging.debug("header pos: %d", position_of_header)
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
        logging.debug('\'%s\'', data_between_header_and_comment)
        comment_pertains_to_header = check_comment(data_between_header_and_comment)
        logging.debug("Comment pertains to header? %s", comment_pertains_to_header)
        if(comment_pertains_to_header):
            #extract the comment for header
            header_comment = extract_comment(source, header, working_end_comment_pos, start_comment_positions)
            #extract source code for header
            header_body = extract_body_source(source, header)
            comment_header_relations["code"] = {"body" : header_body, "comment" : header_comment}
            logging.debug("Header: %s", header)
            logging.debug("Body: %s", header_body)
            if(len(header_body) < 25 or len(header_comment) < 2): continue;
            logging.debug("Comment: %s", header_comment)
            #outFile.write("{\n")
            json.dump(comment_header_relations, outFile)
            outFile.write('\n')
            #outFile.write('\n}')
    logging.debug("Headers: %s", headers)
    return comment_header_relations



def extract_comment(source, header, comment_end_position, start_comment_positions):
    header_position = source.find(header)
    ##logging.debug("Start comment locations:", start_comment_positions)
    min_distance = -1
    #find minimum distance
    working_start_comment_pos = start_comment_positions[0]
    for start_comment in start_comment_positions:
        distance = header_position - start_comment
        if distance < 0: break;
        minmin_distance_pos = max(min_distance, distance)
        working_start_comment_pos = start_comment
    data_between_end_and_start = source[working_start_comment_pos:comment_end_position+2]
    #logging.debug('Comment:\'',data_between_end_and_start,'\'')
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
            logging.debug("Skipped:'%s'", text[start_single_quote_pos : pos-1])
            logging.debug("1: %d",pos)

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
            logging.debug("2: %d",pos)
            logging.debug("Skipped:'%s'", text[start_quote_pos : pos])
        #now we know we aren't in a quote and can look for comments outside of quotes
        #first we will check for single line comments
        else:
            if text[pos: pos+2] == '//' : 
                skip_pos_start = pos;
                pos = pos + 2
                moved_index = True
                while(pos < len(text) - 2 and text[pos: pos+1] != '\n'):
                    pos = pos + 1
                logging.debug("1: Skipping: '%s'", text[skip_pos_start : pos])
                text = text[0:skip_pos_start] + text[pos:]
                distance_removed = pos - skip_pos_start
                #logging.debug("Distance moved: ", distance_removed)
                pos = pos - distance_removed + 1
                logging.debug("3: %d",pos)

            #now we check for multiline ones
            if  text[pos: pos+2] == '/*':
                skip_pos_start = pos;
                pos = pos + 2
                moved_index = True
                while(pos < len(text) - 2 and text[pos: pos+2] != '*/'):
                    pos = pos + 1
                logging.debug("2: Skipping: '%s'", text[skip_pos_start : pos])
                text = text[0:skip_pos_start] + text[pos+2:]
                distance_removed = pos - skip_pos_start
                #logging.debug("Distance moved: ", distance_removed)
                pos = pos - distance_removed + 1
                logging.debug("4: %d",pos)
        if not moved_index: pos = pos + 1;
    return text
    #return re.compile(r'(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',re.DOTALL | re.MULTILINE).sub(comment_replacer, text)


open_list = ["{"]
close_list = ["}"]
def is_balanced(myStr):
    logging.debug("Sent string:----------------------------------------------------------\n%s\n----------------------------------------------------------n", myStr)
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
    logging.debug("Starting source::____________________\n%s\n____________________",source)
    cleaned_source = remove_comments(source)
    logging.debug("Removed comment source:____________________\n%s\n____________________",cleaned_source)
    header_pos = cleaned_source.find(header)
    logging.debug("Header(%d): %s", header_pos,  header)
    #logging.debug(cleaned_source[header_pos:header_pos+len(header)])
    count = 0
    source_to_balance = cleaned_source
    logging.debug("Started balancing method for header: %s", header)
    logging.debug("Starting source: %s", source_to_balance)
    amount_removed = 0
    x = 0
    while(not is_balanced(source_to_balance[header_pos:header_pos+len(header)+1 + count])):
        logging.debug("Source so far:________\n%s\n__________", source_to_balance[header_pos:header_pos+len(header)+1 + count])
        #find opening quote
        pos = header_pos+len(header) + count
        moved_index = False
        if source_to_balance[pos: pos +1] == "'": #first quote wont have anything behind it
            logging.debug("Found first tick")
            logging.debug("Source before removal:________\n%s\n__________", source_to_balance[header_pos:header_pos+len(header)+1 + count])
            starting_len = len(source_to_balance)
            pos = pos + 1
            moved_index = True
            inside_quotes = True
            start_quote_pos = pos
            logging.debug("Going inside quotes")
            _dbg_count = 0
            while(inside_quotes):
                if(_dbg_count > 50): logging.critical("Infinite loop found"); exit();
                _dbg_count = _dbg_count + 1
                logging.debug("'-Char: %s",source_to_balance[pos: pos +1])
                if(source_to_balance[pos: pos +1] == "'"):
                    inside_quotes = False
                    if(source_to_balance[pos-1: pos] == "\\"): inside_quotes = True;
                    if(source_to_balance[pos-2: pos-1] == "\\"): inside_quotes = False;
                pos = pos + 1
            end_quote_pos = pos - 1
            logging.debug("--Skipping elements inside of quotes:_________________\n%s\n_________________", source_to_balance[start_quote_pos : end_quote_pos])
            amount_removed = end_quote_pos - start_quote_pos
            logging.debug("Amount removed: %d", amount_removed)
            #pos = pos - amount_removed + 1
            #header_pos = header_pos - amount_removed 
            source_to_balance = source_to_balance[:start_quote_pos] + source_to_balance[end_quote_pos:]
            count = count + 2 
            pos = pos + 1
            logging.debug("Source after removal:\n________\n%s\n__________", source_to_balance[header_pos : header_pos+len(header) + count])
            ending_len = len(source_to_balance)
            logging.debug("starting len: %d\nending len: %d", starting_len, ending_len)

#TODO SKIPPING SINGLE QUOTES AND DOUBLE QUOTES FAILS

        #this section handles skipping past quotes
        if source_to_balance[pos: pos +1] == '"': #first quote wont have anything behind it
            logging.debug("Found first quotation")
            logging.debug("Source before removal:________\n%s\n__________", source_to_balance[header_pos:header_pos+len(header)+1 + count])
            starting_len = len(source_to_balance)
            pos = pos + 1
            moved_index = True
            inside_quotes = True
            start_quote_pos = pos

            _dbg_count = 0
            while(inside_quotes): #we are inside a quote
                if(_dbg_count > 50): logging.critical("Infinite loop found"); exit();
                _dbg_count = _dbg_count + 1
                logging.debug("\"-Char: %s",source_to_balance[pos: pos +1])
                if(source_to_balance[pos] == "\""): #found a potential ending quote
                    logging.debug("Maybe leaving?")
                    inside_quotes = False
                    if(source_to_balance[pos-1] == "\\"):
                        logging.debug("Found \\ character")
                        escape_count = 0
                        esc_pos = pos - 1

                        while(source_to_balance[esc_pos] == '\\'):
                            escape_count = escape_count + 1
                            esc_pos = esc_pos - 1
                        if(escape_count % 2 == 0): inside_quotes = False;
                        else: inside_quotes = True;



                        # logging.debug("no")
                        # inside_quotes = True
                        # if(source_to_balance[pos-2] == "\\"):
                        #     logging.debug("yes")
                        #     inside_quotes = False
                        #     if(source_to_balance[pos-3] == "\\"):
                        #         logging.debug("no2")
                        #         inside_quotes = True
   
                pos = pos + 1
            end_quote_pos = pos - 1
            logging.debug("--Skipping elements inside of quotes:_________________\n%s\n_________________", source_to_balance[start_quote_pos : end_quote_pos])
            amount_removed = end_quote_pos - start_quote_pos
            logging.debug("Amount removed: %d", amount_removed)
            #pos = pos - amount_removed + 1
            #header_pos = header_pos - amount_removed 
            source_to_balance = source_to_balance[:start_quote_pos] + source_to_balance[end_quote_pos:]
            count = count + 2 
            pos = pos + 1
            logging.debug("Source after removal:\n________\n%s\n__________", source_to_balance[header_pos : header_pos+len(header) + count])
            ending_len = len(source_to_balance)
            logging.debug("starting len: %d\nending len: %d", starting_len, ending_len)
        if not moved_index: count = count + 1
        #logging.debug("Count:", count)
        #logging.debug("len(source_to_balance):", len(source_to_balance))
        if(count > len(source_to_balance)): return "NO";
    logging.debug("Balanced source:\n____________________\n%s\n____________________", source_to_balance[header_pos:header_pos+len(header)+1 + count])
    #logging.debug("balanced:\n", cleaned_source[header_pos:header_pos+len(header)+1 + count])
    #header_pos = cleaned_source.find(header)
    body_source = source_to_balance[header_pos:header_pos+len(header)+1 + count]
    logging.debug("Source code for header '%s':\n____________________\n%s\n____________________", header, body_source)
    return body_source

    #right now we have cleaned source, now we need to use a stack to get the code from header to end of method.

#gets constuctor headers and returns those headers
def getConstructorHeaders(source, classname):
    headers = []
    while(source.find("public " + classname) != -1):
        posOfConstructor = source.find("public " + classname)
        posOfNewLine = source.find("\n", posOfConstructor)
        #logging.debug(source[posOfConstructor:posOfNewLine - 1])
        headers.append(source[posOfConstructor:posOfNewLine - 1])
        source = source[posOfNewLine:]
    
    return headers




def parseSource(source_directory):
    try:
        f = open(source_directory, mode="r", encoding="utf-8")
        data = f.read()
        name_out_file.write(source_directory + "\n")

    except:
        logging.debug("Failed to read data")
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
        logging.debug("Error, couldn't parse javalang")
        return

    #logging.debug(methods)
    methodNames = []
    for method in methods:
        #logging.debug(methods[method])
        #data = {}
        #data['code'] = methods[method]
        methodNames.append(method)
        # json.dump(data, outFile)
        # outFile.write('\n')
        #logging.debug("Done")

    getJavaComments(methodNames, source_directory, methods)
    
startFromName = ''#'\\resources\outputCode\Java\HabitatGUIJava\src\sample\Main.java'
def parseCode(root):
    logging.critical("Beginning")
    extension = ''
    if(language == 'Java'):
        extension = JAVA_EXT
    elif(language == "C++"):
        extension = CPLUSPLUS_EXT
    elif(language == "Python"):
        extension = PYTHON_EXT
    else:
        logging.critical("Default language -- Testing")
        extension = JAVA_EXT
    if(startFromName == ''):
        logging.critical("Starting from scratch...")
        for path, subdirs, files in os.walk(root):
            for name in files:
                if(name[-len(extension):] == extension):
                    logging.critical(os.path.join(path, name))
                    parseSource(os.path.join(path, name))
    else:
        logging.critical("Resuming...")
        for path, subdirs, files in os.walk(root):
            for name in files:
                if(name[-len(extension):] == extension):
                    if(name != startFromName):
                        logging.error("Skipped %s",os.path.join(path, name))
                        continue
                    logging.critical(os.path.join(path, name))
                    parseSource(os.path.join(path, name))


if __name__ == '__main__':
    #filename = 'resources/outputCode/'
    #language = "TestLang"

    #filename = 'D:\\Projects\\gitscraper\\resources\\outputCode\\Java\\.emacs.d\\lib\\jdee-server\\src\\main\\java\\jde\\parser\\ParseException.java'
    #filename = 'D:\\Projects\\gitscraper\\resources\\outputCode\\Java\\.emacs.d\\lib\\jdee-server\\src\\main\\java\\jde\\parser\\TokenMgrError.java'
    
    filename = 'D:\\Projects\\gitscraper\\resources\\outputCode\\'
    language = "Java"
    #parseSource(filename)
    
    #parseSource(filename + language + "/3d-renderer/src/matrix/Matrix.java")
    #parseSource(filename + language + "/3d-renderer/src/matrix/MatrixException.java")
    #parseSource(filename + language + "/3d-renderer/src/render/Camera.java")
    #parseSource("D:\\Projects\\gitscraper\\resources\\outputCode\\Java\\.emacs.d\\lib\\jdee-server\\src\\main\\java\\jde\\parser\\ParseException.java")
    #parseSource("D:\\Projects\\gitscraper\\resources\\outputCode\\Java\\.emacs.d\\lib\\jdee-server\\src\\main\\java\\jde\\juci\\LispWriter.java")
    #test_file = open("D:\\Projects\\gitscraper\\resources\\outputCode\\Java\\02June2018\\src\\test\\java\\SeleniumGrid\\Grid_Practice_23March_2018.java")
    #logging.debug(remove_comments(test_file.read()))
    #logging.debug(remove_comments("/*hello*/\ncap.setBrowserName(\"chrome //this is cool\");"))
    #parseSource("D:\\Projects\\gitscraper\\resources\\outputCode\\Java\\02June2018\\src\\test\\java\\SeleniumGrid\\Grid_Practice_23March_2018.java")
    # test = open(filename + language + "/3d-renderer/src/matrix/Matrix.java").read()
    # logging.debug(test)
    # logging.debug(re.search("^(.+)\n\(", test))

    #parseSource("D:\\Projects\\gitscraper\\resources\\outputCode\\Java\\09-08-Projeto-Bicicleta\\src\\Bicicleta.java") #UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe1 in position 27: invalid continuation byte
    #parseSource("D:\\Projects\\gitscraper\\resources\\outputCode\\Java\\1.-Java-Basics-Homeworks\\3_Java_Loops_Methods_Classes\\lib\\joda-time-2.3\\src\\main\\java\\org\\joda\\time\convert\\StringConverter.java") 
    
    #parseSource("TestFile.java") 
    #code = open(filename).read();
    #extract_body_source(code, "protected String add_escapes(String str)")

    #logging.debug(code, "\n is balanced : ", is_balanced(code))
    #file = open("TestFile.java").read();
    #extract_body_source(file, "public void sup1(int x)")
    #extract_body_source(file, "public void sup2()")
    #print('''D:\\Projects\\gitscraper\\resources\\outputCode\\Java\\.emacs.d\\lib\\jdee-server\\src\\main\\java\\jde\\parser\\TokenMgrError.java'''); 
    parseCode(filename + language)