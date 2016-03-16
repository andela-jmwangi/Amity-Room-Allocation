from db.DatabaseManager import DatabaseManager


class Rooms(object):
    """This class provides various details about rooms"""

    def __init__(self):
        self.db = DatabaseManager("Amity.sqlite")

    def get_rooms_with_occupants(self):
        """gets a list of staff allocated to a specific room or all rooms in general"""

        list_rooms = []  # initiate empty list
        # query db to check if a room exists with less occupants than its
        # maximum capacity
        cursor = self.db.query(
            "SELECT * from Rooms where Curppl > 0")
        for row in cursor:
            list_rooms.append(row[1])  # populate list with room names(row[1]).
        return list_rooms

    def get_room_type(self, room_name):
        """queries db to get room type given the name of a room"""

        room_type = ""
        cursor = self.db.query(
            "SELECT Room_type from Rooms where Name = '" + room_name + "'")
        for row in cursor:
            room_type = row[0]  # get room type to be returned
        return room_type
