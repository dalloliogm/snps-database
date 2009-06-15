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

    for stat in ['iHS', 'XPEHH']:
        for x in xrange(200):
            i = eval('%s("snp_%s")' % (stat, str(x)))
            i.ame = random.random()
            i.csasia = random.random()
            i.easia = random.random()
            i.eur = random.random()
            i.mena = random.random()
            i.oce = random.random()
            i.ssafr = random.random()

            i.version = 0

    # Fst requires a different setup
    pops = 'ame csasia easia eur mena oce ssafr'.upper().split()

    for pop in pops:
        for x in xrange(200):
            f = Fst(x)
            f.population_key = pop
            f.ame = random.random()
            f.csasia = random.random()
            f.easia = random.random()
            f.eur = random.random()
            f.mena = random.random()
            f.oce = random.random()
            f.ssafr = random.random()

            f.version = 0


    session.commit()
    

if __name__ == '__main__':
    setup_randomdb()
    from pprint import pprint
    pprint(session.query(iHS.snp_id, iHS.ame, iHS.eur, iHS.version).limit(10).all())

