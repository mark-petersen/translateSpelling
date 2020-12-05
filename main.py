'''
Convert standard spelling to American Spelling
usage: 
python convert_html.py input.html output.html
where input.html is the original in standard spelling,
and output.html is in reform spelling.  
Create input.html by saving a page from your web
browser.  View output.html by openning that file
from disk in your web browser.
In addition, this script must have access to the 
file DIAMBG, a dictionary of American (reform) 
spelling, in the run directory.
Mark Petersen
August 2016
'''

import numpy as np
import string as str
import sys
import pickle
import time

# if len(sys.argv)<3:
#     print "input and output files required"
#     sys.exit()
    
################################################
#
#  Read and parse dictionary
#
################################################



# Open file of entries for American (reform) spelling.
t0 = time.time()
dictFileName = 'DIAMBG'
f = open(dictFileName, 'r')
rawString = f.read()
f.close()

# Create a python dictionary relating each
# standard word and it's reform version
a = rawString.split()
standardToReform = {}
for i in range(int(len(a)/2)):
    standardToReform[a[2*i]] = a[2*i+1]

t1 = time.time()
print('dictionary read and create:',t1-t0)
pickle.dump( standardToReform, open( dictFileName+'.p', 'wb' ) )
t2 = time.time()
print('pickle dump:',t2-t1)
t1 = time.time()
dictPickle = pickle.load( open( dictFileName+'.p', 'rb' ) )
t2 = time.time()
print('pickle read:',t2-t1)

################################################
#
#  Read in text file to translate
#
################################################

# f = open(sys.argv[1], 'r')
# x = f.read()
# f.close()

x = 'one two three four I love you too, though through the thicken I may judge you'

################################################
#
#  Translate text
#
################################################

# x is input, y is output, just like in highschool algebra.
# Initialize y as an empty list.
y=[]
i=0
# Iterate over all characters in input string
while i< len(x):
    iBeg = i

    # Check for beginning of html declaration.
    # If found, take the declaration verbatim
    if x[i]=='<':
        while x[i]!='>':
            i+=1
        i+=1
        y.append( x[iBeg:i] )

    # Check for beginning of a word.  Advance the
    # index until the whole word is found.
    elif x[i].isalpha():
        while x[i].isalpha():
            i+=1
            if i==len(x):
              break
        word = x[iBeg:i].lower()

        # Translate word to reform spelling.
        try:
            reformWord = standardToReform[word]
 
            # Keep upper case the same as the original
            if x[iBeg:i].istitle():
                y.append( reformWord.title() )
            elif x[iBeg:i].isupper():
                y.append( reformWord.upper() )
            else:
                y.append( reformWord )

        # If word is not found in the dictionary, take it
        # verbatim.
        except:
            y.append( x[iBeg:i] )

    # If the character is not a letter, take it directly.
    else:
        y.append( x[i] )
        i+=1

################################################
#
#  Save translated text as new file
#
################################################
print(x)
print(''.join(y))

# f = open(sys.argv[2], 'w')
# f.write(''.join(y))
# f.close()