import json


def parse(filename, outputFilename, shouldKeepComments):
    f = open(filename)
    data = json.load(f)
    fw = open(outputFilename, "a", encoding='utf-8')
    for code in data:
        if(shouldKeepComments == 0):
            fw.write(code['code'])
        else:
            fw.write('/*\n'+code['nl'] + '\n*/\n' + code['code'])
if __name__ == "__main__":
    parse('resources//example.json', 'resources//traintextcomments', 1)
    #parse('resources//train.json', 'resources//traintext', 0)