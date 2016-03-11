import unittest
from models import Personnel
from db  import DatabaseManager

"""Unit tests for testing various functions in Personnel class
"""


class PersonnelTests(unittest.TestCase):

    """Tests whether functions returns the correct list of
        unallocated persons
    """

    def test_unallocated(self):
        personnel = Personnel.Personnel()
        # initialise two lists with different number of elements
        list1 = ["Jack", "Mwangi", "Wachira"]
        list2 = ["Jack", "Wachira"]
        list_unallocated = personnel.getunallocated(
            list2, list1)  # get difference of the two lists
        # check whether the length of the difference is equal to 1
        self.assertEqual(len(list_unallocated), 1)

    """Tests whether function retrieves correct list of room allocations
    """

    def test_room_allocations(self):
        personnel = Personnel.Personnel()
        # get number of allocations before insert
        num_before_insert = personnel.getallallocations()
        self.db = DatabaseManager.DatabaseManager("Amity.sqlite")
        # insert allocation manually
        self.db.query(
            "INSERT into Allocations (Personnel_Name, Room_type, Room_name, Personnel_type) VALUES('TestRecord','OFFICE','TestRoom','STAFF')")
        # get number of allocations after insert
        num_after_insert = personnel.getallallocations()
        # compare whether the number of allocations increased
        self.assertGreater(num_after_insert, num_before_insert)

    """Tests whether function gets correct room name
    """

    def test_room_allocated(self):
        personnel = Personnel.Personnel()
        # returns the room name given room type and fellow name
        room_allocated = personnel.getroomallocated(
            "OFFICE", "ANDREW PHILLIPS")
        self.assertEqual(room_allocated, "Narnia")
