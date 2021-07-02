import parse_comments, logging, sys, multiprocessing


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', stream=sys.stderr, level=logging.ERROR)### CRITICAL ERROR WARNING INFO DEBUG NOTSET


def get_names(root):
    logging.critical("Beginning")
    extension = parse_comments.getExtension()

    found_name = False;
    for path, subdirs, files in os.walk(root):
        for name in files:
            if(name[-len(extension):] == extension):
                logging.error("Skipped %s",os.path.join(path, name))
                continue
            else:
                found_name = True
                logging.critical(os.path.join(path, name))
                #parseSource(os.path.join(path, name))

main_root = "D:\\Projects\\gitscraper\\resources\\outputCode\\Java"
if __name__ == '__main__':
    p1 = multiprocessing.Process(target=get_names, args=(10, ))
    p2 = multiprocessing.Process(target=get_names, args=(10, ))
  
    p1.start()
    p2.start()
  
    p1.join()
    p2.join()
  
    # both processes finished
    logging.critical("Done!")