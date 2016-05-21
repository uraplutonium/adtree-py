'''
Created on May 15, 2012
@author: Felix
'''

import cProfile as profile
#import pstats
import MyPStats as pstats
import random

attributeList = None
adTree = None
ct = None
    
Record = None
ADTree = None
ContingencyTable = None

def importModules(recordModule, ADTreeModule, ContingencyTableModule):
    import Profile
    Profile.Record = __import__(recordModule)
    Profile.ADTree = __import__(ADTreeModule)
    Profile.ContingencyTable = __import__(ContingencyTableModule)
    
def makeADTree():
    import Profile
    recordNums = [num for num in range(1, Profile.Record.recordsLength+1)]
    Profile.adTree = Profile.ADTree.ADNode(1, recordNums)
    
def makeContingencyTable():
    import Profile
    Profile.ct = Profile.ContingencyTable.ContingencyTable(Profile.attributeList, Profile.adTree)

def randRecords(arityLength, averageArity, recordsLength, distinctRecords=False, randArity=False):
    # sumArity >= arityLength
    sumArity = arityLength*averageArity
    
    if not randArity:
        arityList = [averageArity]*arityLength
    else:
        arityList = [1]*arityLength
        arityRange = sumArity-arityLength
        arityIndexList = random.sample(range(0, arityLength), arityLength)
        arityIndexList.sort()
        split = []
        for i in range(0, arityLength):
            split.append(random.choice(range(0, arityRange+1)))
        split.sort()
        split.insert(0, 0)
        split.append(arityRange)
        for i, eachArityIndex in enumerate(arityIndexList):
            arityList[eachArityIndex] += split[i+1]-split[i]
    
    recordsTable = []
    arityLength = len(arityList)
    if not distinctRecords:
        for i in range(0, recordsLength):
            recordsTable.append([random.randint(1, arityList[index]) for index in range(0, arityLength)])
    else:
        productList = [1]*arityLength
        for attributeIndex in range(arityLength-1, 0, -1):
            productList[attributeIndex-1] = productList[attributeIndex] * arityList[attributeIndex]
        maxDistinctRecord = productList[0]*arityList[0]
        
        if recordsLength>maxDistinctRecord:
            recordsLength = maxDistinctRecord

        sampleList = random.sample(range(0, maxDistinctRecord), recordsLength)
        
        for eachValue in sampleList:
            record = [0]*arityLength
            for attributeIndex in range(0, arityLength):
                record[attributeIndex] = int(eachValue/productList[attributeIndex]+1)
                eachValue %= productList[attributeIndex]
            recordsTable.append(record)
    return [arityList, recordsTable]

def randAttributeList(attributeLength):
    import Profile
    sampleSize = 1 if attributeLength<=1 else random.randint(1, attributeLength-1)
    attributeList = random.sample(range(1, Profile.Record.arityLength+1), sampleSize)
    attributeList.sort()
    return attributeList

def testAllFactors(profilePath, suffix, arityLengthStart, arityLengthEnd, arityLengthStep, averageArityStart, averageArityEnd, averageArityStep, randomArity, recordsLengthStart, recordsLengthEnd, recordsLengthStep, distinctRecords, RminStart, RminEnd, RminStep, attributeLengthStart, attributeLengthEnd, attributeLengthStep, sampleSize, ctSize, ADTreeModule, contingencyTableModule, recordModule):
    import Profile
    
    importModules(recordModule, ADTreeModule, contingencyTableModule)
    Profile.ADTree.importModules(recordModule)
    Profile.ContingencyTable.importModules(recordModule, ADTreeModule)
    
#    adTreeFile = open(profilePath + 'adTree_results_' + suffix + '.txt', 'w')
#    adTreeFile.close()
    ctFile = open(profilePath + 'ct_results_' + suffix + '.txt', 'w')
    ctFile.close()
    
    ADTreeIndex = 0
    CTIndex = 0
    for eachArityLength in range(arityLengthStart, arityLengthEnd+1, arityLengthStep):
        for eachAverageArity in range(averageArityStart, averageArityEnd+1, averageArityStep):
            for eachRecordsLength in range(recordsLengthStart, recordsLengthEnd+1, recordsLengthStep):
                args = randRecords(eachArityLength, eachAverageArity, eachRecordsLength, distinctRecords, randomArity)
                Profile.Record.initRecord(args)
                for eachRmin in range(RminStart, RminEnd+1, RminStep):
                    Profile.ADTree.Rmin = eachRmin
                
                    attributeEnd = attributeLengthEnd+1
                    attributeStart = attributeEnd if attributeEnd-1>eachArityLength else attributeLengthStart
                    
#                    adTreeStats = pstats.Stats(profilePath + 'none.prof')
                    ctStatsList = []
                    for eachCTStats in range(attributeStart, attributeEnd, attributeLengthStep):
                        ctStatsList.append(pstats.Stats(profilePath + 'none.prof'))
                    for eachSample in range(0, sampleSize):
                        if eachSample%10==0: print(eachSample)
                        makeADTree()
