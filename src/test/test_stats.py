#!/usr/bin/env python
"""
Tests the setup of the stats table, and some queries on it
"""


import unittest as U
import logging
from schema.connection import *
from sqlalchemy.sql import func


class TestStats(U.TestCase):
    """
    Tests for known values
    """

    @classmethod
    def setUpAll(cls):
        logging.basicConfig(level = logging.DEBUG)

    def test_ForEveryChromosomeThereIsAtLeastOneStatSaved(self):
        chromosomes = [str(chr) for chr in range(1, 22)]
        
        for chr in chromosomes:
            stats = Stats.query().filter(Stats.population_key == 'eur').filter(Stats.snp.has(chromosome = str(chr))).limit(1).all()
            logging.debug(stats)

            print
            print chr
            print stats

            self.assertNotEqual(stats, [])

class TestXPEHH(U.TestCase):
    """
    Tests for known values
    """

    @classmethod
    def setUpAll(cls):
        logging.basicConfig(level = logging.DEBUG)

    def test_ForEveryChromosomeThereIsAtLeastOneStatSaved(self):
        chromosomes = [str(chr) for chr in range(1, 22)]
        chromosomes.extend(['X', 'Y'])
        
        for chr in chromosomes:
            stats = XPEHH.query().filter(XPEHH.snp.has(chromosome = str(chr))).limit(1).all()
            logging.debug(stats)

            print
            print chr
            print stats

            self.assertNotEqual(stats, [])


