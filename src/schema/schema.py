#!/usr/bin/env python
# Create a database for HGDP data
"""
To use it, you should better use 'from connection import *' (see connection.py
script) to use the existing MySql database on my computer.

Refer to tutorial.txt for an introduction
"""

from elixir import Entity, Field, Unicode, Integer, UnicodeText, String, Text, Float, Boolean
from recipes.enum import Enum
from elixir import ManyToOne, OneToMany, OneToOne, ManyToMany, DateTime
from elixir import metadata, using_options
from elixir.ext.versioned import acts_as_versioned
from config import connection_line
from datetime import datetime
import logging
import operator


from pathway_table import Pathway
from stats_tables import Stats, Fst, iHS, XPEHH
from sqlalchemy import desc

class SNP(Entity):
    """ Table 'SNPs'.
    
    This class represents both the table SNP, and the structure of an instance of a SNP object
    
    >>> from debug_database import *
    >>> metadata.bind = 'sqlite:///:memory:'
    >>> setup_all(); create_all()
    >>> print metadata
    MetaData(Engine(sqlite:///:memory:))
    >>> rs1333 = SNP('rs1333')    # tests SNP.__init__
    >>> print rs1333              # tests SNP.__repr__
    SNP rs1333

    Let's add six genotypes. The first individual is homozygote for 'allele2', 

    >>> rs1333.add_genotype('200109')
    Traceback (most recent call last):
    ...
    NotImplementedError: Sorry, not implemented yet!
    >>> session.close()
    """
    using_options(tablename = 'snps')
    
    id                  = Field(String(30), primary_key=True, unique=True, index=True)
    chromosome          = Field(String(10), index=True)
    physical_position   = Field(Integer, index=True)
    genetic_position    = Field(Integer)
    original_strand     = Field(String(1))

#    next_snp            = ManyToOne('SNP')   # next SNP on the chromosome
#    previous_snp        = OneToOne('SNP')

    # allele1 can be only A or T. allele2 only C or G
    allele1             = Field(Enum(values=('A', 'T', '-')))
    allele2             = Field(Enum(values=('C', 'G', '-')))
    derived_allele      = Field(Enum(values=('A', 'C', 'T', 'G', '-')), default = '-')
    ancestral_allele    = Field(Enum(values=('A', 'C', 'T', 'G', '-')), default = '-',)
