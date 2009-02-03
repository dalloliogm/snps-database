database to handle SNPs data.

To setup the database, edit src/config.txt, and then execute 'make upload_database' from the src dir.

To work with the database, you should move to the src directory, open a python shell, and then import * from schema.connection:

$: cd src
$: ipython
>>> from schema.connection import *

Then you will have imported the metadata objects Individual, SNP, etc.. and everything needed to work with the database.
Refer to elixir tutorial for the syntax and an introduction:
- http://elixir.ematia.de/trac/wiki/TutorialDivingIn

Testing: to test the various script, move to the corresponding directories (src/HGDPIO, src/schema) and then use nosetests.

