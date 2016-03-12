import unittest
from db.DatabaseManager import DatabaseManager
from models import Rooms

"""Unit tests for testing various functions in Rooms class
"""


class RoomsTests(unittest.TestCase):

    """Tests whether function returns correct number of
    rooms with occupants
    """

    def test_rooms_with_occupatants(self):
        rooms = Rooms.Rooms()
        # get number of rooms before insert
        num_before_insert = rooms.get_rooms_with_occupants()
        self.db = DatabaseManager("Amity.sqlite")
        # insert record to increase number of available rooms
        self.db.query(
            "INSERT into Rooms (Name, Maxppl, Curppl, Room_type) VALUES('TestRoom','4','2','OFFICE')")
        # get number of rooms after insert
        num_after_insert = rooms.get_rooms_with_occupants()
        # compare whether the number of available rooms increased
        self.assertGreater(num_after_insert, num_before_insert)

    """Tests whether function returns correct type of Rooms i.e OFFICE or LIVING
    """

    def test_room_type(self):
        rooms = Rooms.Rooms()
        # check which room type Valhalla is
        room_type = rooms.get_room_type("Valhalla")
        self.assertEqual(room_type, "OFFICE")
        
