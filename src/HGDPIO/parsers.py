from schema.schema import *
#from connection import *
import re
import logging
import csv
from sqlalchemy.orm.exc import NoResultFound

def iHS_parser_new(handle, session, metadata):
    """
    >>> from schema.debug_database import * 
    >>> from StringIO import StringIO

#    >>> snps = (SNP('rs10907192', physical_position = 1782971L), 
#    ...            SNP('rs16824500', physical_position = 1783072L), 
#    ...            SNP('rs4648592', physical_position = 1790894L), 
#    ...            SNP('rs7525092', physical_position = 1799950L))
#    >>> session.commit()

    >>> iHS_all_file = StringIO(
    ... '''chromosome      snpID   position.cM     position        allele1 allele2 ancestralAllele daf.AME  ihs.raw.AME     ihs.std.AME     daf.CSASIA      ihs.raw.CSASIA  ihs.std.CSASIA  daf.EASIA    ihs.raw.EASIA   ihs.std.EASIA   daf.EUR ihs.raw.EUR     ihs.std.EUR     daf.MENA        ihs.raw.MENA    ihs.std.MENA    daf.OCE ihs.raw.OCE     ihs.std.OCE     daf.SSAFR       ihs.raw.SSAFR   ihs.std.SSAFR
    ... 1       rs10907192      1.1171738152    1782971 A       G       G       0.07    1.994   1.79669447708548        0.234   1.07    0.422834558885843       0.118   0.883   0.395983962980141       NA      NA      NA      0.178   0.991   0.176012616404265       0.074   0.386   -0.142779233287260      0.465   1.231   1.69078796331248
    ... 1       rs16824500      1.1171806204    1783072 A       G       A       NA      NA      NA      NA      NA      NA      NA      NA      NA      NA      NA   NA      NA      NA      NA      0.796   0.487   0.415106391256120       0.752   -0.499  -0.122547389464255
    ... 1       rs4648592       1.117763149     1790894 A       G       G       0.094   0.721   0.117070264658037       0.174   1.321   0.690723748986451       0.122   0.983   0.549206740586772       0.239   0.985   0.351044493463773       0.206   0.992   0.281080754514218       NA      NA      NA      0.099   -0.312  -2.14970667471286
    ... 1       rs7525092       1.1178159302    1799950 T       C       C       0.094   0.721   0.117070264658037       0.174   1.321   0.690723748986451       0.164   0.883   0.430366296275457       0.239   0.985   0.351044493463773       0.212   0.904   0.158312286773808       NA      NA      NA      0.139   -0.38   -2.13341547242042''')
    >>> iHS_all_file.name = ''

    >>> iHS_all_parser(iHS_all_file, session, metadata)

#    >>> session.query(SNP.id, SNP.ancestral_allele, SNP.derived_allele).all()

    >>> session.query(Stats).all()[:2]
    [stats on SNP SNP rs10907192 on easia: iHS 0.39598396298, daf 0.118, stats on SNP SNP rs10907192 on ssafr: iHS 1.69078796331, daf 0.465]

    """ 
    try:
        filename = handle.name
        file_lastmodif = os.stat(handle.name).st_mtime
    except:
        filename = ''
        file_lastmodif = ''

    for line in handle:
        fields = line.split()

        if fields and not line.startswith('chromosome'):
            chromosome = fields[0]
            snp_id = fields[1]

            snp = session.query(SNP).filter_by(id = snp_id).one()
            logging.debug(snp)

            genetic_position = fields[2]
            if genetic_position == 'NA':
                snp.genetic_position = None
            else:
                snp.genetic_position = float(fields[2])
#            else:
#                raise TypeError('genetic position?? %s' % line)
            try:
                snp.physical_position == int(fields[3])
            except:
                logging.debug('snp.position not corresponding')
                logging.debug(snp)
                logging.debug(fields[3])
#            assert snp.allele1 == fields[4]
#            assert snp.allele2 == fields[5]
            ancestral_allele = fields[6]
