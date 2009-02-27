"""
Read the iHS all continent file and upload stats
"""

from HGDPIO import parsers

def upload_iHS_stats(iHS_filehandle, session, metadata):
    """
    upload individuals from the rosenberg files.
    """
    parsers.iHS_all_parser(iHS_filehandle, session, metadata)
#    session.add_all(individuals)

    print 'upload of iHS Stats by continent to database %s completed' % metadata

if __name__ == '__main__':

    from schema.connection import *

    from ConfigParser import SafeConfigParser
    c = SafeConfigParser()
    c.read('config.txt')
    iHS_all_filename = c.get('Data files', 'iHS_by_cont') + '/940LiUnrel-ihsContinent-all.tab'
    handle = open(iHS_all_filename, 'r')
    metadata.bind.echo = True

    upload_iHS_stats(handle, session, metadata)

