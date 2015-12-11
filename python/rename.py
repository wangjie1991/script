#!/usr/bin/env python
import os
import sys

# def getFormatOut(curNum):
    # return '%05d' % curNum

def getFormatOut(curNum):
    if 0 <= curNum < 10:
        return '0000%d' % curNum                
    elif 10 <= curNum < 100:
        return '000%d' % curNum
    elif 100 <= curNum < 1000:
        return '00%d' % curNum
    elif 1000 <= curNum < 10000:
        return '0%s' % curNum
    else:
        return str(curNum)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'python %s inFile.list outBAT setName postfix' % sys.argv[0]
        sys.exit(1)

    fin = open(sys.argv[1],'r')
    fout = open(sys.argv[2],'w')
    setName = sys.argv[3]
    postfix = sys.argv[4]
    tDic = {}

    while 1:
        curLine = fin.readline()
        if not curLine: break
        baseName = curLine[curLine.rfind('/')+1:] 
        tDic[baseName] = curLine.rstrip()
    fin.close()

    curNum = 0
    for key in sorted(tDic.keys()):
        fout.write('cp \'%s\' newName/%s_%s.%s\n' % (tDic[key],setName,getFormatOut(curNum),postfix))
        curNum += 1
    fout.close()


