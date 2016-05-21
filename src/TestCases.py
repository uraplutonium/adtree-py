from FDNets import *
import FakeDateset
from EvaFunctions import *
from Dataset import *
import random
from BayesNetNode import *
from FileRecord import *
import cProfile
import MyPStats as pstats

profPath = '/media/uraplutonium/Cardboard/Workspace/AD-Tree-2014/'
testData = None
testNet = None

def calculateBIC(): # this line should be fixed at line 16 for cProfile
    import TestCases
    bic = BIC(TestCases.testNet, TestCases.testData, True)
    print('THE BIC: ' + str(bic))
    
def testEvaFunctions():
    bayesNet = fdnet
    FDNets.update()
    dataset = FakeDateset.FakeDateset(bayesNet, 1000)
    bic = BIC(testnet, dataset)
    #bic = BIC(bayesNet, dataset)
    print('BIC SCORE:')
    print(bic)

def testFDNet():
    print('test FDNet')
    b = FakeDateset.FakeDateset(fdnet, 1000)
    print(b.count(['True', 'True', 'True']))
    print(b.count(['False', 'True', 'False']))

def testDataset(dataPath):
    a = dataset(dataPath, True)
    a.displayAll()


def testFileRecord():
    initRecord(['/media/uraplutonium/Cardboard/Workspace/AD-Tree-2014/src/iris_labelled.csv'])
    print(getRecord(0, 0))
    print('----------')
    print(getRecord(57, 1))
    print('----------')
    print(getRecord(149, 3))

    print('now we are going to make some queries')

    data.displayAll()

    q1 = [1, 1, 1, 1, 1]
    q2 = [7, 8, 8, 2, 1]
    q3 = [10, 10, 9, 10, 3]

    print('q1:' + str(q1))
    print(count(q1))
    print('q2:' + str(q2))
    print(count(q2))
    print('q3:' + str(q3))
    print(count(q3))

def testADTree():
    import FileRecord as Record
    import SparseADTree as ADTree
    import IteratedListContingencyTable as ContingencyTable
    initRecord(['/media/uraplutonium/Cardboard/Workspace/AD-Tree-2014/src/iris_labelled.csv'])
    ADTree.importModules('FileRecord')
    ContingencyTable.importModules('FileRecord', 'SparseADTree')
    recordNums = [num for num in range(1, Record.recordsLength+1)]
    adtree = ADTree.ADNode(1, recordNums)
    contab = ContingencyTable.ContingencyTable([1, 3], adtree)
    for i in range(10):
        query = [i, 1]
        count = contab.getCount(query)
        print('Q:', query, 'C:', count)
   
'''
Add random links to the given Bayesian network
'''
def randStruct(net):
    import TestCases
    candidates = net.nodes[:]
    parentNum = random.randint(1, len(net.nodes)-1)
    for i in range(0, parentNum):
        # childIndex means how many children are there in the bayesnet
        # this is the alpha
        #childIndex = random.randint(0, int(round(float(len(candidates))/3))-1)
        childIndex = random.randint(0, len(candidates)-1)
        child = candidates[childIndex]
        candidates[childIndex:childIndex+1] = []
        # the second randint means how many parents does a child have
        # this is the beta
        for eachParent in random.sample(candidates, random.randint(1, int(round(float(len(candidates))/2)))):
        #for eachParent in random.sample(candidates, random.randint(1, int(round(float(len(candidates))/8)))):
        #for eachParent in random.sample(candidates, 1):
            Node.makePair(eachParent, child)
            print('PAIR: ' + child.name + ' <- ' + eachParent.name)


