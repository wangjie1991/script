#!/usr/bin/env python
#-*- coding: utf_8 -*-

import os
import sys
import codecs
import shutil

'''
*********************************************
parse Infomation from TextGrid Transcription
author: yunliao hu
email:  huyunliao@pachiratech.com
Right Reserved
*********************************************
'''

codeTypeTuple = ('UTF_8','gbk','UTF_16')
FilterString={'', 'sil', 'noi', '*', 'music'}

def judgeCodeType(fileName):
    '''
    get Type of "fileName"
    '''
    for curType in codeTypeTuple:
        try:
            codecs.open(fileName,'r',curType).readline()
        except UnicodeError:
            continue
        else:
            return curType
    return False

def transCodeType(sFile,sType,tFile,tType):
    '''
    transfer "sFile" of "sType" to "tFile" of "tType"
    '''
    try:
        fList = codecs.open(sFile,'r',sType).readlines()
    except UnicodeDecodeError:
        return False
    else:
        fout = codecs.open(tFile,'w',tType)
        try:
            fout.write(''.join(fList))
        except UnicodeEncodeError:
            fout.close()
            return False
        else:
            fout.close()
            return True

def getFormatOut(curNum):
    if 0 <= curNum < 10:
        return '000%d' % curNum
    elif 10 <= curNum < 100:
        return '00%d' % curNum
    elif 100 <= curNum < 1000:
        return '0%d' % curNum
    else:
        return str(curNum)

speakerType = ('SERVER','CLIENT','other')

class segInfo:
    def __init__(self,curIndex,curSerNum,curType):
        self.index = curIndex
        self.serialNum = curSerNum
        self.spkType = curType
        self.startTime = 0.0
        self.endTime = 0.0
        self.trans = ''

    def setStartTime(self,curTime):
        self.startTime = curTime

    def setEndTime(self,curTime):
        self.endTime = curTime

    def setSpkType(self,curType):
        self.spkType = curType

    def setTrans(self,curTrans):
        self.trans = curTrans

    def getSegInfo(self):
        outSerNum = getFormatOut(self.serialNum)
        curRole = ''
        if self.spkType == 'SERVER':
            curRole = 'svr'
        elif self.spkType == 'CLIENT':
            curRole = 'clt'
        else:
            curRole = 'otr'
        outLine = ''
        if self.trans and self.trans != '*':
            outLine = '_%s_%s.wav [%.2f,%.2f]\n' % (curRole,outSerNum,self.startTime,self.endTime)
        return outLine

    def getTransInfo(self):
        outSerNum = getFormatOut(self.serialNum)
        curRole = ''
        if self.spkType == 'SERVER':
            curRole = 'svr'
        elif self.spkType == 'CLIENT':
            curRole = 'clt'
        else:
            curRole = 'otr'
        outLine = ''
        if self.trans and self.trans != '*':
            outLine = '_%s_%s.wav %s\n' % (curRole,outSerNum,self.trans)
            #outLine = '_%s_%s.wav [%.2f,%.2f] %s\n' % (curRole,outSerNum,self.startTime,self.endTime,self.trans)
        return outLine


def filterTime(timeLine):
    time = timeLine[timeLine.rfind('=')+1:]
    time = time.strip()
    return float(time[:time.find('.')+3])

def filterIndex(timeLine):
    time = timeLine[timeLine.rfind('=')+1:]
    time = time.strip()
    return float(time[:time.find('.')+3])

def filterTrans(transLine):
    trans = transLine[transLine.rfind('=') + 1:]
    trans = trans.strip()
    trans = trans.replace('"','')
    trans = trans.strip()
    return trans

def parseInfo(curFile):
    baseName = curFile[curFile.rfind('/')+1: curFile.rfind('.TextGrid')]
    toopenFile = curFile
    curType = judgeCodeType(curFile)
    if curType != 'UTF_8':
        toopenFile = '%s.TextGrid.bak' % baseName
        transCodeType(curFile,curType,toopenFile,'UTF-8')
    ftin = open(toopenFile,'r')
    serverNum = 0
    clientNum = 0
    otherNum  = 0
    layerFlag = ''
    segDic = {}

    while 1:
        curLine = ftin.readline()
        if not curLine:break
        if curLine.find('item [') != -1:
            if curLine.find('item [1]') != -1: # SPEAKER info layer
                layerFlag = 'PEOPLE'
            elif curLine.find('item [2]') != -1: # PEOPLE info layer
                layerFlag = 'SPEAKER'
            else:
                layerFlag = 'UNKNOWN'
        if curLine.find('intervals [') != -1:
            #curIndex = curLine[curLine.rfind('[')+1:curLine.rfind(']')]

            if layerFlag == 'SPEAKER':
                startTimeLine = ftin.readline()
                endTimeLine = ftin.readline()
                transLine = ftin.readline()
                curTrans = filterTrans(transLine)
                curType = ''
                curNum = 0
                if curTrans:
                    curIndex = filterIndex(startTimeLine)

                    curStartTime = filterTime(startTimeLine)
                    curEndTime = filterTime(endTimeLine)
                    if curTrans.find('A') != -1:
                        serverNum += 1
                        curNum = serverNum
                        curType = 'SERVER'
                    elif curTrans.find('B') != -1:
                        clientNum += 1
                        curNum = clientNum
                        curType = 'CLIENT'
                    else:
                        otherNum += 1
                        curNum = otherNum
                        curType = 'other'
                    segDic[curIndex] = segInfo(curIndex,curNum,curType)
                    segDic[curIndex].setStartTime(curStartTime)
                    segDic[curIndex].setEndTime(curEndTime)

            elif layerFlag == 'PEOPLE':
                startTimeLine = ftin.readline()
                endTimeLine = ftin.readline()
                transLine = ftin.readline()
                curTrans = filterTrans(transLine)

                curIndex = filterIndex(startTimeLine)

                if curTrans != '' and segDic.has_key(curIndex): # filter invalid trans here
                    segDic[curIndex].setTrans(curTrans)
    ftin.close()
    if os.path.exists('%s.TextGrid.bak' % baseName):
        os.remove('%s.TextGrid.bak' % baseName)
        
    segInfoList = []
    transInfoList = []

    for index in sorted(segDic.keys()):
        if segDic[index].getTransInfo() :
            segInfoList.append('%s%s' % (baseName,segDic[index].getSegInfo()))
            transInfoList.append('%s%s' % (baseName,segDic[index].getTransInfo()))
    return segInfoList,transInfoList

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'python %s inFileList outcutWavList outtrans' % sys.argv[0]
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        print 'cannot find ',sys.argv[1]
        sys.exit(1)

    fin = open(sys.argv[1],'r')
    fcout = open(sys.argv[2],'w')
    ftout = open(sys.argv[3],'w')
    while 1:
        curFile = fin.readline()
        if not curFile: break
        curFile = curFile.rstrip()
        if not os.path.exists(curFile):
            print 'cannot find %s' % curFile
            continue
        if not judgeCodeType(curFile):
            print 'unknown code type of %s' % curFile
            continue
        segList,transList = parseInfo(curFile)
        outName = curFile[curFile.rfind('/')+1:curFile.rfind('.TextGrid')]
        fcout.write('XXX/%s.wav\n' % outName)
        fcout.write(''.join(segList))
        fcout.write('.\n')
        ftout.write(''.join(transList))
    fin.close()
    fcout.close()
    ftout.close()
     
