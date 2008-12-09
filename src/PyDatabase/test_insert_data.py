#!/usr/bin/env python
"""
Unittest for HGDP database
"""
import unittest

from connection import session 
from elixir import metadata, setup_all, create_all
from sqlalchemy.exceptions import IntegrityError
from schema import Individual, Population, SNP, RefSeqGene

class TestHGDPDatabase(unittest.TestCase):
    """
    Test the HGDP database APIs (sqlalchemy + elixir)
    """
    
    def setUp(self):
        """create a test database in RAM memory"""
        metadata.bind = 'sqlite:///:memory:'
#        metadata.bind.echo = True
        setup_all()
        create_all()
    
    def test_insertIndividual(self):
        """test the insertion of a few individuals and populations"""
        me = Individual('Giovanni')
        hannibal = Individual('Annibal')
        
        # create populations
        italians = Population('Italians')
        cartaginians = Population('Cartaginians')    # would be better to use more hgdp-related examples
        
        me.population = italians
        hannibal.population = cartaginians   
        
        session.commit()
        session.clear()
        
    def test_duplicatedIndividual(self):
        """adding a duplicated individual should fail
        """
        
        Individual('clone')
        session.clear()
        self.assertRaises(IntegrityError, Individual, 'clone')
        
    
    def test_alotofInsertIndividual(self):
        individuals = [Individual('Ind' + str(i+1)) for i in range(1000)]
        session.commit()
        session.query(Individual).limit(100)
    
    def test_query(self):
        print Individual.query().all()
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHGDPDatabase)
    unittest.TextTestRunner(verbosity=2).run(suite)
#    suite = unittest.TestSuite()
#    suite.addTest(TestHGDPDatabase())
#    suite.run()
#    unittest.main()
