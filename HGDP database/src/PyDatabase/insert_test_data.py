#!/usr/bin/env python
# insert test data into the database

from sqlalchemy import *
from connection import engine
from schema import SNP, Individual, Population, Version, Genotype
from session import session

snp1 = SNP('rs1111')
snp1

session.add(snp1)
session.commit()

# close when finished
session.close()
