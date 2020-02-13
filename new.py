import time
import struct
import sys
unit = sys.argv[1]
now = time.localtime()
arquivo = open("C:/Users/3AEMAQ21/Desktop/log.txt", "a")
arquivo.write("%s %d/%d/%d %d:%d:%d\n" %(unit, now.tm_mday, now.tm_mon, now.tm_year, now.tm_hour, now.tm_min, now.tm_sec))
arquivo.close()