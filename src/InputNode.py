''' InputNode.py


S. Tanimoto, 30 Jan 2009

This file provides:

Input Node class definition.
Methods for filtering events.

What's working:
  Node construction, including parsing the filter spec. and compiling a regular expression
    for each reg. expression in the filter.

  Applying the filter to an event.

What's not working yet:
  Computing posterior probabilities here.  (Should set it to 1, depending on the response method)
  Enabling other input nodes.  Being enabled by other input nodes.
  Managing tokens.
  Signalling to the engine that downstream nodes should be updated.
  This should be done by returning a True value, instead of a string.

'''

import BayesNetNode
import re  # regular expression module, for matching input filter conditions.

class Input_Node(BayesNetNode.Node):
  def setprops(self, eventtype, thefilter, responsemethod, token):
    self.event_type = eventtype
    self.filter = thefilter
    self.response_method = responsemethod
    self.token = token
    self.parsefilter()

  def parsefilter(self):
    ''' Filter should be of the form
        '{Prop1:/regex1/}{Prop2:/regex2/}...{Propn:/regexn/}'
        for example:
       '{Desc:/Zoom in|zoom in/}'
    '''
    mydict = {}
    fields = self.filter[1:-1].split("}{")
    pairlist = [f.split(":") for f in fields]
    for parts in pairlist:
      regex = re.compile(parts[1][1:-1])
      mydict[parts[0]]=regex
    self.filter_struc = mydict
    
  def apply_filter(self, event_struc):
    print "Input node "+self.name+" with filter: "+self.filter+" considering event: "+str(event_struc)
    # Test whether the event Type matches the filter Desc.
    event_type = get_event_prop("Type", event_struc)
    keys = self.filter_struc.keys()
    for key in keys:
      filter_regex = self.filter_struc[key]
      #import re
      print "Using 're' search to match event_type: "+event_type
      result = filter_regex.search(event_type)
      if result==None:
        print "No match; failed on "+key+": "+str(self.filter_struc[key])
        return "Nothing"
    if result != None:
      print "We have a match! " + event_type
      # Should do something.
    return "Done"

def get_event_prop(the_prop, event_struc):
   ''' Retrieve the attribute corresponding to the_prop in a list of
      attribute-value pairs '''
   for [p, v] in event_struc:
       if p==the_prop: return v
   return "NULL"
  


