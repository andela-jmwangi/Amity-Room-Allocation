import unittest
import sqlite3
from db import DatabaseManager

"""Unit tests for testing various functions in DatabaseManager class
"""


class DatabaseManagerTests(unittest.TestCase):

    """Tests whether function returns all the rooms
    """

    def test_getrooms(self):
        db = DatabaseManager.DatabaseManager("Amity.sqlite")
        rooms_list = db.getrooms()  # retrieve full list of rooms
        # all the rooms should be 20 in number
        self.assertEqual(len(rooms_list), 20)

    """Tests whether function returns correct number of tables in Amity.sqlite db
    """

    def test_tablecount(self):
        db = DatabaseManager.DatabaseManager("Amity.sqlite")
        num_tables = db.gettablecount()  # retrieve count of tables
        self.assertEqual(num_tables, 4)  # all the tables should be 4 in number

    """Tests whether the function creates the three tables
    """

    def test_createtables(self):
        db = DatabaseManager.DatabaseManager("Amity.sqlite")
        num_tables = db.gettablecount()  # retrieve count of tables
        db.createtables()
        # tables should be 4 in number
        self.assertEqual(db.gettablecount(), 4)

    """Tests whether function returns type cursor for the query
    """

    def test_query(self):
        db = DatabaseManager.DatabaseManager("Amity.sqlite")
        # query returns a cursor object type
        cur = db.query("SELECT * from Allocations")
        # check if type is sqlite2 cursor object
        self.assertEqual(type(cur), sqlite3.Cursor)