#!/usr/bin/env python
# Create a database for HGDP data
"""
This is the schema for a database designed to handle HGDP SNPs data.
To use it, you should better use 'from connection import *' (see connection.py
script) to use the existing MySql database on my computer.

Refer to tutorial.txt for an introduction
"""

from elixir import Entity, Field, Unicode, Integer, UnicodeText, String, Text
from recipes.enum import Enum
from elixir import ManyToOne, OneToMany, OneToOne, ManyToMany, DateTime
from elixir import metadata, using_options
from elixir.ext.versioned import acts_as_versioned
from config import connection_line
from datetime import datetime
import logging

#from PopGen.Gio.Individual import Individual
#from PopGen.Gio.SNP import SNP
#from PopGen.Gio.Individual import Individual


class SNP(Entity):
    """ Table 'SNPs'.
    
    This class represents both the table SNP, and the structure of an instance of a SNP object
    
    >>> rs1333 = SNP('rs1333')    # tests SNP.__init__
    >>> print rs1333              # tests SNP.__repr__
    SNP rs1333
    >>> rs1333.refseqgene = 'cox2' 

    Let's add six genotypes. The first individual is homozygote for 'allele2', 

    >>> rs1333.add_genotype('200109')
    """
    using_options(tablename = 'snps')
    
    id                  = Field(String(30), primary_key=True, unique=True)
    chromosome          = Field(String(10), index=True)
    physical_position   = Field(Integer)
    original_strand     = Field(String(1))

    next_snp            = ManyToOne('SNP')   # next SNP on the chromosome
    previous_snp        = OneToOne('SNP')

    # allele1 can be only A or T. allele2 only C or G
    allele1             = Field(Enum(values=('A', 'T', '-')))
    allele2             = Field(Enum(values=('C', 'G', '-')))
    derived_allele      = Field(String(1))
#    dbSNP_ref           = Field(String(10)) # TODO: check if necessary ()
    
    genotypes           = Field(Text(2000), default='')  
    haplotypes_index    = Field(Integer)
    
    # Reference to closest gene 
    refseqgene          = ManyToOne('RefSeqGene')
    # The following annotations come from a file called HumanHap650v3GeneAnnotation

    hap_chromosome = Field(String(10))
    hap_coordinate = Field(Integer)
    hap_genomebuild = Field(String(40))
    gene_symbol = Field(Text)
    gene = Field(Text)
    location = Field(Text)
    location_relative_to_gene = Field(String(30))
    coding_status = Field(String(30))
    aminoacid_change = Field(String(40))
    id_with_mouse = Field(String(40))
    phast_conservation = Field(Integer) # TODO: supports negative numbers?

    # versioning
    snp_build           = Field(String(40))
    genotypes_file      = Field(String(80)) # input file containing the genotypes
    genomic_build       = Field(String(40)) # build on ucsc

    def __init__(self, id, chromosome = '', genotypes = '', allele1='-', allele2='-'):
        self.id = id
        self.chromosome = chromosome
        self.genotypes = genotypes
        self.allele1 = allele1
        self.allele2 = allele2
            
    def __repr__(self):
        # this method will be called when, in python code, you will do 'print SNP'.
        return 'SNP '  + self.id

    def get_dbSNP_url(self):
        """get the url to dbSNP"""
        raise NotImplementedError

    def get_ensembl_ref(self):
        """get the url to ensembl (put this in RefSeqGene?)"""
        raise NotImplementedError

    def get_genes(self, upstream, downstream):
        """Get genes in an interval of [upstream, downstream] from the snp position
        
        >>> rs1333 = SNP('rs1333')
        >>> rs1333.chromosome = '11'
        >>> rs1333.physical_position = 900
        >>> rs1333.get_genes(100, 100)
        -> all genes 100 upstream or downstream the position,
        from 800 to 1000 on chromosome 11

        The genes are included if they 

        >>> gene1 = RefSeqGene()
        """
        if not isinstance(upstream, int) and not isinstance(downstream, int):
            raise TypeError("SNP.get_genes requires two integers as input")
        
        if (chromosome is None) or (physical_position is None):
            raise ValueError('unknown coordinates for current snp')

        # get the proper interval where to find genes
        lower_limit = self.physical_position - upstream
        upper_limit = self.physical_position + downstream

        genes = RefSeqGene.query().filter_by(chromosome = self.chromosome).\
                                        filter_by(cdsStart >= lower_limit).\
                                        filter_by(cdsEnd =< upper_limit).all()
        return genes


    def add_genotype(self, genotype):
        """add genotypes"""
        # check that 'genotype' only contains 0, 1, 2
        # update table
        raise NotImplementedError

    def get_genotype_by_individuals(self, individuals, format='n'):
        """Given a list of individuals, get its genotype

        >>> snp = SNP.query().first()
        >>> snp.get_genotype_by_individuals(individuals = ('HGDP00001', 'HGDP01419'))
        [193L, 791L]

        format can be:
        - c -> character 
        - n -> numerical (0, 1, 2)
        """
        genotypes = []
        for ind in individuals:
            if isinstance(ind, Individual):
                ind_index = ind.genotypes_index
            elif isinstance(ind, str):
