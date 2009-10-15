#!/usr/bin/env python
"""
upload all <global> FST to the database

usage:
$: python insert_Fst.py <chromosome>


sample input file:
rs12255619      0.0284
rs10904494      0.0460
rs11591988      0.2583
rs10904561      0.0733
rs7906287       0.1570
rs9419557       0.0864
rs9286070       0.1430
rs11253562      0.1023
rs4881551       0.0484
rs4880750       0.0704
rs11594819      0.0886
rs10903451      0.0970
rs12779173      0.0457

"""
from schema.connection import *

#print metadata.bind
import sys

results_by_continent_dir = "/home/gioby/Data/HGDP/Results/fst/"
#           0  1   2    3      4    5    6   7   8     9    10      11      12      13      14    15
header = 'chr pos AME CSASIA EASIA EUR MENA OCE SSAFR EUR-p OCE-p MENA-p EASIA-p CSASIA-p SAFR-p AME-p' # why AME-p is last?

try:
    chromosome = sys.argv[1]
    print chromosome
    fst_filename = results_by_continent_dir + "/940LiUnrel-polyQC-chr" + chromosome + "-fst.tab"
    fst_file = open(fst_filename, 'r')
except:
    print fst_filename
    raise ValueError(__doc__)
print fst_file

for line in fst_file:
    (snp_id, fst_val) = line.split()
    if fst_val != "NA":
        fst_val = float(fst_val)
    else:
        fst_val = None
    print snp_id, fst_val
    snp = SNP.get_by(id = snp_id)
    fst = Fst(snp_id)
    fst.value = fst_val
    session.commit()

#






if __name__ == '__main__':
    pass

