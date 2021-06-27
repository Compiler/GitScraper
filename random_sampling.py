import parse_comments
import sys,os,string,logging
from random import seed
from random import randint

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', stream=sys.stderr, level=logging.CRITICAL)### CRITICAL ERROR WARNING INFO DEBUG NOTSET


language = 'Java'
code_dir = "D:\\Projects\\gitscraper\\resources\\outputCode\\"+language+"\\"

def get_subdir_count(root):
    return len(next(os.walk(root))[1])

def parse_files(path, files, extension):
    for name in files:
        if(name[-len(extension):] == extension):
            logging.critical("File used: '%s'", os.path.join(path, name))
            return 1
    return 0

def grab_random_samples(root, count):
    selections = []
    subdir_count = (int)((get_subdir_count(root) - 1)) * 1
    if(subdir_count < count): logging.critical("Dataset too small for sample count"); return;
    logging.critical("Subdirectory count: %d", subdir_count)
    for _ in range(count):
        selections.append(randint(0, subdir_count))
    selections.sort()
    logging.critical(selections)
    logging.critical(selections[0])
    extension = parse_comments.getExtension()
    logging.critical("Extension used: .%s", extension)
    walk_count = 0
    files_read = 0
    extension = parse_comments.getExtension()
    index = 0
    for path, subdirs, files in os.walk(root):
        if(index < count and files_read < count):
            if(walk_count < selections[index]):
                walk_count = walk_count + 1;
                continue;
            bit = parse_files(path,files,extension)
            files_read = files_read + bit
            index = index + bit
        else: break;


grab_random_samples(code_dir, 1000);