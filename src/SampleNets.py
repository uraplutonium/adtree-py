'''SampleNets.py
   Test data for developing the SIGMA Editor.
'''

# Here is the example Bayes net used in lecture.

from BayesNetNode import *
from BayesUpdating import *

mynet = BayesNet("Test Net")
nodeA = Node('A', 'Accident', 400, 160)
nodeB = Node('B', 'Barb Late', 300, 300)
nodeC = Node('C', 'Chris Late', 500, 300)
mynet.add_node(nodeA)
mynet.add_node(nodeB)
mynet.add_node(nodeC)
nodeB.add_parent('A')
nodeC.add_parent('A')
nodeA.add_child('B')
nodeA.add_child('C')
nodeA.set_prior('True', 0.2)
nodeA.set_prior('False', 0.8)
nodeB.p["B=True|['A']=['True']"]   = 0.5
nodeB.p["B=True|['A']=['False']"]   = 0.15
nodeB.p["B=False|['A']=['True']"]   = 0.5
nodeB.p["B=False|['A']=['False']"]   = 0.85
nodeC.p["C=True|['A']=['True']"]   = 0.3
nodeC.p["C=True|['A']=['False']"]   = 0.1
nodeC.p["C=False|['A']=['True']"]   = 0.7
nodeC.p["C=False|['A']=['False']"]   = 0.9

print('testtest')

def test1():
    update_node_with_k_parents(nodeB)
    update_node_with_k_parents(nodeC)

def test_cart_prod():
    s1 = ['a','b']; s2 = [0,1]; s3 = [7,8,9]
    s1s2s3 = gen_cartesian_product([s1,s2,s3])
    print s1s2s3

nodeD = Node('D', 'Disease', 200, 160)
mynet.add_node(nodeD)
nodeB.add_parent('D')
nodeD.add_child('B')
nodeD.set_prior('True', 0.111)
nodeD.set_prior('False', 0.889)
nodeB.p["B=True|['A', 'D']=['True', 'True']"]   = 0.9
nodeB.p["B=True|['A', 'D']=['True', 'False']"]   = 0.45
nodeB.p["B=True|['A', 'D']=['False', 'True']"]   = 0.75
nodeB.p["B=True|['A', 'D']=['False', 'False']"]   = 0.1
nodeB.p["B=False|['A', 'D']=['True', 'True']"]   = 0.1
nodeB.p["B=False|['A', 'D']=['True', 'False']"]   = 0.55
nodeB.p["B=False|['A', 'D']=['False', 'True']"]   = 0.25
nodeB.p["B=False|['A', 'D']=['False', 'False']"]   = 0.9

from InputNode import Input_Node
nodeI = Input_Node('Z','Zooms', 100, 200)
nodeI.setprops('ZoomIn','{DESC:/ZoomIn|Zoom In/}','(ACCUM_ZENO 0.7)',0)
mynet.add_node(nodeI)

event_seq_1 = [
    "[DateTime:2009-01-29-23-17-57-028],[SessionID:15],[Type:LoadImage],[Desc:mona-rgb.jpg]",
    "[DateTime:2009-01-29-23-18-18-043],[SessionID:15],[Type:ZoomIn],[Desc:238,194]",
    "[DateTime:2009-01-29-23-18-19-223],[SessionID:15],[Type:ZoomIn],[Desc:238,194]",
    "[DateTime:2009-01-29-23-18-19-874],[SessionID:15],[Type:ZoomIn],[Desc:238,194]",
    "[DateTime:2009-01-29-23-18-20-185],[SessionID:15],[Type:ZoomIn],[Desc:238,194]",
    "[DateTime:2009-01-29-23-18-49-736],[SessionID:15],[Type:Calc],[Desc:RGB(0,0,255)]"
    
    ]
