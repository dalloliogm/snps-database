/* #LOAD DATA LOCAL INFILE 'genes_refseq' into table refseqgenes FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' (name, chrom, strand, txStart, txEnd, cdsStart, cdsEnd, exonCount, exonStarts, exonEnds, alternateName, cdsStartStat, cdsEndStat) */

LOAD DATA LOCAL INFILE 'genes_refseq_mar2006', into table refseqgenes FIELDS TERMINATED BY '\t' ENCLOSED BY "" (ncbi_transcript_id, chromosome, strand, txStart, txEnd, cdsStart, cdsEnd, exonCount, exonStarts, exonEnds, alternateName, cdsStartStat, cdsEndStat, exonFrames)

/* genomic_build */

/* name, chrom, strand, txStart, txEnd, cdsStart, cdsEnd, exonCount, exonStarts, exonEnds, alternateName, cdsStartStat, cdsEndStat, exonFrames */
