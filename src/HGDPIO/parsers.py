from schema.schema import *
#from connection import *
import re
import logging
import csv
from sqlalchemy.orm.exc import NoResultFound

def rosenberg_parser(handle):
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
    ... '''
    """
    # I won't use the csv module because it has problems with the field 21
    headers = handle.readline().split()
    for line in handle:
        fields = line.split()
        ind_id = fields[24].replace('"', '')
        included_in_dataset952 = fields[15]
        has_not_duplicated = fields[9]

#        logging.debug(str([ind_id, included_in_dataset952, has_not_duplicated]))

        if (included_in_dataset952 == "1") and (has_not_duplicated == "1"):
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

        
#        raw_input()

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
    
    running this script will add all the genotypes to the snp database:
    >>> genotypes_parser(genotypes_file)

    >>> SNP.query().limit(3)
    
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
    for column_id in range(len(header_fields)):
        ind_id = header_fields[column_id]
#        logging.debug(ind_id)

        #Check if there is an individual with the current id in the database
        individual = Individual.get_by(name = ind_id)
#        logging.debug(individual)
        if individual is not None:
            individual.genotype_index = column_id
            individuals.append(individual)
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
        
        # read all the file's rows
        for n in range(1, len(fields)):
            if n-1 not in excluded_columns:
                # this is a valid genotype that we want to include in the db
                current_genotype = fields[n]
                snp.genotypes += current_genotype

                if allele1_is_set is not True:
                    if current_genotype[0] in ('a', 'A', 't', 'T'):
                        snp.allele1 = unicode(current_genotype[0].upper())
                        allele1_is_set = True
                if allele2_is_set is not True:
                    if current_genotype[1] in ('c', 'C', 'g', 'G'):
                        snp.allele2 = unicode(current_genotype[1].upper())
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
