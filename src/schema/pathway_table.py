#!/usr/bin/env python
"""
Table to store pathways
"""

from schema import *
from elixir import Entity, Field, Unicode, Integer, UnicodeText, String, Text, Float
from elixir import ManyToOne, OneToMany, OneToOne, ManyToMany, DateTime
from elixir import metadata, using_options
from config import connection_line
import logging
import operator


class Pathway(Entity):
    """
    >>> from debug_database import *
    >>> from elixir import setup_all, create_all
    >>> metadata.bind = 'sqlite:///:memory:'
    >>> setup_all(); create_all()
    >>> print metadata
    MetaData(Engine(sqlite:///:memory:))

    >>> path = Pathway()
    >>> snps = [SNP(str(x)) for x in xrange(10)]
    >>> genes = [RefSeqTranscript(str(x)) for x in xrange(4)]

    >>> path.genes = genes
    >>> print path.genes
    """
    title = Field(Text)
    kegg_id = Field(Text(20))

    genes = OneToMany('RefSeqTranscript')
    snps = OneToMany('SNP')
    




if __name__ == '__main__':
    pass

