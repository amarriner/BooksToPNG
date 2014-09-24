# BooksToPNG

*Silly script(s) to convert novels to images and back again*

These two scripts can encrypt and decrypt a text (generally a novel) into a PNG and back into a text file. The first 
script encrypts the book by using groups of three character's unicode values for RGB pixel colors. The second script can
then read the resulting PNG pixel by pixel and decode those into unicode characters and write them to a file. The UNIX diff 
of the source text and the decrypted image text should be clean.

Sample input (Little Women from [Project Gutenberg](http://www.gutenberg.org/)) and sample image and text output are in 
the files subdirectory.