#    dbSNP_ref           = Field(String(10)) # TODO: check if necessary ()
    
    genotypes           = Field(Text(2000), default='')  
    haplotypes_index    = Field(Integer)
    
    annotations         = OneToOne('Annotations')
    stats               = OneToMany('Stats')

    # Pathways and genes
    genes               = ManyToMany('RefSeqTranscript')#, inverse='RefSeqTranscript.transcript_id') # ManyToOne w.b. better?
    pathways            = ManyToMany('Pathway')

    # versioning
    snp_build           = Field(String(80))
    genotypes_file      = Field(String(80)) # input file containing the genotypes
    genomic_build       = Field(String(80)) # build on ucsc

    def __init__(self, id, chromosome = '', genotypes = '', allele1='-', allele2='-',
                        physical_position = None):
        self.id = id
        self.chromosome = str(chromosome)
        self.genotypes = genotypes
        self.allele1 = allele1
        self.allele2 = allele2
        if physical_position is not None:
            self.physical_position = int(physical_position)
        self.annotations = Annotations()        

    def __repr__(self):
        # this method will be called when, in python code, you will do 'print SNP'.
        return 'SNP '  + self.id

    def get_dbSNP_url(self):
        """get the url to dbSNP"""
        type = self.id[0:2]     # should always be rs
        id = self.id[2:]
        url = "http://www.ncbi.nlm.nih.gov/SNP/snp_ref.cgi?type=%s&rs=%s" % (type, id)
        return url

    def get_transcripts(self, upstream = 0, downstream = 0):
        """Get transcripts in an interval of [upstream, downstream] from the snp position
        
        >>> from debug_database import *
        >>> metadata.bind = 'sqlite:///:memory:'
        >>> setup_all(); create_all()
        >>> print metadata
        MetaData(Engine(sqlite:///:memory:))
        >>> rs1333 = SNP('rs1333')
        >>> rs1333.chromosome = '11'
        >>> rs1333.physical_position = 900


        ### INCLUSION CRITERIAS ###
        Let's say we want to get all transcripts 100 upstream or downstream the position,
            so from 800 to 1000 on chromosome 11.

        >>> transcript1 = RefSeqTranscript('transcript1', 11, 700, 800)   # not included 
        >>> transcript2 = RefSeqTranscript('transcript2', 11, 700, 810)   # not included, it ends within the interval but it starts before
        >>> transcript3 = RefSeqTranscript('transcript3', 11, 800, 900)   # included
        >>> transcript4 = RefSeqTranscript('transcript4', 11, 900, 1000)  # included
        >>> transcript5 = RefSeqTranscript('transcript5', 11, 1000, 1100) # not included 

        >>> transcriptreverse = RefSeqTranscript('transcriptreverse', 11, 900, 800)   # included

        >>> transcripts = rs1333.get_transcripts(100, 100)
        >>> print [tr.transcript_id for tr in transcripts]
        ['TRANSCRIPT3', 'TRANSCRIPT4', 'TRANSCRIPTREVERSE']

        >>> session.close()
        """
        if not isinstance(upstream, int) and not isinstance(downstream, int):
            raise TypeError("SNP.get_transcripts requires two integers as input")
        
        if (self.chromosome is None) or (self.physical_position is None):
            raise ValueError('unknown coordinates for current snp')

        # get the proper interval where to find transcripts
        lower_limit = self.physical_position - upstream
        upper_limit = self.physical_position + downstream

        transcripts = RefSeqTranscript.query().filter_by(chromosome = self.chromosome).\
                                        filter(RefSeqTranscript.txStart >= lower_limit).\
                                        filter(RefSeqTranscript.txEnd <= upper_limit).all()
        return transcripts

    def get_position_from_transcript(self, transcript_id):
        """
        determine the position with respect to a transcript (in the coding region, #n upstream/downstream, etc)

        >>> from debug_database import *
        >>> metadata.bind = 'sqlite:///:memory:'
        >>> setup_all(); create_all()
        >>> print metadata
        MetaData(Engine(sqlite:///:memory:))
        >>> rs1333 = SNP('rs1333')
        >>> rs1333.chromosome = '11'
        >>> rs1333.physical_position = 900


        >>> transcript1 = RefSeqTranscript('transcript1', 11, 700, 800) # downstream
        >>> transcript2 = RefSeqTranscript('transcript2', 11, 800, 910) # within
        >>> transcript3 = RefSeqTranscript('transcript3', 11, 890, 930) # within
        >>> transcript4 = RefSeqTranscript('transcript4', 11, 910, 1000) # upstream
        
        >>> rs1333.get_position_from_transcript(transcript1)
        'downstream'
        >>> rs1333.get_position_from_transcript('transcript1')
        'downstream'
        >>> rs1333.get_position_from_transcript(transcript2)
        'inside_gene'
        >>> rs1333.get_position_from_transcript(transcript3)
        'inside_gene'
        >>> rs1333.get_position_from_transcript(transcript4)
        'upstream'

        """
        outputs = ['upstream', 'downstream', 'inside_gene', 'coding', 'intronic', 'other_chromosome']
        position = ''
        
        if isinstance(transcript_id, RefSeqTranscript):
            transcript = transcript_id
        elif isinstance(transcript_id, str):   # todo: check for __str__ method?
            transcript = RefSeqTranscript.get_by(alternateName = transcript_id.upper())
        else:
            transcript = None
        if transcript is None:
            raise ValueError('transcript %s not present in database' % transcript_id)

        snp_position = self.physical_position
        if transcript.chromosome != self.chromosome:
            position = 'other_chromosome'

        elif snp_position < transcript.txStart:
            position = 'upstream'
        elif transcript.txStart < snp_position < transcript.txEnd:
            position = 'inside_gene'
        elif snp_position > transcript.txEnd:
            position = 'downstream'

        return position

    def add_genotype(self, genotype):
        """add genotypes"""
        # check that 'genotype' only contains 0, 1, 2
        # update table
        raise NotImplementedError('Sorry, not implemented yet!')

    def get_genotype_by_individuals(self, individuals, format='n'):
        """Given a list of individuals, get its genotype

        individuals can be:
        - a single string (corresponding to an individual.id) or Individual object;
        - a list of strings or of Individual objects.

        format can be:
        - c -> character 
        - n -> numerical (0, 1, 2)

        >>> from connection import *
        >>> metadata.bind = 'mysql://guest:@localhost:3306/hgdp_test'
        >>> setup_all()

        >>> snp = SNP.get_by(id = 'rs13125929')
        >>> snp.get_genotype_by_individuals('HGDP00001')
        '0'

        >>> snp.get_genotype_by_individuals(individuals = ('HGDP00001', 'HGDP01419'), format = 'n')
        ('0', '0')
        
        >>> snp.get_genotype_by_individuals(individuals = ('HGDP00001', 'HGDP01419'), format = 'c')
        ('TT', 'TT')

        >>> session.close()
        """

        if isinstance(individuals, str) or isinstance(individuals, Individual):
            # TODO: may refactored by using recursion
            individuals = (individuals, )
        elif not (isinstance(individuals, list) or isinstance(individuals, tuple)):
            raise TypeError("individuals should be a list of string or Individual objects, or a single individual/string")

        ind_indexes = Individual.query.filter(Individual.name.in_(individuals)).from_self(Individual.genotypes_index).all()
        ind_indexes = [int(i[0]) for i in ind_indexes]
        
        if not ind_indexes:
            genotypes = ()
        else:
            if format == 'c':
                genotypes = tuple(map(self.get_genotype_char, ind_indexes))
            else:
                genotype_getter = operator.itemgetter(*ind_indexes)
                genotypes = genotype_getter(self.genotypes) # TODO: convert to a list for backward compatibility?
     
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


    def get_nearby_snps(self, upstream, downstream):
        """
        Get all snps in a window of (upstream, downstream) bases

        >>> from connection import *
        >>> metadata.bind = 'mysql://guest:@localhost:3306/hgdp_test'
        >>> setup_all()

        >>> snp = SNP.get_by(id = 'rs13125929')
        >>> print snp.get_nearby_snps(100000, 105000)[:7]
        [SNP rs4690284, SNP rs13114862, SNP rs11724335, SNP rs12509346, SNP rs10002444, SNP rs9884834, SNP rs2213704]
        """
        if not isinstance(upstream, int) and not isinstance(downstream, int):
            raise TypeError("SNP.get_nearby_snps requires two integers as input")

        lower_limit = self.physical_position - upstream
        upper_limit = self.physical_position + downstream

        snps = SNP.get_snps_by_region(self.chromosome, lower_limit, upper_limit).filter(SNP.id != self.id)
