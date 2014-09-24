#!/usr/bin/env python
"""Convert novels/text to images...somehow"""

import gd
import sys


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

   f = open('little_women.txt')
   text = f.read()
   f.close()

   return text


def set_pixels_by_text(image):
   """Run through text and generate an image from it"""

   i = 0
   coords = [0, 0]
   rgb = [0, 0, 0]

   text = load_text()

   for c in text:

      rgb[i % 3] = ord(c)

      if i % 3 == 0 and i > 0:
         color = image.colorAllocate(tuple(rgb))
         image.setPixel(tuple(coords), color)

         coords = increment_coords(coords)

      i += 1

   return coords


def main():
   """Initial entry point"""

   image = gd.image(DIMENSIONS, True)
   black = image.colorAllocate((  0,   0,   0))
   white = image.colorAllocate((255, 255, 255))
   image.fill((0, 0), white)

   coords = set_pixels_by_text(image)

   smaller = gd.image((DIMENSIONS[0], coords[1]), True)
   image.copyTo(smaller, (0, 0), (0, 0), (DIMENSIONS[0], coords[1]))
   smaller.writePng('/home/amarriner/public_html/book.png')


if __name__ == '__main__':
   sys.exit(main())
