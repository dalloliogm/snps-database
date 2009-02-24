#!/usr/bin/env python
"""
Reads the data from HGDP (samples) and load it in the database 

"""

from HGDPIO import parsers
from schema.debug_database import *

def upload_rosenberg_individuals(rosenberg_file, session, metadata):
    """
    upload individuals from the rosenberg files.
    """
    individuals = parsers.rosenberg_parser(rosenberg_file, session, metadata)
    session.add_all(individuals)

    print 'upload of Rosenberg Individuals to database %s completed' % metadata

if __name__ == '__main__':
    rosenberg_path = '../data/Annotations/hgdpSampleinfoRosenberg-extended.csv'
    rosenberg_file = open(rosenberg_path, 'r')
    from schema.connection import session, metadata # is session necessary?
    print metadata
    metadata.bind.echo = True
    upload_rosenberg_individuals(rosenberg_file, session, metadata)
    
