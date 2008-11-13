#!/usr/bin/env python

import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# create database connection. 
#connection_line = "%s://%s:%s@%s:%s/%s" % (config.DBMS, config.db_user, config.db_password, config.db_host, config.db_port, config.db_name)
engine = create_engine(config.connection_line, echo=False)
engine.connect()

# I will use declaration mapping in this code. This means that both the tables and the instances of every row will be defined at the same time.
# see 'object mapping' on sqlalchemy manual.
# see also http://www.sqlalchemy.org/docs/05/ormtutorial.html#datamapping_declarative
Base = declarative_base()