import scrape_usernames, file_utils, parse_repos
import sys, logging

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', stream=sys.stderr, level=logging.DEBUG)### CRITICAL ERROR WARNING INFO DEBUG NOTSET



if __name__=='__main__':
    username_filename = "ScrapedUsers\\List_of_usernames.txt"
    username_file = open(username_filename, "r", encoding="utf-8")
    file_utils.add_newline_if_missing(username_filename)
    request_instance = scrape_usernames.Requester_Instance()
    for line in username_file:
        
        line = line[:-1]
        if(request_instance.validateUser(line) == 1):
            logging.error("\"%s\": Validated!", line)
            parse_repos.scrapeRepos(line)
        else:
            logging.error("\"%s\": Invalidated!", line)

        