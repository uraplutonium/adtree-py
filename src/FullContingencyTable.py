'''
Created on May 22, 2012

@author: Felix
'''
#import SparseADTree as ADTree
Record = None
ADTree = None

def importModules(recordModule, ADTreeModule):
    import FullContingencyTable
    FullContingencyTable.Record = __import__(recordModule)
    FullContingencyTable.ADTree = __import__(ADTreeModule)

class ContingencyTable(list):
    
    def __init__(self, attributeList, ADN):
        self.__attributeList = attributeList
        self.__dimension = len(attributeList)

        if ADN:
            if attributeList:   # AD-node that has Vary node children
                VN = ADN.getVNChild(attributeList[0])
                MCV = VN.getMCV()
                CTList = []
    
                for eachAttributeValue in range(1, Record.arityList[attributeList[0]-1]+1):       
                    if eachAttributeValue != MCV:
                        childADN = VN.getADNChild(eachAttributeValue)
                        CTList.append(ContingencyTable(attributeList[1:], childADN))
                    else:
                        CTList.append(None) # leave a position for MCV
                            
                # calculate the contingency table for MCV
                CTList[MCV-1] = ContingencyTable(attributeList[1:], ADN)
                for i, eachNotMCVCT in enumerate(CTList):
                    if i+1 != MCV:
                        CTList[MCV-1].subInRow(eachNotMCVCT)
                
                self.extend(ContingencyTable.concatenate(attributeList[0], CTList))
            else:   # leaf AD-node
                self.append([ADN.getCount()])
        else:
            if attributeList:   # zero AD-node with subtree
                CTList = []
                for eachAttributeValue in range(1, Record.arityList[attributeList[0]-1]+1):          
                    CTList.append(ContingencyTable(attributeList[1:], None))
                self.extend(ContingencyTable.concatenate(attributeList[0], CTList))
            else:   # zero leaf AD-node
                self.append([0])
    
    @staticmethod
    def concatenate(attributeNum, CTList):
        '''Make the concatenation of all conditional contingency tables for attributeNum'''
        resultCT = []
        for eachAttributeValue in range(1, Record.arityList[attributeNum-1]+1):
            for eachRow in CTList[eachAttributeValue-1]:
                resultCT.append([eachAttributeValue] + eachRow)
        return resultCT
    
    def subInRow(self, other):      
        for index, row in enumerate(self):
            row[-1] -= other[index][-1]
        
    def getCount(self, query):
        rowNum = 0
        for i, eachAttributeValue in enumerate(query):
            while(self[rowNum][i] != eachAttributeValue):
                rowNum+=1
        return self[rowNum][-1]
        