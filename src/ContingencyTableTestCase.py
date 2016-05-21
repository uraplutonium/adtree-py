#!/home/uraplutonium/Documents/Python-3.2.3 python
'''
Created on May 24, 2012
@author: Felix
'''
import unittest
import random

largeTest = True
leafTest = False

# Data for empty records test
arityList1 = [5, 7, 2]
recordsTable1 = []

# Data for one arity test
arityList2 = [6, 2]
recordsTable2 = [[5, 1],
                 [4, 1],
                 [6, 1],
                 [4, 1],
                 [1, 1],
                 [2, 1],
                 [2, 1],
                 [4, 1]]

# Data for arity value one test
arityList3 = [1, 3, 1, 5]
recordsTable3 = [[1, 2, 1, 4],
                 [1, 2, 1, 5],
                 [1, 3, 1, 1],
                 [1, 1, 1, 1],
                 [1, 2, 1, 4],
                 [1, 3, 1, 5],
                 [1, 1, 1, 1],
                 [1, 1, 1, 5]]

# Data for one, all and discontinuous attributes test
arityList4 = [2, 4, 2, 6]
recordsTable4 = [[1, 1, 2, 1],
                [1, 2, 1, 1],
                [1, 2, 1, 1],
                [1, 2, 2, 3],
                [1, 2, 2, 4],
                [1, 2, 2, 1],
                [1, 4, 1, 2],
                [1, 4, 2, 2],
                [1, 4, 2, 2],
                [2, 1, 1, 6],
                [2, 1, 1, 5],
                [2, 1, 1, 6],
                [2, 1, 2, 3],
                [2, 1, 2, 2],
                [2, 1, 2, 1],
                [2, 1, 2, 2],
                [2, 2, 2, 3],
                [2, 3, 1, 5],
                [2, 3, 1, 6],
                [2, 3, 2, 5],
                [2, 3, 2, 5],
                [2, 3, 2, 4]]

# Data for different Rmin test
arityList5 = [2, 4, 2]
recordsTable5 = [[1, 1, 2],
                [1, 2, 1],
                [1, 2, 1],
                [1, 2, 2],
                [1, 2, 2],
                [1, 2, 2],
                [1, 3, 1],
                [1, 3, 1],
                [1, 3, 1],
                [1, 3, 1],
                [1, 4, 1],
                [1, 4, 2],
                [1, 4, 2],
                [2, 1, 1],
                [2, 1, 1],
                [2, 1, 1],
                [2, 1, 2],
                [2, 1, 2],
                [2, 1, 2],
                [2, 1, 2],
                [2, 2, 2],
                [2, 3, 1],
                [2, 3, 1],
                [2, 3, 2],
                [2, 3, 2],
                [2, 3, 2],
                [2, 4, 1],
                [2, 4, 1],
                [2, 4, 1],
                [2, 4, 1]]

class ContingencyTableTest(unittest.TestCase): 
    
    def setUp(self):
        self.Record = None
        self.ADTree = None
        self.ContingencyTable = None
        
#        random.seed(0)

        recordModule = 'ArrayRecord'
#        recordModule = 'FileRecord'

#        ADTreeModule = 'FullADTree'
#        ADTreeModule = 'ZeroADTree'
        ADTreeModule = 'SparseADTree'
#        ADTreeModule = 'LeafFullADTree'
#        ADTreeModule = 'LeafSparseADTree'

        contingencyTableModule = 'FullContingencyTable'
