#!/usr/bin/env python
"""
Unittest for HGDP database

TestInsertDelete
    tests the insertion of a lot of records in the database
TestRecordsProperties
    tests all the properties of the various records (population.region, etc..)
TestRelationships
    tests all relationships?
TestHGDPIO
    tests the HGDPIO libraries, to parse HGDP files and insert them in the database
TestGenotypesExtract
    tests extraction of genotypes from the corresponding row
"""
import unittest

from connection import session 
from elixir import metadata, setup_all, create_all, cleanup_all
from sqlalchemy.exceptions import IntegrityError
from schema import Individual, Population, SNP, RefSeqGene

class TestHGDPDatabase(unittest.TestCase):
    """
    Metaclass for all the unittests
    """
    def setUp(self):
        """create a test database in RAM memory"""
        metadata.bind = 'sqlite:///:memory:'
#        metadata.bind.echo = True
        setup_all()
        create_all()
        
#    def tearDown(self):
#        cleanup_all()

class TestInsertDelete(TestHGDPDatabase):
    """
    Test the insertion and deletion of records into the 
    HGDP database.  
    """
        
    def test_insertIndividual(self):
        """test the insertion of a few individuals and populations
        """
        session.flush()
        me = Individual('Giovanni')
        hannibal = Individual('Annibal')
        
        # create populations
        italians = Population('Italians')
        cartaginians = Population('Cartaginians')    # would be better to use more hgdp-related examples
        
        me.population = italians
        hannibal.population = cartaginians

        session.commit()
        session.clear()   
    
    def test_insertALotOfIndividual(self):
        """Tests the insertion of a lot of individuals
        """
        session.commit()
        setup_all()
#        metadata.bind.echo = True
        individuals = [Individual('Ind' + str(i+1)) for i in range(100)]
   
        session.commit()
        session.clear()
        
    def test_duplicatedIndividual(self):
        """adding a duplicated individual should return an IntegrityError
        """
        session.flush()
        clone = Individual('clone')
        clone_again = Individual('clone')
        self.assertRaises(IntegrityError, session.commit)
        session.rollback()    
        session.clear()


    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestInsertDelete)
    unittest.TextTestRunner(verbosity=4).run(suite)
#    suite = unittest.TestSuite()
#    suite.addTest(TestHGDPDatabase())
#    suite.run()
#    unittest.main()

