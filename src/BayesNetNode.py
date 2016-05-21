''' BayesNetNode.py


S. Tanimoto, 11 Jan 2009

This file provides:

-- Node class definitions.
'''

#import Tkinter

class Node:

    name_node_hash = {}
    def __init__(self, name, desc, x, y, poss_vals = ['True', 'False']):
        self.name = name # name of the node
        self.desc = desc # description
        self.x = x # two-dimensional?
        self.y = y
        Node.name_node_hash[name] = self
        self.parents = [] # saves the parents of the node in a list
        self.children = [] # save the children of the node in a list
        self.possible_values = poss_vals # all the possible values, enumerable
        self.p = {} # Hash, so that number of parents can change.
        self.current_prob = {} # a hash map, current probabilities, one for each possible_value.
        default_prob = 1.0 / len(poss_vals) # you know this, init value
        for pv in poss_vals:
            self.current_prob[pv] = default_prob #
            self.p[self.name+"="+pv] = default_prob

    def get_prior(self, poss_val):
        return self.p[self.name+"="+poss_val]
        
    def set_prior(self, poss_val, prob):
        self.p[self.name+"="+poss_val] = prob
        self.current_prob[poss_val] = prob
        
    def add_parent(self, parent_name):
        #print("before" + Node.name_node_hash)
        p = Node.name_node_hash[parent_name] # set p points to the parent instance
        self.parents.append(p)
        #print("after" + Node.name_node_hash)
        return p
                
    def add_child(self, child_name):
        c = Node.name_node_hash[child_name]
        self.children.append(c)
        return c

    def makePair(parentNode, childNode):
        parentNode.add_child(childNode.name)
        childNode.add_parent(parentNode.name)   
        
class BayesNet:
    def __init__(self, name):
        self.name = name # the name of a BN
        self.nodes = [] # use a list to store all the nodes
        self.input_nodes = [] # ??

    ''' add a node to the BN '''
    def add_node(self, node):
        self.nodes.append(node) # simply append the new node to the node list
        from InputNode import Input_Node # check whether the new node is a input-node
        if isinstance(node, Input_Node):
            self.input_nodes.append(node)

    ''' return the input node list '''
    def get_input_nodes(self):
        return self.input_nodes

    ''' display all nodes '''
    def display_all_nodes(self):
        for eachNode in self.nodes:
            print(eachNode.name)
            print(eachNode.p)
            print(eachNode.current_prob)

