import xlrd
import xlwt

print ("hello")
workbook = xlrd.open_workbook("database.xls")
#read content of Sheet1
sheet = workbook.sheet_by_name("Sheet1")

      
def getWordsFromRound(database,round1):
    'gets all the words for one round'
    table=database.sheet_by_index(0)
    nrows=table.nrows
    mylist=[]
    ##table.cell(colNumber,rowNumber)
    ##print(table.cell(1,0))
    for i in range(1,nrows):
        cell=table.cell(i,3).value
        if cell == round1 :
            mylist.append(table.cell(i,0))
    return mylist
    
def getDef(database,rownumber):
    table=database.sheet_by_index(0)
    defination=table.cell(2,rownumber).value
    return defination

def getWords(database,rownumber):
    table=database.sheet_by_index(0)
    word=table.cell(0,rownumber).value
    #print(word)
    return word

def getScore(database,rownumber):
    table = database.sheet_by_index(0)
    Score=table.cell(2,rownumber).value
    return Score

def main():
    database=xlrd.open_workbook("‪C:/Users/X1/Desktop/database.xls");
    list=getWordsFromRound(database, 1)
    print(list[1])

def getIndex(database,round):
    table=database.sheet_by_index(0)
    nrows=table.nrows
    list=[]
    
    for i in round(nrows):
        cell=table.cell(4,i).value
        if cell == round :
            list.append(i)
    return list

#name=input('Plese enter your name: ')
print('ROUND 1')
print(getWordsFromRound(workbook, 1))
score=0
indexDef=0

#want to go through every definition and print in out
#and check if word typed in matched definition given
for word in range(1,3): #word stands for row number
    print(getDef(workbook,word))
    answer=input('type in word that match definition: ')
    print('this is the answer: ',getWords(workbook,word))
    if answer==getWords(workbook, word):
        print('Correct!!!')
        score = score + int(getScore(workbook, word))

print('Game over')
print('Your Score is: ',score)

