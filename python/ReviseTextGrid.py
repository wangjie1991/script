#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import codecs

dic = {}

def ParseDict(file):
    global dic
    fin = codecs.open(file, 'r', encoding='utf-8')
    for line in fin:
        line = line.strip()
        words = line.split('\t')
        if (len(words) != 2):
            print line
            continue
        if words[0] not in dic:
            dic[words[0]] = words[1]
    #for (key, value) in dic.items():
    #    print "%s,%s" % (key,value)
    fin.close()

def ParseFile(file):
    global dic

    fin = codecs.open(file, 'r', encoding='utf-16')
    fout = codecs.open(file+".revise", 'w', encoding='utf-8')

    for line in fin:
        line = line.rstrip('\r\n')
        if line.find('text') != -1:
            for (key, value) in dic.items():
                line = line.replace(key, value)
        fout.write(line+'\n')

    fin.close()
    fout.close()

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print 'python %s dict.txt file.list' % sys.argv[0]
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        print 'cannot find ', sys.argv[1]
        sys.exit(1)

    if not os.path.exists(sys.argv[2]):
        print 'cannot find ', sys.argv[2]
        sys.exit(1)

    ParseDict(sys.argv[1])

    flist = codecs.open(sys.argv[2], 'r', encoding='utf-8')
    for line in flist:
        line = line.strip()
        if not os.path.exists(line):
            print 'cannot find %s' % line
            continue
        ParseFile(line)
    flist.close()