#        contingencyTableModule = 'ListContingencyTable'
#        contingencyTableModule = 'IteratedListContingencyTable'
#        contingencyTableModule = 'DictContingencyTable'
#        contingencyTableModule = 'IteratedDictContingencyTable'
#        contingencyTableModule = 'TreeContingencyTable'
#        contingencyTableModule = 'IteratedTreeContingencyTable'
        
        self.importModules(recordModule, ADTreeModule, contingencyTableModule)
        self.ADTree.importModules(recordModule)
        self.ContingencyTable.importModules(recordModule, ADTreeModule)
    
    def importModules(self, recordModule, ADTreeModule, ContingencyTableModule):
        self.Record = __import__(recordModule)
        self.ADTree = __import__(ADTreeModule)
        self.ContingencyTable = __import__(ContingencyTableModule)
        
    def queryGenerator(self, attributeList=None):
        attributeList = attributeList if attributeList else [n for n in range(1, self.Record.arityLength+1)]
        queryNum = 1
        for eachArity in [self.Record.arityList[attributeNum-1] for attributeNum in attributeList]:
            queryNum *= eachArity
                    
        for eachQueryNum in range(0, queryNum):
            query = []
            for eachArity in [self.Record.arityList[attributeNum-1] for attributeNum in attributeList]:
                query.append(eachQueryNum % eachArity + 1)
                eachQueryNum //= eachArity
            yield query
        
    def randQueryGenerator(self, queryListLength):
        attributeList = [n for n in range(1, self.Record.arityLength+1)]
        queryNum = 1
        for eachArity in [self.Record.arityList[attributeNum-1] for attributeNum in attributeList]:
            queryNum *= eachArity
            
        queryListLength = queryListLength if queryListLength < queryNum else queryNum
        queryList = random.sample(range(1, queryNum+1), queryListLength)
        
        for eachQueryNum in queryList:
            query = []
            for eachArity in [self.Record.arityList[attributeNum-1] for attributeNum in attributeList]:
                query.append(eachQueryNum % eachArity + 1)
                eachQueryNum //= eachArity
            yield query
    
    def randArityList(self, arityLength, maxArityValue):
        arityList = []
        for i in range(0, arityLength):
            arityList.append(random.randint(1, maxArityValue))
        return arityList
    
    def randRecordsTable(self, recordLength, arityList):
        recordsTable = []
        arityLength = len(arityList)
        for i in range(0, recordLength):
            recordsTable.append([random.randint(1, arityList[index]) for index in range(0, arityLength)])
        return recordsTable
    
    #================ Test Cases ================

    def testEmptyRecords(self):
        # Test on empty records
        self.Record.initRecord([arityList1, recordsTable1])
        recordNums = [num for num in range(1, self.Record.recordsLength+1)]        
        adTree = self.ADTree.ADNode(1, recordNums)
        
        # make a contingency table
        attributeList = [attribute for attribute in range(1, self.Record.arityLength+1)]
        ct = self.ContingencyTable.ContingencyTable(attributeList, adTree)        # generate every possible query and test on each queries
        for eachQuery in self.queryGenerator():
            expectedCount = recordsTable1.count(eachQuery)
            actualCount = ct.getCount(eachQuery)
#            print('Q:', eachQuery, 'C_exp:', expectedCount, 'C_act:', actualCount)
            self.assertEquals(expectedCount, actualCount)
    
    def testOneArity(self):
        # Test on data with only one arity 
        self.Record.initRecord([arityList2, recordsTable2])
        recordNums = [num for num in range(1, self.Record.recordsLength+1)]        
        adTree = self.ADTree.ADNode(1, recordNums)

        # make a contingency table
        attributeList = [attribute for attribute in range(1, self.Record.arityLength+1)]
        ct = self.ContingencyTable.ContingencyTable(attributeList, adTree)        # generate every possible query and test on each queries
        for eachQuery in self.queryGenerator():
            expectedCount = recordsTable2.count(eachQuery)
            actualCount = ct.getCount(eachQuery)
#            print('Q:', eachQuery, 'C_exp:', expectedCount, 'C_act:', actualCount)
            self.assertEquals(expectedCount, actualCount)
    
    def testArityValueOne(self):
        # Test on data with arity value 1
        self.Record.initRecord([arityList3, recordsTable3])
        recordNums = [num for num in range(1, self.Record.recordsLength+1)]        
        adTree = self.ADTree.ADNode(1, recordNums)
        
        # make a contingency table
        attributeList = [attribute for attribute in range(1, self.Record.arityLength+1)]
        ct = self.ContingencyTable.ContingencyTable(attributeList, adTree)
        # generate every possible query and test on each queries
        for eachQuery in self.queryGenerator():
            expectedCount = recordsTable3.count(eachQuery)
            actualCount = ct.getCount(eachQuery)
