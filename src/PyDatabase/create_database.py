#!/ create database schema and tables
"""
Create/Update database schema.
"""

from schema import Base, engine
#Base.drop_all(Individual, SNP, Genotype, Population)    # TODO: implement a way to reset the database 
Base.metadata.drop_all()

Base.metadata.create_all(engine)

for table in Base.metadata.sorted_tables:
    print table