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

    individualsfile = 'test/rosenberg_sample.txt'
    testfile = 'test/genotypes_sample.txt'
#    _db_is_set = False
    known_individuals = {'HGDP00218': {'index': 0,},
                    'HGDP00248': {'index': 12,},
                    'HGDP00232': {'index': 2,},
                    'HGDP00222': {'index': 3,},
                    'HGDP00228': {'index': 4,},
                    'HGDP00239': {'index': 5,},
                    'HGDP00258': {'index': 6,},
                    'HGDP00247': {'index': 7,},
                    'HGDP00234': {'index': 8,},
                    'HGDP00214': {'index': 9,},
                    'HGDP00262': {'index': 10,},}

    known_snps = ('rs4911642', 
            'rs2027653', 
            'rs5747620', 
            'rs9605903', 
            'rs5747968', 
            'rs2236639', 
            'rs5747999', 
            'rs11089263', 
            'rs2096537', 
            'rs9604959', 
            'rs9604967', 
            'rs4819849', 
            'rs9605028',
            'rs1892844', 
            'rs361973', 
            'rs2845371', 
            'rs16981507')
    not_included_individuals = ('HGDP01004', 'HGDP00996')
    excluded_columns = [1, 11]

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
        assert len(snps) == 17

    def test_genotypeindex(self):
        """test if the right index is added to every individual"""
        for ind_id in self.known_individuals.keys():
            ind = Individual.query.filter_by(name=ind_id).one()
            print ind_id, ind.genotype_index, self.known_individuals[ind_id]['index']
            self.assertEqual(ind.genotype_index, self.known_individuals[ind_id]['index'])


    def test_SameNumberOfFields(self):
        """
        test if every line in the parser is splitted in the same number of fields
        """
        pass

    def test_NotIncluded(self):
        """
        Checks that the individuals that should not be included, are not in the database
        """
        for snp in self.not_included_individuals:
            db_snp = SNP.query.filter_by(id=snp).all()
            self.assertEqual(db_snp, [])

    def test_KnownSNPs(self):
        """
        """
        for snp in self.known_snps:
            print snp
            db_snp = SNP.query.filter_by(id=snp).one()
            print db_snp, dir(db_snp)
            self.assert_(db_snp.id == snp)

    def test_FirstSNP(self):
        """Get the first individual and check it"""
        snp1 = SNP.query().all()[0]


