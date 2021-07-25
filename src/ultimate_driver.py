import scrape_usernames, file_utils, parse_repos
import sys, logging
import time

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
 stream=sys.stderr, level=logging.CRITICAL)### CRITICAL ERROR WARNING INFO DEBUG NOTSET



if __name__=='__main__':
    username_filename = "D:\\Projects\\gitscraper\\ScrapedUsers\\name_combinations.txt"
    valid_user_output = "D:\\Projects\\gitscraper\\ScrapedUsers\\valid_name_combinations.txt"
    valid_users = open(valid_user_output, "w", encoding="utf-8")
    username_file = open(username_filename, "r", encoding="utf-8")

    #file_utils.add_newline_if_missing_big(username_filename)
    print("Preprocess done")
    request_instance = scrape_usernames.Requester_Instance()



    last_line = "Aamirgraphic"
    resume = False
    for line in username_file:
        if(not resume):
            if(line != last_line+"\n"): logging.critical("Skipped: '%s'", line); continue;
            else: resume = True;

        line = line[:-1]
        if(request_instance.validateUser(line) == 1):
            logging.critical("\"%s\": Validated!", line)
            valid_users.write(line+"\n")
            parse_repos.scrapeRepos(line)
        else:
            pass#logging.critical("\"%s\": Invalidated!", line)

        