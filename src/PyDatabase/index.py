#!/usr/bin/env python
"""
Create indexes 

pasted from sqlalchemy tutorial

Will be useful later when I will have to generate indexes on SNPs
"""

# create a table
sometable.create()

# define an index
i = Index('someindex', sometable.c.col5)

# create the index, will use the table's bound connectable if the `bind` keyword argument not specified
i.create()

