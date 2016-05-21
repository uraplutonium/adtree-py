'''
Created on Sep 21, 2014
@author: Felix
'''

class dataset:
    def __init__(self, filePath, symbolic=False):
        self.__arityNameList = []
        self.__arityList = []
        self.__data = []
        self.__arityLength = 0
        self.__dataNum = 0
        self.__arities = []
        self.__types = set()
        
        file = open(filePath)
        for i, eachline in enumerate(file):
            if i==0:
                # the first line
                self.__arityNameList = eachline[:-1].split(',')
                self.__arityLength = len(self.__arityNameList)
                for i in range(0, self.__arityLength):
                    self.__arities.append(set())
            else:
                # the data field
                self.__data.append(eachline[:-1].split(','))
                for j, eachValue in enumerate(self.__data[-1]):
                    self.__arities[j].add(eachValue)

        self.__dataNum = len(self.__data)
        for eachArity in self.__arities:
             self.__arityList.append(len(eachArity))

        # convert __data and __arities to symbolic
        if symbolic:
            for i, eachEntry in enumerate(self.__data):
                for j, eachValue in enumerate(eachEntry):
                    self.__data[i][j] = list(self.__arities[j]).index(eachValue)+1
            for j in range(0, self.__arityLength):
                self.__arities[j] = range(1, self.__arityList[j]+1)
                
                    
    def getArityList(self):
        return self.__arityList

    def getTypeList(self):
        return self.__typeList
    
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
        return self.__data.count(query)
    
    def getArityLength(self):
        return self.__arityLength
    
    def getEntry(self, row, column):
        return self.__data[row][column]

    def getArityNames(self):
        return self.__arityNameList

    def getDataNum(self):
        return self.__dataNum

    def getArities(self):
        return self.__arities

    def getTypes(self):
        return self.__types

    def displayAll(self):
        print("================================")
        print("====self.__arityNameList")
        print(self.__arityNameList)
        print("====self.__arityList")
        print(self.__arityList)
        #print("\n====self.__data")
        #print(self.__data)
        print("\n====self.__arityLength")
        print(self.__arityLength)
        print("\n====self.__dataNum")
        print(self.__dataNum)
        print("\n====self.__arities")
        for eachArity in self.__arities:
            print(eachArity)
        print("\n====self.__types")
        print(self.__types)
        print("================================")

    def printData(self):
        print("\n====self.__data")
        print(self.__data)
