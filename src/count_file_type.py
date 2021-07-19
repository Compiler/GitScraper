import os, re


if __name__ == '__main__':
    root = "D:\\Projects\\gitscraper\\resources\\outputCode\\Java"
    extension = ".java"
    count = 0
    for path, subdirs, files in os.walk(root):
                for name in files:
                    if(name[-len(extension):] == extension):
                        count = count + 1
                        print(name)

    print("There are",count,"",extension, "files")
