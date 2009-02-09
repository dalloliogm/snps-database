#!/usr/bin/env python
"""
Drop the RefSeqGene table and recreate it (this table has been developed after 
the genotypes have uploaded, so I don't want to drop everything again and reupload)
"""

from schema.connection import *

RefSeqGene.table.drop()

RefSeqGene.table.create()
