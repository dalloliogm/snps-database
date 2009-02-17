#!/usr/bin/env python
"""
Instantiate a connection to the database

From this module, you should import session
"""
from elixir import session, metadata, setup_all, create_all, drop_all
from config import connection_line
from schema import *

metadata.bind = 'sqlite:///:memory:'
print 'using test database %s ' % metadata.bind
#metadata.bind.echo = True
setup_all()
create_all()

