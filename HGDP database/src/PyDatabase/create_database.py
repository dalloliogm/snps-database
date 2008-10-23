#!/usr/bin/env python
# Create a database for HGDP data

"""
Creates a temporary database (in RAM, using sqlite) for HGDP data.

Refer to sqlalchemy manual, and in particular to this passage:
- http://www.sqlalchemy.org/docs/05/ormtutorial.html#datamapping_declarative

"""

from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


# this will create a temporary database in Ram memory, using an engine called sqlite. 
engine = create_engine('sqlite:///:memory:', echo=True)

# I will use declaration mapping in this code. This means that both the tables and the instances of every row will be defined at the same time.
# see 'object mapping' on sqlalchemy manual.
# see also http://www.sqlalchemy.org/docs/05/ormtutorial.html#datamapping_declarative
Base = declarative_base()

class SNP(Base):
    """
    Table 'SNP'.
    
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
    __tablename__ = 'SNP'
    
    SNP_Id                  = Column(String(10), primary_key=True)
    chromosome              = Column(String(10))        # should be a choice between 1-22-XY
    physical_position       = Column(Integer)
    genetic_position        = Column(Integer)
    reference_allele_freq   = Column(Float)
    derived_allele_freq     = Column(Float)
    original_strand         = Column(String(1))
    dbSNP_ref               = Column(String(10))
    gene_hugo_symbol        = Column(String(20))
    gene_refseq             = Column(String(20))
    version                 = Column(Float)
    
    def __init__(self,  SNP_Id):
        # this method will be launched when you create an instance of a SNP object. 
        # e.g. when you call rs1334 = SNP(id='rs1334') 
        self.SNP_Id = SNP_Id            # should check whether this already exists.
        
    def __repr__(self):
        # this method will be called when, in python code, you will do 'print SNP'.
        return 'SNP '  + self.SNP_Id

class Genotype(Base):
    __tablename__ = 'Genotype'
    
    SNP_Id                  = Column()
    Individual_Id           = Column()
    Genotype_Code           = Column()
    
    
def _test():
    """tests the application"""
    import doctest
    doctest.testmod()
    
if __name__ == '__main__':
    _test()