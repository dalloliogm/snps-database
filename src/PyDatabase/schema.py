#!/usr/bin/env python
# Create a database for HGDP data

"""
Creates a temporary database (in RAM, using sqlite) for HGDP data.

Refer to sqlalchemy manual, and in particular to this passage:
- http://www.sqlalchemy.org/docs/05/ormtutorial.html#datamapping_declarative

"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime
from sqlalchemy.orm import relation, backref
from connection import engine, Base
from sqlalchemy.databases.mysql import MSEnum, MSLongBlob
import datetime
import logging

logging.debug(Base.metadata)
#from PopGen import Gio

class SNP(Base):        # I could derive this from PopGen classes, but it would be a mess 
    """
    Table 'SNPs'.
    
    This class represents both the table SNP, and the structure of an instance of a SNP object
    
    # First, you have to instantiate a connection to a database, if you haven't already done it:
    >>> engine = create_engine('sqlite:///:memory:', echo=True)
    >>> from sqlalchemy.orm import sessionmaker
    >>> Session = sessionmaker(engine)
    >>> session = Session()
    
    # Create a table called SNP in a temporary database:
    >>> from create_database import SNP
    >>> SNP.metadata.create_all(engine)    
    
    # Create a SNP object with the id rs1334:
    >>> rs1334 = SNP('rs1334')
    >>> rs1334.chromosome = 11
    
    # Insert SNP rs1334 into SNP table:
    >>> session.add(rs1334)    #doctest +ELLIPSIS
    >>> session.commit()
    
    # Get all SNPs in chromosome 11 (should be only rs1334)
    >>> session.query(SNP).filter_by(chromosome = 11).all()
    [SNP rs1334]
    """
    __tablename__ = 'snps'
    
    snp_id                  = Column(String(10), primary_key=True)
    chromosome              = Column(String(10), index = True)  # should be a choice between 1-22-XY
    physical_position       = Column(Integer)
    genetic_position        = Column(Integer)
    reference_allele        = Column(String(2))
    derived_allele          = Column(String(2))
    original_strand         = Column(MSEnum('+', '-', ' ')) # could be standardized by usign a sqlalchemy recipe
    dbSNP_ref               = Column(String(10))
    refseq_gene             = relation('RefSeqGene', backref='RefSeqGene.id')
    
    # duplicated snps:
    aliases                 = relation('SNP', backref=backref('snps.snp_id'))
#    version                 = Column(Integer, ForeignKey('versions.id'))
    last_modified           = Column(DateTime, onupdate=datetime.datetime.now)

    
    def __init__(self,  snp_id):
        # this method will be launched when you create an instance of a SNP object. 
        # e.g. when you call rs1334 = SNP(id='rs1334') 
        self.snp_id = snp_id            # should check whether this already exists.
        self.chromosome = ''
        self.aliases = ''
        
        
    def __repr__(self):
        # this method will be called when, in python code, you will do 'print SNP'.
        return 'SNP '  + self.snp_id


class Individual(Base):
    """
    Table 'Individuals'
    
    >>> ind = Individual('HGDP_Einstein')
    >>> print ind
    Mr. HGDP_Einsten (population = 1)
    >>> print Einstein + ' Albert'            # Test __add__ method
    Einstein Albert
    >>> print Einstein in ('Einstein', )      # Test __eq__ method
    True
    """
    __tablename__ = 'individuals'
    
    id                      = Column(Integer, primary_key = True)
    population              = relation('Population', backref=backref('individuals', 
                                                                     order_by='Individual.id'))
    sex                     = Column(Integer)
#    version                 = Column(Integer, ForeignKey('versions.id'))
    last_modified           = Column(DateTime, onupdate=datetime.datetime.now)
    
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
    
#class Genotype(Base):
#    """
#    Table 'Genotypes'
#    """
#    __tablename__ = 'genotypes'
#    
#    genotype_id             = Column(Integer, primary_key = True)
#    snp_id                  = relation(SNP, backref = backref('snps.snp_id'))
#    individual_id           = relation(Individual, backref = ('individuals.individual_id'))
#    genotype_code           = Column(MSEnum('0', '1', '2'))
##    version                 = Column(Integer, ForeignKey('versions.id'))
#    last_modified           = Column(DateTime, onupdate=datetime.datetime.now)
#    
#    def __init__(self):
#        pass
    

class Population(Base):
    """
    Table 'Populations'
    Refers to the standard population table of ## populations
    """
    __tablename__ = 'populations'
    
    id                      = Column(Integer, primary_key = True)
    individuals             = relation('Individual', order_by = 'Individual.id', 
                                       backref = 'population')
    name                    = Column(String(50))
    geographycal_area       = Column(String(30))
#    version                 = Column(Integer, ForeignKey('versions.id'))
    last_modified           = Column(DateTime, onupdate=datetime.datetime.now)
    
    def __init__(self):
        pass


#class Version(Base):
#    """
#    Table 'Version'
#    
#    Every SNP/Individual/Population row has a 'version' field, which indicates when it has been last changed 
#    """
#    __tablename__ = 'versions'
#    
#    id                      = Column(Integer, primary_key = True) 
#    description             = Column(String(100))  
#    date                    = Column(Date)
#    
#    def __init__(self):
#        pass
    
    
class RefSeqGene(Base):
    """
    Table 'RefSeq Genes'.
    
    Obtained from http://genome.ucsc.edu, table browser, human assembly march 2006, Genes and gene prediction tracks, known genes, refseq genes
    
    """
    __tablename__ = 'refseqgenes'
    
    id                      = Column(Integer, primary_key = True)   # autoincrement is enabled by default
    name                    = Column(String(255))
    chrom                   = Column(String(255))
    strand                  = Column(MSEnum('+', '-', ' '))
    txStart                 = Column(Integer(10))
    txEnd                   = Column(Integer(10))
    cdsStart                = Column(Integer(10))
    cdsEnd                  = Column(Integer(10))
    exonCount               = Column(Integer)
    exonStarts              = Column(MSLongBlob)
    exonEnds                = Column(MSLongBlob)
    alternateName           = Column(String(255))  # name2 in UCSC
    cdsStartStat            = Column(MSEnum('none','unk','incmpl','cmpl'))
    cdsEndStat              = Column(MSEnum('none','unk','incmpl','cmpl'))
    exonFrames              = Column(MSLongBlob)
    
    snps                    = relation('SNP', backref = backref('refseqgene', order_by = 'RefSeqGene.id'))
    
    last_modified           = Column(DateTime, onupdate=datetime.datetime.now)    
    def __init__(self):
        pass
    
    
def _test():
    """tests the application"""
    import doctest
    doctest.testmod()
    
if __name__ == '__main__':
#    _test()
#    Base.metadata.drop_all(engine)
    print Base.metadata
    Base.metadata.create_all()
