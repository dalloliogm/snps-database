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


class _BaseSNPStats(Entity):
    snp_id = Field(Text(20))
    population_key = Field(Text(50))
    value = Field(Float(2, 32), index=True)

    def __init__(self, snp_id, popkey, value):
        self.snp_id = snp_id.lower().strip()
        self.population_key = popkey.upper().strip()
        self.value = value

    def __repr__(self):
        return 'stat on snp %s on pop %s' % (self.snp_id, self.population_key)

class _BaseStat(Entity):
    position = Text(30)
    chromosome = Text(6)

class iHS(_BaseSNPStats):
    using_options(tablename = 'ihs', inheritance = 'concrete')

class XPEHH(_BaseSNPStats):
    using_options(tablename = 'xpehh', inheritance = 'concrete')

class Fst(_BaseSNPStats):
    using_options(tablename = 'fst', inheritance = 'concrete')

def _test():
    import random
    from elixir import session, metadata, setup_all, create_all
    connection_line = 'sqlite:///:memory:'
    metadata.bind = connection_line

    setup_all()
    create_all()

    [iHS('snp_%s' % i, 'pop', random.random()) for i in xrange(10)]

if __name__ == '__main__':
    _test()
