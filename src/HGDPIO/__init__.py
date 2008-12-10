#!/usr/bin/env python
"""
This module provides functions and objects to handle HGDP data and 
import it on the database.

Most of the code here has been copied from PopGen.Gio. In the future,
it will be good to unify the two copies into a single function.
"""

from PyDatabase import connection

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
    ... "HGDP00151"    "F"    "Makrani"    "Pakistan"    "Asia"    "Makrani"''')
    >>> samples = samplesParser(samples_file)
    >>> print [sample for sample in samples if sample.region == "Pakistan"]
    [Mr. HGDP00001 (Brahui Test), Mr. HGDP00003 (Brahui), Mr. HGDP00151 (Makrani)]
    """
    splitter = re.compile('"\s+"')
    handle.readline()   # skip headers
    header = handle.readline()
    if header is None:
        raise ValueError('Empty file!!')
    
    individuals = []                # not necessary with the database
    
    for line in handle.readlines(): 
        row = splitter.split(line)
        
        if row is None: break   # FIXME: optimize
        if len(row) != 6:
            raise ValueError("wrong number of columns in current line")
        
        ind_id = row[0].replace('"', '')
#        logging.debug(row)
        sex = row[1]    # TODO: translate this to 1/2 
        pop = row[2]    # TODO: use Population object
        region = row[3]
        continent = row[4]
        unit = row[5].replace('"', '')
        
        # create an Individual object
        Ind = Individual(ind_id, pop, region=region, continent=continent, 
                        working_unit=unit, sex=sex)
        individuals.append(Ind)

    return individuals