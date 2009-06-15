#!/Usr/bin/env python


from schema.schema import *
from elixir import setup_all, create_all, session
from schema.config import connection_line

metadata.bind = connection_line
metadata.bind.echo = True

def create_new_database():
    # Read schema and create entities
    setup_all()
    
    # Drop all the existing database. Warning!!
    choice = raw_input('drop all existing data? [y/N]')
    if choice in ('y', 'Y', 'yes', 'Yes', '1'):
        metadata.drop_all()
    
    # Issue the commands to the local database
    create_all()
    
if __name__ == '__main__':
    create_new_database()
