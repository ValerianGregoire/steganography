import numpy as np
import sys
from PIL import Image

"""
Valérian Grégoire--Bégranger - 2024

Steganography reading tool.
"""

def printDoc():
    """Displays the documentation of the script and exits"""

    print("""[steganographyRead.py]
Reads hidden text from an image.

Flags:
    -h: Displays this message and exits.
    -nored: The R channel in RGB will remain untouched.
    -nogreen: The G channel in RGB will remain untouched.
    -noblue: The B channel in RGB will remain untouched.
    -l: The number of characters to read from the image.
    -n: The number of LSB the message are written on.

Example:
    python ./read.py <imagePath.jpg> <outputPath.png> | -flags
""")
    exit(0)

def toAlnum(message):
    """Converts a binary string to ASCII compliant text."""

    # Output alphabetical string
    output = ''

    # Split the message in bytes to convert each char later on
    bytes = [[]]
    while len(message):
        if not (len(bytes[-1]) < 8):
            bytes.append([])
        bytes[-1].append(message[0])
        message = message[1:]

    # Convert each byte to ASCII code
    for byte_ in bytes:
        output += chr(int(''.join(byte_), 2))
    
    return ''.join(char if ord(char) < 128 else ' ' for char in output)

def getImage(filePath):
    """Imports and converts an image file to a numpy array."""

    # Get the image object
    try: 
        img  = Image.open(filePath) 
    except IOError:
        print("The image could not be opened. Exiting...")
        exit(1)

    # Grayscale detection
    gray = False
    if img.mode == "L":
        print("The image was detected as grayscale.")
        gray = True
    
    # Convert the image to a numpy array for further computations
    img = np.array(img)

    return img, gray

def readMessage(image, nchars, lsb = 1,
                nored = False, nogreen = False, noblue = False):
    """Reads the least significant bits of pixels from an image"""

    # Get array dimensions to differentiate between RGB and grayscale
    try:
        height, width, depth = image.shape
        gray = False
    except ValueError:
        height, width = image.shape
        depth = 0
        gray = True

    # Function output
    message = []

    # Channels to read from
    channels = []
    if not nored:
        channels.append(0)
    if not nogreen:
        channels.append(1)
    if not noblue:
        channels.append(2)

    # Reading loop
    for i in range(height):
        for j in range(width):
            # Grayscale computations
            if gray:
                data = "{:08}".format(int(bin(image[i,j])[2:]))[-lsb:]
                for dat in data:
                    message.append(dat)
                if nchars and len(message) >= nchars * 8:
                    return "".join(message)
            
            # RGB computations
            else:
                for ch in channels:
                    data = "{:08}".format(int(bin(image[i,j,ch])[2:]))[-lsb:]
                    for dat in data:
                        message.append(dat)
                    if nchars and len(message) >= nchars * 8:
                        return "".join(message)
    
    return "".join(message)

def saveMessage(message, file):
    """Opens a file to write a message in it."""
    open(file,'w').write(message)

if __name__ == "__main__":
    print("")

    # Get arguments
    args = sys.argv[1:]
    
    # Flags
    gray, nored, nogreen, noblue = False, False, False, False
    nchars, lsb = 0, 1

    # Show the documentation if needed
    if "-h" in args or not len(args):
        printDoc()

    # Update flags
    if len(args) > 1:
        if "-nored" in args:
            nored = True
        if "-nogreen" in args:
            nogreen = True
        if "-noblue" in args:
            noblue = True
        if "-l" in args:
            try:
                nchars = int(args[args.index("-l") + 1])
                print(f"The first {nchars} characters will be processed.")
            except IndexError or TypeError:
                print("The -l flag needs to be followed by an integer value.\n")
                exit(1)
        else:
            print("Treating every character from the image.")
        
        if "-n" in args:
            try:
                lsb = int(args[args.index("-n") + 1])
            except IndexError or TypeError:
                print("The -n flag needs to be followed by an integer value.\n")
                exit(1)

            if lsb < 1 or lsb > 8:
                print("The amount of least significant bytes to read must be between 1 and 8.")
                exit(1)

    # Get image
    inputFormats = (".png", ".tiff", ".bmp")
    outputFormats = (".txt", ".msg", ".doc")
    inputFile = args[0]
    outputFile = args[1]

    if not (inputFile[-4:] in inputFormats):
        print("The format of the input file is not supported.")
        print("Please use .jpg, .png, .jpeg, .tiff, .bmp files as input.")
        exit(1)

    if not (outputFile[-4:] in outputFormats):
        print("The format of the output file is not supported.")
        print("Please use .txt, .msg, .doc files as output.")
        exit(1)
    
    # Get image
    img, gray = getImage(inputFile)

    # User information
    print(f"The message will be read using the{f' {lsb}' if lsb > 1 else ''} least significant bit{'s' if lsb > 1 else ''} of each pixel.")
    if not gray:
        print(f"The message will be read using the {'' if nored else 'R'}{'' if nogreen else 'G'}{'' if noblue else 'B'} color channels of each pixel.")

    # Read data
    bitsMessage = readMessage(img, nchars, lsb = lsb,
                              nored=nored, nogreen=nogreen, noblue=noblue)

    # Convert data to strings
    message = toAlnum(bitsMessage)

    # Save the obtained message to a text file
    saveMessage(message, outputFile)
    print(f"The obtained message was saved to {outputFile}.")

    # Display the obtained message
    print(f"\nObtained message:\n{message}")

