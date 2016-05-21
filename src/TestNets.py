from BayesNetNode import *
from BayesUpdating import *

# create the bayesnet
testnet = BayesNet("felix's test net")

# create nodes
tn_s1 = Node('s1', 'server 1', 100, 100)
tn_s2 = Node('s2', 'server 2', 300, 100)
tn_u = Node('u', 'user', 200, 400)

# add nodes to the bayesnet, codes below should not be changed through tests
testnet.add_node(tn_s1)
testnet.add_node(tn_s2)
testnet.add_node(tn_u)

# build the connections between nodes, change codes below to test

''' FULL NET ''
tn_s2.add_parent('s1')
tn_s1.add_child('s2')

tn_u.add_parent('s1')
tn_s1.add_child('u')

tn_u.add_parent('s2')
tn_s2.add_child('u')'''

''' s2->s1 ''
tn_s1.add_parent('s2')
tn_s2.add_child('s1')
'''

''' s1->s2 ''
tn_s2.add_parent('s1')
tn_s1.add_child('s2')
'''

''' s2->u ''
tn_u.add_parent('s2')
tn_s2.add_child('u')
'''

''' u->s2 ''
tn_s2.add_parent('u')
tn_u.add_child('s2')
'''

''' u->s1 ''
tn_s1.add_parent('u')
tn_u.add_child('s1')
'''

''' s1->u ''
tn_u.add_parent('s1')
tn_s1.add_child('u')
'''

''' FULL NET '''
tn_s2.add_child('s1')
tn_s1.add_parent('s2')

tn_u.add_parent('s1')
tn_s1.add_child('u')

tn_u.add_parent('s2')
tn_s2.add_child('u')
