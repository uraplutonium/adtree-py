''' OutputNode.py


S. Tanimoto, 31 Jan 2009

This file provides:

Output Node class definition.
Methods for performing actions.

'''


import BayesNetNode


print "First: Output node class definition..."


class Output_Node(BayesNetNode.Node):
  def setprops(self, actionList):
    self.action_list = actionList

  def perform_actions(self):
    print "Output node "+self.name+" with action_list: "+self.action_list
    


