'''
Created on Jul 19, 2012
@author: Felix

The following improvement methods are used:
1. Using tree structure instead of linear structure such like list or dict
'''
Record = None
ADTree = None

def importModules(recordModule, ADTreeModule):
    import TreeContingencyTable
    TreeContingencyTable.Record = __import__(recordModule)
    TreeContingencyTable.ADTree = __import__(ADTreeModule)
    
class ContingencyTable(object):

    def __init__(self, attributeList, ADN):
        if attributeList:   # AD-Node that has Vary node children
            self.__children = [None]*(Record.arityList[attributeList[0]-1])
            VNChild = ADN.getVNChild(attributeList[0])
            MCV = VNChild.getMCV()
            for eachAttributeValue in range(1, Record.arityList[attributeList[0]-1]+1):
                ADNChild = VNChild.getADNChild(eachAttributeValue)
                if ADNChild:    # AD-Node with non-Zero counting
                    self.__children[eachAttributeValue-1] = ContingencyTable(attributeList[1:], ADNChild)
                elif eachAttributeValue == MCV:   # MCV AD-Node
                        self.__children[eachAttributeValue-1] = ContingencyTable(attributeList[1:], ADN)
                    # else: AD-Node with Zero counting, which already initialised as None
            
            # calculate the contingency table for MCV
            for i, eachNotMCVCT in enumerate(self.__children):
                if i+1 != MCV:
                    self.__children[MCV-1].subInTree(eachNotMCVCT)
        else:       # leaf AD-Node
            self.__count = ADN.getCount()
            self.__children = None

    def subInTree(self, other):
        if other:
            if self.__children: # self is not leaf CT node
                for i, eachChild in enumerate(self.__children):
                    if eachChild:   # eachChild is not a Zero CT node
                        eachChild.subInTree(other.__children[i])
            else: # self is a leaf CT node
                self.__count -= other.__count
        
    def getCount(self, query):
        CTN = self
        for eachNum in query:
            CTN = CTN.__children[eachNum-1]
            if not CTN:
                return 0
        return CTN.__count
