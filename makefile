SRC_DIR = src/
ENTRY_POINT = $(SRC_DIR)core.py

all: main

main:
	python3 $(ENTRY_POINT)