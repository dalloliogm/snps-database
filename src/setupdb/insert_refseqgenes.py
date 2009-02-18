#!/usr/bin/env python
"""
Insert the UCSC refseqgene table in the db.
"""

import logging
import re

def upload_annotations(refseq_annotations_fh, session, metadata):
    """
    upload annotations

    >>> from schema.debug_database import *
    >>> print metadata
    MetaData(Engine(sqlite:///:memory:))
    >>> annotations = StringIO.StringIO('''\
    ... "NR_024077" "chr1"  "-" 4268    14754   14754   14754   10  "4268,4832,5658,6469,"   "4692,4901,5810,6631,6918"   "WASH2P"    "unk"   "unk"   "-1,-1,-1,-1,"
    ... "NM_001005484"  "chr1"  "+" 58953   59871   58953   59871   1   58953   59871   "OR4F5" "cmpl"  "cmpl"  0
    ... "NM_001005224"  "chr1"  "+" 357521  358460  357521  358460  1   357521  358460  "OR4F3" "cmpl"  "cmpl"  0)
    >>> upload_annotations(annotations)
    >>> gene1 = RefSeqGene.query().filter_by(ncbi_transcript_id = 'NR_024077')
    >>> print gene1.chromosome, gene1.strand, gene1.txStart
    chr1 - 4268

    """
    metadata.bind.echo = True
    session.bind = metadata.bind    # necessary for doing session.execute

#    for ind in session.execute('select * from individuals limit 10;'):
#        print ind

#    session.execute("""LOAD DATA LOCAL INFILE '%s' into table refseqgenes FIELDS TERMINATED BY '\t' ENCLOSED BY "" (ncbi_transcript_id, chromosome, strand, txStart, txEnd, cdsStart, cdsEnd, exonCount, exonStarts, exonEnds, alternateName, cdsStartStat, cdsEndStat, exonFrames)""" % refseq_annotations_filename)

#    annotations_fh = open(refseq_annotations_filename, 'r')
    logging.basicConfig(level=logging.DEBUG)
    for line in refseq_annotations_fh:
        line = line.strip()
        if line and not line.startswith('"#'):
            gene = RefSeqGene()
            gene.sourcefile = refseq_annotations_fh.name

            fields = line.split()
            logging.debug(fields)
            
            gene.bin = fields[0]
            gene.ncbi_transcript_id = fields[1].replace('"', '')
            chromosome = fields[2].replace('"', '')
            gene.chromosome = re.findall('chr(.*)', chromosome)[0]
            gene.strand = fields[3][1]
            gene.txStart = int(fields[4])
            gene.txEnd = int(fields[5])
            gene.cdsStart = int(fields[6])
            gene.cdsEnd = int(fields[7])
            gene.exonCount = int(fields[8])
            gene.exonStarts = fields[9].replace('"', '')
            if len(fields) > 10:
                gene.exonEnds = fields[10].replace('"', '')
                if len(fields) > 11:
                    unknown = fields[11]
                    gene.alternateName = fields[12].replace('"', '')
                    gene.cdsStartStat = fields[13].replace('"', '')
                    gene.cdsEndStat = fields[14].replace('"', '')
                    gene.exonFrames = fields[15].replace('"', '')

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


