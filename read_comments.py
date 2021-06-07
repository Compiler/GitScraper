import json

code_dir = "code.json"
code_file = open("code.json")
instances = code_file.readlines()
#each instance is a json object that contains a method source code and a comment with it
#Example:
# print("Code:", json_rep['code']['body'])
# print("Comment:", json_rep['code']['comment'])
for instance in instances:
    json_rep = json.loads(instance)