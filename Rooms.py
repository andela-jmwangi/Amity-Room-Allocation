from DatabaseManager import DatabaseManager
"""This class stores details of a room
"""


class Rooms(object):

    def __init__(self):
        self.db = DatabaseManager("Amity.sqlite")

        """gets a list of staff allocated to a specific room or all rooms in general
        """

    def get_rooms_with_occupants(self):
        pass

    def get_room_type(self, room_name):
        room_type = ""
        cursor = self.db.query(
            "SELECT Room_type from Rooms where Name = '" + room_name + "'")
        for row in cursor:
            room_type = row[0]
        return room_type

    """prints a list of all room allocations
    """ 
    def printallocations():
        pass