#            if ancestral_allele == 'NA':
#                snp.ancestral_allele = '-'
#            else:
#                snp.ancestral_allele = ancestral_allele

            stat_indexes = {'AME': (7, 9), 'CSASIA': (10, 12), 'EASIA': (13, 15),
                            'EUR': (16, 18), 'MENA': (19, 21), 'OCE': (22, 24),
                            'SSAFR': (25, 27)}

            for (popkey, indexes) in stat_indexes.items():
                stat = Stats(snp, popkey)
               
                daf = fields[indexes[0]]
                if daf == 'NA':
                    stat.daf_iHS = None
                else:
                    stat.daf_iHS = float(daf)

                iHS = fields[indexes[1]]
                if iHS == 'NA':
                    stat.iHS = None
                else:
                    stat.iHS = float(iHS)
 
                stat.iHS_file = filename
                stat.iHS_file_lastmodification = file_lastmodif


d
def iHS_all_parser(handle, session, metadata):
    """
    >>> from schema.debug_database import * 
    >>> from StringIO import StringIO

    >>> snps = (SNP('rs10907192', physical_position = 1782971L), 
    ...            SNP('rs16824500', physical_position = 1783072L), 
    ...            SNP('rs4648592', physical_position = 1790894L), 
    ...            SNP('rs7525092', physical_position = 1799950L))
    >>> session.commit()

    >>> iHS_all_file = StringIO(
    ... '''chromosome      snpID   position.cM     position        allele1 allele2 ancestralAllele daf.AME  ihs.raw.AME     ihs.std.AME     daf.CSASIA      ihs.raw.CSASIA  ihs.std.CSASIA  daf.EASIA    ihs.raw.EASIA   ihs.std.EASIA   daf.EUR ihs.raw.EUR     ihs.std.EUR     daf.MENA        ihs.raw.MENA    ihs.std.MENA    daf.OCE ihs.raw.OCE     ihs.std.OCE     daf.SSAFR       ihs.raw.SSAFR   ihs.std.SSAFR
    ... 1       rs10907192      1.1171738152    1782971 A       G       G       0.07    1.994   1.79669447708548        0.234   1.07    0.422834558885843       0.118   0.883   0.395983962980141       NA      NA      NA      0.178   0.991   0.176012616404265       0.074   0.386   -0.142779233287260      0.465   1.231   1.69078796331248
    ... 1       rs16824500      1.1171806204    1783072 A       G       A       NA      NA      NA      NA      NA      NA      NA      NA      NA      NA      NA   NA      NA      NA      NA      0.796   0.487   0.415106391256120       0.752   -0.499  -0.122547389464255
    ... 1       rs4648592       1.117763149     1790894 A       G       G       0.094   0.721   0.117070264658037       0.174   1.321   0.690723748986451       0.122   0.983   0.549206740586772       0.239   0.985   0.351044493463773       0.206   0.992   0.281080754514218       NA      NA      NA      0.099   -0.312  -2.14970667471286
    ... 1       rs7525092       1.1178159302    1799950 T       C       C       0.094   0.721   0.117070264658037       0.174   1.321   0.690723748986451       0.164   0.883   0.430366296275457       0.239   0.985   0.351044493463773       0.212   0.904   0.158312286773808       NA      NA      NA      0.139   -0.38   -2.13341547242042''')
    >>> iHS_all_file.name = ''

    >>> iHS_all_parser(iHS_all_file, session, metadata)

#    >>> session.query(SNP.id, SNP.ancestral_allele, SNP.derived_allele).all()

    >>> session.query(Stats).all()[:2]
    [stats on SNP SNP rs10907192 on easia: iHS 0.39598396298, daf 0.118, stats on SNP SNP rs10907192 on ssafr: iHS 1.69078796331, daf 0.465]

    """ 
    try:
        filename = handle.name
        file_lastmodif = os.stat(handle.name).st_mtime
    except:
        filename = ''
        file_lastmodif = ''

    for line in handle:
        fields = line.split()

        if fields and not line.startswith('chromosome'):
            chromosome = fields[0]
            snp_id = fields[1]

            snp = session.query(SNP).filter_by(id = snp_id).one()
            logging.debug(snp)

            genetic_position = fields[2]
            if genetic_position == 'NA':
                snp.genetic_position = None
            else:
                snp.genetic_position = float(fields[2])
