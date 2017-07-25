import math
import FileRecord as Record
import SparseADTree as ADTree
#import IteratedTreeContingencyTable as ContingencyTable
import IteratedListContingencyTable as ContingencyTable
#import ListContingencyTable as ContingencyTable
#import FullContingencyTable as ContingencyTable
#import TreeContingencyTable as ContingencyTable
#import IteratedTreeContingencyTable as ContingencyTable

ContingencyTable = None
adtree = None

def importContabModule(contabModule):
    import EvaFunctions
    EvaFunctions.ContingencyTable = __import__(contabModule)

def initADTree(dataPath):
    import EvaFunctions
    Record.initRecord([dataPath])
    ADTree.importModules('FileRecord')
    ContingencyTable.importModules('FileRecord', 'SparseADTree')
    recordNums = [num for num in range(1, Record.recordsLength+1)]
    EvaFunctions.adtree = ADTree.ADNode(1, recordNums)

def BIC(bn, dataset, use_adtree=False):
    print("========================================")
    print("Start calculating BIC score for bayesnet \"" + bn.name + ("\" with" if use_adtree else "\" without") + " ADTree acceleration.")
    import EvaFunctions
    
    bicScore = 0
    penalisation = 0
    # the first summation for each node in the bayesnet
    for eachNode in bn.nodes:
        print("Calculating for node " + eachNode.name)
        # compute the index number of the current node
        i = dataset.getArityNames().index(eachNode.name)
        # compute the list that contains index of the parents of the current node
        parentsIndexList = [dataset.getArityNames().index(parentNode.name) for parentNode in (eachNode.parents)]
        
        # if the current node has no parents, compute the next one
        if not parentsIndexList:
            continue

        contab1 = None
        contab2 = None
        if use_adtree:
            bufList1 = parentsIndexList[:]
            bufList2 = parentsIndexList[:]
            bufList1.sort()
            bufList2.append(i)
            bufList2.sort()
            # calculate the contab1 for m1(mij*) according to the parentList
            contab1 = EvaFunctions.ContingencyTable.ContingencyTable([v+1 for v in bufList1], adtree)
            # calculate the contab2 for m1(mijk) according to the parentList.append(i) (bufList2)
            contab2 = EvaFunctions.ContingencyTable.ContingencyTable([v+1 for v in bufList2], adtree)
            
        #print("start computing for node " + eachNode.name)
        
        # the queris to get all the m_ij* for each combination of parents values(j)
        queries = []

        # generate every possible queries
        queryNum = 1
        for eachParentIndex in parentsIndexList:
            queryNum *= dataset.getArityList()[eachParentIndex]
        print("qi = " + str(queryNum))
        
        # generate each query, such like (T, *, F), for the second summation
        for eachQueryNum in range(0, queryNum):
            tmpQueryNum = eachQueryNum
            query = []
            for eachAttribute in range(dataset.getArityLength()-1, -1, -1):
                if eachAttribute in parentsIndexList:
                    arity = dataset.getArityList()[eachAttribute]
                    query.insert(0, list(dataset.getArities()[eachAttribute])[tmpQueryNum % arity])
                    tmpQueryNum = tmpQueryNum/arity
                else:
                    query.insert(0, '*')
                    
            ###########################################
            # this is the calculation of mij*
            m1=0
            if use_adtree:
                symQuery1 = [list(dataset.getArities()[eachValue]).index(query[eachValue])+1 for eachValue in bufList1]
                m1 = contab1.getCount(symQuery1)
            else:
                m1 = dataset.count(query)
            #print("mij* " + str(query) + " = " + str(m1))
            ###########################################

            # the third summation for each value of the current node
            for eachValueIndex in range(0, dataset.getArityList()[i]):
                tmpQuery = query
                tmpQuery[i] = list(dataset.getArities()[i])[eachValueIndex]

                ###########################################
                # this is the calculation of mijk
                m2 = 0
                if use_adtree:
                    symQuery2 = [list(dataset.getArities()[eachValue]).index(query[eachValue])+1 for eachValue in bufList2]
                    m2 = contab2.getCount(symQuery2)
                else:
                    m2 = dataset.count(tmpQuery)
                #print("mijk " + str(tmpQuery) + " = " + str(m2))
                ###########################################

                if m2==0:
                    continue

                if m1==0:
                    continue # should this be allowed happening?

                # calculate the first part
                buf = float(m2) * math.log((float(m2)/float(m1)), 10)
                #print("first part:" + str(buf))
                bicScore = bicScore + buf
        # calculate the penalisation
        penalisation = penalisation + queryNum*(dataset.getArityList()[i]-1)
        # the end of first summation

    # finish the calculation of penalisation
    penalisation = penalisation/2*math.log(float(dataset.getDataNum()), 10)
    print("Calculation finished.")
    print("Score " + str(bicScore))
    print("Penalise " + str(penalisation))
    print("========================================")
    return bicScore-penalisation
