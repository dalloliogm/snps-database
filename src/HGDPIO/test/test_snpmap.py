import unittest
import commands
import logging

from schema.debug_database import *
from elixir import drop_all, setup_all, create_all, cleanup_all
setup_all()

class test_map(unittest.TestCase):
    """
    Test the genotypes parser
    """

#    individualsfile = 'test/rosenberg_sample.txt'
    mapfile = 'test/map_sample.txt'

    known_snps = {'rs4911642' : {'chromosome': 'M', 'position': 9900, },
            'rs2027653' : {'chromosome': 'M', 'position': 9951, },
            'rs5747620' : {'chromosome': '4', 'position': 30979886, },
            'rs9605903' : {'chromosome': '4', 'position': 186505570, },
            'rs5747968' : {'chromosome': '4', 'position': 131516474, },
            'rs2236639' : {'chromosome': '4', 'position': 182579995, },
            'rs5747999' : {'chromosome': '4', 'position': 166098831, },
            'rs11089263' : {'chromosome': '4', 'position': 159087423, },
            'rs2096537' : {'chromosome': '5', 'position': 1000, },
            'rs9604959' : {'chromosome': '5', 'position': 1200, },
            'rs9604967' : {'chromosome': '5', 'position': 1400, },
            'rs4819849' : {'chromosome': '5', 'position': 1600, },
            'rs9605028' : {'chromosome': '5', 'position': 2000, },
            'rs1892844' : {'chromosome': '10', 'position': 10000, },
            'rs361973' : {'chromosome': '10', 'position': 12000, },
            'rs2845371' : {'chromosome': '10', 'position': 14000, },
            'rs16981507' : {'chromosome': '10', 'position': 16000, },
            }

    @classmethod
    def setUpClass(cls):
#        self._setupdb()
        logging.basicConfig(level=logging.DEBUG, format="%(funcName)s - %(lineno)d - %(message)s")
        metadata.bind = 'sqlite:///:memory:'
        create_all()

        # upload some SNPs to test the get_by_or_update behaviour
#        SNP('rs4911642')
#        SNP('rs2027653')
#        SNP('rs5747620')
        for snp_id in cls.known_snps:
            SNP(snp_id)
        session.commit()
#        logging.debug(SNP.query().all())

        from parsers import snpmap_parser
        # populate with some individuals
        snpmap_parser(open(cls.mapfile, 'r'))
        logging.debug('DB (snp test) has been set')

#    def test_NumberGenotypes(self):
#        """test how many genotypes have been added"""
#        snps = SNP.query().all()
#        print len(snps)
#        print snps
#        assert len(snps) == 17

    def test_ChromosomeAndPosition(self):
        """Test if chromosome and position are uploaded correctly"""
        for snp_id in self.known_snps:
            snp = SNP.get_by(id=snp_id)
            self.assertEqual(self.known_snps[snp_id]['chromosome'], snp.chromosome)
            self.assertEqual(self.known_snps[snp_id]['position'], snp.physical_position)

#    def test_GenotypesFile(self):
#        """test if the url the to the SNP map file is saved correctly"""
#        for snp in SNP.query().all():
#            self.assertEqual(snp.genotypes_file, self.mapfile)

    def test_KnownSNPs(self):
        """
        """
        for snp in self.known_snps:
            print snp
            db_snp = SNP.get_by(id=snp)
            print db_snp, dir(db_snp)
            self.assert_(db_snp.id == snp)

    def test_FirstSNP(self):
        """Get the first individual and check it"""
        snp1 = SNP.query().all()[0]


