#!/usr/bin/env python
"""
Test the performance on retrieval of data from hgdp db

"""

import unittest as U
import logging
from schema.connection import *

class SNPTest(U.TestCase):
    """
    Tsts 
    """
    
    @classmethod
    def setUpAll(cls):
        logging.debug('database connection initialized')
        metadata.bind.echo = True
        

    def setUp(self):
        pass

#    def tearDown(self):
#        self.session.clear()


    def testChromosome22(self):
        chr22snps = SNP.query.filter_by(chromosome = 22).all()
        print chr22snps
#        assert 1 == 2

    def testGetSNPIdFromChromosome22(self):
        chr22snpsids = session.query(SNP.id).filter_by(chromosome = 22).all()
        print chr22snpsids


    def testBantu(self):
        bantus = Individual.query.filter(Individual.population.has(working_unit = 'bantu')).all()
        print bantus
        self.assertEqual(len(bantus), 19)
