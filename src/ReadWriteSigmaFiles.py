
'''ReadWriteSigmaFiles.py
  Decode and encode XML

  Input and output work 
  Input of prob. distributions is implemented.  They are read from the
  XML and stored as a list of floats, as the value of node.pd.
  For them to be used in updating, they are also entered into the
  hash table with the approproate keys that identify the Proposition and Condition
  for the conditional probability.
  

'''

from BayesNetNode import Node, BayesNet
from InputNode import Input_Node
from OutputNode import Output_Node
import SIGMAEditor

import xml.dom.minidom as MiniDom
#from xml.dom.minidom import Node as DomNode

def open_sigma_file():
    filename=None
    if filename==None:
        filename = "gma-mona.igm"
    try:
        wholeDOMTree = MiniDom.parse(filename)
    except:
        print "The file \""+filename+"\" could not be parsed as an XML file."
        return
    try:
        model = wholeDOMTree.getElementsByTagName("model")[0]
    except:
        print "Although "+filename+" is an XML file, no 'model' tag was found."
        return
    NAME = get_textual_part(model, "modelname")
    print "Model name is: "+NAME
    VERSION = get_textual_part(model,"version")
    AUTHORS = get_textual_part(model,"authors")
 
    new_sigma_diag = BayesNet(NAME)
    inputNodes = model.getElementsByTagName("inputnode")
    for node in inputNodes: new_sigma_diag.add_node(build_input_node(node))
    midNodes = model.getElementsByTagName("midnode")
    for node in midNodes: new_sigma_diag.add_node(build_mid_node(node))
    outputNodes = model.getElementsByTagName("outnode")
    for node in outputNodes: new_sigma_diag.add_node(build_output_node(node))
    SIGMAEditor.CURRENT_SIGMA_DIAGRAM = new_sigma_diag
    SIGMAEditor.showBayesNet(new_sigma_diag)

def get_domnode_text(domnode):
    '''Given a node of a DOM, go through its children. For each child that is
       a textual node, concatenate its content with that of the others and return it.'''
    text=""
    parts = domnode.childNodes
    for p in parts:
        if p.nodeType == p.TEXT_NODE:
            text += p.data
    return text

def get_textual_part(domnode, desc):
    '''Return a string containing the value of this domnode's component named desc.'''
    text=""
    try:
        part = domnode.getElementsByTagName(desc)[0]
        text = get_domnode_text(part)
    except: pass
    return text

def build_input_node(domnode):
    x = get_textual_part(domnode,"x")
    y = get_textual_part(domnode,"y")
    nodeid = get_textual_part(domnode,"nodeid")
    label = get_textual_part(domnode,"label")
    pd = get_textual_part(domnode,"pd")
    node = Input_Node(nodeid,label,int(x),int(y))
    set_probabilities(domnode, node)
    handle_links(node, domnode)
    node.response_method = get_textual_part(domnode,"response_method")
    node.event_type = get_textual_part(domnode,"eventtype")
    node.filter = get_textual_part(domnode,"filter")
    node.token = get_textual_part(domnode,"token")
    node.parsefilter()
    return node

def build_output_node(domnode):
    x = get_textual_part(domnode,"x")
    y = get_textual_part(domnode,"y")
    nodeid = get_textual_part(domnode,"nodeid")
    label = get_textual_part(domnode,"label")
    pd = get_textual_part(domnode,"pd")
    node = Output_Node(nodeid,label,int(x),int(y))
    set_probabilities(domnode, node)
    handle_links(node, domnode)
    node.action_list = get_textual_part(domnode,"action")
    return node

def build_mid_node(domnode):
    x = get_textual_part(domnode,"x")
    y = get_textual_part(domnode,"y")
    nodeid = get_textual_part(domnode,"nodeid")
    label = get_textual_part(domnode,"label")
    pd = get_textual_part(domnode,"pd")
    node = Node(nodeid,label,int(x),int(y))
    handle_links(node, domnode)
    set_probabilities(domnode, node)
    return node

def set_probabilities(domnode, node):
    prior = float(get_textual_part(domnode,"prior"))
    node.possible_values = ['True', 'False']
    node.set_prior('True',prior)
    node.set_prior('False',1.0-prior)
    temp = get_textual_part(domnode, "pd")
    print "Node pd string list = " + temp
    templst = temp.split(",")
    print "Node pd string list = " + str(templst)
    node.pd = [float(p) for p in templst if p!='']
    print "Node pd = "+str(node.pd)
    if len(node.parents)>0: convert_probs_to_hash(node)

