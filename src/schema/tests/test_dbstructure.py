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
from elixir import metadata, setup_all, create_all, drop_all
from sqlalchemy.exceptions import IntegrityError
from schema.schema import Individual, Population, SNP, RefSeqTranscript

class TestHGDPDatabase(unittest.TestCase):
    """
    Metaclass for all the unittests
    """
    @classmethod
    def setUpClass(cls):
        """create a test database in RAM memory"""
        metadata.bind = 'sqlite:///:memory:'
#        metadata.bind.echo = True
        setup_all()
        create_all()
        
    @classmethod
    def tearDownClass(self):
        # clear the session and rollback any open transaction
        session.close()
        # drop all tables, so that we don't leak any data from one test to the
        # other
        drop_all()

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
        cartaginians = Population('Cartaginians')    
        
        me.population = italians
        hannibal.population = cartaginians
#        print Individual.query().all()

    def test_insertALotOfIndividual(self):
        """Tests the insertion of a lot of individuals
        """
        session.commit()
        setup_all()
        individuals = [Individual('Ind' + str(i+1)) for i in range(100)]    #TODO: use an higher value
        
        session.commit()
        for ind in individuals: 
            ind.delete()
#        print Individual.query().all()
        
    def test_duplicatedIndividual(self):
        """adding a duplicated individual should return an IntegrityError
        """
        session.flush()
        clone = Individual('clone')
        clone_again = Individual('clone')
        self.assertRaises(IntegrityError, session.commit)
        session.rollback()

class TestSNPs(TestHGDPDatabase):
    """Test all properties in SNP table
    """
    def test_insertSNP(self):
        pass
    
class TestRecordsProperties(TestHGDPDatabase):
    """tests all the properties of the various records (population.region, etc..)
    """
    
    def test_IndividualMethods(self):
        """Tests all properties in Individual
        """
        me = Individual('giovanni', sex = 'm', population='Italians', region='abruzzo',
                        macroarea = 'Europe', working_unit = 'Italians')
        
        # individual.name must be uppercase.
        # This is not beatiful, but I don't know how to change it.
        self.assertTrue(me.name == 'GIOVANNI')
        self.assertFalse(me.name == 'giovanni') # :(
        self.assertFalse(me.name == 'Giovanni') # :(
        self.assertFalse(me.name == 'GioVanNi') # :(
        
        # Tests the __eq__ and __ne__ methods
        self.assertTrue(me == 'Giovanni')
        self.assertTrue(me == 'GIOVANNI')
        self.assertTrue(me == 'GiovANNi')
        self.assertTrue(me == 'Giovanni')
        
        # This is also not very beatiful
        self.assertTrue(me.sex == 'm')
        self.assertFalse(me.sex == 'M') # :(
        self.assertFalse(me.sex == '1') # :(
        
        self.assert_(me.population == 'italians')
        
        # Test Individuals with a space in their names:
        you = Individual('napoleon bonaparte')
        self.assert_(you == 'napoleon bonaparte')
               
        
    def test_PopulationMethods(self):
        """Tests all properties in Population
        """
        unni = Population('Unni')
        
class TestGetFilter(TestHGDPDatabase):
    """tests get_by, filter_by, etc..
    """
    def test_getandfilter(self):
        me = Individual('giovanni', population='italians')
        
        me_getby = Individual.get_by(name = 'GIOVANNI')
        assert me_getby == me
        
        me_filterby = session.query(Individual).filter_by(name = 'GIOVANNI')
        assert me_filterby[0] == me
        
        # The only way to do a case-indipendent search is by using .filter:
        me_filter = session.query(Individual).filter(Individual.name.like('giovanni'))
        assert me_filter[0] == me
#        
#        me_filterby = Individual.filter(name = 'GIOVAnnI')
#        print me_filterby         
#    
if __name__ == '__main__':
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestInsertDelete)
#    TestRecordsProperties
#    unittest.TextTestRunner(verbosity=4).run(suite)

#    suite = unittest.TestSuite()
#    
#    suite.addTest(TestInsertDelete())
#    suite.addTest(TestRecordsProperties())
#    suite.run()
    unittest.main()

