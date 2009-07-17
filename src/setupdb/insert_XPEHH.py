#!/usr/bin/env python
"""
insert all the XP-EHH values into the db

usage:
$: python insert_XPEHH.py <chromosome number> 

The argument chromosome_number is required because the script uploads a chromosome at a time. This allows to execute multiple jobs at a time
"""


from schema.connection import *

#print metadata.bind
import sys

results_by_continent_dir = "/home/gioby/Data/HGDP/Results/XPEHH/Rsb_7continents_Pvalue_22chromosomes/"
#           0  1   2    3      4    5    6   7   8     9    10      11      12      13      14    15
header = 'chr pos AME CSASIA EASIA EUR MENA OCE SSAFR EUR-p OCE-p MENA-p EASIA-p CSASIA-p SAFR-p AME-p' # why AME-p is last?

try:
    chromosome = sys.argv[1]

except:
    raise ValueError(__doc__)
filename = results_by_continent_dir + "lnRsb_7conti_Pvalue.sm_chr" + chromosome
xpehh_file = open(filename, 'r')

line_count = 0


# CLEAN DATA
#session.remove

#DDL('LOAD DATA INFILE %s INTO TABLE xpehh FIELDS TERMINATED BY "\t"           ' % (filename))


for line in xpehh_file:
    line_count += 1
    fields = line.split()
#    print len(fields)
    chr = fields[0]
    assert chr == chromosome
    assert len(fields) == 16
    position = fields[1]
    snp = session.query(SNP).filter(SNP.physical_position == position).filter(SNP.chromosome == chr).all()[0]
    print snp

    #TODO: instantiate the multiple relationship SNP->Stats->XP-EHH
    xp = XPEHH(snp.id)
#    xp.snp_id = snp.id

    if fields[2] != 'nan':
        xp.ame = float(fields[2])

    if fields[3] != 'nan':
        xp.csasia = float(fields[3])
    if fields[4] != 'nan':
        xp.eas5a = float(fields[4])
    if fields[5] != 'nan':
        xp.eur = float(fields[5])
    if fields[6] != 'nan':
        xp.mena = float(fields[6])
    if fields[7] != 'nan':
        xp.oce = float(fields[7])
    if fields[8] != 'nan':
        xp.ssafr = float(fields[8])
    if fields[9] != 'nan':
        xp.eur_p = float(fields[9])
    if fields[10] != 'nan':
        xp.oce_p = float(fields[10])
    if fields[11] != 'nan':
        xp.mena_p = float(fields[11])
    if fields[12] != 'nan':
        xp.easia_p = float(fields[12])
    if fields[13] != 'nan':
        xp.csasia_p = float(fields[13])
    if fields[14] != 'nan':
        xp.ssafr_p = float(fields[14])
    if fields[15] != 'nan':
        xp.ame_p = float(fields[15])

    xp.original_file = filename
    xp.version = 1
    if line_count % 100 == 0:
        session.commit()


    





if __name__ == '__main__':
    pass

