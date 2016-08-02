
'''
Created on Dec 3, 2015

@author: aaronhu
'''
import xlrd
import xlwt
import xlutils
import unicodedata
import random
from lib2to3.pgen2.token import EQUAL
from xlutils.copy import copy



def getWordsFromRound(round):
    database=xlrd.open_workbook('data/database.xls');
    table=database.sheet_by_index(0)
    nrows=table.nrows
    thekeys=[]
    Mylist={}
    Myscdlist = {}
    for i in range(1, nrows):
        cell=table.cell(i, 3).value
        word = table.cell(i, 0).value
        defn = table.cell(i, 1).value
        if cell == round:
            thekeys.append(word)
            Mylist[word] = defn
    random.shuffle(thekeys)
    return Mylist

def shufflewords(list):
    keys = list.keys()
    random.shuffle(keys)
    print(keys)


def getMaxRound():
    database=xlrd.open_workbook('data/database.xls');
    table=database.sheet_by_index(0)
    nrows=table.nrows
    maxRound = 0
    for i in range(1, nrows):
        r = table.cell(i, 3).value
        if r > maxRound:
            maxRound = r
    return int(maxRound)

def getTotalScore():
    database=xlrd.open_workbook('data/database.xls');
    table=database.sheet_by_index(0)
    nrows=table.nrows
    score = 0
    for i in range(1, nrows):
        score += table.cell(i, 2).value
    return int(score)
    
def getDef(rownumber):
    database=xlrd.open_workbook('data/database.xls');
    table=database.sheet_by_index(0)
    definition=table.cell(rownumber,1).value
    return definition
    
def getWord(rownumber):
    database=xlrd.open_workbook('data/database.xls');
    table=database.sheet_by_index(0)
    word=table.cell(rownumber,0).value
    return word

def getRowNumber(word):
    database = xlrd.open_workbook('data/database.xls');
    table = database.sheet_by_index(0)
    nrows=table.nrows
    for i in range(1,nrows):
        currentWord= table.cell(i,0).value
        if currentWord == word:
            rowNumber = i
    return rowNumber
    
def getScore(rownumber):
    database=xlrd.open_workbook('data/database.xls')
    table = database.sheet_by_index(0)
    Score=table.cell(rownumber,2).value
    return int(Score)
    

def getIndex(round):
    database=xlrd.open_workbook('data/database.xls');
    table=database.sheet_by_index(0)
    nrows=table.nrows
    list=[]
    
    for i in range(1,nrows):
        cell=table.cell(i,3).value
        if cell == round :
            list.append(i)
    return list

def loadname(row):
    database=xlrd.open_workbook('data/database.xls')
    table=database.sheet_by_index(1)
    name = table.cell(row,0).value
    return name

def loadscore(row):
    database=xlrd.open_workbook('data/database.xls')
    table=database.sheet_by_index(1)
    score = table.cell(row,1).value
    return score

def loadround(row):
    database=xlrd.open_workbook('data/database.xls')
    table=database.sheet_by_index(1)
    round = table.cell(row,2).value
    return round
    
def savename(row,name):
    database = xlrd.open_workbook('data/database.xls')
    database2 = copy(database)
    table = database2.get_sheet(1)
    table.write(row,0,name)
    database2.save('data/database.xls')
    
def savescore(row,score):
    database = xlrd.open_workbook('data/database.xls')
    database2 = copy(database)
    table = database2.get_sheet(1)
    table.write(row,1,score)
    database2.save('data/database.xls')
    
def saveround(row,round):
    database = xlrd.open_workbook('data/database.xls')
    database2 = copy(database)
    table = database2.get_sheet(1)
    table.write(row,2,round)
    database2.save('data/database.xls')
    
if __name__ == '__main__':
    """
    database=xlrd.open_workbook('data/database.xls');
    savename(1,"AMY")
    savescore(1,46)
    saveround(1,2)
    
    print(loadname(1))
    print(loadscore(1))
    print(loadround(1))
    
    print(getWordsFromRound(1))
    print(getWordsFromRound(2))
    print(getWordsFromRound(3))
    print(getTotalScore())
    print(getMaxRound())
"""
    getWordsFromRound(1)
    #list = ['word'=1,'hello'=2,'nancy'=3,'father'=4]
    #shufflewords(list)
    