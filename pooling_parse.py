import parse_comments, logging, sys, multiprocessing, os


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', stream=sys.stderr, level=logging.ERROR)### CRITICAL ERROR WARNING INFO DEBUG NOTSET

def get_names(root, names):
    logging.critical("Beginning")
    extension = parse_comments.getExtension()

    resume_name = check_resume_status();
    if(resume_name == ''):
        for path, subdirs, files in os.walk(root):
            for name in files:
                if(name[-len(extension):] == extension):
                    logging.critical(os.path.join(path, name))
                    names.append(os.path.join(path,name))
                    continue
    else:
        found_name = False;
        for path, subdirs, files in os.walk(root):
            for name in files:
                if(found_name == False and name != resume_name): continue;
                else:
                    found_name = True;
                    if(name[-len(extension):] == extension):
                        logging.critical(os.path.join(path, name))
                        names.append(os.path.join(path,name))
                        continue
            # else:
            #     logging.error("Skipped %s",os.path.join(path, name))
                #parseSource(os.path.join(path, name))


def parse_from_path(path):
    parse_comments.parseSource(path)

def check_resume_status():
    startFromName = ''
    with open('D:\\Projects\\gitscraper\\resources\\ResultingJSON\\' + "Java" + '\\comment_code_data_names.txt', 'rb') as f:
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        startFromName = f.readline().decode()
        startFromName = ' '.join(startFromName.split());
    return startFromName

main_root = "D:\\Projects\\gitscraper\\resources\\outputCode\\Java\\"
if __name__ == '__main__':
    sub_root_1 = "1403_DB_Basic"
    sub_root_2 = "15619"

    manager = multiprocessing.Manager()
    names = manager.list()
    p1 = multiprocessing.Process(target=get_names, args=(main_root + sub_root_1, names))
    p2 = multiprocessing.Process(target=get_names, args=(main_root + sub_root_2, names))
  
    p1.start()
    p2.start()
  
    p1.join()
    p2.join()
    logging.error("Checking names")
    print(names)
  
    # both processes finished
    logging.critical("Done!")