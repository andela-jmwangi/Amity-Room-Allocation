from DatabaseManager import DatabaseManager
from Rooms import Rooms
from clint.textui import colored, puts, indent
from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format
from colorama import init, Fore, Back, Style
from collections import defaultdict
"""This class stores details of personnel
"""


class Personnel(object):

    def __init__(self):
        self.db = DatabaseManager("Amity.sqlite")
        self.rooms = Rooms()

    """returns a list of personnel who have been allocated rooms
    """
    def getallocated():

        pass

    """returns a list of personnel who have not been allocated rooms
    """
    def getunallocated():

        pass

    """returns a list of all room allocations
    """

    def getallallocations(self, **specific_room_name):
        spec_room = specific_room_name.get('room_name', "null")
        if spec_room == "null":
            query_string = "SELECT * from Allocations"
        else:
            query_string = "SELECT * from Allocations where Room_name = '" + \
                spec_room + "' "
        allocated_rooms_list = []
        cursor = self.db.query(query_string)
        for row in cursor:
            personnel_name = row[0]
            room_type = row[1]
            room_name = row[2]
            personnel_type = row[3]
            allocated_rooms_list.append(
                [personnel_name, room_name, personnel_type, room_type])
        return allocated_rooms_list

    """returns the room name the specific person has been allocated
    """

    def getroomallocated(self, room_type, personnel_name):
        allocatedroom = ""
        cursor = self.db.query(
            "SELECT Room_name from Allocations where Personnel_Name = '" + personnel_name + "' and Room_type = '" + room_type + "'")
        for row in cursor:
            allocatedroom = row[0]
        return allocatedroom
