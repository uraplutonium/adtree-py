'''
Created on Sep 21, 2014
@author: Felix
'''

class FakeDateset:
    def __init__(self, bn, dataNum):
        self.__bn = bn
        self.__arityNameList = []
        self.__arityList = []
        self.__arityLength = len(bn.nodes)
        self.__dataNum = dataNum
        self.__arities = []
        self.__types = set()

        for eachNode in bn.nodes:
            self.__arityNameList.append(eachNode.name)
            self.__arities.append(set())
            self.__arities[-1].add('True')
            self.__arities[-1].add('False')
            self.__arityList.append(2)

        self.__types.add('True')
        self.__types.add('False')
        
    def getArityList(self):
        return self.__arityList

    def count(self, query):
        if '*' not in query:
            return self.__fullCount(query)
        else:
            for i, eachAttribute in enumerate(query):
                if eachAttribute != '*':
                    continue
                else:
                    c = 0
                    for eachValue in self.__arities[i]:
                        tmpQuery = query[:i] + [eachValue] + query[i+1:]
                        #print(tmpQuery)
                        c = c+self.count(tmpQuery)
                    return c

    def __fullCount(self, query):
        prob = 1
        for i, eachValue in enumerate(query):
            probKey = self.__bn.nodes[i].name + "=" + eachValue
            if self.__bn.nodes[i].parents:
                probKey = probKey + '|'
                names = []
                values = []
                for eachParentNode in self.__bn.nodes[i].parents:
                    names.append(eachParentNode.name)
                    a = self.__arityNameList.index(eachParentNode.name)
                    values.append(query[self.__arityNameList.index(eachParentNode.name)])
                probKey = probKey + str(names) + '=' + str(values)
                
            #print(probKey + " : " + str(self.__bn.nodes[i].p[probKey]))
            prob = prob*self.__bn.nodes[i].p[probKey]
        return  int(round(prob*self.__dataNum))
    
    def getArityLength(self):
        return self.__arityLength
    
    def getArityNames(self):
        return self.__arityNameList

    def getDataNum(self):
        return self.__dataNum

    def getArities(self):
        return self.__arities

    def getTypes(self):
        return self.__types
    
