#!/usr/bin/env python
"""query the database"""

from sqlalchemy import *
from connection import engine
from schema import SNP, Individual, Population, Version, Genotype, RefSeqGene
from session import session

# gets the first 5 elements from the RefSeqGene table
results = session.query(RefSeqGene).limit(5)
for r in results:
    print r.id, r.name