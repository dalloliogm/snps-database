#!/usr/bin/env python
"""
Fix bug #4 - run this script only once

"""

from HGDPIO import parsers
from schema.debug_database import *
import logging
import glob

def update_individuals(genotypesfile, ):
    """
    upload individuals from the rosenberg files.
    """
    from schema.connection import session, metadata # is session necessary?
    logging.basicConfig(level=logging.DEBUG)
    print metadata
#    metadata.bind = 'sqlite:///:memory:'
    metadata.bind.echo = True
    
    parsers.individuals_genotypesindex_parser(open(genotypesfile, 'r'))
    session.commit()

#    rosenberg_file = open(rosenberg_path, 'r')
#    parsers.rosenberg_parser(rosenberg_file)

    print 'fixed individuals.genotypes_index to database %s completed' % metadata
#    from schema import *
#    print SNP.get_by()


def _test():
    """test the current module
    
    note: use nosetest to test the library"""
    import doctest 
    doctest.testmod()

if __name__ == '__main__':
    _test()
    update_individuals('/home/gioby/Data/HGDP/Genotypes_by_chr/chr10.geno')
 
