'''
Created on Jul 30, 2012
@author: Felix

The following improvement methods are used:
1. Using tree structure instead of linear structure such like list or dict
2. Using one loop/iteration to build Contingency table instead of recursion
3. Using list of lists to represent tree structure instead of having a "Node" class
'''
Record = None
ADTree = None

def importModules(recordModule, ADTreeModule):
    import IteratedTreeContingencyTable
    IteratedTreeContingencyTable.Record = __import__(recordModule)
    IteratedTreeContingencyTable.ADTree = __import__(ADTreeModule)

class ContingencyTable(object):
    
    def __init__(self, attributeList, adTree):        
        attributeIndex = 0
        self.__ctTree = [0]*Record.arityList[attributeList[attributeIndex]-1]
        self.__dimension = len(attributeList)
        stack = [self.__ctTree, None, adTree]        
        
        while stack:
            ADN = stack.pop()
            if ADN == -1:   # make MCV
                MCV = stack.pop()
                ctTree = stack.pop()
                if attributeIndex > self.__dimension-1: # if the depth of whole ctTree is only 1
                    for eachAttributeValue in range(1, Record.arityList[attributeList[attributeIndex-1]-1]+1):
                        if eachAttributeValue != MCV:
                            ctTree[MCV-1] -= ctTree[eachAttributeValue-1]
                else:
                    for eachAttributeValue in range(1, Record.arityList[attributeList[attributeIndex-1]-1]+1):
                        if eachAttributeValue != MCV:
                            isResultZero = self.subInTree(ctTree[MCV-1], ctTree[eachAttributeValue-1], self.__dimension-attributeIndex)
                            if isResultZero:
                                ctTree[MCV-1] = 0
                attributeIndex -= 1
            elif ADN:   # expand AD-node            
                if attributeIndex<self.__dimension:   # AD-node that has Vary node children             
                    atrValue = stack.pop()
                    ctTree = stack[-1]  # note it's not stack.pop()
                    VN = ADN.getVNChild(attributeList[attributeIndex])
                    MCV = VN.getMCV()
                    stack.append(MCV)
                    stack.append(-1)
                    for attributeValue in range(Record.arityList[attributeList[attributeIndex]-1], 0, -1):
                        ADNToPush = None
                        if attributeValue != MCV:
                            ADNToPush = VN.getADNChild(attributeValue)
                        else:
                            ADNToPush = ADN
                        if ADNToPush:
                            if attributeIndex+1<self.__dimension:   # if the depth of ctTree is larger than 1
                                ctTree[attributeValue-1] = [0]*Record.arityList[attributeList[attributeIndex+1]-1]
                                stack.append(ctTree[attributeValue-1])
                            else:    
                                stack.append(ctTree)
                            stack.append(attributeValue)
                        stack.append(ADNToPush)
                    attributeIndex += 1
                else:   # leaf AD-node               
                    atrValue = stack.pop()
                    ctTree = stack.pop() 
                    ctTree[atrValue-1] = ADN.getCount()
            # else: zero AD-node with subtree or a single leaf
            
    def subInTree(self, MCVTree, otherTree, depth):
        if otherTree and MCVTree:
            isMCVTreeZero = False
            for i, eachChild in enumerate(MCVTree):
                if depth<=1:
                    MCVTree[i] -= otherTree[i]
                    isMCVTreeZero = isMCVTreeZero or MCVTree[i]
                else:
                    isResultZero = self.subInTree(MCVTree[i], otherTree[i], depth-1)
                    if isResultZero:
                        MCVTree[i] = 0
                    isMCVTreeZero = isMCVTreeZero or (not isResultZero)
            isMCVTreeZero = not isMCVTreeZero
            return isMCVTreeZero
                        
    def getCount(self, query):
        CTN = self.__ctTree
        for eachNum in query:
            CTN = CTN[eachNum-1]
            if not CTN:
                return 0
        return CTN
    