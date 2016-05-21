'''
Created on Jun 5, 2012

@author: Felix
'''

Rmin = -1
Record = None

def importModules(recordModule):
    import FullADTree
    FullADTree.Record = __import__(recordModule)
    
class ADNode(object):
    '''
    The value of attribute this ADN is represented as the index of this ADN in its parent VN's children list
    eg. The index of this ADN in parent VN's children list is 2(since the index starts from 0),
        if this ADN is representing ai=3
    '''
    
    def __init__(self, startAttributeNum, recordNums):
        '''Make a ADNode and its children nodes'''
        self.__count = len(recordNums)
        self.__children = [None]*(Record.arityLength+1-startAttributeNum)
        for eachAttributeNum in range(startAttributeNum, Record.arityLength+1):
            self.__children[eachAttributeNum-startAttributeNum] = VaryNode(eachAttributeNum, recordNums)
    
    def getCount(self):
        return self.__count
    
    def getVNChild(self, attributeNum):
        '''attributeNum ranges from 1(NOT 0) to the max attribute number'''
        return self.__children[attributeNum + len(self.__children) - Record.arityLength - 1]
        
class VaryNode(object):
    '''
    The attribute number is represented as the index of this VN in its parent ADN's children list
    eg. The index of this VN in parent ADN's children list is 2(since index starts from 0),
        if this VN is representing a3.
    '''
    
    def __init__(self, attributeNum, recordNums):
        '''Make a Vary Node and its children nodes'''
        self.__MCV = 0
        self.__children = [None]*(Record.arityList[attributeNum-1])
        
        #Initialises the childNum list for each attribute value
        childNums = [[] for eachAttributeValue in range(Record.arityList[attributeNum-1])]
        
        #This loop puts the amount for each attribute value into childNums list from the recordsTable
        for eachRecordNum in recordNums:
            value = Record.getRecord(eachRecordNum-1, attributeNum-1)
            childNums[value-1].append(eachRecordNum)

        #Get the MCV from childNums
        self.__MCV = childNums.index(max(childNums, key=len))+1
        
        #This loop creates AD-Nodes for each attribute value and attaches them to this Vary Node
        for eachAttributeValue in range(1, Record.arityList[attributeNum-1]+1):
            self.__children[eachAttributeValue-1] = ADNode(attributeNum+1, childNums[eachAttributeValue-1])
                
    def getMCV(self):
        return self.__MCV
    
    def getADNChild(self, attributeValue):
        '''attributeValue ranges from 1(NOT 0) to the Record.arityList[attributeNum]'''
        return self.__children[attributeValue-1]