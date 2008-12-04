#!/usr/bin/env python
"""
>>> from connection import session 
>>> from elixir import metadata, setup_all, create_all
>>> from schema import Individual, Population, SNP, RefSeqGene
>>> metadata.bind = 'sqlite:///:memory:'
>>> setup_all()
>>> create_all()

>>> me = Individual('Giovanni')
>>> hannibal = Individual('Annibal')

# create populations
>>> italians = Population('Italians')
>>> cartaginians = Population('Cartaginians')    # would be better to use more hgdp-related examples

>>> me.population = italians
>>> hannibal.population = cartaginians 

 

>>> session.commit()
>>> session.clear()

"""


if __name__ == '__main__':
    import doctest
    doctest.testmod()