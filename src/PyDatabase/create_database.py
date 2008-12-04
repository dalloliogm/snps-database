#!/Usr/bin/env python


from schema import *
from elixir import setup_all, create_all, session
from config import connection_line

metadata.bind = connection_line
metadata.bind.echo = True

setup_all()

# Issue the commands to the local database
create_all()