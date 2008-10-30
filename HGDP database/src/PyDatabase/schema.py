#!/usr/bin/env python
# Create a database for HGDP data

"""
Creates a temporary database (in RAM, using sqlite) for HGDP data.

Refer to sqlalchemy manual, and in particular to this passage:
- http://www.sqlalchemy.org/docs/05/ormtutorial.html#datamapping_declarative

"""

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from connection import engine, Base
from sqlalchemy.databases.mysql import MSEnum, MSLongBlob

class SNP(Base):
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
    chromosome              = Column(String(10))        # should be a choice between 1-22-XY
    physical_position       = Column(Integer)
    genetic_position        = Column(Integer)
    reference_allele_freq   = Column(Float)
    derived_allele_freq     = Column(Float)
    original_strand         = Column(MSEnum('+', '-', ' '))
    dbSNP_ref               = Column(String(10))
    gene_hugo_symbol        = Column(String(20))
    gene_refseq             = Column(String(20))
    version                 = Column(Integer, ForeignKey('versions.id'))
    
    def __init__(self,  SNP_Id):
        # this method will be launched when you create an instance of a SNP object. 
        # e.g. when you call rs1334 = SNP(id='rs1334') 
        self.SNP_Id = SNP_Id            # should check whether this already exists.
        
    def __repr__(self):
        # this method will be called when, in python code, you will do 'print SNP'.
        return 'SNP '  + self.SNP_Id

class Genotype(Base):
    """
    Table 'Genotypes'
    """
    __tablename__ = 'genotypes'
    
    genotype_id             = Column(Integer, primary_key = True)
    snp_id                  = Column(String(10))
    individual_id           = Column(Integer)
    genotype_code           = Column(MSEnum('0', '1', '2'))
    version                 = Column(Integer, ForeignKey('versions.id'))
    
class Individual(Base):
    """
    Table 'Individuals'
    """
    __tablename__ = 'individuals'
    
    individual_id           = Column(Integer, primary_key = True)
    population_id           = Column(Integer)
    version                 = Column(Integer, ForeignKey('versions.id'))
    
class Population(Base):
    """
    Table 'Populations'
    """
    __tablename__ = 'populations'
    
    population_id           = Column(Integer, primary_key = True)
    name                    = Column(String(50))
    geographycal_area       = Column(String(30))
    version                 = Column(Integer, ForeignKey('versions.id'))
    
class Version(Base):
    """
    Table 'Version'
    
    Every SNP/Individual/Population row has a 'version' field, which indicates when it has been last changed 
    """
    __tablename__ = 'versions'
    
    id                      = Column(Integer, primary_key = True) 
    description             = Column(String(100))       
    
    
    
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
    
    
def _test():
    """tests the application"""
    import doctest
    doctest.testmod()
    
if __name__ == '__main__':
#    _test()
#    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
