#!/usr/bin/env python
"""
This module provides functions and objects to handle HGDP data and 
import it on the database.

Most of the code here has been copied from PopGen.Gio. In the future,
it will be good to unify the two copies into a single function.
"""

from schema.schema import *
#from connection import *
import re
import logging

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


def samples_parser(handle, ):
    """
    parse a file with descriptions of Individuals (samples) in hgdp
    
    >>> from schema.debug_database import *
    >>> print metadata
    MetaData(Engine(sqlite:///:memory:))
    >>> from StringIO import StringIO
    >>> samples_file = StringIO(
    ... '''"sample"
    ... "code"  "sex"    "population"    "region"        "continent"     "Unidad"
    ... "HGDP00001"    "M"    "Brahui Test"    "Pakistan"      "Asia"  "Brahui"
    ... "HGDP00003"    "M"    "Brahui"    "Pakistan"      "Asia"  "Brahui"
    ... "HGDP01362"    "M"    "French Basque"    "France"    "Europe"    "Basque"
    ... "HGDP00004"    "F"    "Brahui"    "Pakistan"      "Asia"  "Brahui"
    ... "HGDP00151"    "F"    "Makrani"    "Pakistan"    "Asia"    "Makrani"''')
    >>> samples = samples_parser(samples_file)
    >>> print samples[:3]
    [Mr. HGDP00001 (brahui test), Mr. HGDP00003 (brahui), Mr. HGDP01362 (french basque)]
    
    # filter all individuals belonging to 'makrani'
    >>> print [individual for individual in samples if individual.population == "makrani"]
    [Mrs. HGDP00151 (makrani)]
    
    # the same as before but using the filter function:
    >>> filter(lambda ind: ind.population == 'MAKRANI', samples)
    [Mrs. HGDP00151 (makrani)]
    
    # Beware that the attributes in population are case sensitive!!!
    >>> filter(lambda ind: ind.population.continent_macroarea == 'asia', samples)
    [Mr. HGDP00001 (brahui test), Mr. HGDP00003 (brahui), Mrs. HGDP00004 (brahui), Mrs. HGDP00151 (makrani)]
    
    >>> session.flush()
    """

    handle.readline()   # skip headers
    header = handle.readline()
    if header is None:
        raise ValueError('Empty file!!')
    
    individuals = []                # not necessary with the database

    splitter = re.compile('"\s+"')    
    for line in handle.readlines():
        # split the line according to spaces and "
        row = splitter.split(line)
        
        if row is None: 
            break   # FIXME: optimize
        if len(row) != 6:
            raise ValueError("wrong number of columns in current line")
        
        ind_id = row[0].replace('"', '')
#        logging.debug(row)
        sex = row[1]
        popname = row[2].lower()
        region = row[3]
        macroarea = row[4]
        unit = row[5].replace('"', '')
        
        # create an Individual object
        # If the population given doesn't exists, a new record is created
        ind = Individual(ind_id, population=popname, sex=sex, region=region, 
                         macroarea=macroarea, working_unit=unit)
        individuals.append(ind)

    return individuals

def load_into_database():
    """launch the various scripts to insert data into the HGDP database."""
    
    from schema.connection import session, metadata
    from schema.connection import Individual, Population, SNP, RefSeqGene
#    session.flush()
    print "now we are connected to the database ", metadata
    
    samples_file = file('../../data/Annotations/samples_subset.csv', 'r')
    print samples_file.readline()
    print samples_file.readline()
    
    ind = Individual.get_by_or_init(identificator = 'Giovanni')
    
    print Individual.query().all()
    print ind
    ind.delete()
    
    session.flush()
    samples_parser(samples_file)
    
    
     

def _test():
    """test the current module"""
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
    load_into_database()
