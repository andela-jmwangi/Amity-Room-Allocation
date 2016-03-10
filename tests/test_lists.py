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
        actual_office = allocations.getavailablerooms("OFFICE")[0]
        randomized_office = allocations.getrandomroom("OFFICE")
        self.assertFalse(actual_office == randomized_office)
