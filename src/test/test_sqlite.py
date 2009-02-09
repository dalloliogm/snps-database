#!/usr/bin/env python
"""
Test the performance on retrieval of data from hgdp db

"""

import unittest as U
import logging
from schema.debug_database import *
from setupdb.insert_individuals import upload_rosenberg_individuals

class SNPTest(U.TestCase):
    """
    Tsts 
    """
    
    @classmethod
    def setUpAll(cls):
        logging.debug('database connection initialized to %s' % metadata)
        metadata.bind.echo = True
        upload_rosenberg_individuals(open('../data/Annotations/hgdpSampleinfoRosenberg-extended.csv', 'r'),
                                        session, metadata)

        

    def setUp(self):
        pass

#    def tearDown(self):
#        self.session.clear()


    def testChromosome22(self):
        chr22snps = SNP.query.filter_by(chromosome = 22).all()
        print chr22snps
#        assert 1 == 2


    def testBantu(self):
        bantus = Individual.query.filter(Individual.population.has(working_unit = 'bantu')).all()
        print bantus
        self.assertEqual(len(bantus), 19)