#            else:
#                raise TypeError('genetic position?? %s' % line)
            try:
                snp.physical_position == int(fields[3])
            except:
                logging.debug('snp.position not corresponding')
                logging.debug(snp)
                logging.debug(fields[3])
#            assert snp.allele1 == fields[4]
#            assert snp.allele2 == fields[5]
            ancestral_allele = fields[6]
            if ancestral_allele == 'NA':
                snp.ancestral_allele = '-'
            else:
                snp.ancestral_allele = ancestral_allele

            stat_indexes = {'AME': (7, 9), 'CSASIA': (10, 12), 'EASIA': (13, 15),
                            'EUR': (16, 18), 'MENA': (19, 21), 'OCE': (22, 24),
                            'SSAFR': (25, 27)}

            for (popkey, indexes) in stat_indexes.items():
                stat = Stats(snp, popkey)
               
                daf = fields[indexes[0]]
                if daf == 'NA':
                    stat.daf_iHS = None
                else:
                    stat.daf_iHS = float(daf)

                iHS = fields[indexes[1]]
                if iHS == 'NA':
                    stat.iHS = None
                else:
                    stat.iHS = float(iHS)
 
                stat.iHS_file = filename
                stat.iHS_file_lastmodification = file_lastmodif


def refseqgenes_parser(handle):
    """
    Parse information for refseqgenes, from a table taken from ucsc
    """
    pass

def snpmap_parser(handle):
    """
    Parse informations on SNPs (chromosome and position)

    >>> from schema.debug_database import *
    >>> from StringIO import StringIO
    >>> snpmap_file = StringIO(
    ... '''MitoT9900C      M       9900
    ... MitoT9951C      M       9951
    ... rs10000543      4       30979886
    ... rs10000918      4       186505570
    ... rs10000929      4       131516474
    ... rs10001378      4       182579995
    ... rs10001548      4       166098831
    ... rs10002472      4       159087423''')

    """
    # SNPs should have already been uploaded to the database, with the genotype_parser function
    for line in handle:
#        logging.debug(line)
        fields = line.split()
        if len(fields) != 3:
            pass
        else:
            id = fields[0].lower()
            snp = SNP.get_by(id=id)

            snp.chromosome = fields[1]
            snp.physical_position = int(fields[2])

def snpHap650Annotations(handle):
    """
    Reads annotations on snps from a file called HumanHap650Yv3 _Gene_Annotation
    """
    pass

