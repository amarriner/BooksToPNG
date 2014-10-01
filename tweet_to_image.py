#!/usr/bin/env python
"""Convert text to images...somehow"""

from twython import Twython, TwythonStreamer
from StringIO import StringIO

import codecs
import json
import keys
import gd
import random
import sys
import time


class TweetToImage(TwythonStreamer):

   # Size of each "pixel"
   PIXEL = 25

   # Initial dimensions of temp image
   DIMENSIONS = (7 * PIXEL, 7 * PIXEL)

   coords = None
   image = None
   image_io = None
   text = ''
   twitter = None
   twitter_user_id = None


   def build_image(self):
      """Builds an image from some text"""

      self.coords = [0, 0]
      self.image = gd.image(self.DIMENSIONS, True)

      # Build the temp images and fill with stop color
      filler = self.image.colorAllocate((0, 0, 0))
      self.image.fill((0, 0), filler)

      self.set_pixels_by_text()
      self.save_image()


   def increment_coords(self):
      """Increment the current pixel coordinates wrapping at the width of DIMENSIONS"""

      self.coords[0] += (1 * self.PIXEL)

      if self.coords[0] >= self.DIMENSIONS[0]:
         self.coords[0] = 0
         self.coords[1] += (1 * self.PIXEL)


   def instantiate_twitter(self):
      """Set up twitter"""

      self.twitter = Twython(keys.consumer_key, keys.consumer_secret, keys.access_token, keys.access_token_secret)
      self.twitter_user_id = self.twitter.verify_credentials()['id']


   def is_followed_by(self, id):
      """Check if the given ID is following me"""

      f = self.twitter.get_followers_ids()
      if id in f['ids']:
         return True
      else:
         return False


   def load_text(self):
      """Load some text from somewhere for use in processing"""

      # Read file in as UTF-8
      f = codecs.open('sample_tweet.json', 'r', encoding='utf-8')
      self.text = json.loads(f.read())['text']
      f.close()


   def on_success(self, data):
      if 'text' in data and not data['in_reply_to_status_id']:

         found_me = False
         for mention in data['entities']['user_mentions']:
            if mention['id'] == self.twitter_user_id:
               found_me = True

         if found_me:

            self.tweet(data)


         elif random.choice(range(100)) < 10 and self.is_followed_by(data['user']['id']):

            self.tweet(data)


         else:

            print ' - Skipping tweet ' + data['text'].encode('utf-8')


      elif 'event' in data:

         if data['event'] == 'follow' and data['target']['screen_name'] == 'TweetToImage':
            print '--------------------------------------------------------------------------------'
            print data['source']['screen_name'] + ' followed me, following back...'

            time.sleep(2)

            self.twitter.create_friendship(screen_name=data['source']['screen_name'], follow=True)


   def on_error(self, status_code, data):
      print status_code


   def pad_text(self):
      """Pad text to 147 characters"""

      for i in range(147 - len(self.text)):
         self.text += ' '


   def save_image(self):
      """Save image out to disk"""

      self.image_io = StringIO()
      self.image.writePng(self.image_io)
      self.image_io.seek(0)


   def set_pixels_by_text(self):
      """Run through text and generate an image from it"""

      i = 0
      rgb = [0, 0, 0]

      # Get text from somewhere
      if not self.text:
         self.load_text()

      for c in self.text:

         # Every third character write out as a pixel where
         # RGB colors are the three previous character's
         # unicode values
         if i % 3 == 0 and i > 0:
            color = self.image.colorAllocate(tuple(rgb))

            self.image.filledRectangle(self.coords, (self.coords[0] + self.PIXEL, 
                                                     self.coords[1] + self.PIXEL), color)

            self.increment_coords()

         rgb[i % 3] = ord(c)

         i += 1


   def tweet(self, t):
      """Tweet"""

      time.sleep(2)

      print '--------------------------------------------------------------------------------'
      print 'Replying to @' + t['user']['screen_name']
      print t['text'].encode('utf-8')

      self.text = t['text'].encode('utf-8')
      self.build_image()

      try:
         self.image_io.seek(0)
         self.twitter.update_profile_image(image=self.image_io)
         self.image_io.seek(0)
      except:
         print '*** Error uploading new profile image!'


      self.twitter.update_status_with_media(status='@' + t['user']['screen_name'] + ' :)',
                                            in_reply_to_status_id=t['id_str'],
                                            media=self.image_io)


def main():
   """Initial entry point"""

   stream = TweetToImage(keys.consumer_key, keys.consumer_secret, keys.access_token, keys.access_token_secret)
   stream.instantiate_twitter()
   stream.user()


if __name__ == '__main__':
   sys.exit(main())
