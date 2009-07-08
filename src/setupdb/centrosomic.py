#!/usr/bin/env python
"""
for every snp in the db, upload the information on whether it is in a centrosome or not
"""
from schema.connection import *
import sys
metadata.bind.echo = True

try:
    chromosome = sys.argv[1] 
except:
    raise TypeError('please run this program with a chromosome number as argument')

centfile = open('/home/gioby/Data/HGDP/Annotations/centromeres.gff', 'r')
centromeres = {}

for line in centfile:
    fields = line.split()
    chr = fields[0][3:]
    if not centromeres.has_key(chr):
        centromeres[chr] = [fields[3], ]
    else:
        centromeres[chr].append(fields[4])

centromeric_snps = SNP.get_snps_by_region(chromosome, centromeres[chromosome][0], centromeres[chromosome][1])

#for snp in SNP.query():
#    if snp.annotations is None:
#        snp.annotations = Annotations()
#
#    snp.annotations.centrosomic = True

for snp in centromeric_snps:
    if snp.annotations is None:
        snp.annotations = Annotations()
    snp.annotations.centrosomic = True
session.commit()

print snp.annotations

if __name__ == '__main__':
    pass

