import parse_comments, logging, sys, multiprocessing, os
from multiprocessing import Pool


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', stream=sys.stderr, level=logging.ERROR)### CRITICAL ERROR WARNING INFO DEBUG NOTSET

def get_names(root, names):
    logging.critical("Beginning")
    extension = parse_comments.getExtension()
    while(len(names) > 100): logging.critical("Waiting"); continue;

    resume_name = check_resume_status();
    #if(resume_name == ''):
    if(True):
        for path, subdirs, files in os.walk(root):
            for name in files:
                if(name[-len(extension):] == extension):
                    #logging.critical(os.path.join(path, name))
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


def parse_from_path(names):
    logging.critical("Attempting source ")
    if(len(names) < 1): return;
    logging.critical("Running source")

    path = names[0];
    names.remove(names[0]);
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

def run_pooled(names):
    while(len(names) > 1):
        logging.critical("Pooling")
        with Pool(10) as p:
            p.map(parse_from_path, [names])

main_root = "D:\\Projects\\gitscraper\\resources\\outputCode\\Java\\"
if __name__ == '__main__':
    sub_root_1 = "1403_DB_Basic"
    sub_root_2 = "15619"
    manager = multiprocessing.Manager()
    names = manager.list()

    p1 = multiprocessing.Process(target=get_names, args=(main_root + sub_root_1, names,))
    p1.start()

  
    p2 = multiprocessing.Process(target=run_pooled, args=(names, ))
    p2.start()
    logging.critical("p1 sent")


    p2.join();
    p1.join()
    logging.error("Checking names")
    print(names)
  
    # both processes finished
    logging.critical("Done!")