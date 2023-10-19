# This code is designed for analyzing element distribution data gained from electron microscopic characterizations.

class EDX:
    ''' This class of function is designed to analyze EDX data. '''
    def __init__(self,data,mode):
        self.data = data

    def Intensity_to_AtomicPercentage(self):

