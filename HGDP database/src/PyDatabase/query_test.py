#!/usr/bin/env python
"""query the database"""

from schema import SNP, Individual, Population, Version, Genotype, RefSeqGene
from session import session

# gets the first 5 elements from the RefSeqGene table
results = session.query(RefSeqGene).limit(5)
for r in results:
    print r.id, r.name
    
# get the first 5 SNPs
results  = session.query(SNP).limit(5)
for r in results:
    print r