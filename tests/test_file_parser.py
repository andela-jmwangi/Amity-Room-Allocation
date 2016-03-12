import unittest
from utils import Fileparser
import os

"""Unit tests for testing various functions in File Parser class
"""


class File_Parsing_Tests(unittest.TestCase):

    """Tests whether functions returns the correct list of rows of a txt file.
    """

    def test_get_line_contents(self):
        parser = Fileparser.Fileparser(
            os.path.dirname(os.path.realpath("testinput.txt")) + "/tests/testinput.txt")
        list_allocations = parser.readfile()
        self.assertEqual(len(list_allocations), 3)
        
