#!/usr/bin/env python
"""
Creates a png schema of the database tables

Requires the python pydot module.

copied from http://www.sqlalchemy.org/trac/wiki/UsageRecipes/SchemaDisplay
"""

from sqlalchemy import MetaData
from recipes.sqlalchemy_schemadisplay import create_schema_graph, create_uml_graph
import config

# create schema graph
graph = create_schema_graph(metadata=MetaData(config.connection_line),
   show_datatypes=False, # The image would get nasty big if we'd show the datatypes
   show_indexes=False, # ditto for indexes
   rankdir='LR', # From left to right (instead of top to bottom)
   concentrate=False # Don't try to join the relation lines together
)
graph.write_png('../../docs/UML/dbschema.png') # write out the file

# UML graph
import schema 
from recipes.sqlalchemy_schemadisplay import create_uml_graph
from sqlalchemy.orm import class_mapper

# lets find all the mappers in our model
mappers = []
for cls in (getattr(schema, attr) for attr in dir(schema) if attr[0] != '_'):
    try:
        mappers.append(class_mapper(cls))
    except:
        pass

# pass them to the function and set some formatting options
graph = create_uml_graph(mappers,
    show_operations=False, # not necessary in this case
    show_multiplicity_one=True # some people like to see the ones, some don't
)
graph.write_png('../../docs/UML/UMLschema.png') # write out the file

