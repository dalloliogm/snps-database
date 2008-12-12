#!/usr/bin/env python
"""
This module provides functions and objects to handle HGDP data and 
import it on the database.

Most of the code here has been copied from PopGen.Gio. In the future,
it will be good to unify the two copies into a single function.
"""

from schema.debug_database import *
import re

def samplesParser(handle, ):
    """
    parse a file with descriptions of Individuals (samples) in hgdp
    
    >>> from StringIO import StringIO
    >>> samples_file = StringIO(
    ... '''"sample"
    ... "code"  "sex"    "population"    "region"        "continent"     "Unidad"
    ... "HGDP00001"    "M"    "Brahui Test"    "Pakistan"      "Asia"  "Brahui"
    ... "HGDP00003"    "M"    "Brahui"    "Pakistan"      "Asia"  "Brahui"
    ... "HGDP01362"    "M"    "French Basque"    "France"    "Europe"    "Basque"
    ... "HGDP00004"    "F"    "Brahui"    "Pakistan"      "Asia"  "Brahui"
    ... "HGDP00151"    "F"    "Makrani"    "Pakistan"    "Asia"    "Makrani"''')
    >>> samples = samplesParser(samples_file)
    >>> print samples[:3]
    [Mr. HGDP00001 (brahui test), Mr. HGDP00003 (brahui), Mr. HGDP01362 (french basque)]
    
    # filter all individuals belonging to 'makrani'
    >>> print [individual for individual in samples if individual.population == "makrani"]
    [Mrs. HGDP00151 (makrani)]
    
    # the same as before but using the filter function:
    >>> filter(lambda ind: ind.population == 'Makrani', samples)
    [Mrs. HGDP00151 (makrani)]
    
    >>> filter(lambda ind: ind.population.continent_macroarea == 'Asia', samples)
    [Mrs. HGDP00151 (makrani), ...]
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
        
        if row is None: break   # FIXME: optimize
        if len(row) != 6:
            raise ValueError("wrong number of columns in current line")
        
        ind_id = row[0].replace('"', '')
#        logging.debug(row)
        sex = row[1]    # TODO: translate this to 1/2 
        popname = row[2].lower()    # TODO: use Population object
        region = row[3]
        macroarea = row[4]
        unit = row[5].replace('"', '')
        
        # Check whether the current population already exists. If not, create it
        # FIXME: this is duplicated code (see Individual.__init__)
#        pop = Population.get_by(original_name = popname)
#        if pop is None:
#            pop = Population(original_name = popname,
#                             region = region, 
#                             continent_macroarea = continent,
#                             working_unit = unit) 

        
        # create an Individual object
        # If the population given doesn't exists, a new record is created automatically
        Ind = Individual(ind_id, population=popname, sex=sex, region=region, 
                         macroarea=macroarea, working_unit=unit)
        individuals.append(Ind)

    return individuals


def _test():
    """test the current module"""
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
