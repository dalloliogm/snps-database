#!/usr/bin/env python
"""
Drop the following tables:
- SNP, Individual, Population, Version, Genotype

BE careful!!! 

"""
#from sqlalchemy import MetaData, engine
from schema import Base, engine
from pprint import pprint

#print dir(engine)
#print dir(session)

## from sqlalchemy tutorial, chapter metadata
## http://www.sqlalchemy.org/docs/05/metadata.html


#for table in reversed(Base.metadata.sorted_tables):
#    print table
#    engine.execute(table.delete())
#    dir(table)

Base.metadata.drop_all()
pprint(Base.metadata.sorted_tables)