#                logging.debug(ind)
                ind_obj = Individual.query().filter_by(name = ind.strip()).first()
                if ind_obj is None:
                    return 'Could not find individual %s' % ind
                ind_index = ind_obj.genotypes_index

            if format == 'c':
                genotypes.append(self.get_genotype_char(ind_index))
            else:
                genotypes.append(ind_obj.genotypes_index)
        return genotypes

    def get_genotype_char(self, ind_index):
        """
        Get the genotype in the 'character' format.

        e.g. instead of [0, 1, 2, 9]
        get ['AA', 'AG', 'GG', 'CC', 'CT', 'TT']
        """
        bin_genotype = self.genotypes[ind_index]
#        logging.debug(bin_genotype, type(bin_genotype))

        char_genotype = ''
        if bin_genotype == '9':
            char_genotype = '--'
        elif bin_genotype == '0':
            char_genotype = self.allele1 + self.allele1
        elif bin_genotype == '1':
            char_genotype = self.allele1 + self.allele2
        elif bin_genotype == '2':
            char_genotype = self.allele2 + self.allele2
        return char_genotype

    @classmethod
    def get_snps_by_region(cls, chromosome, lower_limit = 0, upper_limit = -1):
        """
        Get the snps within a region
        >>> print SNP.get_snps_by_region('11', 1000000, 1050000)
        [SNP rs9442372,
        SNP rs3737728,
        SNP rs11260588,
        SNP rs9442398,
        SNP rs6687776,
        SNP rs9651273,
        SNP rs4970405,
        SNP rs12726255]

        note: if upper_limit == -1, get all the snps until the end of the chr.
        """
        if upper_limit == -1:
            snps = SNP.query.filter(SNP.chromosome == str(chromosome).upper()).\
                filter(SNP.physical_position > lower_limit).all()
        else:
            snps = SNP.query.filter(SNP.chromosome == str(chromosome).upper()).\
                filter(SNP.physical_position > lower_limit).\
                filter(SNP.physical_position < upper_limit).all()

        snps.sort(key=lambda x:x.physical_position)
        return snps
    
    def get_next_snp(self):
        """get the next SNP on the chromosome
        """
        return SNP.get_by(id = self.next_snp)
    
    def get_previous_snp(self):
        """get the previous SNP on the chromosome
        """
        return SNP.get_by(id = self.previous_snp)

class Articles(Entity):
    """ Table 'Articles'


    Many SNPs and Individuals are referenced in other articles.
    This table allows to quickly know if a SNP or an Individual has been studied 
    in a certain article.
    """
    using_options(tablename = 'articles')

    individuals = ManyToMany('Individual')
    snps = ManyToMany('SNP')
    authors = Field(String(100))
    title = Field(String(100))
    doi = Field(String(30))


