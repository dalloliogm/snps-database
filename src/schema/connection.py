#!/usr/bin/env python
"""
Instantiate a connection to the database

From this module, you should import session
"""
from elixir import session, metadata, setup_all
from config import connection_line
from schema import *
from sqlalchemy.sql import func

metadata.bind = connection_line
#metadata.bind.echo = True
setup_all()

