import parse_comments, file_utils
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
            filename = os.path.join(path, name)
            logging.critical("File used: '%s'", filename)
            return [1, filename]
    return [0, -1]

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
    sampled_file_paths = []
    for path, subdirs, files in os.walk(root):
        if(index < count and files_read < count):
            if(walk_count < selections[index]):
                walk_count = walk_count + 1;
                continue;
            [bit, accepted_file_name] = parse_files(path,files,extension)
            if(bit == 1):
                sampled_file_paths.append(accepted_file_name)
            files_read = files_read + bit
            index = index + bit
        else: break;

    return sampled_file_paths


if __name__ == '__main__':
    sample_path = "C:\\Users\\Work\\Documents\\GitScraper\\code.json"
    sample_count = 1000
    sample_runs = 50
    sample_returns = []
    sample_sum = 0
    for i in range(0, 50):
        file_utils.clear_file(sample_path);
        for sample in grab_random_samples(code_dir, sample_count):
            parse_comments.parseSource(sample)
        sample_line_count = file_utils.get_line_count(sample_path)
        sample_sum = sample_sum + sample_line_count
        logging.critical("%d samples produced %d code:comment relations.", sample_count, sample_line_count)
        file_utils.clear_file(sample_path);
    logging.critical("================================\nSample sum: %d\nSample runs: %d\nSample average: %d\n======================", sample_sum, sample_runs, sample_sum / sample_runs)
    