#            print('Q:', eachQuery, 'C_exp:', expectedCount, 'C_act:', actualCount)
            self.assertEquals(expectedCount, actualCount)

    def testOneAttribute(self):
        # Test on one particular attribute
        self.Record.initRecord([arityList4, recordsTable4])
        recordNums = [num for num in range(1, self.Record.recordsLength+1)]        
        adTree = self.ADTree.ADNode(1, recordNums)
        
        # test with one attribute randomly
        attributeList = [random.randint(1, self.Record.arityLength)]
        # make a contingency table
        ct = self.ContingencyTable.ContingencyTable(attributeList, adTree)
        # generate every possible query and test on each queries
        records = [[self.Record.getRecord(rowNum, attributeList[0]-1)] for rowNum in range(0, self.Record.recordsLength)]
        for eachQuery in self.queryGenerator(attributeList):#[[query] for query in range(1, self.ADTree.arityList[columnNum-1]+1)]:
            expectedCount = records.count(eachQuery)
            actualCount = ct.getCount(eachQuery)
#            print('Q:', eachQuery, 'C_exp:', expectedCount, 'C_act:', actualCount)
            self.assertEquals(expectedCount, actualCount)

    def testAllAttributes(self):
        # Test on all attributes
        self.Record.initRecord([arityList4, recordsTable4])
        recordNums = [num for num in range(1, self.Record.recordsLength+1)]        
        adTree = self.ADTree.ADNode(1, recordNums)
        
        # make a contingency table
        attributeList = [attribute for attribute in range(1, self.Record.arityLength+1)]
        ct = self.ContingencyTable.ContingencyTable(attributeList, adTree)
        # generate every possible query and test on each queries
        for eachQuery in self.queryGenerator():
            expectedCount = recordsTable4.count(eachQuery)
            actualCount = ct.getCount(eachQuery)
#            print('Q:', eachQuery, 'C_exp:', expectedCount, 'C_act:', actualCount)
            self.assertEquals(expectedCount, actualCount)
    
    def testDiscontinuousAttributes(self):
        # Test on several discontinuous attributes
        self.Record.initRecord([arityList4, recordsTable4])
        recordNums = [num for num in range(1, self.Record.recordsLength+1)]        
        adTree = self.ADTree.ADNode(1, recordNums)
        
        for i in range(1, 11):
            attributeList = random.sample(range(1, self.Record.arityLength+1), random.randint(1, self.Record.arityLength-1))
            attributeList.sort()
            
            # make a contingency table
            ct = self.ContingencyTable.ContingencyTable(attributeList, adTree)            
            # generate every possible query and test on each queries
            records = [[self.Record.getRecord(rowNum, columnNum-1) for columnNum in attributeList] for rowNum in range(0, self.Record.recordsLength)]
            for eachQuery in self.queryGenerator(attributeList):
                expectedCount = records.count(eachQuery)
                actualCount = ct.getCount(eachQuery)
#                print('Q:', eachQuery, 'C_exp:', expectedCount, 'C_act:', actualCount)
                self.assertEquals(expectedCount, actualCount)
                
    def testDifferentRmin(self):
        # Test on all attributes
        if not leafTest:
            return
        for r in range(-1, 30):
            self.Record.initRecord([arityList5, recordsTable5])
            self.ADTree.Rmin = r
            recordNums = [num for num in range(1, self.Record.recordsLength+1)]        
            adTree = self.ADTree.ADNode(1, recordNums)
#            print('Rmin:', r)
            
            # make a contingency table
            attributeList = [attribute for attribute in range(1, self.Record.arityLength+1)]
            ct = self.ContingencyTable.ContingencyTable(attributeList, adTree)
            # generate every possible query and test on each queries
            for eachQuery in self.queryGenerator():
                expectedCount = recordsTable5.count(eachQuery)
                actualCount = ct.getCount(eachQuery)
