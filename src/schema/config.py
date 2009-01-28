#!/usr/bin/env perl

import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('../config.txt')


DBMS = config.get('Database configuration', 'DBMS')
db_name = config.get('Database configuration', 'db_name')
host = config.get('Database configuration', 'host')
port = config.get('Database configuration', 'port')
user = config.get('Database configuration', 'user')
password = config.get('Database configuration', 'password')

connection_line = "%s://%s@%s:%s/%s" % (DBMS, user, host, port, db_name)