def rosenberg_parser(handle, session, metadata):
    """
    Parse the annotations on individuals and populations provided in the Rosenberg 2006.
    
    >>> from schema.debug_database import *
    >>> from StringIO import StringIO
    >>> rosenberg_file = StringIO(
    ... '''
    ... "HGDPIndividualNumber"	"PopulationCode"	"PopulationName"	"SamplingLocation"	"GeographicRegionOfPopulation"	"Sex"	"InHGDP.CEPHpanel.CannEtAl2002.."	"AnalyzedInRosenbergEtAl2002."	"PopulationLabelBelievedToBeCorrect."	"HasNoDuplicatesInPanel."	"AnalyzedInRosenbergEtAl2005.datasetH1048.."	"HasNoKnown1stDegreeRelativesInPanel."	"HasNoKnown1stOr2ndDegreeRelativesInPanel."	"HasAParentOrOffspringInPanel."	"IncludedInDataset971.No1stDegreeRelatives.."	"IncludedInDataset952.No1stOr2ndDegreeRelatives.."	"DuplicationConjugate.OnlyDiffersFromSampleNumberIfSampleIsDuplicated."	"AlternatePopulationCode.OnlyDiffersFromPrimaryPopulationCodeForBantuSouthAfrica."	"AlternatePopulationName.OnlyDiffersFromPrimaryPopulationNameForBantuSouthAfrica."	"OrangeQInRosenbergEtAl2002Fig1K.5"	"BlueQInRosenbergEtAl2002Fig1K.5"	"PinkQInRosenbergEtAl2002Fig1K.5"	"GreenQInRosenbergEtAl2002Fig1K.5"	"PurpleQInRosenbergEtAl2002Fig1K.5"	"hgdp.id"	"population/working unit"	"studySetLiNorel"	"continent"	"Li"
    ... 705	81	"Colombian"	"Colombia"	"AMERICA"	"m"	1	1	1	1	1	0	0	1	0	0	705	81	"Colombian"	1	3	108	5	883	"HGDP00705"	"Colombian"	"FALSE"	"AME"	"TRUE"
    ... 793	81	"Colombian"	"Colombia"	"AMERICA"	"f"	1	1	1	1	1	0	0	1	0	0	793	81	"Colombian"	2	139	131	1	727	"HGDP00793"	"Colombian"	"FALSE"	"AME"	"TRUE"
    ... 709	81	"Colombian"	"Colombia"	"AMERICA"	"m"	1	1	1	1	1	0	0	1	0	0	709	81	"Colombian"	1	1	104	7	887	"HGDP00709"	"Colombian"	"FALSE"	"AME"	"TRUE"
    ... ''')
    """
    # I won't use the csv module because it has problems with the field 21
    headers = handle.readline().split()
    individuals = []

    for line in handle:
        fields = line.split('\t')
        ind_id = fields[24].replace('"', '')
        included_in_dataset952 = fields[15]
        has_not_duplicated = fields[9]
#        print fields
        included_in_Li = fields[-1].strip().replace('"', '')
        print included_in_Li
        print included_in_Li == '"TRUE"'
#        print included_in_dataset952
#        raw_input()
     
#        logging.debug(included_in_Li)
#        logging.debug(len(fields))

#        logging.debug(str([ind_id, included_in_dataset952, has_not_duplicated]))

        if (included_in_dataset952 == "1") and (included_in_Li == "TRUE"):
#            print ind_id
            ind = Individual(ind_id, source_file = handle.name, sex = fields[5][1])
            ind.hgdp_individual_number = fields[0]

            popname = fields[2].replace('"', '').lower()
            popcode = fields[1].replace('"', '')
            working_unit = fields[25].replace('"', '')
            region = fields[3].replace('"', '')
            continent_code = fields[27].replace('"', '')
            continent = fields[4].replace('"', '')
#            logging.debug(str((popname, popcode, working_unit, region, continent, continent_code)))
            try:
                population = Population.query.filter_by(popname = popname).one()
            except NoResultFound:
                population = Population(popname = popname, popcode = popcode,
                                working_unit = working_unit, region = region,
                                continent_macroarea = continent, 
                                continent_code = continent_code) 
                population.source_file = handle.name

            ind.population = population
            individuals.append(ind)
    session.add_all(individuals)
    return individuals

        
#        raw_input()

def individuals_genotypesindex_parser(handle):
    """
    add genotypes_index to every individual.
    I am writing this script to fix a typo (see bug #4)
    """
#    handle.readline()       # first line is empty??
    header = handle.readline()
    if header is None:
        raise ValueError('Empty file!!')

    header_fields = header.split()
#    logging.debug(header_fields)
    individuals = []

    current_index = 0
    for ind_id in header.split():

        #Check if there is an individual with the current id in the database
        individual = Individual.get_by(name = ind_id)
        if individual is not None:
            individual.genotypes_index = current_index
            current_index += 1

