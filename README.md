# BooksToPNG

*Silly script(s) to convert novels to images and back again*

These two scripts can encrypt and decrypt a text (generally a novel) into a PNG and back into a text file. The first 
script encrypts the book by using groups of three character's unicode values for RGB pixel colors. The second script can
then read the resulting PNG pixel by pixel and decode those into unicode characters and write them to a file. The UNIX diff 
of the source text and the decrypted image text should be clean.

Sample input (Little Women from [Project Gutenberg](http://www.gutenberg.org/)) and sample image and text output are in 
the files subdirectory.

The script tweet_to_image.py is a streaming twitter client that will tweet encoded images at twitter users if they either
@ mention the bot or if they follow the bot, a 1/10 chance will reply to their tweet with an encoded image.