#                        profile.run('makeADTree()', profilePath + 'adTreeProfile.prof')
#                        adTreeStats.add(profilePath + 'adTreeProfile.prof')
                        for i, eachAttributeLength in enumerate(range(attributeStart, attributeEnd, attributeLengthStep)):
                            for eachCTSample in range(0, ctSize):
                                Profile.attributeList = randAttributeList(eachAttributeLength)
                                profile.run('makeContingencyTable()', profilePath + 'ctProfile.prof')
                                ctStatsList[i].add(profilePath + 'ctProfile.prof')
                            CTIndex += 1
                    ADTreeIndex += 1
                    
#                    adTreeStats.strip_dirs().dump_stats(profilePath + 'adTreeProfile.prof')
#                    adTreeStats = pstats.Stats(profilePath + 'adTreeProfile.prof')
                    
#                    cumtime = adTreeStats.getTime(('Profile.py', 25, 'makeADTree'), 'cumtime')
#                    print('#AD\t' + str(eachArityLength) +'\t' + str(eachAverageArity) +'\t' + str(eachRecordsLength) +'\t' + str(eachRmin) + '\t' + str(cumtime*1000/sampleSize))
#                    adTreeFile = open(profilePath + 'adTree_results_' + suffix + '.txt', 'a')
#                    adTreeFile.write(str(eachArityLength) + '\t' + str(eachAverageArity) + '\t' + str(eachRecordsLength) +'\t' + str(eachRmin) + '\t' + str(cumtime*1000/sampleSize) + '\n')
#                    adTreeFile.close()
                    for i, eachAttributeLength in enumerate(range(attributeStart, attributeEnd, attributeLengthStep)):
                        ctStatsList[i].strip_dirs().dump_stats(profilePath + 'ctProfile.prof')
                        ctStatsList[i] = pstats.Stats(profilePath + 'ctProfile.prof')
                        cumtime = ctStatsList[i].getTime(('Profile.py', 30, 'makeContingencyTable'), 'cumtime')
                        print('#CT\t' + str(eachArityLength) +'\t' + str(eachAverageArity) +'\t' + str(eachRecordsLength) +'\t' + str(eachRmin) +'\t' + str(eachAttributeLength) +'\t' + str(cumtime*1000/sampleSize/ctSize))
                        ctFile = open(profilePath + 'ct_results_' + suffix + '.txt', 'a')
                        ctFile.writelines(str(eachArityLength) + '\t' + str(eachAverageArity) + '\t' + str(eachRecordsLength) +'\t' + str(eachRmin) + '\t' + str(eachAttributeLength) + '\t' + str(cumtime*1000/sampleSize/ctSize) + '\n')
                        ctFile.close()
                    
def testArityLength(profilePath, arityLengthStart, arityLengthEnd, arityLengthStep, averageArity, recordsLength, Rmin, attributeLength, sampleSize, ctSize, ADTreeModule, contingencyTableModule, recordModule='ArrayRecord'):
    print('======== test arity length ========')
    testAllFactors(profilePath, 'arityLength', arityLengthStart, arityLengthEnd, arityLengthStep, averageArity, averageArity, 1, False, recordsLength, recordsLength, 1, False, Rmin, Rmin, 1, attributeLength, attributeLength, 1, sampleSize, ctSize, ADTreeModule, contingencyTableModule, recordModule)

def testArityValue(profilePath, arityLength, averageArityStart, averageArityEnd, averageArityStep, randomArity, recordsLength, Rmin, attributeLength, sampleSize, ctSize, ADTreeModule, contingencyTableModule, recordModule='ArrayRecord'):
    print('======== test arity value ========')
    testAllFactors(profilePath, 'arityValue', arityLength, arityLength, 1, averageArityStart, averageArityEnd, averageArityStep, randomArity, recordsLength, recordsLength, 1, False, Rmin, Rmin, 1, attributeLength, attributeLength, 1, sampleSize, ctSize, ADTreeModule, contingencyTableModule, recordModule)

def testRecordsLength(profilePath, arityLength, averageArity, recordsLengthStart, recordsLengthEnd, recordsLengthStep, distinctRecords, Rmin, attributeLength, sampleSize, ctSize, ADTreeModule, contingencyTableModule, recordModule='ArrayRecord'):
    print('======== test records length ========')
    suffix = 'recordsLength_distinct' if distinctRecords else 'recordsLength_random'
    testAllFactors(profilePath, suffix, arityLength, arityLength, 1, averageArity, averageArity, 1, False, recordsLengthStart, recordsLengthEnd, recordsLengthStep, distinctRecords, Rmin, Rmin, 1, attributeLength, attributeLength, 1, sampleSize, ctSize, ADTreeModule, contingencyTableModule, recordModule)
    
