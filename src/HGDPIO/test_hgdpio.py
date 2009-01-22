import unittest
import commands
import logging

from schema.debug_database import *
from elixir import drop_all, setup_all, create_all

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
        
        # create a debug database in memory (could have used debug_database)
        print metadata.bind
        metadata.bind.echo = True

        from parsers import rosenberg_parser
        rosenberg_parser(open(self.testfile, 'r'))
#        individuals = Individual.query().all()
#        logging.debug(individuals)

    def setUp(self):
        print self._db_is_set
        if self._db_is_set == 0:
            self.setupdb()
#
#    def tearDown(self):
#        drop_all()

    def test_individuals(self):
        """test how many individuals"""
        individuals = Individual.query().all()
        logging.debug('dsad')
        logging.debug(individuals)

    def test_SameNumberOfFields(self):
        """
        test if every line in the parser is splitted in the same number of fields
        """
        pass

    def somethingelse(self):
        pass

