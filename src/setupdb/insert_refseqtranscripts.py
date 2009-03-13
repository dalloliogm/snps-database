#!/usr/bin/env python
"""
Insert the UCSC refseqtranscript table in the db.
"""

import logging
import re

def upload_annotations(refseq_annotations_fh, session, metadata):
    """
    upload annotations

    >>> from schema.debug_database import *
    >>> print metadata
    MetaData(Engine(sqlite:///:memory:))
    >>> setup_all()
    >>> annotations = StringIO.StringIO('''\
    ... 12  "NR_024077" "chr1"  "-" 4268    14754   14754   14754   10  "4268,4832,5658,6469,"   "4692,4901,5810,6631,6918"   "WASH2P"    "unk"   "unk"   "-1,-1,-1,-1,"
    ... 31  "NM_001005484"  "chr1"  "+" 58953   59871   58953   59871   1   58953   59871   "OR4F5" "cmpl"  "cmpl"  0
    ... 13  "NM_001005224"  "chr1"  "+" 357521  358460  357521  358460  1   357521  358460  "OR4F3" "cmpl"  "cmpl"  0)
    >>> upload_annotations(annotations)
    >>> transcript = RefSeqTranscript.query().filter_by(ncbi_transcript_id = 'NR_024077')
    >>> print transcript.chromosome, transcript.strand, transcript.txStart
    chr1 - 4268

    """
    metadata.bind.echo = True
    session.bind = metadata.bind    # necessary for doing session.execute

#    for ind in session.execute('select * from individuals limit 10;'):
#        print ind

#    session.execute("""LOAD DATA LOCAL INFILE '%s' into table refseqtranscript FIELDS TERMINATED BY '\t' ENCLOSED BY "" (ncbi_transcript_id, chromosome, strand, txStart, txEnd, cdsStart, cdsEnd, exonCount, exonStarts, exonEnds, alternateName, cdsStartStat, cdsEndStat, exonFrames)""" % refseq_annotations_filename)

#    annotations_fh = open(refseq_annotations_filename, 'r')
    logging.basicConfig(level=logging.DEBUG)
    for line in refseq_annotations_fh:
        line = line.strip()
        if line and not line.startswith('"#'):
            transcript = RefSeqTranscript()
            transcript.source_file = refseq_annotations_fh.name

            fields = line.split()
            logging.debug(fields)
            
            transcript.bin = fields[0]
            transcript.transcript_id = fields[1].replace('"', '')
            chromosome = fields[2].replace('"', '')
            transcript.chromosome = re.findall('chr(.*)', chromosome)[0]
            transcript.strand = fields[3][1]
            transcript.txStart = int(fields[4])
            transcript.txEnd = int(fields[5])
            transcript.cdsStart = int(fields[6])
            transcript.cdsEnd = int(fields[7])
            transcript.exonCount = int(fields[8])
            transcript.exonStarts = fields[9].replace('"', '')
            if len(fields) > 10:
                transcript.exonEnds = fields[10].replace('"', '')
                if len(fields) > 11:
                    unknown = fields[11]
                    transcript.alternateName = fields[12].replace('"', '')
                    transcript.cdsStartStat = fields[13].replace('"', '')
                    transcript.cdsEndStat = fields[14].replace('"', '')
                    transcript.exonFrames = fields[15].replace('"', '')

            session.commit()

if __name__ == '__main__':
    # Import configuration options
    from ConfigParser import SafeConfigParser
    c = SafeConfigParser()
    c.read('config.txt')
    refseq_annotations_filename = c.get('Data files', 'refseq_annotations')
    refseq_annotations_fh = open(refseq_annotations_filename, 'r')

    from schema.connection import *

    print metadata
    upload_annotations(refseq_annotations_fh, session, metadata)


