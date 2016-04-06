# FUSE-file-system-project

#Project represents a FUSE (File System in User Space) which is a project used to demonstrate file systems for CSCI-C435.
#Background information: Instructor has a Gieger counter which measures cosmic radiation and that sends a signal to A Raspberry Pi on pin 23. We have been instructed to retreive these signals on "HIGH" and using the Time library generate time statmps at the time that an event occurs and export this file ocntaining timestamps to our FUSE system. The FUSE system will open this file containing comma seperated timestamps and compare them generating a sequence of RANDOM BITS based on the length of time between the timestamps. Those random bits will be stored in an array of  Random Numbers and each element of that array will be used as a seed for a psuedorandom number generator which be handled in the Read function of our FUSE system and the time stamps will be rewritten to the file ocntaining our original timestamps.    
