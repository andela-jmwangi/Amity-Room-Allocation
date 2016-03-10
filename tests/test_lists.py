import unittest
from .. import Allocations
from .. import DatabaseManager

"""Unit tests for testing various list functions
"""


class ListTests(unittest.TestCase):

    """Tests random room functionality
    """

    def test_getrandomroom(self):
        allocations = Allocations.Allocations("")
        db = DatabaseManager.DatabaseManager("Amity.sqlite")
        actual_office_list = filter(lambda lvn: 'OFFICE' in lvn, db.getrooms())
        randomized_office_list = allocations.getrandomroom("OFFICE")
        self.assertFalse(actual_office_list == randomized_office_list)
