import unittest
import commands
import logging

from schema.debug_database import *
from elixir import drop_all

class test_rosenberg(unittest.TestCase):
    """
    Test the rosenberg parser
    """

    testfile = 'rosenberg_sample.txt'
    _db_is_set = 0

    def setupdb(self):
        """
        SetUpAll method
        """
        logging.basicConfig(level=logging.DEBUG)
        self._db_is_set = 1
        from parsers import rosenberg_parser
        rosenberg_parser(open(self.testfile, 'r'))

    def setUp(self):
        print self._db_is_set
        create_all()
        if self._db_is_set == 0:
            self.setupdb()
#
    def tearDown(self):
        drop_all()

    def test_individuals(self):
        """test how many individuals"""
        print Individual.query().all()
        print 'dsad'

    def test_SameNumberOfFields(self):
        """
        test if every line in the parser is splitted in the same number of fields
        """
        pass