def testBIC(dataPath, contabName, l_init, l_getCount):
    import TestCases
    print('======== test for ' + contabName + ' ========')
    random.seed(0)

    # 1. init the dataset
    TestCases.testData = dataset(dataPath)
    #TestCases.testData.displayAll()
    
    T = 10
    BIC_ncalls = 0
    BIC_cumtime = 0
    CT_ncalls = 0
    CT_cumtime = 0
    COUNT_ncalls = 0
    COUNT_cumtime = 0
    
    for i in range(0, T):
        print('======== ' + str(i) + ' ========')

        importContabModule(contabName)
        
        # build a bayesnet randomly according to the info from the dataset
        # 2. create the bayesnet
        TestCases.testNet = BayesNet(contabName + '_bayesnet')
    
        # 3. create nodes
        x = 100
        y = 100
        for i in range(0, TestCases.testData.getArityLength()):
            newNode = Node(TestCases.testData.getArityNames()[i],
                        TestCases.testData.getArityNames()[i] + ' discription',
                        x, y,
                        list(TestCases.testData.getArities()[i]))
            if x<=500:
                x += 100
            else:
                y += 100
                x = 100
            TestCases.testNet.add_node(newNode)
        
        # 4. initialise the ADtree
        initADTree(dataPath)

        # 5. randomly generate the structure
        randStruct(TestCases.testNet)

        # 6. calculate the BIC of irisRandNet upon the irisdata
        calculateBIC()

        '''
        import TestCases
        cProfile.run('calculateBIC()', TestCases.profPath + contabName + '.prof')
        p = pstats.Stats(TestCases.profPath + contabName + '.prof')
        p.strip_dirs().dump_stats(TestCases.profPath + contabName + '.prof')
        p = pstats.Stats(TestCases.profPath + contabName + '.prof')
        '''
        #p.print_stats()

        '''
        BIC_ncalls = BIC_ncalls + p.getTime(('TestCases.py', 15, 'calculateBIC'), 'ncalls')
        BIC_cumtime = BIC_cumtime + p.getTime(('TestCases.py', 15, 'calculateBIC'), 'cumtime')
        CT_ncalls = CT_ncalls + p.getTime((contabName+'.py', l_init, '__init__'), 'ncalls')
        CT_cumtime = CT_cumtime + p.getTime((contabName+'.py', l_init, '__init__'), 'cumtime')
        COUNT_ncalls = COUNT_ncalls + p.getTime((contabName+'.py', l_getCount, 'getCount'), 'ncalls')
        COUNT_cumtime = COUNT_cumtime + p.getTime((contabName+'.py', l_getCount, 'getCount'), 'cumtime')
        '''

    print('iteration times: ' + str(T))
    #print('BIC_ncalls: ' + str(BIC_ncalls) + ' BIC_cumtime: ' + str(BIC_cumtime))
    #print('CT_ncalls: ' + str(CT_ncalls) + ' CT_cumtime: ' + str(CT_cumtime))
    #print('COUNT_ncalls: ' + str(COUNT_ncalls) + ' COUNT_cumtime: ' + str(COUNT_cumtime))
    #ctFile = open(profPath + 'BIC_profile.csv', 'a')
    #ctFile.writelines(str(contabName) + ',' + str(BIC_ncalls) + ',' + str(BIC_cumtime) + ',' + str(CT_ncalls) + ',' + str(CT_cumtime) + ',' + str(COUNT_ncalls) + ',' + str(COUNT_cumtime) + '\n')
    #ctFile.close()
                
if __name__ == '__main__':
    #testEvaFunctions()
    #testFDNet()
    #testDataset()
    #testIris()
    #testKDD()
    #testADTree()
    #testFileRecord()

    irisDataPath = '/media/uraplutonium/Cardboard/Workspace/AD-Tree-2014/src/iris_labelled.csv'
    stumbleDataPath = '/media/uraplutonium/Cardboard/Workspace/AD-Tree-2014/src/stumbleupon.csv'
    KDDDataPath = '/media/uraplutonium/Cardboard/Workspace/AD-Tree-2014/src/kdd10000DM.csv'
    
    ctFile = open(profPath + 'BIC_profile.csv', 'a')
    ctFile.writelines('ContabName,BIC_ncalls,BIC_cumtime,CT_ncalls,CT_cumtime,COUNT_ncalls,COUNT_cumtime\n')
    ctFile.close()
    
    ctInfoList = [['FullContingencyTable', 17, 65],
                  ['ListContingencyTable', 23, 80],
                  ['DictContingencyTable', 22, 79],
                  ['TreeContingencyTable', 18, 48],
                  ['IteratedListContingencyTable', 23, 82],
                  ['IteratedDictContingencyTable', 23, 84],
                  ['IteratedTreeContingencyTable', 20, 86]]

    for eachCTInfo in ctInfoList:
        testBIC(irisDataPath, eachCTInfo[0], eachCTInfo[1], eachCTInfo[2])
