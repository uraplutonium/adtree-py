'''
Created on Jun 23, 2012
@author: Felix
'''

arityList = []
recordsTable = []
arityLength = 0
recordsLength = 0

def initRecord(args):
    arity = args[0]
    record = args[1]
    import ArrayRecord
    ArrayRecord.arityList = arity
    ArrayRecord.recordsTable = record
    ArrayRecord.arityLength = len(ArrayRecord.arityList)
    ArrayRecord.recordsLength = len(ArrayRecord.recordsTable)

def getRecord(row, column):
    return recordsTable[row][column]

def count(query):
    return recordsTable.count(query)