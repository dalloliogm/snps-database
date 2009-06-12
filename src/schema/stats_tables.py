#!/usr/bin/env python
"""
Tables to contain various stats

"""
from elixir import Entity, EntityMeta, Field, Unicode, Integer, UnicodeText, String, Text, Float
from recipes.enum import Enum
from elixir import ManyToOne, OneToMany, OneToOne, ManyToMany, DateTime
from elixir import metadata, using_options
from elixir.ext.versioned import acts_as_versioned
from config import connection_line
from datetime import datetime
import logging
import operator


class _Base_SNPbyContinent_Stat(Entity):
    snp_id = Field(Text(20))
    population_key = Field(Text(50))
    value = Field(Float(2, 32), index=True)

    mean = Field(Float(2, 32))
    dev_std = Field(Float(2, 32))

    ame = Field(Float(2, 32))
    ame_p = Field(Float(2, 32))
    ame_q = Field(Float(2, 32)) 

    csasia = Field(Float(2, 32))
    csasia_p = Field(Float(2, 32))
    csasia_q = Field(Float(2, 32))

    easia = Field(Float(2, 32))
    easia_p = Field(Float(2, 32))
    easia_q = Field(Float(2, 32))

    eur = Field(Float(2, 32))
    eur_p = Field(Float(2, 32))
    eur_q = Field(Float(2, 32))

    mena = Field(Float(2, 32))
    mena_p = Field(Float(2, 32))
    mena_q = Field(Float(2, 32))

    oce = Field(Float(2, 32))
    oce_p = Field(Float(2, 32))
    oce_q = Field(Float(2, 32))

    ssafr = Field(Float(2, 32))
    ssafr_p = Field(Float(2, 32))
    ssafr_q = Field(Float(2, 32))

    def __init__(self, snp_id):
        self.snp_id = str(snp_id).lower().strip()
#        self.population_key = popkey.upper().strip()
#        self.value = value

    def __repr__(self):
        return 'stat on snp %s' % (self.snp_id) 

class _BaseStat(Entity):
    position = Text(30)
    chromosome = Text(6)

class iHS(_Base_SNPbyContinent_Stat):
    using_options(tablename = 'ihs', inheritance = 'concrete')

class XPEHH(_Base_SNPbyContinent_Stat):
    using_options(tablename = 'xpehh', inheritance = 'concrete')

class Fst(_Base_SNPbyContinent_Stat):
    using_options(tablename = 'fst', inheritance = 'concrete')

def _test():
    import random
    from elixir import session, metadata, setup_all, create_all
    connection_line = 'sqlite:///:memory:'
    metadata.bind = connection_line

    setup_all()
    create_all()

    [iHS('snp_%s' % i, ) for i in xrange(10)]

if __name__ == '__main__':
    _test()