def genotypes_parser(handle, ):
    """
    Parse a genotypes file handler.
    
    It upload a Marker object to the database for every line of the file

    >>> from schema.debug_database import *
    >>> print metadata
    MetaData(Engine(sqlite:///:memory:))
    >>> from StringIO import StringIO
    >>> genotypes_file = StringIO(
    ... '''  HGDP00001    HGDP00002    HGDP00003    HGDP00004    HGDP00005    HGDP00006    HGDP00007    HGDP00008    HGDP00009    HGDP000010
    ... rs1112390    AA    GG    AG    AA    AA    AA    AA    AA    AA    AA   
    ... rs1112391    TT    TC    CC    CC    CC    CC    CC    CC    CC    CC
    ... MitoA11252G    AA    AA    AA    AA    AA    AA    AA    AA    AA    AA
    ... rs11124185    TC    TT    TT    TT    TT    TT    TT    TT    TT    TT
    ... MitoA13265G    AA    AA    AA    AA    AA    AA    AA    AA    AA    AA
    ... MitoA13264G    GG    AA    AA    AA    GG    AG    AA    AA    AA    AA
    ... MitoA13781G    AA    AA    AA    AA    AA    AA    --    AA    AA    AA
    ... MitoA14234G    AA    AA    AA    AA    AA    AA    AA    AA    AA    AA
    ... MitoA14583G    AA    AA    AA    AA    AA    AA    AA    AA    AA    AA
    ... MitoA14906G    GG    GG    GG    GG    GG    GG    GG    GG    GG    GG
    ... MitoA15219G    AA    AA    AA    GG    AA    AA    AA    AA    AA    AA''')

    # fix required only for StringIO objects
    >>> genotypes_file.name = 'stringio object'
    
    running this script will add all the genotypes to the snp database:
    >>> genotypes_parser(genotypes_file)

    >>> SNP.query().limit(3).all()
    [SNP rs1112390, SNP rs1112391, SNP MitoA11252G]
    
    """
    # read the header, containing the Individuals names
#    handle.readline()       # first line is empty??
    header = handle.readline()
    if header is None:
        raise ValueError('Empty file!!')

    header_fields = header.split()
#    logging.debug(header_fields)
    individuals = []

    excluded_columns = []  # a list of the genotypes to be excluded when parsing the snps fields
    current_index = 0
    for column_id in range(len(header_fields)):
        ind_id = header_fields[column_id]
#        logging.debug(ind_id)

        #Check if there is an individual with the current id in the database
        individual = Individual.get_by(name = ind_id)
#        logging.debug(individual)
        if individual is not None:
            individual.genotypes_index = current_index
            individual.column_index = column_id
            current_index += 1
            individuals.append(individual)
            logging.debug(individual.genotypes_index)
        else: 
            excluded_columns.append(column_id)
#    logging.debug(individuals)
    logging.debug(excluded_columns)
    
    # Read snp file line by line.
    for line in handle.readlines():
        fields = line.split()   # TODO: add more rigorous conditions
        if fields is None:
            break

        allele1_is_set = False
        allele2_is_set = False
         
        # Initialize a SNP object 
        snp = SNP(id = fields[0], genotypes='')
#        logging.debug(snp)
        snp.genotypes_file = handle.name
        # Try to determine chromosome's number from file name
        chr = re.findall('/chr(.*).geno', handle.name)
        if chr != []:
            snp.chromosome = unicode(chr[0])
        
        # read all the file's rows
        for n in range(1, len(fields)):
            if n-1 not in excluded_columns:
                # this is a valid genotype that we want to include in the db
                current_genotype = fields[n].upper()
#                snp.genotypes += current_genotype

                if current_genotype in ('AA', 'TT',):
                    genotype_code = '0'
                elif current_genotype in ('CC', 'GG'):
                    genotype_code = '2'
                elif current_genotype in ('--', ):
                    genotype_code = '9'
                elif current_genotype in ('AC', 'AG', 'TC', 'TG'):
                    genotype_code = '1'
                else:
                    raise TypeError('genotype is of unknown format')

                snp.genotypes += genotype_code

                if allele1_is_set is not True:
                    if current_genotype[0] in ('A', 'T'):
                        snp.allele1 = current_genotype[0].upper()
                        allele1_is_set = True
                if allele2_is_set is not True:
                    if current_genotype[1] in ('C', 'G'):
                        snp.allele2 = current_genotype[1].upper()
                        allele2_is_set = True
#    session.commit()

#        logging.debug(snp.genotypes)
     

def _test():
    """test the current module"""
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    _test()
