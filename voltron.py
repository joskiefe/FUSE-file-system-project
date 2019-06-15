==========================Generic Fuse File System=========================
# Author: John Hutchins
# Team Voltron
#
# This is an outline of our basic FUSE file system.  The program currently takes 2 command line arguments
# and stores these as the directory and mount point.  These are used because Dr. Wolfer mentioned
# that we need these in the call to our system.  Specifically, in my notes I wrote the initial call
# to the system as "python myfusefs.py -f dir mp" with dir referring to the directory and mp
# referring to the mount point.  I'm not sure what the -f is for, if anyone figures out what it's
# for feel free to modify the code to use it.  I did read that using the getopt module may make using
# command line arguments easier, but I just wanted to get an outline set up.
#
# Currently, the program does assume perfect input, specifically a call of the form:
#
#                             python voltron.py dir mp
#
# From here we need to fill in all of the functions.  I will continue working on it,
# but I wanted to get the skeleton of the code put up so you guys could take a look.  


import numpy as np
import sys
import time
import pigpio


# These two lines were used for testing the command line arguments
#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

arg_count = 0

for args in sys.argv:
    if (arg_count == 1):
        directory = args
    elif (arg_count == 2):
        mountpoint = args
    arg_count+=1

print 'directory = ', directory
print 'mountpoint = ', mountpoint

def stat():
    print 'stat system call was called'

def open():
    print 'open system call was called'

def close():
    print 'close system call was called'

def read():
    print 'read system call was called'

def write():
    print 'write system call was called'

def unlink():
    print 'unlink system call was called'

def link():
    print 'link system call was called'

def getattr():
    print 'getattr system call was called'

def dir():
    print 'dir system call was called'
