# Quick testing of the writing/reading of images

# Interpreter
PYTHON = python

# Program
WRITE_PROGRAM = ./write.py
READ_PROGRAM = ./read.py

# Flags (-h <-n value> -gray -nored -nogreen -noblue)
WRITE_FLAGS = -n 1

# Flags (-h <-n value> <-l value> -nored -nogreen -noblue)
READ_FLAGS= -n 1 -l 100


# Target data
WRITE_INPUT_FILE = ./neptune.jpg
WRITE_OUTPUT_FILE = ./encryptedFile.png
READ_INPUT_FILE = ./encryptedFile.png
READ_OUTPUT_FILE = ./readText.txt

all: run

run:
	$(PYTHON) $(WRITE_PROGRAM) $(WRITE_INPUT_FILE) $(WRITE_OUTPUT_FILE) $(WRITE_FLAGS) 
	$(PYTHON) $(READ_PROGRAM)  $(READ_INPUT_FILE)  $(READ_OUTPUT_FILE)  $(READ_FLAGS) 

clean:
	rm $(WRITE_OUTPUT_FILE) $(READ_OUTPUT_FILE)