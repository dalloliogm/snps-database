#!/usr/bin/env python
"""
Insert the UCSC refseqgene table in the db.
"""

def upload_annotations(refseq_annotations_filename, session, metadata):
    """
    upload annotations
    """
    metadata.bind.echo = True


if __name__ == '__main__':
    # Import configuration options
    from ConfigParser import SafeConfigParser
    c = SafeConfigParser()
    c.read('config.txt')
    refseq_annotations_filename = c.get('Data files', 'refseq_annotations')

    from schema.connection import *

    print metadata
    upload_annotations(refseq_annotations_filename, session, metadata)


