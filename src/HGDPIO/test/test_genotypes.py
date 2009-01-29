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
                    'HGDP00248': {'index': 10,},
                    'HGDP00232': {'index': 1,},
                    'HGDP00222': {'index': 2,},
                    'HGDP00228': {'index': 3,},
                    'HGDP00239': {'index': 4,},
                    'HGDP00258': {'index': 5,},
                    'HGDP00247': {'index': 6,},
                    'HGDP00234': {'index': 7,},
                    'HGDP00214': {'index': 8,},
                    'HGDP00262': {'index': 9,},}

    known_snps = {'rs4911642' : {'raw_genotype' : 'TTTCTT--TTTCTCTCTTTT--', 
                                    'genotype_code': '01090111009', 'allele1': 'T', 'allele2': 'C'}, 
            'rs2027653' : {'raw_genotype' : '--TTTTTTTTTTTTTTTTTTTT', 
                                    'genotype_code': '90000000000', 'allele1': 'T', 'allele2': 'C'}, 
            'rs5747620' : {'raw_genotype' : 'TCTTTCTTTTTTTTTTTCTTTT', 
                                    'genotype_code': '10100000100', 'allele1': 'T', 'allele2': 'C'}, 
            'rs9605903' : {'raw_genotype' : 'TTTTTTTTTCTTTTTTTTTTTT', 
                                    'genotype_code': '00001000000', 'allele1': 'T', 'allele2': 'C'}, 
            'rs5747968' : {'raw_genotype' : 'TTTTTGTTTGTTTTTTTTTTTT', 
                                    'genotype_code': '00101000000', 'allele1': 'T', 'allele2': 'G'}, 
            'rs2236639' : {'raw_genotype' : 'GGGGAGGGAGAGGGGGGGGGGG', 
                                    'genotype_code': '22121122222', 'allele1': 'A', 'allele2': 'G'}, 
            'rs5747999' : {'raw_genotype' : 'CCACCCCCCCCCCCCCACACCC', 
                                    'genotype_code': '21222222112', 'allele1': 'A', 'allele2': 'C'}, 
            'rs11089263' : {'raw_genotype' : 'CCACCCCCACCCCCCCACACCC', 
                                    'genotype_code': '21221222112', 'allele1': 'A', 'allele2': 'C'}, 
            'rs2096537' : {'raw_genotype' : 'CCACCCACACCCCCCCACACAC', 
                                    'genotype_code': '21211222111', 'allele1': 'A', 'allele2': 'C'}, 
            'rs9604959' : {'raw_genotype' : 'TCTC--CCCCTTTCTCCCCCCC', 
                                    'genotype_code': '11922011222', 'allele1': 'T', 'allele2': 'C'}, 
            'rs9604967' : {'raw_genotype' : 'CCCCCCCCCCCCCCCCCCCCCC', 
                                    'genotype_code': '22222222222', 'allele1': '-', 'allele2': 'C'}, 
            'rs4819849' : {'raw_genotype' : 'AAAAAAAAAAAA--AAAAAAAA', 
                                    'genotype_code': '00000090000', 'allele1': 'A', 'allele2': '-'}, 
            'rs9605028' : {'raw_genotype' : 'AAAAAAAAAAAAAAAAAAAAAA', 
                                    'genotype_code': '00000000000', 'allele1': 'A', 'allele2': '-'},
            'rs1892844' : {'raw_genotype' : 'AAAAAAAAAAAAAAAAAAAAAA', 
                                    'genotype_code': '00000000000', 'allele1': 'A', 'allele2': '-'}, 
            'rs361973' : {'raw_genotype' : 'AGAGAAAAAAAGAA----AAAA', 
                                    'genotype_code': '11000109900', 'allele1': 'A', 'allele2': 'G'}, 
            'rs2845371' : {'raw_genotype' : 'AGAGGGAGAGAGGGAAAAAGGG', 
                                    'genotype_code': '11211120012', 'allele1': 'A', 'allele2': 'G'}, 
            'rs16981507' : {'raw_genotype' : 'CCTCCCCCCCCCCCCCCCCCCC', 
                                    'genotype_code': '21222222222', 'allele1': 'T', 'allele2': 'C'}
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
            print self.known_snps[snp_id]['genotype_code'], snp.genotypes
            self.assertEqual(self.known_snps[snp_id]['genotype_code'], snp.genotypes)
           

    def test_GenotypeIndex(self):
        """test if the right index is added to every individual"""
        for ind_id in self.known_individuals.keys():
            ind = Individual.get_by(name=ind_id)
            print ind_id, ind.genotypes_index, self.known_individuals[ind_id]['index']
            self.assertEqual(ind.genotypes_index, self.known_individuals[ind_id]['index'])


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


