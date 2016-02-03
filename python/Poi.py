#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import codecs

poi = set()

def ParseFile(fin):
    global poi

    for line in fin:
        # find line "item [2]"
        if line.find('item [2]') != -1:
            break

    for line in fin:
        if (not line) or (line.find('item [3]') != -1):
            break
        if line.find('text') != -1:
            text = line[line.rfind('=')+1:]
            text = text.replace('"','')
            text = text.strip()
            for word in text.split("，".decode('utf-8')):
                poi.add(word)


if __name__ == '__main__':

    if (len(sys.argv) != 3):
        print 'python %s textgrid.list poi.txt' % sys.argv[0]
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        print 'cannot find ', sys.argv[1]
        sys.exit(1)

    flist = codecs.open(sys.argv[1], 'r', encoding='utf-8')
    fpoi = codecs.open(sys.argv[2], 'w', encoding='utf-8')

    for line in flist:
        line = line.strip()
        if not os.path.exists(line):
            print 'cannot find %s' % line
            continue
        ftg = codecs.open(line, 'r', encoding='utf-16')
        ParseFile(ftg)
        ftg.close()
    
    for word in poi:
        fpoi.write(word+"\n")

    flist.close()
    fpoi.close()


