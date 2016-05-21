''' SIGMAEditor.py


S. Tanimoto, 1 Jan 2009

This file provides:

-- Tkinter GUI window
-- Node, Edge, and Network display
-- Sample network
 ..... should someday include GUI drag-and-drop editing and testing of
  SIGMA diagrams.
  
'''

from Tkinter import *
import tkFont
from BayesNetNode import *
from BayesUpdating import *
import ReadWriteSigmaFiles
# import EventStreamEditor # Possible in the future: linked editor


TK_ROOT = None
SP_CANVAS = None
TITLE = " SIGMA Diagram Editor"
CURRENT_SIGMA_DIAGRAM = None
def showBayesNet(theBayesNet):
    global TK_ROOT, SP_CANVAS
    TK_ROOT = Tk(className=TITLE) # Create window
    TK_ROOT.grid_rowconfigure(0, weight=1)
    TK_ROOT.grid_columnconfigure(0, weight=1)
    SP_CANVAS = Canvas(TK_ROOT, width=1100, height=500, xscrollcommand=None,
                yscrollcommand=None)
    SP_CANVAS.grid(row=0,column=0,sticky='nesw')
    headingFont = tkFont.Font(family="Helvetica", size=18)
    SP_CANVAS.create_text(350, 50, font=headingFont,
            text='Bayes Net with Probability Updating using Conditional Probability Values')
    for node in theBayesNet.nodes:
        display_parent_links(node)
    for node in theBayesNet.nodes:
        display_node(node)
    createMenu(TK_ROOT)
    TK_ROOT.mainloop()

def createMenu(theRoot):
    print "Creating the menu..."
    menu_bar = Menu(theRoot)
    theRoot.config(menu=menu_bar)
    fileMenu = Menu(menu_bar)
    menu_bar.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="New", command=new_net)
    fileMenu.add_command(label="Open SIGMA diagram file...", command=ReadWriteSigmaFiles.open_sigma_file)
    fileMenu.add_command(label="Save SIGMA diagram As...", command=ReadWriteSigmaFiles.save_sigma_file)
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=exit_SigmaEngine)

    editMenu = Menu(menu_bar)
    menu_bar.add_cascade(label="Edit", menu=editMenu)
    editMenu.add_command(label="Copy", command=copy_node)
    editMenu.add_command(label="Paste", command=paste_node)

    runMenu = Menu(menu_bar)
    menu_bar.add_cascade(label="Run", menu=runMenu)
    runMenu.add_command(label="Run", command=run_current_sigma_diag)
    runMenu.add_command(label="Load event sequence file...", command=load_event_seq_file)

    helpMenu = Menu(menu_bar)
    menu_bar.add_cascade(label="SIGMA Help", menu=helpMenu)
    helpMenu.add_command(label="Instructions", command=show_instructions)
    helpMenu.add_command(label="About", command=show_about)
    
def new_net(): pass
def copy_node(): pass
def paste_node(): pass
def run_current_sigma_diag():
    import time
    print "Running current SIGMA diagram with a test sequence of events."
    import SampleNets
    eventList = SampleNets.event_seq_1
    for event in eventList:
        process_event(event)
        time.sleep(1)

def process_event(event):
    print "Processing event: "+event
    event_structure = parse_event(event)
    print "The event_structure is: "+str(event_structure)
    for node in CURRENT_SIGMA_DIAGRAM.get_input_nodes():
        result = node.apply_filter(event_structure)
        print "Result is: "+result
        
EVENT_SEQ = []        
def load_event_seq_file():
    global FILE_NAME, EVENT_SEQ
    import tkFileDialog
    FILE_NAME = tkFileDialog.askopenfilename(
        filetypes=[("Event sequence file", ".txt")])
    try:
        file = open(FILE_NAME, "r")
        contents = file.read()
        file.close()
        print "Here are the contents of the event sequence file as read in: "
        print contents
        lines = contents.split("\n")
    except:
        print "Could not load new data from file: ", FILE_NAME
        return
    # Parse the contents:
    EVENT_SEQ = lines
    #print "EVENT_SEQ = "+str(EVENT_SEQ)