#        snps.pop(snps.index(self))
        return snps
    
    @classmethod
    def get_snps_by_region(cls, chromosome, lower_limit = 0, upper_limit = -1):
        """
        Get the snps within a region
        >>> from connection import *    # be careful - don't write anything to the db!
        >>> metadata.bind = 'mysql://guest:@localhost:3306/hgdp_test'
        >>> setup_all()
        >>> print SNP.get_snps_by_region('1', 1000000, 1050000).all()
        [SNP rs9442372, SNP rs3737728, SNP rs11260588, SNP rs9442398, SNP rs6687776, SNP rs9651273, SNP rs4970405, SNP rs12726255]

        note: if upper_limit == -1, get all the snps until the end of the chr.
        >>> SNP.get_snps_by_region('Y', -1, 13000000).all()
        [SNP rs2058276, SNP rs1865680]

        >>> session.close()
        """
        # note: doesn't work if self.physical_position is none.
        if upper_limit == -1:
            snps = SNP.query.filter(SNP.chromosome == str(chromosome).upper()).\
                filter(SNP.physical_position > lower_limit).\
                order_by(SNP.physical_position)#.all()
        else:
            snps = SNP.query.filter(SNP.chromosome == str(chromosome).upper()).\
                filter(SNP.physical_position > lower_limit).\
                filter(SNP.physical_position < upper_limit).\
                order_by(SNP.physical_position)#.all()

