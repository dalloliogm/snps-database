#!/usr/bin/env python
"""
Reads the data from HGDP (samples) and load it in the database 

"""

from HGDPIO import parsers
from schema.debug_database import *
import logging
import glob

def upload_genotypes(genotypes_by_chr_dir, ):
    """
    upload individuals from the rosenberg files.
    """
    from schema.connection import session, metadata # is session necessary?
    logging.basicConfig(level=logging.DEBUG)
    print metadata
#    metadata.bind = 'sqlite:///:memory:'
    metadata.bind.echo = True
    
    genotypes_by_chr_dir = '/home/gioby/Data/HGDP/Genotypes_by_chr'
    for filename in glob.glob(genotypes_by_chr_dir + '/*.geno'):
        print filename
        parsers.genotypes_parser(open(filename, 'r'))
        session.commit()

#    rosenberg_file = open(rosenberg_path, 'r')
#    parsers.rosenberg_parser(rosenberg_file)

    print 'upload of Genotypes to database %s completed' % metadata
#    from schema import *
#    print SNP.get_by()


def _test():
    """test the current module
    
    note: use nosetest to test the library"""
    import doctest 
    doctest.testmod()

if __name__ == '__main__':
    _test()
    upload_genotypes('')
    
