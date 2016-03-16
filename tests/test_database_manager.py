import unittest
import sqlite3
from db import DatabaseManager


class DatabaseManagerTests(unittest.TestCase):
    """Unit tests for testing various functions in DatabaseManager class"""

    def test_getrooms(self):
        """Tests whether function returns all the rooms"""

        db = DatabaseManager.DatabaseManager("Amity.sqlite")
        rooms_list = db.get_rooms()  # retrieve full list of rooms
        # all the rooms should be 20 in number
        count = 0
        for room_type, data in rooms_list.iteritems():
            for name, num in data.iteritems():
                count += 1
        self.assertEqual(count, 20)

    def test_tablecount(self):
        """Tests whether function returns correct number of tables in Amity.sqlite db"""

        db = DatabaseManager.DatabaseManager("Amity.sqlite")
        num_tables = db.get_table_count()  # retrieve count of tables
        self.assertEqual(num_tables, 4)  # all the tables should be 4 in number

    def test_createtables(self):
        """Tests whether the function creates the three tables"""
        db = DatabaseManager.DatabaseManager("Amity.sqlite")
        num_tables = db.get_table_count()  # retrieve count of tables
        db.create_tables()
        # tables should be 4 in number
        self.assertEqual(num_tables, 4)

    def test_query(self):
        """Tests whether function returns type cursor for the query"""
        db = DatabaseManager.DatabaseManager("Amity.sqlite")
        # query returns a cursor object type
        cur = db.query("SELECT * from Allocations")
        # check if type is sqlite2 cursor object
        self.assertEqual(type(cur), sqlite3.Cursor)
