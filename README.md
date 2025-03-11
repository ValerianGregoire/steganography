# steganography
Integration of a steganography algorithm with command lines and a tkinter GUI in python.

# Motivations
Steganography is the practice of concealing information within digital images in a way that is imperceptible to the human eye. Unlike cryptography, which scrambles data to make it unreadable, steganography hides the existence of the data itself by embedding it into the pixel values of an image, often by manipulating the least significant bits (LSBs) of the color channels. This allows the carrier image to look unchanged while secretly containing hidden information.

Developing a Python program for image steganography is particularly interesting because it combines multiple technical concepts:

- Image processing: Working with libraries like Pillow, OpenCV, or NumPy lets you manipulate pixel data directly, offering hands-on experience in how images are represented digitally (using RGB channels, bitwise operations, etc.).

- Bitwise operations: Steganography often involves modifying the LSBs of pixel values — a perfect way to deepen your understanding of how data is stored and processed at the binary level.

- Algorithm design: Crafting efficient embedding and extraction algorithms tests your problem-solving skills — ensuring the hidden data is not only secure but also retrievable without corrupting the host image.

# Theory
## Writing process
- The user provides two inputs:
    - A message they want to hide (a string of text).
    - An image that will act as the carrier (typically a PNG or BMP to avoid compression artifacts).
- The message is converted to binary:
    - Each character of the message is converted into its binary ASCII representation.
    - Example:
        - "A" → 65 in ASCII → 01000001 in binary.
- Prepare the image:
    - The image is read pixel by pixel, and each pixel’s RGB values (usually 8 bits each) are extracted.
- Embed the binary message:
    - The least significant bit(s) (LSB) of each color channel (R, G, B) is replaced by one bit of the message.
- All bits that make up the message are written this way.

## Reading process
The reading process is the same as the writing process in a reversed manner.

# Results
This project lead to the creation of a simple steganography software to [read](./src/read.py) and [write](./src/write.py) files with hidden messages. The software may be used through command lines. A [Makefile](./src/Makefile) was written to assist the user in writing correct commands. Additionnally, an [app](./src/app.py) was created to further simplify the steganography process for the user.

## App interface
The app GUI is the following

### Write tab
![WriteTab](./Documents/images/write_tab.png?raw=true "WriteTab")

This tab allows the user to hide a message in an image. The image is then written to the user's Desktop. The user can choose which color channels to use (RGB), or to output a greyscale image. The number of LSB to write on can also be chosen to hide more data in less space, at the expanse of further image quality degradation. It is recommended to write on the last or last two bytes of each pixel at most to keep sufficient image quality.

### Read tab
![ReadTab](./Documents/images/read_tab.png?raw=true "ReadTab")

This tab allows the user to retrieve a hidden message from an image. The user can choose which color channels to use (RGB) for reading. Greyscale images are automatically recognized, and do not require any tuning apart from the choice of LSB to read the message on.

## Example
### Writer call
After calling the [write](./src/write.py) program either through the [app](./src/app.py) program, or the [Makefile](./src/Makefile), a confirmation that the writing process was completed.
![WriteOutput](./Documents/images/write_output.png?raw=true "WriteOutput")

### Output comparison
The original image is the following :
![Neptune](./Documents/images/neptune.jpg?raw=true "Neptune")

The image with a hidden message is :
![NeptuneHidden](./Documents/images/neptune_hidden.png?raw=true "NeptuneHidden")

As one can observe, no difference can be seen by the human eye.

### Reader call
When passed to the [reader](./src/read.py), we obtain the following output :
![ReadOutput](./Documents/images/read_output.png?raw=true "ReadOutput")

The retrieved message is the one that was written using the [writing](./src/write.py) tool.

# Conclusion
This project successfully demonstrated the implementation of an image steganography algorithm using Python, integrating both command-line functionality and a user-friendly GUI with Tkinter. By embedding hidden messages within the least significant bits (LSBs) of pixel values, the project illustrated the core principles of steganography — concealing data in a way that is visually imperceptible.

The results were conclusive, as the software effectively encoded and decoded messages without altering the apparent quality of the carrier images. The flexibility provided by allowing users to choose the number of LSBs and color channels for both writing and reading further enhances the program's utility. The side-by-side comparison of the original and encoded images confirmed that the modifications remained undetectable to the human eye.

Beyond the practical implementation, the project serves as a solid foundation for understanding control theory concepts like bitwise operations, binary data handling, and algorithm design. The detailed explanation of each step, from binary conversion to pixel manipulation, ensures that future engineers can build upon this work, fostering deeper exploration into digital image processing and secure data embedding.
