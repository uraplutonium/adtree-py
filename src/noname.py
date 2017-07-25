'''
Created on Jun 5, 2012

@author: Felix
'''

import cProfile as profile
import pstats
import ArrayRecord as Record
import SparseADTree as ADTree
import TreeContingencyTable as ContingencyTable

arityList = [4, 3, 2, 5]
recordsTable = [[1, 2, 1, 4], [2, 2, 2, 5], [1, 3, 1, 1], [4, 1, 2, 1],
                [2, 2, 1, 4], [4, 3, 2, 5], [3, 1, 1, 1], [1, 1, 2, 5]]

def foo1():
    for i in range(50000):
        stack = []
        tree = [None, None, None, None]
        tree[1] = [None, None]
        tree[1][1] = [None, None, None]
    #    print('tree', tree)
        
        stack.append(tree[1])
        t = stack.pop()
        stack.append(t[1])
        t = stack.pop()
        t[1] = ['list 1']
        t[2] = ['list 2']
        
    #    print('tree', tree)

def foo2():
    for i in range(50000):
        stack = []
        tree = [None, None, None, None]
        tree[1] = [None, None]
        tree[1][1] = [None, None, None]
    #    print('tree', tree)
        
        stack.append([1])
        tn = stack.pop()
        stack.append(tn+[1])
        tn = stack.pop()
        t=tree
        for eacht in tn:
            t=t[eacht]
        t[1] = ['list 1']
        t[2] = ['list 2']
        
    #    print('tree', tree)
    
if __name__ == '__main__':
    # import the original dataset to the record module
    Record.initRecord([arityList, recordsTable])
    
    # declare that the ADTree module uses ArrayRecord module as dataset
    ADTree.importModules('ArrayRecord')
    
    # declare that the ContingencyTable uses ArrayRecord and SparsADTree modules 
    ContingencyTable.importModules('ArrayRecord', 'SparseADTree')
    
    # initialise recordNums containing all numbers in the dataset
    recordNums = [num for num in range(1, Record.recordsLength+1)]
    
    # build an AD-Tree with attribute list starts from the first attribute,
    # and for all the records
    adtree = ADTree.ADNode(1, recordNums)
    
    # build a contingency table for the first and third attributes
    contab = ContingencyTable.ContingencyTable([1, 3], adtree)
    
#    path = '/media/uraplutonium/Cardboard/Workspace/AD-Tree-2014/src/package/profile/'
#    stat = pstats.Stats(path+'none.prof')
#    for i in range(10000):
#        profile.run('contab = ContingencyTable.ContingencyTable([1, 3], adtree)', path+'prof.prof')
#        stat.add(path+'prof.prof')
#    stat.strip_dirs().dump_stats(path+'prof.prof')
#    stat = pstats.Stats(path+'prof.prof')
#    stat.sort_stats("time").print_stats()

    # query for [1, 1], [2, 1], [3, 1] and [4, 1], and print on screen
    for i in range(4):
        query = [i+1, 1]
        count = contab.getCount(query)
        print('Q:', query, 'C:', count)



#    profile.run("foo1()", "prof1.txt")
#    p = pstats.Stats("prof1.txt")
#    p.sort_stats("time").print_stats()
#    print('===============')
#    profile.run("foo2()", "prof2.txt")
#    p = pstats.Stats("prof2.txt")
#    p.sort_stats("time").print_stats()
