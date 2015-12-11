# Import the os module, for the os.walk function
import os, sys

for rootDir in sys.argv[1:]:
    for dirName, subdirList, fileList in os.walk(rootDir):
        print('%s\t%d\t%d' % (dirName, len(subdirList), len(fileList)))
