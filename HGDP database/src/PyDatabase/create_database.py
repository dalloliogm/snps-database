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
    
    This class represents both the table SNP, and the structure  
    """
    __tablename__ = 'SNP'
    
    SNP_Id                  = Column(String(10), primary_key=True)
    chromosome              = Column(String(10))        # should be a choice between 1-22-XY
    physical_position       = Column(Integer)
    genetic_position        = Column(Integer)
    reference_allele_freq   = Column(Float)
    
    def __init__(self):
        # this method will be launched when you create 
    
    
        