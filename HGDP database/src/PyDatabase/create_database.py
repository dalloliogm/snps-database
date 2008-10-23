#!/usr/bin/env python
# Create a database for HGDP data

"""
Creates a temporary database (in RAM, using sqlite) for HGDP data.

Refer to sqlalchemy manual, and in particular to this passage:
- http://www.sqlalchemy.org/docs/05/ormtutorial.html#datamapping_declarative

"""

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


# this will create a temporary database in Ram memory, using an engine called sqlite. 
engine = create_engine('sqlite:///:memory:', echo=True)
metadata = MetaData()

Base = declarative_base()

class SNP(Base):
    __tablename__ = 'SNP'
    
    SNP_Id = Column(String(10), primary_key=True),
    chromosome = Column(String(10)),        # should be a choice between 1-22-XY
    physical_position = Column(Integer),
    genetic_position = Column(Integer),
    reference_allele_freq = Column()
        