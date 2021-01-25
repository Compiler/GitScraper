SRC_DIR = src/
ENTRY_POINT = $(SRC_DIR)core.py

all: main


main:
	python3 $(ENTRY_POINT)


req:
	pip3 install requests
	pip3 install beautifulsoup4