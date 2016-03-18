import unittest
from utils import FileParser
import os


class File_Parsing_Tests(unittest.TestCase):
    """Unit tests for testing various functions in File Parser class"""

    def test_get_line_contents(self):
        """Tests whether functions returns the correct list of rows of a txt file."""

        parser = FileParser.FileParser(
            os.path.dirname(os.path.realpath("testinput.txt")) + "/tests/testinput.txt")
        list_allocations = parser.read_file()
        self.assertEqual(len(list_allocations), 3)