#                print('Q:', eachQuery, 'C_exp:', expectedCount, 'C_act:', actualCount)
                self.assertEquals(expectedCount, actualCount)
            
    def testNumerousCases(self):
        # Test on several random discontinuous attributes in a large numbers of test cases
        if not largeTest:
            return
        for times in range(0, 1000):
            arityList = self.randArityList(4, 4)
            self.Record.initRecord([arityList, self.randRecordsTable(500, arityList)])
            recordNums = [num for num in range(1, self.Record.recordsLength+1)]        
            adTree = self.ADTree.ADNode(1, recordNums)
            
            # make a contingency table
            attributeList = [attribute for attribute in range(1, self.Record.arityLength+1)]
            ct = self.ContingencyTable.ContingencyTable(attributeList, adTree)
            # generate every possible query and test on each queries
            for eachQuery in self.randQueryGenerator(500):
                expectedCount = self.Record.count(eachQuery)
                actualCount = ct.getCount(eachQuery)
#                print('Q:', eachQuery, 'C_exp:', expectedCount, 'C_act:', actualCount)
                self.assertEquals(expectedCount, actualCount)
    
    def testLargeArity(self):
        # Test on data with large airty value
        if not largeTest:
            return
        arityList = self.randArityList(2, 1000)
        self.Record.initRecord([arityList, self.randRecordsTable(500, arityList)])
        recordNums = [num for num in range(1, self.Record.recordsLength+1)]        
        adTree = self.ADTree.ADNode(1, recordNums)
        
        # make a contingency table
        attributeList = [attribute for attribute in range(1, self.Record.arityLength+1)]
        ct = self.ContingencyTable.ContingencyTable(attributeList, adTree)
        # generate every possible query and test on each queries
        for eachQuery in self.randQueryGenerator(500):
            expectedCount = self.Record.count(eachQuery)
            actualCount = ct.getCount(eachQuery)
#            print('Q:', eachQuery, 'C_exp:', expectedCount, 'C_act:', actualCount)
            self.assertEquals(expectedCount, actualCount)
    
    def testNumerousArity(self):
        # Test on data with a large number of arities
        if not largeTest:
            return
        arityList = self.randArityList(20, 2)
        self.Record.initRecord([arityList, self.randRecordsTable(500, arityList)])
        recordNums = [num for num in range(1, self.Record.recordsLength+1)]        
        adTree = self.ADTree.ADNode(1, recordNums)
        
        # make a contingency table
        attributeList = [attribute for attribute in range(1, self.Record.arityLength+1)]
        ct = self.ContingencyTable.ContingencyTable(attributeList, adTree)
        # generate every possible query and test on each queries
        for eachQuery in self.randQueryGenerator(500):
            expectedCount = self.Record.count(eachQuery)
            actualCount = ct.getCount(eachQuery)
#            print('Q:', eachQuery, 'C_exp:', expectedCount, 'C_act:', actualCount)
            self.assertEquals(expectedCount, actualCount)
    
    def testNumerousRecords(self):
        # Test on large number of records
        if not largeTest:
            return
        arityList = self.randArityList(2, 2)
        self.Record.initRecord([arityList, self.randRecordsTable(1000000, arityList)])
        recordNums = [num for num in range(1, self.Record.recordsLength+1)]        
        adTree = self.ADTree.ADNode(1, recordNums)
        
        # make a contingency table
        attributeList = [attribute for attribute in range(1, self.Record.arityLength+1)]
        ct = self.ContingencyTable.ContingencyTable(attributeList, adTree)
        # generate every possible query and test on each queries
        for eachQuery in self.randQueryGenerator(500):
            expectedCount = self.Record.count(eachQuery)
            actualCount = ct.getCount(eachQuery)
#            print('Q:', eachQuery, 'C_exp:', expectedCount, 'C_act:', actualCount)
            self.assertEquals(expectedCount, actualCount)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()