import unittest
from db.DatabaseManager import DatabaseManager
from utils.Allocations import Allocations


class AllocationTests(unittest.TestCase):
    """Unit tests for testing various functions in Allocations class"""

    def test_has_room(self):
        """Tests whether function returns if a fellow has a room"""
        allocations = Allocations(
            [["DummyName", "DummyPersonType", "DummyResiding"]])
        # test dummy record
        self.assertFalse(
            allocations.has_room("DummyName", "DummyRoomType"), False)

    def test_are_room_available(self):
        """Tests whether function returns an available room for a certain category"""

        allocations = Allocations(
            [["DummyName", "DummyPersonType", "DummyResiding"]])
        # test dummy record
        self.assertFalse(
            allocations.are_room_available("DummyRoomType"), False)  # The record doesnt exist in the db, should return False

    def test_get_available_rooms(self):
        """Tests whether function returns an available room for a certain category"""
        allocations = Allocations(
            [["DummyName", "DummyPersonType", "DummyResiding"]])
        # if dummy record doesnt exist in the db, should return False
        list_rooms = allocations.get_available_rooms("DummyRoomType")
        self.assertEquals(len(list_rooms), 0)

    def test_randomize_list(self):
        """Tests whether function actually randomizes list passed to it"""
        list1 = ["jack", "john", "james", "peter"]  # initial list
        allocations = Allocations(
            [["DummyName", "DummyPersonType", "DummyResiding"]])
        randomized_list = allocations.randomize_list(list1)  # randomized list
        self.assertNotEqual(list1, randomized_list)  # compare the two lists

    def test_save_allocation(self):
        """Tests saveallocation function"""
        # get number of rows before insert
        db = DatabaseManager("Amity.sqlite")
        cursor = db.query("SELECT * from Allocations")
        rows_before = len(cursor.fetchall())
        allocations = Allocations(
            [["DummyName", "DummyPersonType", "DummyResiding"]])
        allocations.save_allocation(
            "TestName", "Testroomname", "Testroomtype", "Testpersonneltype")  # insert record
        cursor = db.query("SELECT * from Allocations")
        # fetch rows after insert to compare
        rows_after = len(cursor.fetchall())
        db.query(
            "DELETE FROM Allocations where Personnel_Name = 'TestName'")
        self.assertGreater(rows_after, rows_before)

    def test_already_having_room(self):
        """Tests if can allocate already having living space room"""
        # insert record with living space
        db = DatabaseManager("Amity.sqlite")
        db.query(
            "INSERT INTO Allocations (Personnel_Name,Room_type,Room_name,Personnel_type) VALUES('TestUnique','LIVING','TESTROOM','STAFF')")
        allocations = Allocations(
            [["TestUnique", "STAFF", "Y"]])
        list_allocations = allocations.allocate()
        db.query(
            "DELETE FROM Allocations where Personnel_Name = 'TestUnique'")
        self.assertEqual(len(list_allocations), 1)

    def test_allocate(self):
        """Tests allocate functionality"""
        allocations = Allocations(
            [["DummyName", "DummyPersonType", "Y"]])
        list_allocated = allocations.allocate()
        db = DatabaseManager("Amity.sqlite")
        db.query(
            "DELETE FROM Allocations where Personnel_Name = 'DummyName'")
        self.assertLessEqual(len(list_allocated), 1)

    def test_allocate_only_office(self):
        """Tests allocate only office"""
        allocations = Allocations(
            [["DummyName", "STAFF", "N"]])
        list_allocated = allocations.allocate()
        db = DatabaseManager("Amity.sqlite")
        db.query(
            "DELETE FROM Allocations where Personnel_Name = 'DummyName'")
        self.assertLessEqual(len(list_allocated), 1)

    def test_unallocated(self):
        """Tests function to determine if it returns rooms that have been unallocated"""
        allocations = Allocations(
            [["DummyName", "DummyPersonType", "Dummyzz"]])
        allocations.allocate()
        list_unallocated = allocations.unallocated()
        db = DatabaseManager("Amity.sqlite")
        db.query(
            "DELETE FROM Allocations where Personnel_Name = 'DummyName'")
        self.assertEquals(type(list_unallocated), list)

    def test_getalloccupiedrooms(self):
        """Tests whether function returns an rooms that have atleast
        one occupant"""
        allocations = Allocations(
            [["DummyName", "DummyPersonType", "DummyResiding"]])
        # update all room current occupants to sero
        db = DatabaseManager("Amity.sqlite")
        # set all Curppl columns to zero
        db.query("UPDATE Rooms set Curppl = '0'")
        list_rooms = allocations.get_all_occupied_rooms()
        self.assertEquals(len(list_rooms), 0)
