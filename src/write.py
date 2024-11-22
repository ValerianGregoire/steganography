import numpy as np
import sys
from PIL import Image

"""
Valérian Grégoire--Bégranger - 2024

Steganography writing tool.
"""

def printDoc():
    """Displays the documentation of the script and exits"""

    print("""[steganographyWrite.py]
Hides text in an image.

Flags:
    -h: Displays this message and exits.
    -gray: Converts the image to grayscale.
    -nored: The R channel in RGB will remain untouched.
    -nogreen: The G channel in RGB will remain untouched.
    -noblue: The B channel in RGB will remain untouched.
    -n: The number of LSB the message will be written on.
    -fromfile: Uses text from a file.

Example:
    python ./write.py <imagePath.png> <outputPath.png> | -flags
""")
    exit(0)

def getMessage(limit):
    """Gets a message to write from the user."""

    # Loops until the user provides a correct message to write
    while True:
        choice = input(f"Write a message to hide in the image ({limit} characters max): ").lstrip().rstrip()
        
        # Make sure every character can be written in 8 bits
        if any(not c.isascii() for c in choice):
            print("Please enter a message without special characters.\n")
            continue
        
        # Make sure the message fits in the image
        if len(choice) > limit or not len(choice):
            print("Please enter a message of correct length.\n")
            continue
        
        print("")
        return choice

def toBinary(message):
    """Converts ASCII compliant text to a binary string."""
    return "".join( ["{:08d}".format( int(bin(ord(chr))[2:]) ) for chr in message] )

def getImage(filePath, gray = False):
    """Imports and converts an image file to a numpy array."""

    # Get the image object
    try: 
        img  = Image.open(filePath) 
    except IOError:
        print("The image could not be opened. Exiting...")
        exit(1)

    # Convert the image to grayscale
    if gray:
        img = img.convert("L")

    # Convert the image to a numpy array for further computations
    img = np.array(img)

    # Get the number of pixels in the image
    px = img.size

    return img, px

def setLSB(x, y, n):
    """Replaces the n least significant bits of x by the binary value of y."""

    # Make sure the output value will not exceed the max bits of the pixel
    if y < 0 or y >= 2**n:
        print(f"A wrong value was passed to function writeBin ({y}).")
        exit(1)

    # Get the two halves of the output value
    x_bin = bin(x)[2:-n]
    y_bin = ("{:0" + str(n) + "d}").format(int(bin(y)[2:]))
    
    # Merge the two results and convert them to base 10
    result = int(x_bin + y_bin, 2)

    return result

def writeMessage(image, message, lsb = 1,
                nored = False, nogreen = False, noblue = False):
    """Writes text to an image as a combination of least significant bits."""
    
    # Get array dimensions to differentiate between RGB and grayscale
    try:
        height, width, depth = image.shape
        gray = False
    except ValueError:
        height, width = image.shape
        depth = 0
        gray = True

    # Function output
    imgOut = np.copy(image)

    # Channels to write to
    channels = []
    if not nored:
        channels.append(0)
    if not nogreen:
        channels.append(1)
    if not noblue:
        channels.append(2)

    # Writing loop
    row, col = 0, 0
    while row < height:
        col = 0
        while col < width:
            # Grayscale computations
            if gray:
                if len(message):
                    imgOut[row,col] = setLSB(imgOut[row,col], int(message[:lsb], 2), lsb)
                    message = message[lsb:]
                    col += 1
                    continue
                break
            
            # RGB computations
            else:
                for ch in channels:
                    if len(message):
                        imgOut[row,col,ch] = setLSB(imgOut[row,col,ch], int(message[:lsb], 2), lsb)
                        message = message[lsb:]
                        continue
                    break
            col += 1
        row += 1
    
    if len(message):
        print(f"The message does not fit into the image.")
        print(f"{int(np.floor(len(message)/8))} characters are missing.")
    else:
        print("The characters were successfully written to the image.")

    return imgOut

def saveImg(image, title = "./output.png", gray = False):
    """Saves a numpy array to a .png file."""

    # Make a PIL image from the numpy array
    img = Image.fromarray(image)

    # Makes sure grayscale images are saved as such
    if gray:
        img = img.convert("L")

    # Saving the image
    img.save(title)
    print(f"The result is saved as {title}.")

if __name__ == "__main__":
    print("")

    # Get arguments
    args = sys.argv[1:]
    
    # Show the documentation if needed
    if "-h" in args or not len(args):
        printDoc()
    
    # Flags
    gray, nored, nogreen, noblue, fromfile = False, False, False, False, False
    lsb = 1

    # Update flags
    if len(args) > 1:
        if "-gray" in args:
            gray = True
        if "-nored" in args:
            nored = True
        if "-nogreen" in args:
            nogreen = True
        if "-noblue" in args:
            noblue = True
        if "-fromfile" in args:
            try:
                message = open(args[args.index("-fromfile") + 1],'r').read()
                fromfile = True
            except FileNotFoundError:
                print("The -fromfile flag needs to be followed by a valid text file path.\n")
                exit(1)
        if "-n" in args:
            try:
                lsb = int(args[args.index("-n") + 1])
            except IndexError or TypeError:
                print("The -n flag needs to be followed by an integer value.\n")
                exit(1)

            if lsb < 1 or lsb > 8:
                print("The amount of least significant bytes to write on must be between 1 and 8.")
                exit(1)
    
    # User information
    print(f"The message will be written using the{f' {lsb}' if lsb > 1 else ''} least significant bit{'s' if lsb > 1 else ''} of each pixel.")
    if not gray:
        print(f"The message will be encrypted using the {'' if nored else 'R'}{'' if nogreen else 'G'}{'' if noblue else 'B'} color channels of each pixel.")

    # Get the input/output files
    inputFormats = (".jpg", ".png", ".jpeg", ".tiff", ".bmp")
    outputFormats = (".png", ".tiff", ".bmp")
    inputFile = args[0]
    outputFile = args[1]

    if not len([x for x in inputFormats if x in inputFile]):
        print("The format of the input file is not supported.")
        print("Please use .jpg, .png, .jpeg, .tiff, .bmp files as input.")
        exit(1)

    if not len([x for x in outputFormats if x in outputFile]):
        print("The format of the output file is not supported.")
        print("Please use .png, .tiff, .bmp files as output.")
        exit(1)

    # Get image
    img, px = getImage(inputFile, gray)
    
    # Get total writable characters count
    multiplier = (3 - (int(nored) + int(nogreen) + int(noblue)))**int(1-gray)
    bits = px*multiplier
    nchars = int(np.floor(bits*lsb/8))
    
    # Get the user message
    if fromfile:
        print("The message to write is read from an external text file.")
        if len(message) > nchars:
            message = message[:nchars] # Crop to max length
    else:
        message = getMessage(nchars)
    binMessage = toBinary(message)

    # Write the message to a new image
    imgOut = writeMessage(img, binMessage, lsb,
                         nored = nored, nogreen = nogreen, noblue = noblue)
    
    # Compute the distance between the two images
    dist = np.linalg.norm(imgOut - img)
    print(f"The distance between the two images is {dist:.2f}.")

    # Save the result
    print("All computations were performed successfully.")
    saveImg(imgOut, outputFile, gray)
