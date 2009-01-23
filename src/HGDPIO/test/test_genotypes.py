import unittest
import commands
import logging

from schema.debug_database import *
from elixir import drop_all, setup_all, create_all, cleanup_all
setup_all()

class test_genotypes(unittest.TestCase):
    """
    Test the genotypes parser
    """

    individualsfile = 'test/rosenberg_sample_short.txt'
    testfile = 'test/genotypes_sample.txt'
#    _db_is_set = False
    known_snps = {'HGDP00448':(),
                    'HGDP00479' : (),
                    'HGDP00985' : (),
                    'HGDP01094' : (),
                    'HGDP00982' : (),
                    'HGDP00911' : (),   
                    'HGDP01202' : (),   
                    'HGDP00927' : (),   
                    'HGDP00461' : (),   
                    'HGDP00451' : (),   
                    'HGDP00986' : (),
                    'HGDP00449' : (),
                    'HGDP009830' : ()}
    not_included = ()

    def setUp(self):
#        self._setupdb()
        logging.basicConfig(level=logging.DEBUG, format="%(funcName)s - %(lineno)d - %(message)s")
        metadata.bind = 'sqlite:///:memory:'
        create_all()
        from parsers import genotypes_parser, rosenberg_parser
        # populate with some individuals
        rosenberg_parser(open(self.individualsfile, 'r'))
        genotypes_parser(open(self.testfile, 'r'))

    def tearDown(self):
        session.close()
        drop_all()

    def test_genotypes(self):
        """test how many genotypes have been added"""
        snps = SNP.query().all()
        print len(snps)
        print snps
        assert len(snps) == 2

    def test_SameNumberOfFields(self):
        """
        test if every line in the parser is splitted in the same number of fields
        """
        pass

    def test_NotIncluded(self):
        """
        Checks that the individuals that should not be included, are not in the database
        """
        for snp in self.not_included:
            db_snp = SNP.query.filter_by(id=snp).all()
            self.assertEqual(db_snp, [])

    def test_KnownSNPs(self):
        """
        """
        for snp in self.known_snps.keys():
            print snp
            db_snp = SNP.query.filter_by(id=snp).one()
            print db_snp, dir(db_snp)
            self.assert_(snp.id == snp)
#        assert 1 == 2

    def test_FirstSNP(self):
        """Get the first individual and check it"""
        snp1 = SNP.query().all()[0]


