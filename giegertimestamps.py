#Program to export timestamps from Raspbery Pi pin 23 off Gieger Counter to FUSE system
#giegertimestamps.py
#=============================timestamp collection==========================
#Author: Joshua Kiefer
#!/usr/bin/env python
import pigpio,time

razpi1 = pigpio.pi()
razpi1.set_mode(23,pigpio.INPUT)               #set pin23 as input
time.sleep(5)                                                  

while 1:

    if razpi1.wait_for_edge(23, pigpio.FALLING_EDGE, 5.0):      #if event occurs on pin23
        timeStamp = time.time()                                                      #create time stamp
        time_stamp_File_Write = open('timestamp.txt', 'a')             #open/create timestamp.txt 
        time_stamp_File_Write.write((str(timeStamp)) + '\n')          #write/append file
        time_stamp_File_Write.flush()                                             #clear fstream buffer
=====================================================================