#        snps.sort(key=lambda x:int(x.physical_position))
        return snps

    def get_stats_by_continent(self):
        """
        >>> from connection import *    # be careful - don't write anything to the db!
        >>> metadata.bind = 'mysql://guest:@localhost:3306/hgdp_test'
        >>> setup_all()
        >>> snp = SNP.get_by(id = 'rs2887286')
        >>> snp.stats[0]
        stats on SNP SNP rs2887286 on ame: iHS 0.806953, daf 0.891
        """
        raise NotImplementedError('Sorry, not implemented yet')
    
    def all_ihs(self):
        """
        Get all stats in a list 
        automatically convert it to floats or keep them to None

        >>> from connection import *    # be careful - don't write anything to the db!
        >>> metadata.bind = 'mysql://guest:@localhost:3306/hgdp_test'
        >>> setup_all()
        >>> snp = SNP.get_by(id = 'rs2887286')

#        >>> print snp.all_ihs()

        >>> print "%1.2f " * 7 % tuple(snp.all_ihs())
        0.81 -1.49 0.08 -2.56 -1.94 0.47 -0.22 
        """
        stats = []
        for stat in sorted(self.stats, key=lambda x:x.population_key):
#            print stat
            if stat.iHS is not None:
#                print stat
                stats.append(float(stat.iHS))
            else:
                stats.append(None)
        return stats

    @classmethod
    def get_stats(self, snplist, stat, pops=None):
        """
        Get a statistical value related to the snp

        For the moment, it can only retrieve a stat at a time

        >>> from connection import *    # be careful - don't write anything to the db!
        >>> metadata.bind = 'mysql://guest:@localhost:3306/hgdp_test'
        >>> setup_all()
        >>> snp = SNP.get_by(id = 'rs2887286')

        >>> snp.get_stats(snp, 'XPEHH', ['ame', 'csasia'])
        """
        # Warning: this function makes use of eval
        # This function doesn't even try to validate user input

        if snplist is None:
            raise TypeError('select at least a snp')
        if isinstance(snplist, list) or isinstance(snplist, tuple):
            snplist_cleaned = []
            for snp in snplist:
                if isinstance(snp, SNP):
                    snplist_cleaned.append(snp.id)
                else:
                    snplist_cleaned.append(snp)
            snplist = snplist_cleaned
        else:   # assume snplist is a string or snp instance containing a single value
            if isinstance(snplist, SNP):
                snplist = (snplist.id, )
            else:
                snplist = (snplist.lower(), )

        if pops is None:
            # return all the populations
            pops = 'ame csasia easia eur mena oce ssafr'.split()
        if isinstance(pops, list) or isinstance(pops, tuple):
            pops = [p.lower() for p in pops]
        else:
            pops = (pops.lower(), )

#        if stats is None:
#            raise TypeError('select a stat')
#        elif isinstance(stats, list) or isinstance(stats, tuple):
#            stats = [s.upper() for s in stats]
#        else:
#            stats = (stats.upper(), )

        queryline = stat + ".query().filter(" + stat + ".snp_id.in_(" + str(snplist) + ")).from_self("
        for pop in pops:
            queryline += stat + '.' + pop + ', '

        queryline += ')'

        print queryline
        stat = eval(queryline).all()
        return stat



    def get_next_snp(self):
        """get the next SNP on the chromosome
        """
