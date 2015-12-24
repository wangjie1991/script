#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'python %s input output suffix' % sys.argv[0]
        sys.exit(1)

    fin = open(sys.argv[1],'r')
    fout = open(sys.argv[2],'w')
    suffix = sys.argv[3]
    dic = {}

    while 1:
        curLine = fin.readline()
        if not curLine: break
        baseName = curLine[curLine.rfind('/')+1:] 
        dic[baseName] = curLine.rstrip()
    fin.close()

    curNum = 0
    for key in sorted(dic.keys()):
        fout.write('cp \'%s\' newName/%05d.%s\n' % (dic[key], curNum, suffix))
        curNum += 1
    fout.close()


