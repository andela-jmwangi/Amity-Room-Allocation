import unittest
from models import Personnel
from db import DatabaseManager


class PersonnelTests(unittest.TestCase):
    """Unit tests for testing various functions in Personnel class"""

    def test_unallocated(self):
        """Tests whether functions returns the correct list of
        unallocated persons"""

        personnel = Personnel.Personnel()
        # initialise two lists with different number of elements
        list1 = ["Jack", "Mwangi", "Wachira"]
        list2 = ["Jack", "Wachira"]
        list_unallocated = personnel.get_unallocated(
            list2, list1)  # get difference of the two lists
        # check whether the length of the difference is equal to 1
        self.assertEqual(len(list_unallocated), 1)

    def test_room_allocations(self):
        """Tests whether function retrieves correct list of room allocations"""
        personnel = Personnel.Personnel()
        # get number of allocations before insert
        num_before_insert = personnel.get_all_allocations()
        self.db = DatabaseManager.DatabaseManager("Amity.sqlite")
        # insert allocation manually
        self.db.query(
            "INSERT into Allocations (Personnel_Name, Room_type, Room_name, Personnel_type) VALUES('TestRecord','OFFICE','TestRoom','STAFF')")
        # get number of allocations after insert
        num_after_insert = personnel.get_all_allocations()
        # compare whether the number of allocations increased
        self.assertGreater(num_after_insert, num_before_insert)

    def test_room_allocated(self):
        """Tests whether function gets correct room name"""
        personnel = Personnel.Personnel()
        # returns the room name given room type and fellow name
        room_allocated = personnel.get_room_allocated(
            "OFFICE", "ANDREW PHILLIPS")
        self.assertEqual(type(room_allocated), unicode)

    def test_residing(self):
        """Tests whether function returns correct residing state"""
        personnel = Personnel.Personnel()
        state = personnel.is_residing("IYANU ALIMI")
        self.assertEquals(state, "Y")
