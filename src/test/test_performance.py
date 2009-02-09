#!/usr/bin/env python
"""
Test the performance on retrieval of data from hgdp db

"""

import unittest as U
import logging
from schema.connection import *
from sqlalchemy.sql import func

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

    def testGetSnpCountByChromosome(self):
        stmt = session.query(SNP.id, SNP.chromosome, func.count('*').label('snp_count')).group_by(SNP.chromosome).subquery()
        print "stmt.c", stmt.c
        for u, count in session.query(SNP, stmt.c.snp_count).\
            outerjoin((stmt, SNP.id==stmt.c.s_id)).order_by(SNP.id):
            print u, count

        print snp_by_chr
        assert 1 == 2


    def testBantu(self):
        bantus = Individual.query.filter(Individual.population.has(working_unit = 'bantu')).all()
        print bantus
        self.assertEqual(len(bantus), 19)
