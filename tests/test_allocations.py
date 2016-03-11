import unittest
from db.DatabaseManager import DatabaseManager
from utils.Allocations import Allocations
from models import Rooms

"""Unit tests for testing various functions in Allocations class
"""


class AllocationTests(unittest.TestCase):

    """Tests whether function returns if a fellow has a room
    """

    def test_has_room(self):
        allocations = Allocations(
            [["DummyName", "DummyPersonType", "DummyResiding"]])
        # test dummy record
        self.assertFalse(
            allocations.hasroom("DummyName", "DummyRoomType"), False)

    """Tests whether function returns an available room for a certain category
    """

    def test_areroomavailable(self):
        allocations = Allocations(
            [["DummyName", "DummyPersonType", "DummyResiding"]])
        # test dummy record
        self.assertFalse(
            allocations.areroomavailable("DummyRoomType"), False)  # The record doesnt exist in the db, should return False

    """Tests whether function returns an available room for a certain category
    """

    def test_getavailablerooms(self):
        allocations = Allocations(
            [["DummyName", "DummyPersonType", "DummyResiding"]])
        # test dummy record
        # The record doesnt exist in the db, should return False
        list_rooms = allocations.getavailablerooms("DummyRoomType")
        self.assertEquals(len(list_rooms), 0)

    """Tests whether function returns an rooms that have atleast one occupant
    """

    def test_getalloccupiedrooms(self):
        allocations = Allocations(
            [["DummyName", "DummyPersonType", "DummyResiding"]])
        # update all room current occupants to sero
        db = DatabaseManager("Amity.sqlite")
        # set all Curppl columns to zero
        db.query("UPDATE Rooms set Curppl = '0'")
        list_rooms = allocations.getalloccupiedrooms()
        self.assertEquals(len(list_rooms), 0)

    """Tests whether function actually randomizes list passed to it
    """

    def test_randomizelist(self):
        list1 = ["jack", "john", "james", "peter"]  # initial list
        allocations = Allocations(
            [["DummyName", "DummyPersonType", "DummyResiding"]])
        randomized_list = allocations.randomizelist(list1)  # randomized list
        self.assertNotEqual(list1, randomized_list)  # compare the two lists

    """Tests saveallocation function
    """

    def test_save_allocation(self):
        # get number of rows before insert
        db = DatabaseManager("Amity.sqlite")
        cursor = db.query("SELECT * from Allocations")
        rows_before = len(cursor.fetchall())
        allocations = Allocations(
            [["DummyName", "DummyPersonType", "DummyResiding"]])
        allocations.saveallocation(
            "TestName", "Testroomname", "Testroomtype", "Testpersonneltype")  # insert record
        cursor = db.query("SELECT * from Allocations")
        rows_after = len(cursor.fetchall())  # fetch rows after insert to compare
        self.assertGreater(rows_after, rows_before)

    """Tests allocate functionality
    """

    def test_allocate(self):
        allocations = Allocations(
            [["DummyName", "DummyPersonType", "Y"]])
        list_allocated = allocations.allocate() 
        self.assertEqual(len(list_allocated),1)

    # """Tests function to determine if it returns rooms that have been unallocated
    # """
    # def test_unallocated(self):
    #     allocations = Allocations(
    #         [["DummyName", "DummyPersonType", "Dummyzz"]])
    #     allocations.allocate()
    #     list_unallocated = allocations.unallocated()
    #     self.assertEquals(type(list_unallocated),set) 
