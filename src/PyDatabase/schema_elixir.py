#!/usr/bin/env python
# Create a database for HGDP data
"""
Creates a temporary database (in RAM, using sqlite) for HGDP data.

Uses Elixir syntax instead of sqlalchemy
- http://elixir.ematia.de/

>>> from elixir import *
>>> metadata.bind = 'sqlite:///:memory:'
>>> metadata.bind.echo = True

>>> setup_all()
>>> create_all()

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
    
    id = Field(String(10), primary_key=True)
    chromosome = Field(String(10))
    physical_position = Field(Integer)
    haplotypes_index = Field(Integer)

    reference_allele = Field(String(1))
    derived_allele = Field(String(1))
    original_strand = Field(String(1))
    dbSNP_ref = Field(String(10))
    
    refseqgene = ManyToOne('RefSeqGene')
    last_modified = Field(DateTime, onupdate=datetime.datetime.now)
    
    def __init__(self, snp_id):
        self.id = snp_id
        self.chromosome = ''
            
    def __repr__(self):
        # this method will be called when, in python code, you will do 'print SNP'.
        return 'SNP '  + self.id 

class Individual(Entity):
    """ Table 'Individuals'
    
    >>> ind = Individual('HGDP_Einstein')
    >>> print ind
    Mr. HGDP_Einsten (population = 1)
    >>> print Einstein + ' Albert'            # Test __add__ method
    Einstein Albert
    >>> print Einstein in ('Einstein', )      # Test __eq__ method
    True
    """
    id = Field(Integer, primary_key = True)    # not necessary
    population = OneToMany('Population')
    sex = Field(String(1))
    
    last_modified = Field(DateTime, onupdate=datetime.datetime.now)
    
    def __init__(self, id):
        """
        """
        self.individual_id = id
        self.population_id = 0      # corresponds to an Undefined Population
        self.sex = 0  
    def __repr__(self):
        if self.sex in (0, 1):
            r = "Mr. %s (%s)" %(self.individual_id, self.population_id)
        else:
            r = "Mrs. %s (%s)" %(self.individual_id, self.population_id)
        return r
    def __str__(self):
        """
        """
        return self.individual_id
    def __add__(self, other):
        return str(self.individual_id) + other 
    def __eq__(self, other):
        return self.individual_id == other
    def __ne__(self, other):
        return self.individual_id != other
    
    
class Population(Entity):
    id = Field(Integer, primary_key = True)
    individuals = ManyToOne('Individual')
    name = Field(String(50))
    geographycal_area = Field(String(30))
#    version                 = Column(Integer, ForeignKey('versions.id'))
    last_modified = Field(DateTime, onupdate=datetime.datetime.now)
    
    def __init__(self):
        pass
    pass

class RefSeqGene(Entity):
    pass    
    
    
    
def _test():
    """ test the current module"""
    import doctest
    doctest.testmod()
    
if __name__ == '__main__':
    _test()
        
        
        