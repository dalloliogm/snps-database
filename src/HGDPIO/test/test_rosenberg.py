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
#    _db_is_set = False

    known_individuals = {'HGDP01011': {'continent_code': 'AMERICA', 
                                    'popname': 'Karitiana'},
                        'HGDP01006': {'continent_code': 'AMERICA', 
                                    'popname': 'Karitiana'}}
    not_included = ('HGDP01004', 'HGDP00996')

    @classmethod
    def setUpClass(cls):
#        self._setupdb()
        logging.basicConfig(level=logging.DEBUG, format="%(funcName)s - %(lineno)d - %(message)s")
        metadata.bind = 'sqlite:///:memory:'
        create_all()
        from parsers import rosenberg_parser
        rosenberg_parser(open(cls.testfile, 'r'))
        logging.debug('DB (rosenberg test) has been set')

#    def tearDown(self):
#        session.close()
#        drop_all()

    def test_individuals(self):
        """test how many individuals"""
        individuals = Individual.query().all()
        print len(individuals)
        print individuals
        assert len(individuals) == 2

    def test_SameNumberOfFields(self):
        """
        test if every line in the parser is splitted in the same number of fields
        """
        pass

    def test_NotIncluded(self):
        """
        Checks that the individuals that should not be included, are not in the database
        """
        for ind in self.not_included:
            db_ind = Individual.query.filter_by(name=ind).all()
            self.assertEqual(db_ind, [])

    def test_KnownIndividuals(self):
        """
        """
        for ind in self.known_individuals.keys():
            print ind
            db_ind = Individual.query.filter_by(name=ind).one()
            print db_ind, dir(db_ind)
            self.assert_(db_ind.name == ind)
#        assert 1 == 2

    def test_FirstIndividual(self):
        """Get the first individual and check it"""
        ind1 = Individual.query().all()[0]


