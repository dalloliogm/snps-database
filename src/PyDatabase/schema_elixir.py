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

from elixir import metadata, Entity, Field, Unicode, Integer, UnicodeText, CHAR, ManyToOne, OneToMany, DateTime
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
    
    id = Field(CHAR(10), primary_key=True)
    chromosome = Field(CHAR(10))
    physical_position = Field(Integer)
    haplotypes_index = Field(Integer)

    reference_allele = Field(CHAR(1))
    derived_allele = Field(CHAR(1))
    original_strand = Field(CHAR(1))
    dbSNP_ref = Field(CHAR(10))
    
    refseqgene = ManyToOne('RefSeqGene')
    last_modified = Field(DateTime, onupdate=datetime.datetime.now)
    
    def __init__(self, snp_id):
        self.id = snp_id
        self.chromosome = ''    

class RefSeqGene(Entity):
    pass    
    
    
    
def _test():
    """ test the current module"""
    import doctest
    doctest.testmod()
    
if __name__ == '__main__':
    _test()
        
        
        