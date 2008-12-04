#!/usr/bin/env python
from connection import session 
from elixir import metadata, setup_all, create_all
from schema import Individual, Population, SNP, RefSeqGene

def setup():
    """create a test database in RAM memory"""
    metadata.bind = 'sqlite:///:memory:'
    setup_all()
    create_all()

def test_insert():
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


def test_alotof_insert():
    individuals = [Individual('Ind' + str(i)) for i in range(1000)]
    session.commit()
    session.query(Individual).limit(100)

def test_query():
    print Individual.query().all()
    
if __name__ == '__main__':
    setup()
    test_insert()
    test_alotof_insert()
    print session.query(Individual).all()