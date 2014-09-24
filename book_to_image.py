#!/usr/bin/env python
"""Convert novels/text to images...somehow"""

import codecs
import gd
import sys


# Initial dimensions of temp image
DIMENSIONS = (500, 5000)


def increment_coords(coords):
   """Increment the current pixel coordinates wrapping at the width of DIMENSIONS"""

   coords[0] += 1

   if coords[0] >= DIMENSIONS[0]:
      coords[0] = 0
      coords[1] += 1

   return coords


def load_text():
   """Load some text from somewhere for use in processing"""

   # Read file in as UTF-8
   f = codecs.open('files/little_women.txt', 'r', encoding='utf-8')
   text = f.read()
   f.close()

   return text


def set_pixels_by_text(image):
   """Run through text and generate an image from it"""

   i = 0
   coords = [0, 0]
   rgb = [0, 0, 0]

   # Get text from somewhere
   text = load_text()

   for c in text:

      # Every third character write out as a pixel where
      # RGB colors are the three previous character's
      # unicode values
      if i % 3 == 0 and i > 0:
         color = image.colorAllocate(tuple(rgb))
         image.setPixel(tuple(coords), color)

         coords = increment_coords(coords)

      rgb[i % 3] = ord(c)

      i += 1

   # Check to see if we stopped "mid-pixel"
   i -= 1
   if i % 3 != 0:
      for j in range(1, (i % 3) + 1):
         rgb[j * -1] = 167

      color = image.colorAllocate(tuple(rgb))
      image.setPixel(tuple(coords), color)


   return coords


def main():
   """Initial entry point"""

   # Build the temp images and fill with stop color
   image = gd.image(DIMENSIONS, True)
   filler = image.colorAllocate((167, 167, 167))
   image.fill((0, 0), filler)

   # Write pixels to image based on input text
   coords = set_pixels_by_text(image)

   # Copy the temp image to a smaller image of the appropriate height
   smaller = gd.image((DIMENSIONS[0], coords[1] + 1), True)
   image.copyTo(smaller, (0, 0), (0, 0), (DIMENSIONS[0], coords[1] + 1))
   smaller.writePng('files/book.png')


if __name__ == '__main__':
   sys.exit(main())
