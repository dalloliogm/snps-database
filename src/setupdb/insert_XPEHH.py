#!/usr/bin/env python
"""
insert all the XP-EHH values into the db

usage:
$: python insert_XPEHH.py <chromosome number> 

The argument chromosome_number is required because the script uploads a chromosome at a time. This allows to execute multiple jobs at a time
"""


from schema.connection import *

print metadata.bind
import sys

results_by_continent_dir = "/Data/HGDP/Results/XPEHH/Rsb_7continents_Pvalue_22chromosomes/"
header = 'chr pos AME CSASIA EASIA EUR MENA OCE SSAFR EUR-p OCE-p MENA-p EASIA-p CSASIA-p SAFR-p AME-p' # why AME-p is last?

try:
    chromosome = sys.argv[1]

except:
    raise ValueError(__doc__)

xpehh_file = open(results_by_continent_dir + "lnRsb_7conti_Pvalue.sm_chr" + 1



if __name__ == '__main__':
    pass