class Individual(Entity):
    """ Table 'Individuals'
    
    >>> ind = Individual('Einstein')
    >>> ind                              # Test __repr__ method
    Mr. EINSTEIN (None)
    >>> print ind + ' Albert'            # Test __add__ method
    EINSTEIN Albert
    >>> print ind in ('Einstein', )      # Test __eq__ method
    True
    
    # You can define an individual and a population in the same statement.
    # If the given population doesn't exists, a new record is initiated
    >>> ind2 = Individual('Spock', 'Vesuvians')
    >>> print ind2.population
    vesuvians
    
    """
    using_options(tablename = 'individuals')
    
    name                = Field(String(30), unique=True, index=True)    # TODO: rename with 'id'?
    hgdp_individual_number = Field(String(10), unique = True)
    population          = ManyToOne('Population')   # TODO: how to index?
    sex                 = Field(Enum((u'm', u'u', u'f', None)))
    
    haplotypes          = Field(Text(650000))
    genotypes_index     = Field(Integer, unique=True)
#    column_index        = Field(Integer, unique=True) # column index in the original file

    articles            = ManyToMany('Articles')
#    population_label_believed_correct = Field(Boolean)
#    studyset_Li_noRel   = Field(Boolean)
    
#    last_modified       = Field(DateTime, onupdate=datetime.now, 
#                          default=datetime.now)

    # versioning
    source_file         = Field(Text(80))
    
    def __init__(self, name, population = None, sex = u'u', source_file = '',
                 region = 'undef', macroarea = 'undef', working_unit = 'undef'):
        
        self.name = str(name).upper() # the individual's name
        
        # checks whether a population with the same name already exists.
        # If not, create it. 
        if population is not None:
            popname = str(population).lower()
            poprecord = Population.get_by(popname = popname)
            if poprecord is None:
                poprecord = Population(popname=popname, region=region, 
                                                continent_macroarea=macroarea, 
                                                working_unit = working_unit) 
            self.population = poprecord
            
        if sex is not None:     
            sex = str(sex).lower()
            if sex in (1, '1', 'm', 'male',):   # does it include also u'm', u'1'?
                self.sex = u'm'
            elif sex in (2, '2', 'f', 'female'):
                self.sex = u'f'
            else:
                self.sex = u'u'
        else:
            self.sex = u'u'

        self.source_file = source_file
        
    def __repr__(self):
        if self.sex in ('m', 'u'):
            rep = "Mr. %s (%s)" % (self.name, self.population)
        else:
            rep = "Mrs. %s (%s)" % (self.name, self.population)
        return rep
    def __str__(self):
        return self.name
    def __add__(self, other):
        return str(self.name) + other 
    def __eq__(self, other):
        return self.name == str(other).upper()
    def __ne__(self, other):
        return self.name != str(other).upper()
   
    def genotypes(self, list_of_snps):
        """Given a list of snps, the their genotypes
        """
        if isinstance(list):
            pass
        pass
          
    def get_genotype(self, snp):
        """Given a snp id, get the genotype
        
        require 'snps' as input.
        snps can be:
        - a snp id string
        - a list of snp id strings
        - a SNP instance
        - a list of SNP instances

#        >>> snp1, snp2 = SNP.query().limit(2).all()
        >>> ind1 = Individual.query().first()
        >>> ind.get_genotypes('rs10009279')
        '1'
        
        >>> ind.get_genotypes(rs10009279, rs13125929)
        """
        genotype = ''
        if isinstance(snp, str):
            snp_h = SNP.get_by(id = snp)
            genotype = snp_h.genotypes[self.genotypes_index]
        if isinstance(snp, SNP):
            genotype = snp.genotypes[self.genotypes_index]
        return genotype

    @classmethod
    def get_by_continent(cls, continent):
        """
        get all individuals belonging to a population working unit

        >>> Individual.get_by_population('Europe')[0:5]
        [Mrs. HGDP01401 (adygei),
         Mrs. HGDP01388 (adygei),
         Mr. HGDP01383 (adygei),
         Mr. HGDP01403 (adygei),
         Mrs. HGDP01387 (adygei)]
        """
        inds = Individual.query.filter(Individual.population.has(continent_macroarea = str(continent.lower()))).all()
        return inds
 
    @classmethod
    def get_by_continent_code(cls, continent_code):
        """
        get all individuals belonging to a population working unit

        >>> Individual.get_by_population('Europe')[0:5]
        [Mrs. HGDP01401 (adygei),
         Mrs. HGDP01388 (adygei),
         Mr. HGDP01383 (adygei),
         Mr. HGDP01403 (adygei),
         Mrs. HGDP01387 (adygei)]
        """
        inds = Individual.query.filter(Individual.population.has(continent_code = str(continent_code.upper()))).all()
        return inds
 
    @classmethod
    def get_by_working_unit(cls, popname):
        """
        get all individuals belonging to a population working unit

        >>> Individual.get_by_population('colombian')
        [Mrs. HGDP00704 (colombian),
         Mrs. HGDP00706 (colombian),
         Mrs. HGDP00702 (colombian),
         Mr. HGDP00710 (colombian),
         Mrs. HGDP00970 (colombian),
         Mr. HGDP00703 (colombian),
         Mrs. HGDP00708 (colombian)]

        """
        inds = Individual.query.filter(Individual.population.has(working_unit = str(popname.lower()))).all()
        return inds
    
