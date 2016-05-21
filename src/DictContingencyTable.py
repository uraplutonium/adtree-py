'''
Created on Jun 5, 2012
@author: Felix

The following improvement methods are used:
1. Using dict instead of list
2. Passing productList through constructor to reduce duplication of calculating productList
3. This ContingencyTable supports being built from LeafSparseADTree
'''
Record = None
ADTree = None
leafList = False

def importModules(recordModule, ADTreeModule):
    import DictContingencyTable
    DictContingencyTable.leafList = (('Leaf' in ADTreeModule) or ('leaf' in ADTreeModule))
    DictContingencyTable.Record = __import__(recordModule)
    DictContingencyTable.ADTree = __import__(ADTreeModule)

class ContingencyTable(object):
    
    def __init__(self, attributeList, ADN, productList=[]):
        self.__CT = {}
        self.__attributeList = attributeList
        self.__dimension = len(attributeList)
        self.__productList = productList
        if not self.__productList and attributeList:
            self.__productList = [1]*self.__dimension
            for index in range(self.__dimension-1, 0, -1):
                self.__productList[index-1] = self.__productList[index] * Record.arityList[self.__attributeList[index]-1]

        ctIndex = 0
        
        if ADN:
            if attributeList:   # AD-node that has Vary node children
                if not leafList or ADN.getCount() >= ADTree.Rmin: # AD-node with children Vary-nodes
                    VN = ADN.getVNChild(attributeList[0])
                    MCV = VN.getMCV()
                    CTList = [None]*(Record.arityList[attributeList[0]-1])
        
                    for eachAttributeValue in range(1, Record.arityList[attributeList[0]-1]+1):
                        adNode = ADN if eachAttributeValue==MCV else VN.getADNChild(eachAttributeValue)
                        CTList[eachAttributeValue-1] = ContingencyTable(attributeList[1:], adNode, self.__productList[1:])
                    # calculate the contingency table for MCV
                    for i, eachNotMCVCT in enumerate(CTList):
                        if i+1 != MCV:
                            CTList[MCV-1].subInRow(eachNotMCVCT)
                    self.concatenate(CTList)
                else:   # AD-node with leaf-list
                    # ctIndex is not necessary to build the current CT, since CT now is build by counting for each records
                    for eachRecordNum in ADN.getLeafList(): # plus one for each of the records in leaf-list
                        recordIndex = 0
                        # calculate the key in CT of a record
                        for eachAttributeIndex in range(self.__dimension):
                            recordIndex += ((Record.getRecord(eachRecordNum-1, self.__attributeList[eachAttributeIndex]-1)-1) * self.__productList[eachAttributeIndex])
                        self.__CT[recordIndex] = self.__CT.get(recordIndex, 0) + 1   # plus one on the counting in CT of the current record
            else:   # leaf AD-node
                self.__CT[ctIndex] = ADN.getCount()
                ctIndex += 1
        else:
            if attributeList:   # zero AD-node with subtree
                ctIndex += Record.arityList[attributeList[0]-1]
            else:   # zero leaf AD-node
                ctIndex += 1
            
    def concatenate(self, CTList):
        '''Make the concatenation of all conditional contingency tables for attributeNum'''
        sliceLength = 1 if self.__dimension<=1 else Record.arityList[self.__attributeList[1]-1]
        for i, eachCT in enumerate(CTList):
            for eachKey in eachCT.__CT:
                self.__CT[i*self.__productList[0]+eachKey] = eachCT.__CT[eachKey]

    def subInRow(self, other):
        for eachKey in self.__CT:
            otherValue = other.__CT.get(eachKey)
            if otherValue:
                self.__CT[eachKey] -= otherValue
        
    def getCount(self, query):
        rowNum = 0
        for j in range(self.__dimension):
            rowNum += ((query[j]-1) * self.__productList[j])
        return self.__CT.get(rowNum, 0)
        