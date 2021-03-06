# -*- coding: utf-8 -*-
import os,codecs,struct
from cStringIO import StringIO
DDS_header = "\x44\x44\x53\x20\x7C\x00\x00\x00\x07\x10\x0A\x00\x00\x04\x00\x00" + \
             "\x00\x04\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x01\x00\x00\x00" + \
             "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" + \
             "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" + \
             "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x00\x00\x00" + \
             "\x04\x00\x00\x00\x41\x54\x49\x31\x00\x00\x00\x00\x00\x00\x00\x00" + \
             "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x10\x40\x00" + \
             "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
GTX_header = "\x47\x66\x78\x32\x00\x00\x00\x20\x00\x00\x00\x07\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x42\x4C\x4B\x7B\x00\x00\x00\x20\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0B\x00\x00\x00\x9C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x34\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x0D\x03\x00\x00\x00\x20\x00\x00\x00\x00\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x02\x03\x03\xF8\x0F\x21\xCC\x00\x00\x7F\x06\x88\x80\x00\x00\x00\x00\x00\x80\x00\x00\xF0\x42\x4C\x4B\x7B\x00\x00\x00\x20\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0C\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00"

GTX_end = "\x42\x4C\x4B\x7B\x00\x00\x00\x20\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
def export_chars(bffnt_name):
    dest = codecs.open("charlist.txt" ,"wb" , "utf-16")
    base_offset = 0x5884b0
    base_size = 0x5a48
    fp = open(bffnt_name ,"rb")
    fp.seek(base_offset + 0x14)
    nums = struct.unpack(">H" , fp.read(2))[0]
    for i in xrange(nums):
        unicode_code = struct.unpack(">H" , fp.read(2))[0]
        char_id = struct.unpack(">H" , fp.read(2))[0]
        uchar = struct.pack("H" , unicode_code).decode('utf-16')
        dest.write("%s"%(uchar))
    dest.close()
    fp.close()



def bffnt2gtx(bffnt_name):
    fp = open(bffnt_name , "rb")
    fp.seek(0x3c)
    GRIDX = ord(fp.read(1))
    GRIDY = ord(fp.read(1))
    FILETOTAL = ord(fp.read(1))
    GRIDX += 1
    GRIDY += 1
    fp.seek(0x40)
    FLIMSIZE = struct.unpack(">I" , fp.read(4))[0]
    fp.seek(0x46)
    FORMAT = struct.unpack(">H" , fp.read(2))[0]
    fp.seek(0x4C)
    WIDTH = struct.unpack(">H" , fp.read(2))[0]
    HEIGHT = struct.unpack(">H" , fp.read(2))[0]
    OFFSET = struct.unpack(">I" , fp.read(4))[0]
    fp.seek(OFFSET)
    TMP = {0:0x1a , 0xb:0x33 , 0xc:0x34, 0xd:0x35 , 0xe:0x1a}
    for i in xrange(FILETOTAL):
        dest = open("gtx\\%02d.gtx"%i , "wb")
        data = fp.read(FLIMSIZE)
        dest.write(GTX_header)
        dest.write(data)
        dest.write(GTX_end)
        SWIZZLE = i
        SWIZZLE *= 2
        if FORMAT in TMP:
            FORMAT = TMP[FORMAT]
        dest.seek(0x46)
        dest.write(struct.pack(">H" , WIDTH))
        dest.seek(0x7E)
        dest.write(struct.pack(">H" , WIDTH))
        dest.seek(0x4A)
        dest.write(struct.pack(">H" , HEIGHT))
        dest.seek(0x60)
        dest.write(struct.pack(">I" , FLIMSIZE))
        dest.seek(0xF0)
        dest.write(struct.pack(">I" , FLIMSIZE))
        dest.seek(0x57)
        dest.write(chr(FORMAT))
        dest.seek(0x76)
        dest.write(chr(SWIZZLE))
        dest.close()
    fp.close()

export_chars("LENS5_SYSTEM_FONT.BFFNT")

bffnt2gtx("LENS5_SYSTEM_FONT.BFFNT")
fl = os.listdir("gtx")
for fn in fl:
    os.system("TexConv2.exe -i gtx/%s -o dds/%s.dds"%(fn , fn))
