from DatabaseManager import DatabaseManager
from Rooms import Rooms

"""This class provides various details about personnels
"""


class Personnel(object):

    def __init__(self):
        self.db = DatabaseManager("Amity.sqlite")
        self.rooms = Rooms()


    """returns a list of personnel who have not been allocated rooms
    """

    def getunallocated(self, allocatedlist, originallist):
        if len(originallist) > len(allocatedlist): # compare which list is geater so as to get the difference
            return set(originallist) - set(allocatedlist)
        else:
            return []

    """returns a list of all room allocations
    """

    def getallallocations(self, **specific_room_name):
        spec_room = specific_room_name.get('room_name', "null") # retrieves the supplied name of the room if present
        if spec_room == "null":
            query_string = "SELECT * from Allocations"
        else:
            query_string = "SELECT * from Allocations where Room_name = '" + \
                spec_room + "' "
        allocated_rooms_list = []
        cursor = self.db.query(query_string) # queries for allocations in db
        for row in cursor:
            personnel_name = row[0]
            room_type = row[1]
            room_name = row[2]
            personnel_type = row[3]
            allocated_rooms_list.append(
                [personnel_name, room_name, personnel_type, room_type])
        return allocated_rooms_list # returns the alloacations to caller

    """returns the room name the specific person has been allocated
    """

    def getroomallocated(self, room_type, personnel_name):
        allocatedroom = ""
        # queries db for room name given the personnel
        cursor = self.db.query(
            "SELECT Room_name from Allocations where Personnel_Name = '" + personnel_name + "' and Room_type = '" + room_type + "'")
        for row in cursor:
            allocatedroom = row[0] # get room name
        return allocatedroom
