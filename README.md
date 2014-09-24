# Convert Novels to Images

*Silly script(s) to convert text to images*

These two scripts can encrypt and decrypt a text (generally a novel) into a PNG and back into a text file. The first 
script encrypts the book by using groups of three character's unicode values for RGB pixel colors. Then the second script 
reads the resulting PNG pixel by pixel and decodes those into unicode characters and writing them to a file. The UNIX diff 
of the source text and the decrypted image text is clean.

Sample input (Little Women from [Project Gutenberg](http://www.gutenberg.org/)) and sample image and text output are in 
the files subdirectory.
