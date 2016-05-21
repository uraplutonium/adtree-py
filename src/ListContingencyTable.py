'''
Created on May 28, 2012
@author: Felix

The following improvement methods are used:
1. Using one dimension array (list) instead of two dimension array (list of list)
2. Initialise list and then update instead of calling of list.append() as much as possible
3. Passing productList through constructor to reduce duplication of calculating productList
4. This ContingencyTable supports being built from LeafSparseADTree
'''
Record = None
ADTree = None
leafList = False

def importModules(recordModule, ADTreeModule):
    import ListContingencyTable
    ListContingencyTable.leafList = (('Leaf' in ADTreeModule) or ('leaf' in ADTreeModule))
    ListContingencyTable.Record = __import__(recordModule)
    ListContingencyTable.ADTree = __import__(ADTreeModule)

class ContingencyTable(object):
    
    def __init__(self, attributeList, ADN, productList=[]):
        self.__attributeList = attributeList
        self.__dimension = len(attributeList)
        self.__productList = productList
        if not self.__productList and attributeList:
            self.__productList = [1]*self.__dimension
            for index in range(self.__dimension-1, 0, -1):
                self.__productList[index-1] = self.__productList[index] * Record.arityList[self.__attributeList[index]-1]

        ctIndex = 0
        ctLength = 1 if not (self.__productList or self.__attributeList) else self.__productList[0]*Record.arityList[self.__attributeList[0]-1]
        self.__CT = [0]*ctLength
        
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
                    self.concatenate(CTList, ctIndex)
                else:   # AD-node with leaf-list
                    # ctIndex is not necessary to build the current CT, since CT now is build by counting for each records
                    for eachRecordNum in ADN.getLeafList(): # plus one for each of the records in leaf-list
                        recordIndex = 0
                        # calculate the index in CT of a record
                        for eachAttributeIndex in range(self.__dimension):
                            recordIndex += ((Record.getRecord(eachRecordNum-1, self.__attributeList[eachAttributeIndex]-1)-1) * self.__productList[eachAttributeIndex])
                        self.__CT[recordIndex] += 1   # plus one on the counting in CT of the current record
            else:   # leaf AD-node
                self.__CT[ctIndex] = ADN.getCount()
                ctIndex += 1
        else:
            if attributeList:   # zero AD-node with subtree
                ctIndex += Record.arityList[attributeList[0]-1]
            else:   # zero leaf AD-node
                ctIndex += 1
        
    def concatenate(self, CTList, ctIndex):
        '''Make the concatenation of all conditional contingency tables for attributeNum'''
        for eachCT in CTList:
            for eachNum in eachCT.__CT:
                self.__CT[ctIndex] = eachNum
                ctIndex += 1

    def subInRow(self, other):
        for index, eachCount in enumerate(self.__CT):
            self.__CT[index] -= other.__CT[index]
        
    def getCount(self, query):
        rowNum = 0
        for j in range(self.__dimension):
            rowNum += ((query[j]-1) * self.__productList[j])
        return self.__CT[rowNum]
        