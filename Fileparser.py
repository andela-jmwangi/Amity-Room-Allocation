"""This class reads the file input and returns appropriate data to caller
"""


class Fileparser(object):

    def __init__(self, pathtofile):
        self.pathtofile = pathtofile
        pass

    def getlinecontents(self):
        with open(self.pathtofile, 'r') as f:
            lines = f.read()  # read file contents into memory
        # make a list of the lines by breaking at line boundaries
        listallocations = lines.splitlines()
        return listallocations
