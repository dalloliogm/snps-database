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
    using_options(tablename = 'pathways')
    name = Field(String(50), primary_key = True)
    title = Field(Text)
    description = Field(Text)
    kegg_id = Field(Text(20))

    genes = ManyToMany('RefSeqTranscript')#, inverse='transcript_id')
    snps = ManyToMany('SNP')#, inverse='SNP.snp_id')
    
    def __init__(self, title):
        self.title = str(title).lower()

    def __repr__(self):
        return 'pathway %s' % self.title

    def add_gene(self, gene):
        """
        Add a gene to the pathway, and automatically add references to all snps in 400,000 bp of each gene
        """
        genes = (gene, )
        self.add_genes(genes)

    def add_genes(self, genes):
        """
        Add multiple genes to the pathway, along with their sorrounding snps (400,000)
        """
        if not (isinstance(genes, list) or isinstance(genes, tuple)):
            print 'not list'
            pass 
        pass


if __name__ == '__main__':
    pass

