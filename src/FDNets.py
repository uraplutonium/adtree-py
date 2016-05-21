from BayesNetNode import *
from BayesUpdating import *

# create the bayesnet
fdnet = BayesNet("felix's test net")

# create nodes
n_s1 = Node('s1', 'server 1', 100, 100)
n_s2 = Node('s2', 'server 2', 300, 100)
n_u = Node('u', 'user', 200, 400)

# add nodes to the bayesnet
fdnet.add_node(n_s1)
fdnet.add_node(n_s2)
fdnet.add_node(n_u)

# build the connections between nodes
n_s2.add_parent('s1')
n_s1.add_child('s2')

n_u.add_parent('s1')
n_s1.add_child('u')

n_u.add_parent('s2')
n_s2.add_child('u')

# set the prior probabilities, of s1
n_s1.set_prior('True', 0.4)
n_s1.set_prior('False', 0.6)

# set the conditional probabilities, of s2 and u
# n_s2|n_s1
n_s2.p["s2=True|['s1']=['True']"] = 0.7
n_s2.p["s2=True|['s1']=['False']"] = 0.3
n_s2.p["s2=False|['s1']=['True']"] = 0.3
n_s2.p["s2=False|['s1']=['False']"] = 0.7

# n_u|n_s2
n_u.p["u=True|['s1', 's2']=['True', 'True']"] = 1
n_u.p["u=True|['s1', 's2']=['True', 'False']"] = 1
n_u.p["u=True|['s1', 's2']=['False', 'True']"] = 1
n_u.p["u=True|['s1', 's2']=['False', 'False']"] = 0
n_u.p["u=False|['s1', 's2']=['True', 'True']"] = 0
n_u.p["u=False|['s1', 's2']=['True', 'False']"] = 0
n_u.p["u=False|['s1', 's2']=['False', 'True']"] = 0
n_u.p["u=False|['s1', 's2']=['False', 'False']"] = 1

def update():
    update_node_with_k_parents(n_s2)
    update_node_with_k_parents(n_u)

bayesNet = fdnet
fdnet.display_all_nodes()
print('=============')
update()
print('=============')
fdnet.display_all_nodes()

