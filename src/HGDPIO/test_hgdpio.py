import unittest
import commands
import logging

from schema.debug_database import *
from elixir import drop_all, setup_all, create_all, cleanup_all
setup_all()

class test_rosenberg(unittest.TestCase):
    """
    Test the rosenberg parser
    """

    testfile = 'test/rosenberg_sample_short.txt'
    _db_is_set = False

    def _setupdb(self):
        """
        SetUpAll method
        """
        logging.basicConfig(level=logging.DEBUG)
        self._db_is_set = True
        
        # create a debug database in memory (could have used debug_database)
        print metadata.bind
        metadata.bind.echo = True

        from parsers import rosenberg_parser
        rosenberg_parser(open(self.testfile, 'r'))
#        individuals = Individual.query().all()
#        logging.debug(individuals)

    def setUp(self):
#        self._setupdb()
        metadata.bind = 'sqlite:///:memory:'
        create_all()

    def tearDown(self):
        session.close()
        drop_all()

    def test_individuals(self):
        """test how many individuals"""
        individuals = Individual.query().all()
        logging.debug('dsad')
        logging.debug(individuals)

    def test_SameNumberOfFields(self):
        """
        test if every line in the parser is splitted in the same number of fields
        """
        assert 1 == 1
        pass
#
    def test_somethingelse(self):
        assert 1 == 1
        pass

