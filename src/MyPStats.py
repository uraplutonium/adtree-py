'''
Created on Jun 28, 2012
@author: Felix
'''

import pstats

class Stats(pstats.Stats):
    
    def getTime(self, func, field):
        cc, nc, tt, ct, callers = self.stats[func]
        if field=='ncalls':
            return nc
        elif field=='tottime':
            return tt
        elif field=='ptottime':
            return tt/nc
        elif field=='cumtime':
            return ct
        elif field=='pcumtime':
            return ct/nc
