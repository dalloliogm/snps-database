from schema.schema import *
#from connection import *
import re
import logging
import csv

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
        individual_included = fields[15]
        Individual(ind_id)
#        print individual_included
#        if individual_included == 1:
#            Individual(ind_id)
        
#        raw_input()



def samples_parser(handle, ):
    """
    parse a file with descriptions of Individuals (samples) in hgdp
    
    >>> from schema.debug_database import *
    >>> print metadata
    MetaData(Engine(sqlite:///:memory:))
    
    >>> from StringIO import StringIO
    >>> samples_file = StringIO(
    ... '''"sample"
    ... "code"  "sex"    "population"    "region"        "continent"     "Unidad"
    ... "HGDP00001"    "M"    "Brahui Test"    "Pakistan"      "Asia"  "Brahui"
    ... "HGDP00003"    "M"    "Brahui"    "Pakistan"      "Asia"  "Brahui"
    ... "HGDP01362"    "M"    "French Basque"    "France"    "Europe"    "Basque"
    ... "HGDP00004"    "F"    "Brahui"    "Pakistan"      "Asia"  "Brahui"
    ... "HGDP00151"    "F"    "Makrani"    "Pakistan"    "Asia"    "Makrani"''')
    >>> samples = samples_parser(samples_file)
    >>> print samples[:3]
    [Mr. HGDP00001 (brahui test), Mr. HGDP00003 (brahui), Mr. HGDP01362 (french basque)]
    
    # filter all individuals belonging to 'makrani'
    >>> print [individual for individual in samples if individual.population == "makrani"]
    [Mrs. HGDP00151 (makrani)]
    
    >>> print samples[0].population.region
    pakistan
    
    >>> print samples[0].population.continent_macroarea
    asia
    
    # the same as before but using the filter function:
    >>> filter(lambda ind: ind.population == 'MAKRANI', samples)
    [Mrs. HGDP00151 (makrani)]
    
    # Beware that the attributes in population are case sensitive!!!
    >>> filter(lambda ind: ind.population.continent_macroarea == 'asia', samples)
    [Mr. HGDP00001 (brahui test), Mr. HGDP00003 (brahui), Mrs. HGDP00004 (brahui), Mrs. HGDP00151 (makrani)]
    
    >>> session.flush()
    """

    handle.readline()   # skip headers
    header = handle.readline()
    if header is None:
        raise ValueError('Empty file!!')
    
    individuals = []                # not necessary with the database

    splitter = re.compile('"\s+"')    
    for line in handle.readlines():
        # split the line according to spaces and "
        row = splitter.split(line)
        
        if row is None: 
            break   # FIXME: optimize
        if len(row) != 6:
            raise ValueError("wrong number of columns in current line")
        
        ind_id = row[0].replace('"', '')
#        logging.debug(row)
        sex = row[1]
        popname = row[2].lower()
        region = row[3]
        macroarea = row[4]
        unit = row[5].replace('"', '')
        
        # create an Individual object
        # If the population given doesn't exists, a new record is created
        ind = Individual(ind_id, population=popname, sex=sex, region=region, 
                         macroarea=macroarea, working_unit=unit, 
                         source_file = handle.name)
        individuals.append(ind)

    return individuals
   

def genotypes_parser(handle, ):
    """
    Parse a genotypes file handler.
    
    It returns a Marker object for every line of the file

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
    # initialize output var
    snps = []
    
    # read the header, containing the Individuals names
#    handle.readline()       # first line is empty??
    header = handle.readline()
    if header is None:
        raise ValueError('Empty file!!')
#    individuals = [Individual(ind_id) for ind_id in header.split()]
    
    # Read snp file line by line.
    for line in handle.readlines():
        fields = line.split()   # TODO: add more rigorous conditions
        if fields is None:
            break
        
        # Initialize a SNP object 
        snp = SNP(id = fields[0])
        snps.append(snp)
        
        # read 
        for n in range(1, len(fields)):
#            current_individual = individuals[n-1]
            current_genotype = fields[n]
            
            snp.genotypes1 += current_genotype[0]
            snp.genotypes2 += current_genotype[1] # TODO: change!!

    return snps
     

def _test():
    """test the current module"""
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    _test()
