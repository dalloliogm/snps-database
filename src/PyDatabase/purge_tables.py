#!/usr/bin/env python
"""
Clean all the entries in the tables:
- SNP, Individual, Population, Version, Genotype

BE careful!!! 

"""

from schema import SNP, Individual, Population, Version, Genotype, RefSeqGene, MetaData
from session import session


# from sqlalchemy tutorial, chapter metadata
# http://www.sqlalchemy.org/docs/05/metadata.html
meta = MetaData()
meta.reflect(bind=someengine)
for table in reversed(meta.sorted_tables):
    someengine.execute(table.delete())

