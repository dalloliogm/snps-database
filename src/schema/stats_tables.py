#!/usr/bin/env python
"""
Tables to contain various stats

"""
from schema import *
import schema
from elixir import Entity, EntityMeta, Field, Unicode, Integer, UnicodeText, String, Text, Float
from recipes.enum import Enum
from elixir import ManyToOne, OneToMany, OneToOne, ManyToMany, DateTime
from elixir import metadata, using_options
from elixir.ext.versioned import acts_as_versioned
from config import connection_line
from datetime import datetime
import logging
import operator


class Stats(Entity):
    using_options(tablename = 'stats')
    snp = ManyToOne('SNP', primary_key = True)

    population_key = Field(String(30), primary_key = True, default = None, index=True)

    iHS = Field(Float(2, 32))      # which is the best precision?
#    iHS_raw = Field(Float(2, 32))   # not storing this for the moment
    daf_iHS = Field(Float(2, 10))

#    iHS_bis = OneToOne('iHS')

    def __init__(self, snp, pop_key=None):
        if isinstance(snp, str):
            snp = SNP.get_by(id = str)
        elif not isinstance(snp, SNP):
            raise TypeError('snp should be a SNP instance or a string')
        self.snp = snp

        self.population_key = str(pop_key).lower()
        

    def __repr__(self):
        repr = 'stats on SNP %s on %s: iHS %s, daf %s' % (self.snp, self.population_key, self.iHS, self.daf_iHS)
        return repr

    def get_by_chromosome(self):
        raise NotImplementedError('Sorry, not implemented yet!')

    def get_by_snp_id(self):
        raise NotImplementedError('Sorry, not implemented yet!')

    def get_by_continent(self):
        """
        create aliases eur<->europe<->Europe etc...
        """
        raise NotImplementedError('Sorry, not implemented yet!')
    
    def get_by_population(self):
        """
        get by working unit
        """
        raise NotImplementedError('Sorry, not implemented yet!')



class _Base_SNPbyContinent_Stat(Entity):
#    snp_id = Field(String(20), index=True, unique=True) # composite key (snp_id + popkey)?
#    stat = ManyToOne('Stats')
#    population_key = Field(Text(50))
#    value = Field(Float(2, 32), index=True)
    snp = ManyToOne('SNP', primary_key=True, backref = "snp_id", inverse='stats', viewonly=True)
#    snp_id = String(20, index=True)

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


    original_file = Field(Text)
    version = Field(Text)

    def __init__(self, snp_id):
        self.snp_id = str(snp_id).lower().strip()
#        self.population_key = popkey.upper().strip()
#        self.value = value

    def __repr__(self):
        return 'stat on snp %s' % (self.snp_id) 

class _BaseStat(Entity):
    position = Field(Text(30))
    chromosome = Field(Text(6))
    value = Field(Float(2, 32))

class iHS(_Base_SNPbyContinent_Stat):
    using_options(tablename = 'ihs', inheritance = 'concrete')

class XPEHH(_Base_SNPbyContinent_Stat):
    using_options(tablename = 'xpehh', inheritance = 'concrete')

class Fst(_Base_SNPbyContinent_Stat):
    """
    Fst are calculated by comparing two different populations.

    Therefore, any entry in this table refer to the Fst values with respect of 
    the population saved in the 'population_key' field.
    """
    using_options(tablename = 'fst', inheritance = 'concrete')

    population_key = Field(Text)

class FstGlobal(_Base_SNPbyContinent_Stat):
    """
    Fst are calculated by comparing two different populations.

    Therefore, any entry in this table refer to the Fst values with respect of 
    the population saved in the 'population_key' field.
    """
    using_options(tablename = 'fst_global', inheritance = 'concrete')

class CLR(_BaseStat):
    using_options(tablename = 'clr', inheritance = 'concrete')    
    

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
