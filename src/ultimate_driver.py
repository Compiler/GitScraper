import scrape_usernames, file_utils, parse_repos
import sys, logging
import time

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', stream=sys.stderr, level=logging.DEBUG)### CRITICAL ERROR WARNING INFO DEBUG NOTSET



if __name__=='__main__':
    username_filename = "D:\\Projects\\gitscraper\\ScrapedUsers\\name_combinations.txt"
    username_file = open(username_filename, "r", encoding="utf-8")

    file_utils.add_newline_if_missing_big(username_filename)
    print("Preprocess done")
    request_instance = scrape_usernames.Requester_Instance()
    for line in username_file:
        
        line = line[:-1]
        if(request_instance.validateUser(line) == 1):
            logging.error("\"%s\": Validated!", line)
            parse_repos.scrapeRepos(line)
        else:
            logging.error("\"%s\": Invalidated!", line)

        