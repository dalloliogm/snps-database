#!/usr/bin/env python
"""
Setup the Pathway and the various Stats tables
"""


from schema.connection import *
from elixir import create_all

metadata.bind.echo = True
create_all()

for table in (Fst, iHS, XPEHH, Pathway):

    table.table.drop()

    table.table.create()







if __name__ == '__main__':
    pass

