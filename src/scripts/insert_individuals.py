#!/usr/bin/env python
"""
Reads the data from HGDP (samples) and load it in the database 

"""

from HGDPIO import parsers
from schema.debug_database import *

def parameters():
    """Read arguments and parameters"""
    
    basedir = '/home/gioby/Data/HGDP/'
    
    # parse parameters
    parser = OptionParser()
    parser.set_defaults(genotypes_by_chr_dir = basedir + 'Genotypes_by_chr/',
                        samplesfilepath = basedir + 'Annotations/samples_subset.csv',
                        selected_chr = [22, ],  #FIXME: only the first chromosome is used 
                        continent = 'Europe')
    parser.add_option('-s', '--samplefile', action='store', type='string', 
                      dest = 'samplesfilepath')
    parser.add_option('-g', '--genotypes_by_chr_dir', action='store', 
                      type='string', dest = 'genotypes_by_chr_dir')
    parser.add_option('-c', '--continent', action='store', type='string', 
                      dest = 'continent')
    parser.add_option('-y', '--chromosomes', action='store', type='list', 
                      dest = 'chromosomes')
    parser.add_option('-t', '--test', action='callback', dest = _test)
    parser.add_option('-h', '--help', action='help')


def load_individuals_into_database():
    """launch the various scripts to insert data into the HGDP database."""
    
    from schema.connection import session, metadata
    from schema.connection import Individual, Population, SNP, RefSeqGene
#    session.flush()
    print "now we are connected to the database:", metadata
    metadata.bind.echo = True
    
    samples_file = file('../../data/Annotations/samples_subset.csv', 'r')
    
    session.flush()
    
    parsers.samples_parser(samples_file)
    session.commit()
    print 'upload of tables finished'

def _test():
    """test the current module"""
    import doctest 
    doctest.testmod()

if __name__ == '__main__':
    _test()
    load_individuals_into_database()
    