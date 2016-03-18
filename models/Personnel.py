from db.DatabaseManager import DatabaseManager
from Rooms import Rooms
from utils.FileParser import FileParser
import os.path


class Personnel(object):
    """This class provides various details about personnels"""

    def __init__(self):
        self.db = DatabaseManager("Amity.sqlite")
        self.rooms = Rooms()

    def get_unallocated(self, allocated_list, original_list):
        """returns a list of personnel who have not been allocated rooms"""
        # compare which list is geater so as to get the difference
        # if len(originallist) > len(allocatedlist):
        temp_unallocated = set(original_list) - set(allocated_list)
        list_unallocated = []

        # check in db whether they have rooms
        for name in temp_unallocated:
            cursor = self.db.query(
                "SELECT * from Allocations where Personnel_Name = '" + name.replace("'", "") + "'")
            count = len(cursor.fetchall())
            if count <= 0:
                list_unallocated.append(name)

        for name in original_list:
            cursor = self.db.query(
                "SELECT * from Allocations where Personnel_Name = '" + name.replace("'", "") + "'")
            count = len(cursor.fetchall())
            if self.is_residing(name) == "N":
                if count <= 0:
                    list_unallocated.append(name)
            else:
                if count == 1:
                    list_unallocated.append(name)
        return list_unallocated

        # else:
        #     return []

    def is_residing(self, name):
        """Get residing status of person"""

        parser = FileParser(
            os.path.dirname(os.path.realpath("filepath")) + "/input.txt")
        all_ppl = parser.read_file()
        for person in all_ppl:
            if name == person[0]:
                residing = person[2]
                return residing

    def get_all_allocations(self, **specific_room_name):
        """returns a list of all room allocations"""

        # retrieves the supplied name of the room if present
        spec_room = specific_room_name.get('room_name', "null")
        if spec_room == "null":
            query_string = "SELECT * from Allocations"
        else:
            query_string = "SELECT * from Allocations where Room_name = '" + \
                spec_room + "' "
        allocated_rooms_list = []
        cursor = self.db.query(query_string)  # queries for allocations in db
        for row in cursor:
            personnel_name = row[0]
            room_type = row[1]
            room_name = row[2]
            personnel_type = row[3]
            allocated_rooms_list.append(
                [personnel_name, room_name, personnel_type, room_type])
        return allocated_rooms_list  # returns the alloacations to caller

    def get_room_allocated(self, room_type, personnel_name):
        """returns the room name the specific person has been allocated"""

        allocated_room = ""
        # queries db for room name given the personnel
        cursor = self.db.query(
            "SELECT Room_name from Allocations where Personnel_Name = '" + personnel_name + "' and Room_type = '" + room_type + "'")
        for row in cursor:
            allocated_room = row[0]  # get room name
        return allocated_room
