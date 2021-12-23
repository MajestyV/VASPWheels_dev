import codecs

class GenMinorScripts:
    """ This class of function is designed to generate the minor scripts for V.A.S.P. calculation."""
    def __init__(self):
        self.name = GenMinorScripts

    def Head(self):
        str = ''

    def WriteScript(self,filename):
        file = codecs.open(filename,'rb','utf-8','ignore')
        file.write()