#        return SNP.get_by(id = self.next_snp)
        if self.physical_position is None:
            raise ValueError('position of the snp in the chromosome has not been uploaded yet')
        return SNP.query().filter_by(chromosome = self.chromosome).\
                filter(SNP.physical_position > self.physical_position).order_by(SNP.physical_position).first()
        
    def get_previous_snp(self):
        """get the previous SNP on the chromosome
        """
        if self.physical_position is None:
            raise ValueError('position of the snp in the chromosome has not been uploaded yet')
        return SNP.query().filter_by(chromosome = self.chromosome).\
                filter(SNP.physical_position > self.physical_position).order_by(SNP.physical_position).first()

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
    
    >>> from debug_database import *
    >>> metadata.bind = 'sqlite:///:memory:'
    >>> setup_all(); create_all()
    >>> print metadata
    MetaData(Engine(sqlite:///:memory:))
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
    
    >>> session.close()
    """
    using_options(tablename = 'individuals')
    
    name                = Field(String(30), unique=True, index=True)    # TODO: rename with 'id'?
    hgdp_individual_number = Field(String(10), unique = True)
    population          = ManyToOne('Population')   # TODO: how to index?
    sex                 = Field(Enum(('m', 'u', 'f', None)))
    
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
    
    def __init__(self, name, population = None, sex = 'u', source_file = '',
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
                self.sex = 'm'
            elif sex in (2, '2', 'f', 'female'):
                self.sex = 'f'
            else:
                self.sex = 'u'
        else:
            self.sex = 'u'

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
   
    def get_genotypes(self, list_of_snps, format = 'n'):
        """Given a list of snps, the their genotypes
        """
        genotypes = []
        if hasattr([], '__iter__') and not isinstance(list_of_snps, str):
            logging.debug("list_of_snps is a list")

            for snp in list_of_snps:
                if format == 'n':
                    genotypes.append(snp.genotypes[self.genotypes_index])
                else:
                    genotype = snp.get_genotype_char(self.genotypes_index)
                    genotypes.append(genotype)
        return genotypes
          
    def get_genotype(self, snp):
        """Given a snp id, get the genotype
        
        require 'snps' as input.
        snps can be:
        - a snp id string
        - a list of snp id strings
        - a SNP instance
        - a list of SNP instances

        >>> from connection import *
        >>> metadata.bind = 'mysql://guest:@localhost:3306/hgdp_test'
        >>> setup_all()

        >>> snp1, snp2 = SNP.query().limit(2).all()
        >>> ind1 = Individual.query().first()
        >>> ind1.get_genotype('rs10009279')
        '1'
        
        >>> ind1.get_genotypes((snp1, snp2))
        ['0', '0']

        >>> session.close()
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

        >>> from connection import *
        >>> metadata.bind = 'mysql://guest:@localhost:3306/hgdp_test'
        >>> setup_all()
        >>> Individual.get_by_continent('Europe')[0:5]
        [Mrs. HGDP01401 (adygei), Mrs. HGDP01388 (adygei), Mr. HGDP01383 (adygei), Mr. HGDP01403 (adygei), Mrs. HGDP01387 (adygei)]

        >>> session.close()
        """
        inds = Individual.query.filter(Individual.population.has(continent_macroarea = str(continent.lower()))).all()
        return inds
 
    @classmethod
    def get_by_continent_code(cls, continent_code):
        """
        get all individuals belonging to a population working unit

        >>> from connection import *
        >>> metadata.bind = 'mysql://guest:@localhost:3306/hgdp_test'
        >>> setup_all()
        >>> Individual.get_by_continent_code('EUR')[0:5]
        [Mrs. HGDP01401 (adygei), Mrs. HGDP01388 (adygei), Mr. HGDP01383 (adygei), Mr. HGDP01403 (adygei), Mrs. HGDP01387 (adygei)]

        >>> session.close()
        """
        inds = Individual.query.filter(Individual.population.has(continent_code = str(continent_code.upper()))).all()
        return inds
 
    @classmethod
    def get_by_working_unit(cls, popname):
        """
        get all individuals belonging to a population working unit

        >>> from connection import *
        >>> metadata.bind = 'mysql://guest:@localhost:3306/hgdp_test'
        >>> setup_all()
        >>> Individual.get_by_working_unit('colombian')
        [Mrs. HGDP00704 (colombian), Mrs. HGDP00706 (colombian), Mrs. HGDP00702 (colombian), Mr. HGDP00710 (colombian), Mrs. HGDP00970 (colombian), Mr. HGDP00703 (colombian), Mrs. HGDP00708 (colombian)]

        >>> session.close()
        """
        inds = Individual.query.filter(Individual.population.has(working_unit = str(popname.lower()))).all()
        return inds
    
class Annotations(Entity):
    using_options(tablename = 'annotations')
    snp = ManyToOne('SNP')
    centromeric = Field(Boolean)
#    gene = OneToMany('RefSeqTranscript')

class Population(Entity):
    """ Table 'Population'
    
    Population supports a methods called 'get_by_or_init', which enable you 
    to create an object in case it doesn't exists already.
    >>> from debug_database import *
    >>> metadata.bind = 'sqlite:///:memory:'
    >>> setup_all(); create_all()
    >>> print metadata
    MetaData(Engine(sqlite:///:memory:))
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

    >>> session.close()
    
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

    @classmethod
    def all_working_units(self):
        """ list all the working units in the table"""
        units = Population.query().from_self(Population.working_unit).group_by(Population.working_unit).all()
        return map(lambda x:x[0], units)

    @classmethod
    def all_continents(self):
        """ list all the continent codes in the table"""
        units = Population.query().from_self(Population.continent_code).group_by(Population.continent_code).all()
        return map(lambda x:x[0], units)

class RefSeqTranscript(Entity):
    """ Table 'RefSeqTranscript'
    name, chrom, strand, txStart, txEnd, cdsStart, cdsEnd, exonCount, exonStarts, exonEnds, alternateName, cdsStartStat, cdsEndStat, exonFrames
    """
    using_options(tablename = 'refseqtranscripts')

    transcript_id = Field(String(15), index=True)

    genomic_build = Field(String(20))

    chromosome = Field(String(10), index=True)
    strand = Field(Enum(('-', '+', None)))
    txStart = Field(Integer)
    txEnd = Field(Integer)
    txCenter = Field(Integer)
    cdsStart = Field(Integer)
    cdsEnd = Field(Integer)
    exonCount = Field(Integer)
    exonStarts = Field(Text)
    exonEnds = Field(Text)
    alternateName = Field(String(100), index=True)
    cdsStartStat = Field(Integer)
    cdsEndStat = Field(Integer)
    exonFrames = Field(Text)

    source_file = Field(String(100))

    def __init__(self, ncbi_id = '', chromosome = '', txStart = None, txEnd = None):
        self.transcript_id = ncbi_id.upper()
        self.chromosome = str(chromosome).lower()

        if txEnd is not None and txStart is not None:
            self.txStart = int(txStart)
            self.txEnd = int(txEnd)
            self.txCenter = (self.txEnd + self.txStart) / 2

    def __repr__(self):
        return "transcript %s on gene %s on chromosome %s (%s-%s)" % \
                    (self.transcript_id, self.alternateName, self.chromosome, self.txStart, self.txEnd)

    def length(self, feature = 't'):
        """Length of the trascript, from txStart to txEnd
        
        if feature == 't', return the transcript length (default)
        if feature == 'c', return the coding length
        """
        if feature.lower() in ('t', 'transcript', 'tr'):
            return self.txEnd - self.txStart
        elif feature.lower() in ('c', 'coding', 'co'):
            return self.cdsEnd - self.cdsStart
        else:
            raise TypeError('unknown value for parameter "feature"')

    def __len__(self):
        return self.txEnd - self.txStart
        
    def get_ensembl_ref(self):
        """get the url to ensembl (put this in RefSeqTranscript?)"""
        raise NotImplementedError

    @classmethod
    def get_by_geneids(cls, genes_list):
        """
        For every gene in list_genes, get the longest transcript
        Only the longest transcript is returned

        >>> from connection import *
        >>> metadata.bind = 'mysql://guest:@localhost:3306/hgdp_test'
        >>> setup_all()
                                 
        >>> transcripts = RefSeqTranscript.get_by_geneids(['ALG2', 'ALG11'])
        >>> print [transcript.transcript_id for transcript in transcripts]
        ['NM_001004127', 'NR_024532']

        >>> RefSeqTranscript.get_by_geneids('ALG2')
        [transcript NR_024532 on gene ALG2 on chromosome 9 (101018527-101024067)]
        """
        if isinstance(genes_list, str):
            genes_list = (genes_list, )     # this must be a list or a tuple
#            transcripts = RefSeqTranscript.query.filter(RefSeqTranscript.alternateName == genes_list).group_by(RefSeqTranscript.alternateName).all()

        transcripts = RefSeqTranscript.query.filter(RefSeqTranscript.alternateName.in_(genes_list)).\
            order_by(desc(RefSeqTranscript.txEnd - RefSeqTranscript.txStart)).\
            group_by(RefSeqTranscript.alternateName).all()
         
        return transcripts


    def get_snps(self, upstream = 0, downstream = 0, relative_to = 'tr'):
        """
        Get all the snps in an interval of (transcript.txstart - downstream, transcript.txEnd + upstream)

        >>> from debug_database import *
        >>> metadata.bind = 'sqlite:///:memory:'
        >>> setup_all(); create_all()
        >>> print metadata
        MetaData(Engine(sqlite:///:memory:))


        Example: get all the snps with upstream=300, downstream=300

        >>> transcript1 = RefSeqTranscript('transcript1', 11, 900, 1100) # txCenter: 1000

        >>> snp1 = SNP('snp1', chromosome = 11, physical_position = 500L)    # not included
        >>> snp2 = SNP('snp2', chromosome = 11, physical_position = 700L)    # not included
        >>> snp3 = SNP('snp3', chromosome = 11, physical_position = 800L)    # included
        >>> snp4 = SNP('snp4', chromosome = 11, physical_position = 1000L)   # included, inside tr
        >>> snp5 = SNP('snp5', chromosome = 11, physical_position = 1200L)   # included
        >>> snp6 = SNP('snp6', chromosome = 11, physical_position = 1300L)   # not included
        >>> snp7 = SNP('snp7', chromosome = 11, physical_position = 1600L)   # not included
        >>> snp8 = SNP('snp8', chromosome = 1, physical_position = 1000L)    # not included (other chromosome)
        >>> snp4b = SNP('snp4b', chromosome = 11, physical_position = 1100L) # included and after snp4

        >>> transcript1.get_snps(300, 300, 'tr').all()
        [SNP snp2, SNP snp3, SNP snp4, SNP snp4b, SNP snp5, SNP snp6]

        Get all snps within the transcript (use 'tr' parameter)
        >>> transcript1.get_snps(0, 0, 'tr').all()
        [SNP snp4]

        >>> session.close()
        """
        if not isinstance(upstream, int) and not isinstance(downstream, int):
            raise TypeError("SNP.get_transcripts requires two integers as input")
        
        if (self.chromosome is None):   # should check also for cdsStart, etc..
            raise ValueError('unknown coordinates for current snp')

        if relative_to in ('tr', 'tx', 'transcript'):

            lower_limit = self.txStart - upstream
            upper_limit = self.txEnd + downstream
#            logging.debug(str(lower_limit + upper_limit))
                    
        elif relative_to in ('center', 'txcenter'):
            lower_limit = self.txCenter - upstream
            upper_limit = self.txCenter + downstream

        else:
            raise ValueError('unknown value for parameter "relative_to"')

#        snps = SNP.query().order_by(SNP.physical_position).\
#                                filter_by(chromosome = self.chromosome).\
#                                filter(SNP.physical_position >= lower_limit).\
#                                filter(SNP.physical_position <= upper_limit)
        snps = SNP.get_snps_by_region(self.chromosome, lower_limit, upper_limit)
        return snps

    @classmethod
    def longest_transcript_by_gene(self, gene):
        """
        Given a gene name, return the longest transcript for it



        >>> from debug_database import *
        >>> metadata.bind = 'sqlite:///:memory:'
        >>> setup_all(); create_all()
        >>> print metadata
        MetaData(Engine(sqlite:///:memory:))


        Example: get all the snps with upstream=300, downstream=300

        >>> transcript1 = RefSeqTranscript('transcript1', 11, 900, 1100) # txCenter: 1000

        >>> snp1 = SNP('snp1', chromosome = 11, physical_position = 500L)    # not included
             
        """
        raise NotImplementedError

    
def _test():
    """ test the current module"""
#    from debug_database import *
    import doctest
    doctest.testmod()
    
if __name__ == '__main__':
    _test()

