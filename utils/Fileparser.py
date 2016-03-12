import csv
import ipdb

"""This class reads the file input and returns appropriate data to caller
"""


class Fileparser(object):

    def __init__(self, pathtofile):
        self.pathtofile = pathtofile

    """Read file contents and return a list
    """ 
    def readfile(self):
        #ipdb.set_trace(context=1)
        list_allocations = []
        contents = [line.rstrip('\n') for line in open(self.pathtofile, 'r')]
        for line in contents:
            words = line.split(" ")
            person_name = words[0] + " " + words[1]
            person_type = words[2]
            residing = "N"
            if len(words) == 4:
                residing = "Y"
            list_allocations.append([person_name, person_type, residing])
        return list_allocations
