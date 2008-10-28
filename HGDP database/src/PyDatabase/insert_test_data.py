#!/usr/bin/env python
# insert test data into the database

from sqlalchemy import *
from connection import engine
from schema import SNPs, Individuals, Populations, Versions, Genotypes
