'''
Created on Sep 25, 2014
@author: Felix
'''

from Dataset import *

arityList = []
data = None
arityLength = 0
recordsLength = 0

def initRecord(args):
    import FileRecord
    FileRecord.data = dataset(args[0], True)
    FileRecord.arityList = FileRecord.data.getArityList()
    FileRecord.arityLength = len(FileRecord.arityList)
    FileRecord.recordsLength = FileRecord.data.getDataNum()

def getRecord(row, column):
    import FileRecord
    return FileRecord.data.getEntry(row, column)

def count(query):
    import FileRecord
    return FileRecord.data.count(query)
