#!/USR/BIN/SUDO PYTHON
# ===========================================================================

#  This script make a data bin to write some data at some sector

# REFERENCES

#  $DateTime: 2017/07/10 10:33:00 $
#  $Author: jaehyek.choi

# when          who            what, where, why
# --------      ---           -------------------------------------------------------
# 2017-07-10    jaehyek        First made.

import struct
from array import array


file_loghead = "loghead.bin"
file_logdata = "logdata.bin"

SECTOR_SIZE = 512

loghead_sectorno = (2*1024*1024*2)
loghead_sectorlen = 2

#LOGHEAD_MAGICNUMBER = 0xAABBCCDD
LOGHEAD_MAGICNUMBER = 0xAAAAAAAA

# data to be written on loghead
logdata_sectorno = loghead_sectorno + loghead_sectorlen
logdata_sectorlen = 0
loghead_magicnumber = LOGHEAD_MAGICNUMBER 
bool_loghead_consoleloop = 1 
bool_loghead_crosstemptest = 1
THRESHOLD_HIGH_TEMP = 75
THRESHOLD_LOW_TEMP = -2
PERFORM_CROSS_TEMP_LOOP = 10
PERFORM_CROSS_READ_LOOP = 10
noise_sleep_microsec = 100000
noise_interval_nanosec = 120
noise_countloop = 2

listloghead = [logdata_sectorno, logdata_sectorlen,loghead_magicnumber,bool_loghead_consoleloop, bool_loghead_crosstemptest]
listloghead1 = [ THRESHOLD_HIGH_TEMP,THRESHOLD_LOW_TEMP,PERFORM_CROSS_TEMP_LOOP,PERFORM_CROSS_READ_LOOP ] 
listloghead2 = [ noise_sleep_microsec, noise_interval_nanosec, noise_countloop] 


def make_sector_loghead():
    " make a bin file for loghead"
    len_empty = SECTOR_SIZE*loghead_sectorlen - struct.calcsize("<%dL%dl%dL"%(len(listloghead ), len(listloghead1), len(listloghead2)))

    listtemp = listloghead + listloghead1 + listloghead2 +  [0x00]* len_empty
    bytes = struct.pack("<%dL%dl%dL%dB"%(len(listloghead ), len(listloghead1), len(listloghead2), len_empty),*listtemp) 
    open(file_loghead, "wb").write(bytes)

def make_sector_logdata():
    "make a bin file for logdata"

    msg = b'hello world\n'
    bytes_msg = struct.unpack("<%dB"%(len(msg)), msg)

    len_empty = SECTOR_SIZE*logdata_sectorlen - len(bytes_msg)
    listtemp = list(bytes_msg) + [0x00] * len_empty

    bytes = struct.pack("<%sB"%(SECTOR_SIZE*logdata_sectorlen),*listtemp  )

    open(file_logdata, "wb").write(bytes)

if __name__ == "__main__" :
    make_sector_loghead()
    #make_sector_logdata()
