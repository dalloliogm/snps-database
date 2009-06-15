#!/usr/bin/env perl

import ConfigParser
import os
import logging

#if os.path.exists('../config.txt'):
#    configfile = '../config.txt'

if os.path.exists('config.txt'):
    logging.debug('using customized config file')
    configfile = 'config.txt'
else:
    logging.debug('using default config file with guest privilegies')
    configfile = '/home/gioby/workspace/HGDP_database/src/config_guest.txt'

config = ConfigParser.RawConfigParser()
config.read(configfile)


DBMS = config.get('Database configuration', 'DBMS')
db_name = config.get('Database configuration', 'db_name')
host = config.get('Database configuration', 'host')
port = config.get('Database configuration', 'port')
user = config.get('Database configuration', 'user')
password = config.get('Database configuration', 'password')

connection_line = "%s://%s:%s@%s:%s/%s" % (DBMS, user, password, host, port, db_name)
