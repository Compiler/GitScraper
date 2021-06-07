import json



x = {
  "1": {"body" : "string hello;", "comment":"/*this is a string*/"},
  "2": {"body" : "string hello;", "comment":"/*this is a string*/"}
}
lines = []
count = 0
line1 = {"body" : "string hello;", "comment":"/*this is a string*/"}
line2 = {"body" : "string hello;", "comment":"/*this is a string*/"}
json_rep = {}
json_rep[str(count)] = line1; count = count + 1;
json.dump(json_rep, outFile)

outFile = open("test.json", "a")

# convert into JSON:
y = json.dumps(x)

# the result is a JSON string:
print(y)
data = json.loads("code.json")
f = open("code_read.txt")
f.write(data)