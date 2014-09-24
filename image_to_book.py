#!/usr/bin/env python
"""Script to decrypt book image into text"""

import codecs
import gd
import sys


def main():
   """Initial entry point"""

   # Read book image generated from book_to_image.py
   book = gd.image('files/book.png')

   # Open a file for writing
   f = codecs.open('files/book.txt', 'w', encoding='utf-8')

   # Step through each pixel in the image (left to right and top to bottom)
   # converting pixels into 3 utf-8 characters.
   # Unicode value 167 is the stop character
   for j in range(book.size()[1]):
      for i in range(book.size()[0]):
         rgb = book.colorComponents(book.getPixel((i, j)))

         for k in range(3):
            if rgb[k] != 167:
               f.write(unichr(rgb[k]))


   # Need a newline at the end of the file
   f.write('\n')
   f.close()


if __name__ == '__main__':
   sys.exit(main())
