#-*- coding: utf_8 -*-

# XXX/AAA.wav           |   AAA_1.wav   "text1" 
# AAA_1.wav [0.0,1.2]   |   AAA_2.wav   "text2"
# AAA_2.wav [1.5,2.0]   |   BBB_1.wav   "text3"
# .                     |   BBB_2.wav   "text4"
# XXX/BBB.wav           |
# BBB_1.wav [0.0,0.8]   |
# BBB_2.wav [1.1,1.9]   |
# .

import os
import sys
import codecs

FilterString=['', 'sil', 'noi', '*', 'music']

def filterTime(line):
    time = line[line.rfind('=')+1:]
    time = time.strip()
    return float(time[:time.find('.')+3])

def filterText(line):
    text = line[line.rfind('=')+1:]
    text = text.replace('"','')
    text = text.replace('。','')
    text = text.replace(' ','')
    text = text.strip()
    return text

def transCodeType(sFile, sType, tFile, tType):
    fin = open(sFile, 'r')
    fout = open(tFile, 'w')
    text = fin.read().decode(sType)
    fout.write(text.encode(tType))
    fin.close()
    fout.close()

def ParseFile(curFile, fcout, ftout):
    count = 0
    baseName = curFile[curFile.rfind('/')+1: curFile.rfind('.TextGrid')]
    pathName = 'XXX/%s.wav\n' % baseName
    fcout.write(pathName)

    transFile = '%s.TextGrid.bak' % baseName
    transCodeType(curFile, 'utf-16', transFile, 'utf-8')
    fin = open(transFile, 'r')
    
    while 1:
        line = fin.readline()

        if not line:
            break

        if line.find('item [2]') != -1:
            break

        if line.find('intervals [') != -1:
            line_xmin = fin.readline()
            line_xmax = fin.readline()
            line_text = fin.readline()

            xmin = filterTime(line_xmin)
            xmax = filterTime(line_xmax)
            text = filterText(line_text)

            if text in FilterString:
                continue

            count += 1
            segWave = '%s_%d.wav [%f,%f]\n' % (baseName, count, xmin, xmax)
            segText = '%s_%d.wav %s\n' % (baseName, count, text)

            fcout.write(segWave)
            ftout.write(segText)
    fcout.write('.\n')

    fin.close()
    if os.path.exists(transFile):
        os.remove(transFile)


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print 'python %s inFileList outcutWavList outtrans' % sys.argv[0]
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        print 'cannot find ', sys.argv[1]
        sys.exit(1)

    flist = open(sys.argv[1],'r')
    fcout = open(sys.argv[2],'w')
    ftout = open(sys.argv[3],'w')

    for curFile in flist:
        curFile = curFile.rstrip('\n')
        if not os.path.exists(curFile):
            print 'cannot find %s' % curFile
            continue
        ParseFile(curFile, fcout, ftout)

    flist.close()
    fcout.close()
    ftout.close()