def convert_probs_to_hash(node):
    import BayesUpdating
    parent_propositions = [[str(p.name).encode('ascii')+
                            '=True', str(p.name).encode('ascii')+'=False'] for p in node.parents]
    print "parent_propositions: "+str(parent_propositions)
    truth_tuples = BayesUpdating.gen_cartesian_product([['True','False'] for p in node.parents])
    print "truth_tuples: "+str(truth_tuples)
    i = 0
    for tt in truth_tuples:
        keystring = str(node.name)+'=True|'+str([par.name.encode('ascii') for par in node.parents]).encode('ascii')
        keystring += "="+str(tt)
        node.p[keystring]=node.pd[i]
        i += 1
    # Test:
    print "Here's what is in the p hashtable for node "+node.name
    for k in node.p.keys():
        print k+" = "+str(node.p[k])

def handle_links(node, domnode):
    parents_str = get_textual_part(domnode,"parents").encode('ascii')
    parents_lst = parents_str.split(",")
    in_ascii = [a.encode('ascii') for a in parents_lst]
    #print "parents are "+str(parents_lst)
    for parent in in_ascii:
        if parent=='': continue
        parent_node = node.add_parent(parent)
        parent_node.add_child(node.name)
        
def save_sigma_file():
  """Brings up a file dialog box, so the user can choose a
  file for saving the current SIGMA diagram. Then converts
  the diagram to XML and saves it."""
  import tkFileDialog
  savefile = tkFileDialog.asksaveasfilename(
    filetypes=[("SIGMA Diagram files", ".igm")],
    defaultextension=".igm")
  if savefile:
    dom = makeSigmaDOM()
    try:
      f = open(savefile, "w")
      dom.writexml(f)
      f.close()
      #global DIRTY; DIRTY = False
    except:
        print "Couldn't write the file: ", savefile
        raise

def makeSigmaDOM():
    from xml.dom.minidom import getDOMImplementation
    impl = getDOMImplementation()

    newdoc = impl.createDocument(None, "model", None)
    top_element = newdoc.documentElement
    modelNameElt = newdoc.createElement("modelname")
    text = newdoc.createTextNode('Test Model')
    top_element.appendChild(modelNameElt)
    modelNameElt.appendChild(text)
    for node in SIGMAEditor.CURRENT_SIGMA_DIAGRAM.nodes:
        nodeToDOM(newdoc, top_element, node)
    return newdoc

def nodeToDOM(doc, parent_element, node):
    '''Create a new element in the document object model for the Bayes net node.
       The document is needed for its method to create the new element.
       Link the new element into the parent_element.'''
    tag = "midnode"
    if isinstance(node, Input_Node):
        tag = "inputnode"
    if isinstance(node, Output_Node):
        tag = "outnode"
    nodeElt = doc.createElement(tag)
    #text = doc.createTextNode("The node's data")
    parent_element.appendChild(nodeElt)
    #nodeElt.appendChild(text)
    # handle the common parts of a node:
    partElt = doc.createElement("nodeid")
    text = doc.createTextNode(node.name)
    nodeElt.appendChild(partElt)
    partElt.appendChild(text)
    partElt = doc.createElement("x")
    text = doc.createTextNode(str(node.x))
    nodeElt.appendChild(partElt)
    partElt.appendChild(text)
    partElt = doc.createElement("y")
    text = doc.createTextNode(str(node.y))
    nodeElt.appendChild(partElt)
    partElt.appendChild(text)
    partElt = doc.createElement("prior")
    text = doc.createTextNode(str(node.get_prior('True')))
    nodeElt.appendChild(partElt)
    partElt.appendChild(text)
    partElt = doc.createElement("label")
    text = doc.createTextNode(node.desc)
    nodeElt.appendChild(partElt)
    partElt.appendChild(text)
    partElt = doc.createElement("pd")
    pdstrlst = [str(p).encode('ascii') for p in node.pd]
    if pdstrlst==[]: pdstr=''
    else:
        pdstr = pdstrlst[0]
        rest = pdstrlst[1:]
        for s in rest:
            pdstr += ","+s
    print "pdstr = "+pdstr
    text = doc.createTextNode(pdstr)
    nodeElt.appendChild(partElt)
    partElt.appendChild(text)
    if isinstance(node, Input_Node):
        partElt = doc.createElement("eventtype")
        text = doc.createTextNode(node.event_type)
        nodeElt.appendChild(partElt)
        partElt.appendChild(text)
        partElt = doc.createElement("filter")
        text = doc.createTextNode(node.filter)
        nodeElt.appendChild(partElt)
        partElt.appendChild(text)
        partElt = doc.createElement("responsemethod")
        text = doc.createTextNode(node.response_method)
        nodeElt.appendChild(partElt)
        partElt.appendChild(text)
        partElt = doc.createElement("token")
        text = doc.createTextNode(str(node.token))
        nodeElt.appendChild(partElt)
        partElt.appendChild(text)
    if isinstance(node, Output_Node):
        partElt = doc.createElement("action")
        text = doc.createTextNode(str(node.action_list))
        nodeElt.appendChild(partElt)
        partElt.appendChild(text)
    
