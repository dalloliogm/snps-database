#!/usr/bin/env python
# Create a database for HGDP data
"""
This is the schema for a database designed to handle HGDP SNPs data.
To use it, you should better use 'from connection import *' (see connection.py
script) to use the existing MySql database on my computer.

Uses Elixir syntax instead of sqlalchemy
- http://elixir.ematia.de/

To make this example working on your system, you will need:
- sqllite
- sqllite bindings for python
- sqlalchemy (best if installed with easy_install. version 0.5)
- elixir plugin for sqlalchemy
On an Ubuntu installation, you will do:
$: sudo apt-get install python-setuptools sqlite python-sqlite2
$: sudo easy_install sqlalchemy Elixir

>>> from elixir import *
>>> metadata.bind = 'sqlite:///:memory:'

#>>> metadata.bind.echo = True

# Create SQLAlchemy Tables along with their mapper objects
>>> setup_all()

# Issue the SQL command to create the Tables
>>> create_all()


Here they are some examples on how to create some individuals 
objects and define their populations.
# Let's create a population:        # TODO: use best examples
>>> pop1 = Population('greeks')

# You can define an individual' population by 
# defining its population field
>>> ind1 = Individual('Archimede')
>>> ind1.population = pop1

# You can also do it by appending an individual to pop.individuals
>>> ind2 = Individual('Spartacus')
>>> pop1.individuals.append(ind2)

# You can also define population and individuals at the same time  
>>> ind3 = Individual('Democritus', population = 'greeks')
>>> ind4 = Individual('ET', population = 'aliens')

>>> pop1.individuals
[Mr. ARCHIMEDE (greeks), Mr. SPARTACUS (greeks), Mr. DEMOCRITUS (greeks)]

>>> session.commit()
>>> Population.query().all()
[greeks, aliens]
>>> print Population.get_by(popname = 'aliens').individuals
[Mr. ET (aliens)]
"""

from elixir import Entity, Field, Unicode, Integer, UnicodeText, String, Text
from recipes.enum import Enum
from elixir import ManyToOne, OneToMany, OneToOne, ManyToMany, DateTime
from elixir import metadata, using_options
from elixir.ext.versioned import acts_as_versioned
from config import connection_line
from datetime import datetime

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
    allele1             = Field(Enum(values=(u'A', u'T', u'-')))
    allele2             = Field(Enum(values=(u'C', u'G', u'-')))
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

    def __init__(self, id, chromosome = '', genotypes = '', allele1=u'-', allele2=u'-'):
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
        pass

    def get_ensembl_ref(self):
        """get the url to ensembl (put this in RefSeqGene?)"""
        pass

    def add_genotype(self, genotype):
        """add genotypes"""
        # check that 'genotype' only contains 0, 1, 2
        # update table
        pass

    def get_genes(self, upstream, downstream):
        """Get genes in an interval of [upstream, downstream] from the snp position
        
        >>> rs1333.get_genes(100, 100)
        -> all genes 100 upstream or downstream the position
        """
        pass

    def get_genotype_by_individuals(self, individuals, format='c'):
        """Given a list of individuals, get its genotype

        format can be:
        - c -> character 
        - n -> numerical (0, 1, 2)
        """
        pass

#    def get_genotype_by_region(self, region, format='c'): # TODO: needed?
#        """Given a chromosomal region, get its genotype
#
#        format can be:
#        - c -> character 
#        - n -> numerical (0, 1, 2)
#        """
#        pass
    
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
    
    def get_genotype(self, snp):
        """Given a snp id, get the genotype
        """
        pass
    
    
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

    chromosome = Field(String(3))
    strand = Field(Enum(('-', '+', None)))
    txStart = Field(Integer)
    txEnd = Field(Integer)
    cdsStart = Field(Integer)
    cdsEnd = Field(Integer)
    exonCount = Field(Integer)
    exonStarts = Field(Text)
    exonEnds = Field(Text)
    alternateName = Field(String(100))
    cdsStart = Field(Integer)
    cdsEnd = Field(Integer)
    exonFrames = Field(Text)

    source_file = Field(String(50))
    
    
    
def _test():
    """ test the current module"""
    import doctest
    doctest.testmod()
    
if __name__ == '__main__':
    _test()
    # could launch test_insert_data here?
#    from elixir import setup_all, create_all, session
