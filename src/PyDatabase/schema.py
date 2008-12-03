#!/usr/bin/env python
# Create a database for HGDP data
"""
Creates a temporary database (in RAM, using sqlite) for HGDP data.

Uses Elixir syntax instead of sqlalchemy
- http://elixir.ematia.de/

>>> from elixir import *
>>> metadata.bind = 'sqlite:///:memory:'
>>> metadata.bind.echo = True

# Create SQLAlchemy Tables along with their mapper objects
>>> setup_all()

# Issue the SQL command to create the Tables
>>> create_all()

>>> pop1 = Population('martians')
>>> ind1 = Individual('Einstein')
>>> ind2 = Individual('Marx')
>>> pop1.individuals.append(ind1)
>>> pop1.individuals.append(ind2)

>>> pop1.individuals
[Mr. Einstein (martians), Mr. Marx (martians)]

>>> session.commit()
"""

from elixir import metadata, Entity, Field, Unicode, Integer, UnicodeText, String, ManyToOne, OneToMany, DateTime
from config import connection_line
import datetime

#from PopGen.Gio.Individual import Individual
#from PopGen.Gio.SNP import SNP
#from PopGen.Gio.Individual import Individual

metadata.bind = connection_line
metadata.bind.echo = True

class SNP(Entity):
    """ Table 'SNPs'.
    
    This class represents both the table SNP, and the structure of an instance of a SNP object
    
    >>> rs1333 = SNP('rs1333')
    """
    
    id                  = Field(String(10), primary_key=True)
    chromosome          = Field(String(10))
    physical_position   = Field(Integer)
    haplotypes_index    = Field(Integer)

    reference_allele    = Field(String(1))
    derived_allele      = Field(String(1))
    original_strand     = Field(String(1))
    dbSNP_ref           = Field(String(10))
    
    refseqgene          = ManyToOne('RefSeqGene')
    last_modified       = Field(DateTime, onupdate=datetime.datetime.now,
                                default = datetime.datetime.now)
    
    def __init__(self, snp_id):
        self.id = snp_id
        self.chromosome = ''
        self.last_modified = datetime.datetime.now()
            
    def __repr__(self):
        # this method will be called when, in python code, you will do 'print SNP'.
        return 'SNP '  + self.id 

class Individual(Entity):
    """ Table 'Individuals'
    
    >>> ind = Individual('Einstein')
    >>> ind                              # Test __repr__ method
    Mr. Einstein (None)
    >>> print ind + ' Albert'            # Test __add__ method
    Einstein Albert
    >>> print ind in ('Einstein', )      # Test __eq__ method
    True
    """
    identificator       = Field(String(10))
    population          = ManyToOne('Population')
    sex                 = Field(String(1))
    
    last_modified       = Field(DateTime, onupdate=datetime.datetime.now, 
                          default = datetime.datetime.now)
    
    def __init__(self, id):
        """
        """
        self.identificator = str(id)
#        self.population = 0      # corresponds to an Undefined Population
        self.sex = 0
#        self.last_modified = datetime.datetime.now()
    def __repr__(self):
        if self.sex in (0, 1):
            r = "Mr. %s (%s)" %(self.identificator, self.population)
        else:
            r = "Mrs. %s (%s)" %(self.identificator, self.population)
        return r
    def __str__(self):
        return self.identificator
    def __add__(self, other):
        return str(self.identificator) + other 
    def __eq__(self, other):
        return self.identificator == other
    def __ne__(self, other):
        return self.identificator != other
    
    
class Population(Entity):
#    id = Field(Integer, primary_key = True)    # created automatically
    individuals         = OneToMany('Individual')
    name                = Field(String(50))
    geographycal_area   = Field(String(30))
#    version                 = Column(Integer, ForeignKey('versions.id'))
    last_modified       = Field(DateTime, onupdate=datetime.datetime.now,
                                default = datetime.datetime.now)
    
    def __init__(self, name=None):
        self.name = name
        
    def __repr__(self):
        return str(self.name)

class RefSeqGene(Entity):
    pass    
    
    
    
def _test():
    """ test the current module"""
    import doctest
    doctest.testmod()
    
if __name__ == '__main__':
    _test()
        
        
        