def parse_event(line):
    lineparts = line[1:-1].split("],[")
    piecelist = map(cleanup, lineparts)
    return piecelist

def cleanup(piece):
    '''
    pieceOK = True
    if piece[0]!='[':
        print 'Expected a left bracket "[" at beginning of event piece: '+ piece
        pieceOK = False
    if piece[-1]!=']':
        print 'Expected a right bracket "]" at end of event piece: '+ piece
        pieceOK = False
    if not pieceOK: return "None:None"
    newpiece = piece[1:-1]
    print "newpiece = "+newpiece
    '''
    halves = piece.split(":")
    return halves
        
    
def show_instructions():
  import tkMessageBox
  tkMessageBox.showinfo("Instructions","The File menu is for loading and saving SIGMA diagram files in XML format.\n\n"+
        "The Edit menu is for editing the nodes in a SIGMA diagram.\n\n"+
        "The Run menu allows trying out a SIGMA diagram on an event sequence.\n")
def show_about():
  import tkMessageBox
  tkMessageBox.showinfo("About","SIGMA Diagram Editor Version 0.1\nCopyright 2009 Steven Tanimoto\n"+
        "University of Washington, Seattle, WA\n\n"+
        "The SIGMA Diagram Editor is an experimental design and analysis tool for\n"+
        "devices that process streams of events.\n")
  
def exit_SigmaEngine():   
  TK_ROOT.quit()
  TK_ROOT.destroy()
  
u = 2.5 # horizontal scale factor
def display_parent_links(n):
    for p in n.parents:
        SP_CANVAS.create_line(u*p.x, p.y, u*n.x, n.y)

import InputNode
import OutputNode

def display_node(n):
    # Displays node n, with its name and its current probabilities.
    # Its conditional distribution n.p is NOT displayed.
    # Neither is its description string.
    w = 160 # Width of node
    h = 80 # Height of node
    node_type = 'mid'
    node_color = 'yellow'
    if isinstance(n, InputNode.Input_Node):
        node_type = 'input'
        node_color = "light green"
    if isinstance(n, OutputNode.Output_Node):
        node_type = 'output'
        node_color = 'red'
    SP_CANVAS.create_rectangle(u*n.x-w/2-3,n.y-h/2-3,
        u*n.x+w/2+2,n.y+h/2+2,fill=node_color)
    SP_CANVAS.create_text(u*n.x,n.y-20-12, text=n.name)
    i = 0
    for pv in n.possible_values:
        SP_CANVAS.create_text(u*n.x,n.y-20+i*12,
            text='P('+n.name+'='+pv+')='+str(n.current_prob[pv]))
        i = i+1
    if isinstance(n, InputNode.Input_Node):
        SP_CANVAS.create_text(u*n.x,n.y-h/2+45, text=abbrev('response method:'+n.response_method))
        SP_CANVAS.create_text(u*n.x,n.y-h/2+60, text=abbrev('filter:'+n.filter))
        SP_CANVAS.create_text(u*n.x,n.y-h/2+75, text='token:'+str(n.token))
    if isinstance(n, OutputNode.Output_Node):
        SP_CANVAS.create_text(u*n.x,n.y-h/2+45, text=abbrev('action:'+n.action_list))

def abbrev(string):
    '''Make sure string has limited length.'''
    maxlen = 27
    if len(string) <= maxlen: return string
    else: return string[:maxlen]
    
if __name__ == '__main__':
    #import SampleNets
    #import FDNets
    
    #SampleNets.test1()
    #FDNets.test1()
    from TestCases import *
    
    global CURRENT_SIGMA_DIAGRAM
#    CURRENT_SIGMA_DIAGRAM = SampleNets.mynet
#    CURRENT_SIGMA_DIAGRAM = FDNets.fdnet


    CURRENT_SIGMA_DIAGRAM = testKDD()
    showBayesNet(CURRENT_SIGMA_DIAGRAM)




