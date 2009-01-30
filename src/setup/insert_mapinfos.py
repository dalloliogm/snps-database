#!/usr/bin/env python
"""
Insert map informations about snps in the database (Chromosome and position)

"""

from HGDPIO import parsers
from schema.debug_database import *

def upload_mapinfos(handle, ):
    """
    upload map infos
    """
    from schema.connection import session, metadata # is session necessary?
    print metadata
    metadata.bind.echo = True
    mapfilepath = '../data/Annotations/HGDP_Map.txt'
    mapfile = open(rosenberg_path, 'r')
    parsers.snpmap_parser(mapfile)

    print 'upload of snp map informations to database %s completed' % metadata


def _test():
    """test the current module
    
    note: use nosetest to test the library"""
    import doctest 
    doctest.testmod()

if __name__ == '__main__':
    _test()
    upload_mapinfos()
    
