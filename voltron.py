==========================Generic Fuse File System=========================
#Team Voltron: Andrew Stone, David Eling, John Hutchins, Josh Kiefer
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
 
	#Commands to use:
	#To unmount:
	#fusermount -u /home/USER/fusefolder/myfs
	#To mount:
	#python ./voltron.py /home/USER/fusefolder /home/USER/fusefolder/myfs


#!/usr/bin/env python
#Team Voltron: Andrew Stone, David Eling, John Hutchins, Josh Kiefer
import stat
import errno
import fuse
import numpy as np
import sys
import random
import time
import os
import io # Allows for os.open without the use of flags
from fuse import Fuse
import re # Allows for regexing of file names
fuse.fuse_python_api = (0, 2)

class VoltronFS(fuse.Fuse):
    def __init__(self, *args, **kw):
        fuse.Fuse.__init__(self, *args, **kw)
        self.root = sys.argv[-2]
        self.userfiles = {}
        self.timestampfiles = {"intermediate":
                               os.path.join(self.root ,"intermediate.txt")
                               ,"timestamps":
                                os.path.join(self.root,"ts2.txt")}
        self.validfilename = re.compile('^[\w,\s-]+\.[A-Za-z]{3}$')
        print self.timestampfiles
        print self.userfiles
        self.CleanFile()

    #Get the attributes for a file or directory
    #if the file name is valid (*.***) return its information if it exists
    #if not create it(with errno.ENOENT)
    def getattr(self, path):
        name = os.path.basename(path)  #Get the real file name from the path
        print "getattr"
        print path
        print self.userfiles
        st = fuse.Stat()
        st.st_mode = stat.S_IFDIR | 0777
        st.st_nlink = 2
        st.st_atime = int(time.time())
        st.st_mtime = st.st_atime
        st.st_ctime = st.st_atime
        if self.validfilename.match(name):
            if name in self.userfiles:
                st = os.stat(self.userfiles[name])
                pass
            else:
                return - errno.ENOENT
        return st
        
    def readlink(self, path):
        print "readlink"
        return 0

    def unlink(self, path):
        print "unlink"
        return 0
        
    def link(self, path, path1):
        print "link"
        return 0

    def truncate(self, path, len):
        print "trunc"
        f = open("." + path, "a")
        f.truncate(len)
        f.close()

    def utime(self, path, times):
        print "utime"
		
    def access(self, path, mode):
        print "access"
        return 
    
    def close(self, path):
        print "close"

    #Return None if the file exists if not return an error
    def open(self, path, flags):
        print "opening"
        name = os.path.basename(path)  #Get the real file name from the path
        if name in self.userfiles:
            return None
        else:
            return -errno.ENOENT

    #Add the given file name to the userfile dictionaries
    def create(self, path, mode, fi=None):
        name = os.path.basename(path)  #Get the real file name from the path
        print "creating"
        self.userfiles[name] = os.path.join(self.root, name)
        print self.userfiles
        return self.userfiles[name]

    def readdir(self, path, offset):
        for f in self.userfiles:
            yield fuse.Direntry(f)
        
    def statfs(self):
        return os.statvfs(".")
		
    def fsinit(self):
        os.chdir(self.root)

    #Use the size of the file provided to determine the number
    #of random bytes to write to the file
    def read(self, path, size, offset, fh=None):
        print "reading"
        print size
        name = os.path.basename(path)  #Get the real file name from the path
        fh = io.open(self.userfiles[name], 'a')
        rngsize = int(os.path.getsize(self.userfiles[name]))
        print rngsize
        rng = np.loadtxt(self.RNG(rngsize))
        for line in rng:
            fh.write(line.astype('U') + u' ')
        fh.close()

    #When given a number in the buffer generate the average number of time 
    #stamps per minute and write to the file
    def write(self, path, buf, offset, fh=None):
        print "writing"
        name = os.path.basename(path)  #Get the real file name from the path 
        fh = io.open(self.userfiles[name], 'a')
        print path
        stamptime = np.loadtxt(self.GetStamps(buf))
        print stamptime[-1]
        print stamptime[0]
        stamptime = np.diff(stamptime)
        stamptime = (np.float64(buf)/np.sum(stamptime))*np.float64(60)/np.float64(2)
        print stamptime
        fh.write(u"\nThe average giegercounter time stamps per minute is ")
        fh.write(stamptime.astype('U') + u'\n')
        fh.close()
        return len(buf)

    #Generate a number of psudorandom numbers from the true random 
    #numbers created from the timestamps
    def RNG(self,original_numbers):
        reseed = 10
        
        stamps = self.GetStamps(8 * (original_numbers/reseed))
        numbers = original_numbers
        
        fi = io.open(self.timestampfiles["intermediate"],'w+b')
        
        for line in stamps:
            fi.write(line)
            fi.flush()
        fi.close()
        stamps = np.loadtxt(self.timestampfiles["intermediate"])
        
        ti = np.diff(stamps)
        til = ti[1:] > ti[:-1]
        til = np.array(til)
        seed = np.packbits(til- 1)
        randnum = []
        
        while(numbers > 0):
            if numbers % reseed == 0:
                random.seed(int(seed[(numbers/reseed)-1]))
            randnum.append(random.getrandbits(8))
            if numbers == 0:
                return randnum
            numbers -= 1
        return randnum
    # Get the number time stamps the caller needs from the timestamps file
    # and return them. 
    def GetStamps(self,stamps):
        print "getting stamps"
        fi = io.open(self.timestampfiles["timestamps"],'r')
        print "got stamps"
        lines = fi.readlines()
        print lines[1:20]
        fi.close()
        print "saving stamps"
        fi = io.open(self.timestampfiles["timestamps"],'w')
        print "saved stamps"
        count = int(stamps)
        print stamps
        print count
        print lines[1:20]
        for line in lines:
            if count == 0:
                fi.write(line)
                fi.flush()
            if count > 0 and count <= stamps:
                count -= 1
        fi.close()

        return lines[0:int(stamps)]

    # Cleans file for future use. Removes extra spaces and lines with multiple time stamps or incorrect data
    def CleanFile(self):
        validdata = re.compile('^[1]{1}\d{9}\.+\d*')
        print "cleaning time stamps file"
        fi = io.open(self.timestampfiles["timestamps"],'r')
        lines = fi.readlines()
        fi.close()
        fi = io.open(self.timestampfiles["timestamps"],'w')
        for line in lines:
            if validdata.match(line):
                fi.write(line)
                fi.flush()
        fi.close()
        print "clean"

if __name__ == '__main__':
    server = VoltronFS()
    usage="""
        Voltron: A filesystem to create random numbers and write them to
        files by our powers combined.
        """ + fuse.Fuse.fusage
    server.parse(errex=1)
    
    server.main()
