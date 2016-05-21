# Add any code that updates the current probability
# values of any of the nodes here.

# For example, here is a method that updates the probability of
# a single node, where this node is assumed to have a single parent.
def update_node_with_one_parent(n):
    '''
      For all possible values pv of the current node,
      For all possible values ppv of the parent,
      Look up the conditional probability of pv given ppv.
         and multiply it by the current prob. of that parent state (ppv)
      and accumulate these to get the current probability of pv.
    '''
    if len(n.parents)!= 1:
        print "The function update_node_with_one_parent cannot handle node "+n.name
        print "It does not have exactly one parent."
        return
    parent = n.parents[0]
    for pv in n.possible_values:
        n.current_prob[pv] = 0.0
        for ppv in n.parents[0].possible_values:
            conditional = n.name+'='+str(pv)+'|'+parent.name+'='+str(ppv)
            n.current_prob[pv] += n.p[conditional] * parent.current_prob[ppv]

def gen_cartesian_product(sets):
    '''Return the cartesian product of a list of sets.
       For example: [['a','b'],[0,1],[7,8,9]] should give a 12 element set of triples.'''
    if len(sets)==1:
        return map(lambda set: [set], sets[0])
    subproduct = gen_cartesian_product(sets[1:])
    prod = []
    for elt in sets[0]:
        new_tuples = map(lambda tup: [elt]+tup, subproduct)
        prod = prod + new_tuples
    return prod

def update_node_with_k_parents(n):
    '''
      For all possible values pv of the current node,
      For all possible values ppv of each of the parents,
      Look up the conditional probability of pv given ppv.
         and multiply it by the current prob. of that parent state (ppv)
      and accumulate these to get the current probability of pv.
    '''
    print "Updating node: "+n.name
    if len(n.parents) < 1:
        print "The function update_node_with_k_parents cannot handle node "+n.name
        print "It does not have any parents."
        return
    cartesian_prod = gen_cartesian_product(map(lambda p: p.possible_values, n.parents))
    parent_names = map(lambda p: p.name, n.parents)
    for pv in n.possible_values:
        n.current_prob[pv] = 0.0
        print "  Updating current prob. of "+pv
        for ppv_tuple in cartesian_prod:
            print "    Adding the contribution for "+str(ppv_tuple)
            conditional = n.name+'='+pv+'|'+str(parent_names) +'='+str(ppv_tuple)
            parent_vector_prob = reduce(lambda a,b:a*b, map(lambda p, pv:p.current_prob[pv], n.parents, ppv_tuple))
            n.current_prob[pv] += n.p[conditional] * parent_vector_prob

#update_node_with_one_parent(nodeB)

