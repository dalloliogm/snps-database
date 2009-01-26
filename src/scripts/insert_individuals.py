#!/usr/bin/env python
"""
Reads the data from HGDP (samples) and load it in the database 

"""

from HGDPIO import parsers
from schema.debug_database import *

#def parameters():
#    """Read arguments and parameters"""
#    
#    basedir = '/home/gioby/Data/HGDP/'
#    
#    # parse parameters
#    parser = OptionParser()
#    parser.set_defaults(genotypes_by_chr_dir = basedir + 'Genotypes_by_chr/',
#                        samplesfilepath = basedir + 'Annotations/samples_subset.csv',
#                        selected_chr = [22, ],  #FIXME: only the first chromosome is used 
#                        continent = 'Europe')
#    parser.add_option('-s', '--samplefile', action='store', type='string', 
#                      dest = 'samplesfilepath')
#    parser.add_option('-g', '--genotypes_by_chr_dir', action='store', 
#                      type='string', dest = 'genotypes_by_chr_dir')
#    parser.add_option('-c', '--continent', action='store', type='string', 
#                      dest = 'continent')
#    parser.add_option('-y', '--chromosomes', action='store', type='list', 
#                      dest = 'chromosomes')
#    parser.add_option('-t', '--test', action='callback', dest = _test)
#    parser.add_option('-h', '--help', action='help')

def upload_rosenberg_individuals():
    """
    upload individuals from the rosenberg files.
    """
    from schema.connection import session, metadata # is session necessary?
    print metadata
    metadata.bind.echo = True
    rosenberg_path = '../data/Annotations/hgdpSampleinfoRosenberg-extended.csv'
    rosenberg_file = open(rosenberg_path, 'r')
    parsers.rosenberg_parser(rosenberg_file)

    print 'upload of Rosenberg Individuals to database %s completed' % metadata


def _test():
    """test the current module
    
    note: use nosetest to test the library"""
    import doctest 
    doctest.testmod()

if __name__ == '__main__':
    _test()
    upload_rosenberg_individuals()
    
