from BayesNetNode import *
from BayesUpdating import *
from Dataset import *

irisdata = dataset("/media/uraplutonium/Cardboard/Workspace/AD-Tree-2014/src/iris_labelled.csv")

# create the bayesnet
irisnet = BayesNet("the iris net")

# create nodes
n_sl = Node('sl', 'sl dis', 100, 100, list(irisdata.getArities()[0]))
n_sw = Node('sw', 'sw dis', 300, 100, list(irisdata.getArities()[1]))
n_pl = Node('pl', 'pl dis', 100, 300, list(irisdata.getArities()[2]))
n_pw = Node('pw', 'pw dis', 300, 300, list(irisdata.getArities()[3]))
n_type = Node('type', 'type dis', 200, 200, list(irisdata.getArities()[4]))

# add nodes to the bayesnet
irisnet.add_node(n_sl)
irisnet.add_node(n_sw)
irisnet.add_node(n_pl)
irisnet.add_node(n_pw)
irisnet.add_node(n_type)

# build the connections between nodes
Node.makePair(n_type, n_sl)
Node.makePair(n_type, n_sw)
Node.makePair(n_type, n_pl)
Node.makePair(n_type, n_pw)
