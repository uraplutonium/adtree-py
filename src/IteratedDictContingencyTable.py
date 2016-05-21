'''
Created on Jun 20, 2012
@author: Felix

The following improvement methods are used:
1. Using dict instead of list
2. Initialise list and then update instead of calling of list.append() as much as possible
3. Using one loop/iteration to build Contingency table instead of recursion
4. This ContingencyTable supports being built from LeafSparseADTree
'''
Record = None
ADTree = None
leafList = False

def importModules(recordModule, ADTreeModule):
    import IteratedDictContingencyTable
    IteratedDictContingencyTable.leafList = (('Leaf' in ADTreeModule) or ('leaf' in ADTreeModule))
    IteratedDictContingencyTable.Record = __import__(recordModule)
    IteratedDictContingencyTable.ADTree = __import__(ADTreeModule)

class ContingencyTable(object):
    
    def __init__(self, attributeList, adTree):
        self.__attributeList = attributeList
        self.__dimension = len(attributeList)
        self.__productList = [1]*self.__dimension
        for index in range(self.__dimension-1, 0, -1):
            self.__productList[index-1] = self.__productList[index] * Record.arityList[self.__attributeList[index]-1]
        self.__CT = {}
        ctIndex = 0
        attributeIndex = 0
        stack = [adTree]
        
        while stack:
            ADN = stack.pop()
            if ADN == -1:   # make MCV
                MCV = stack.pop()
                sliceNumber = Record.arityList[attributeList[attributeIndex-1]-1]
                sliceLength = self.__productList[attributeIndex-1]
                MCVSliceStartIndex = -1*sliceLength*(sliceNumber-MCV+1)
                for attributeValue in range(1, sliceNumber+1):
                    if attributeValue != MCV:
                        for offset in range(sliceLength):
                            targetSliceStartIndex = -1*sliceLength*(sliceNumber-attributeValue+1)
                            if self.__CT.get(ctIndex + MCVSliceStartIndex + offset, None):
                                self.__CT[ctIndex + MCVSliceStartIndex + offset] -= self.__CT.get(ctIndex + targetSliceStartIndex + offset, 0)
                attributeIndex -= 1
            elif ADN:   # expand AD-node
                if attributeIndex<self.__dimension:   # AD-node that has Vary node children
                    if not leafList or ADN.getCount() >= ADTree.Rmin: # AD-node with children Vary-nodes
                        VN = ADN.getVNChild(attributeList[attributeIndex])
                        MCV = VN.getMCV()
                        stack.append(MCV)
                        stack.append(-1)
                        for attributeValue in range(Record.arityList[attributeList[attributeIndex]-1], 0, -1):
                            if attributeValue != MCV:
                                stack.append(VN.getADNChild(attributeValue))
                            else:
                                stack.append(ADN)
                        attributeIndex += 1
                    else:   # AD-node with leaf-list
                        for eachRecordNum in ADN.getLeafList(): # plus one for each of the records in leaf-list
                            recordIndex = 0
                            # calculate the index in CT of a record
                            for eachAttributeIndex in range(attributeIndex, self.__dimension):
                                recordIndex += ((Record.getRecord(eachRecordNum-1, self.__attributeList[eachAttributeIndex]-1)-1) * self.__productList[eachAttributeIndex])
                            self.__CT[ctIndex + recordIndex] = self.__CT.get(ctIndex + recordIndex, 0) + 1   # plus one on the counting in CT of the current record
                        # add nodesNumber to move ctIndex forward in CT
                        nodesNumber = 1
                        for eachArity in [Record.arityList[attributeNum-1] for attributeNum in attributeList[attributeIndex:]]:
                            nodesNumber *= eachArity
                        ctIndex += nodesNumber
                else:   # leaf AD-node
                    self.__CT[ctIndex] = ADN.getCount()
                    ctIndex += 1
            else:   # zero AD-node with subtree or a single leaf
                nodesNumber = 1
                for eachArity in [Record.arityList[attributeNum-1] for attributeNum in attributeList[attributeIndex:]]:
                    nodesNumber *= eachArity
                ctIndex += nodesNumber
                
#        print('dict', self.__CT)
                        
    def getCount(self, query):
        rowNum = 0
        for j in range(self.__dimension):
            rowNum += ((query[j]-1) * self.__productList[j])
        return self.__CT.get(rowNum, 0)
    