def testAttributeLength(profilePath, arityLength, averageArity, recordsLength, Rmin, attributeLengthStart, attributeLengthEnd, attributeLengthStep, sampleSize, ctSize, ADTreeModule, contingencyTableModule, recordModule='ArrayRecord'):
    print('======== test attribute length ========')
    testAllFactors(profilePath, 'attributeLength', arityLength, arityLength, 1, averageArity, averageArity, 1, False, recordsLength, recordsLength, 1, False, Rmin, Rmin, 1, attributeLengthStart, attributeLengthEnd, attributeLengthStep, sampleSize, ctSize, ADTreeModule, contingencyTableModule, recordModule)
    
def testRmin(profilePath, arityLength, averageArity, recordsLength, RminStart, RminEnd, RminStep, attributeLength, sampleSize, ctSize, ADTreeModule, contingencyTableModule, recordModule='ArrayRecord'):
    print('======== test Rmin ========')
    testAllFactors(profilePath, 'Rmin', arityLength, arityLength, 1, averageArity, averageArity, 1, False, recordsLength, recordsLength, 1, False, RminStart, RminEnd, RminStep, attributeLength, attributeLength, 1, sampleSize, ctSize, ADTreeModule, contingencyTableModule, recordModule)

def testSuite(contingencyTableModule, path, sampleSize, ctSize, arityLength, averageArity, recordsLength, Rmin, attributeLength):
    print('######## ' + contingencyTableModule + ' ########')
    ADTreeModule = 'SparseADTree'
    testArityLength(path, 1, 15, 1, averageArity, recordsLength, Rmin, attributeLength, sampleSize, ctSize, ADTreeModule, contingencyTableModule)
    testArityValue(path, arityLength, 2, 11, 1, False, recordsLength, Rmin, attributeLength, sampleSize, ctSize, ADTreeModule, contingencyTableModule)
    testArityValue(path, arityLength, 2, 11, 1, True, recordsLength, Rmin, attributeLength, sampleSize, ctSize, ADTreeModule, contingencyTableModule)
    testRecordsLength(path, arityLength, averageArity, 0, 50000, 2000, False, Rmin, attributeLength, sampleSize, ctSize, ADTreeModule, contingencyTableModule)
    testRecordsLength(path, 14, averageArity, 0, 10000, 500, True, Rmin, attributeLength, sampleSize, ctSize, ADTreeModule, contingencyTableModule)
    testAttributeLength(path, 17, averageArity, recordsLength, Rmin, 1, 17, 1, sampleSize, ctSize, ADTreeModule, contingencyTableModule)

    if contingencyTableModule != 'FullContingencyTable' and contingencyTableModule != 'TreeContingencyTable' and contingencyTableModule != 'IteratedTreeContingencyTable':
        ADTreeModule = 'LeafSparseADTree'
        testRmin(path, arityLength, averageArity, 10000, 0, 10000, 200, attributeLength, sampleSize, ctSize, ADTreeModule, contingencyTableModule)

if __name__ == '__main__':
    path = '/media/uraplutonium/Cardboard/Workspace/AD-Tree-2014/src/package/profile/'
#    path = '/usr/fd570/adtree/profile/'
    seed = random.randint(0, 99)

    sampleSize = 2    #2
    ctSize = 200
    arityLength = 7
    averageArity = 2
    recordsLength = 10000
    Rmin = -1
    attributeLength = 5
    
    print('seed:' + str(seed))
        
    subPath1 = path + 'fullCT/'
    random.seed(seed)
    testSuite('FullContingencyTable', subPath1, sampleSize, ctSize, arityLength, averageArity, recordsLength, Rmin, attributeLength)
     
    subPath2 = path + 'listCT/'
    random.seed(seed)
    testSuite('ListContingencyTable', subPath2, sampleSize, ctSize, arityLength, averageArity, recordsLength, Rmin, attributeLength)
    
    subPath3 = path + 'iterListCT/'
    random.seed(seed)
    testSuite('IteratedListContingencyTable', subPath3, sampleSize, ctSize, arityLength, averageArity, recordsLength, Rmin, attributeLength)
    
    subPath4 = path + 'dictCT/'
    random.seed(seed)
    testSuite('DictContingencyTable', subPath4, sampleSize, ctSize, arityLength, averageArity, recordsLength, Rmin, attributeLength)
    
    subPath5 = path + 'iterDictCT/'
    random.seed(seed)
    testSuite('IteratedDictContingencyTable', subPath5, sampleSize, ctSize, arityLength, averageArity, recordsLength, Rmin, attributeLength)

    subPath6 = path + 'treeCT/'
    random.seed(seed)
    testSuite('TreeContingencyTable', subPath6, sampleSize, ctSize, arityLength, averageArity, recordsLength, Rmin, attributeLength)
    
    subPath7 = path + 'iterTreeCT/'
    random.seed(seed)
    testSuite('IteratedTreeContingencyTable', subPath7, sampleSize, ctSize, arityLength, averageArity, recordsLength, Rmin, attributeLength)
