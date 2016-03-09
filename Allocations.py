
from DatabaseManager import DatabaseManager
import random

"""This class handles all allocation tasks
"""


class Allocations(object):
    def __init__(self, personnel_name, personnel_type, residing):
        self.personnel_name = personnel_name
        self.personnel_type = personnel_type
        self.residing = residing
        self.db = DatabaseManager("Amity.sqlite")

    """determines if personnel has a room
    """

    def hasroom(self, personnel_name, room_type):
    	# query db to check if name exists in Allocations table
        cursor = self.db.query("SELECT * from Allocations where Personnel_Name = '" + personnel_name + "' and Room_type = '" + room_type +"')
        if cursor.rowcount > 0:
            return True  # return true if one or more records have been found
        return False  # return false if no record found

     """checks whether there is a room available for a certain category i.e either office or livingspace
     """

    def isroomavailable(self, room_type):
    	# query db to check if a room exists with less occupants than its maximum capacity
        cursor = self.db.query(
            "SELECT * from Rooms where Maxpple > Curpple and Room_type = '" + room_type + "'")
        if cursor.rowcount > 0:
            return True #return true if one or more records have been found
        return False #return false if no record found

    """checks for available rooms (rooms with available slots) and returns them
    """

    def getavailablerooms(self, room_type):
        listrooms = [] #initiate empty list
        # query db to check if a room exists with less occupants than its maximum capacity
        cursor = self.db.query(
            "SELECT * from Rooms where Maxpple > Curpple and Room_type = '" + room_type + "'")
        for row in cursor:
            listrooms.append(row[1]) #populate list with room names(row[1]).
        return listrooms

    """returns a randomised list of personnel or rooms
    """

    def getrandomlist(self, all):
        listrandomindices = random.sample(
            range(0, len(all)), len(all) - 1) #generate a list with random indices.
        randomisedlist = [] 
        for num in listrandomindices:
            randomisedlist.append(all[num]) #populate randomizedlist with random entries based on listrandomindices list
        return randomisedlist

    """returns a list of allocations
    """

    def allocate(self, listrooms, listpersonnel):
    	allocations = {} #initiate allocations dict
    	i = 0
    	for person in listpersonnel:
    		allocations[person] = listrooms[i]
    		i += 1
    	return allocations


