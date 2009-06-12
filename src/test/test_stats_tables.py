from nose import with_setup
import unittest
import random
from elixir import session, metadata, setup_all, create_all
from schema.stats_tables import *
from schema.schema import *

def setup_randomdb():
    connection_line = 'sqlite:///:memory:'
    metadata.bind = connection_line
#    metadata.bind.echo = True
    setup_all()
    create_all()

    for x in xrange(200):
        i = iHS(x)
        i.ame = random.random()
        i.csasia = random.random()
        i.easia = random.random()
        i.eur = random.random()
        i.mena = random.random()
        i.oce = random.random()
        i.ssafr = random.random()

    session.commit()
    

if __name__ == '__main__':
    s = setup_randomdb()
