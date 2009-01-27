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

    known_snps = {'rs4911642' : {'genotype' : 'TTTCTT--TTTCTCTCTTTT--', 'allele1': 'T', 'allele2': 'C'}, 
            'rs2027653' : {'genotype' : '--TTTTTTTTTTTTTTTTTTTT', 'allele1': 'T', 'allele2': 'C'}, 
            'rs5747620' : {'genotype' : 'TCTTTCTTTTTTTTTTTCTTTT', 'allele1': 'T', 'allele2': 'C'}, 
            'rs9605903' : {'genotype' : 'TTTTTTTTTCTTTTTTTTTTTT', 'allele1': 'T', 'allele2': 'C'}, 
            'rs5747968' : {'genotype' : 'TTTTTGTTTGTTTTTTTTTTTT', 'allele1': 'T', 'allele2': 'G'}, 
            'rs2236639' : {'genotype' : 'GGGGAGGGAGAGGGGGGGGGGG', 'allele1': 'A', 'allele2': 'G'}, 
            'rs5747999' : {'genotype' : 'CCACCCCCCCCCCCCCACACCC', 'allele1': 'A', 'allele2': 'C'}, 
            'rs11089263' : {'genotype' : 'CCACCCCCACCCCCCCACACCC', 'allele1': 'A', 'allele2': 'C'}, 
            'rs2096537' : {'genotype' : 'CCACCCACACCCCCCCACACAC', 'allele1': 'A', 'allele2': 'C'}, 
            'rs9604959' : {'genotype' : 'TCTC--CCCCTTTCTCCCCCCC', 'allele1': 'T', 'allele2': 'C'}, 
            'rs9604967' : {'genotype' : 'CCCCCCCCCCCCCCCCCCCCCC', 'allele1': '-', 'allele2': 'C'}, 
            'rs4819849' : {'genotype' : 'AAAAAAAAAAAA--AAAAAAAA', 'allele1': 'A', 'allele2': '-'}, 
            'rs9605028' : {'genotype' : 'AAAAAAAAAAAAAAAAAAAAAA', 'allele1': 'A', 'allele2': '-'},
            'rs1892844' : {'genotype' : 'AAAAAAAAAAAAAAAAAAAAAA', 'allele1': 'A', 'allele2': '-'}, 
            'rs361973' : {'genotype' : 'AGAGAAAAAAAGAA----AAAA', 'allele1': 'A', 'allele2': 'G'}, 
            'rs2845371' : {'genotype' : 'AGAGGGAGAGAGGGAAAAAGGG', 'allele1': 'A', 'allele2': 'G'}, 
            'rs16981507' : {'genotype' : 'CCTCCCCCCCCCCCCCCCCCCC', 'allele1': 'T', 'allele2': 'C'}
            }
    not_included_individuals = ('HGDP01004', 'HGDP00996')
    excluded_columns = [1, 11]

    _db_set_up = False

    @classmethod
    def setUpClass(cls):
#        self._setupdb()
        logging.basicConfig(level=logging.DEBUG, format="%(funcName)s - %(lineno)d - %(message)s")
        metadata.bind = 'sqlite:///:memory:'
        create_all()
        from parsers import genotypes_parser, rosenberg_parser
        # populate with some individuals
        rosenberg_parser(open(cls.individualsfile, 'r'))
        genotypes_parser(open(cls.testfile, 'r'))
        logging.debug('DB (genotype test) has been set')

    def test_NumberGenotypes(self):
        """test how many genotypes have been added"""
        snps = SNP.query().all()
        print len(snps)
        print snps
        assert len(snps) == 17

    def test_GenotypesFile(self):
        """test if the url the to the genotypes file is saved correctly"""
        for snp in SNP.query().all():
            self.assertEqual(snp.genotypes_file, self.testfile)

    def test_SNPGenotypes(self):
        """test if the genotypes have been uploaded correctly"""
        for snp_id in self.known_snps:
            snp = SNP.get_by(id=snp_id)
            print snp_id, snp.id
            print self.known_snps[snp_id]['genotype'], snp.genotypes
            self.assertEqual(self.known_snps[snp_id]['genotype'], snp.genotypes)
           

    def test_GenotypeIndex(self):
        """test if the right index is added to every individual"""
        for ind_id in self.known_individuals.keys():
            ind = Individual.get_by(name=ind_id)
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
            db_snp = SNP.get_by(id=snp)
            self.assertEqual(db_snp, None)

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