class Population(Entity):
    """ Table 'Population'
    
    Population supports a methods called 'get_by_or_init', which enable you 
    to create an object in case it doesn't exists already.
    >>> martians = Population('martians')
    
    # It is recommended to use the 'set' method to modify a population's 
    # attribute after it has already been created.
    >>> martians.set('continent_macroarea', 'mars')
    >>> martians.continent_macroarea
    'mars'
    
    # You can also modify a pop's attributes manually, but remenber to use 
    # lower case strings 
    >>> martians.continent_macroarea = 'Mars'    # will give you trouble
    ...                                          # because is not lowercase.
    
    """
    using_options(tablename = 'populations')
    
    individuals         = OneToMany('Individual')

    popname             = Field(String(50), unique=True, index=True)
    popcode             = Field(Integer, index=True)
#    alternate_popname   = Field(String(50)
    working_unit        = Field(String(50))
    region              = Field(String(50))
    continent_macroarea = Field(String(30), index=True)
    continent_code      = Field(String(8), index=True)
    # TODO: sort the input file by continent, working_unit, populations
    
#    version                 = Column(Integer, ForeignKey('versions.id'))
#    last_modified       = Field(DateTime, onupdate=datetime.now,
#                                default = datetime.now)
    source_file         = Field(String(80))
    
    def __init__(self, popname, popcode=0, working_unit='undef', 
                 region = 'undef', continent_macroarea='undef', 
                 continent_code = 'undef'):
        #TODO: add a set method
        self.popname = str(popname).lower()
        self.popcode = str(popcode).upper()
        self.working_unit = str(working_unit).lower()
        self.region = str(region.lower())
        self.continent_macroarea = str(continent_macroarea).lower()
        self.continent_code = str(continent_code).upper()
        
    def set(self, name, value):
        setattr(self, name, str(value).lower())        
        
    def __repr__(self):
        return self.popname
    
    def __str__(self):
        return str(self.popname)
    
    def __eq__(self, other):
        return str(self.popname) == str(other).lower()
    def __ne__(self, other):
        return str(self.popname) == str(other).lower()

class RefSeqGene(Entity):
    """ Table 'RefSeqGene'
    name, chrom, strand, txStart, txEnd, cdsStart, cdsEnd, exonCount, exonStarts, exonEnds, alternateName, cdsStartStat, cdsEndStat, exonFrames
    """
    using_options(tablename = 'refseqgenes')

    ncbi_transcript_id = Field(String(15))

    genomic_build = Field(String(20))

    chromosome = Field(String(10))
    strand = Field(Enum(('-', '+', None)))
    txStart = Field(Integer)
    txEnd = Field(Integer)
    cdsStart = Field(Integer)
    cdsEnd = Field(Integer)
    exonCount = Field(Integer)
    exonStarts = Field(Text)
    exonEnds = Field(Text)
    alternateName = Field(String(100))
    cdsStartStat = Field(Integer)
    cdsEndStat = Field(Integer)
    exonFrames = Field(Text)

    source_file = Field(String(50))

    def __init__(self, ncbi_id, chromosome, cdsStart, cdsEnd):
        self.ncbi_transcript_id = ncbi_id.upper()
        self.chromosome = chromosome.lower()
        self.cdsStart = int(cdsStart)
        self.cdsEnd = int(cdsEnd)


    
    
    
def _test():
    """ test the current module"""
    import doctest
    doctest.testmod()
    
if __name__ == '__main__':
    _test()

