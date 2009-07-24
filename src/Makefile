CHROMOSOMES = 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 X XY Y
AUTOSOMAL_CHROMOSOMES = 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22

connect:
	ipython -i -c 'from schema.connection import *'

clean_pyc:
	@echo 'removing all .pyc files'
	find . -iname '*.pyc' -delete

test_all: test_hgdpio test_schema test_known_values

test_known_values:
	-nosetests test/test_knowvalues.py

test_schema:
	-(cd schema; nosetests --with-doctest -v)
#	- python -c "import hotshot.stats ; stats = hotshot.stats.load('./profiles/schema.prof') ; stats.sort_stats('time', 'calls') ; stats.print_stats(200)"
test_hgdpio:
	-(cd HGDPIO; nosetests --with-profile --profile-stats-file=../profiles/HGDPIO.prof)
	-python -c "import hotshot.stats ; stats = hotshot.stats.load('./profiles/HGDPIO.prof') ; stats.sort_stats('time', 'calls') ; stats.print_stats(200)"

upload_database: setupdb/create_database.py setupdb/insert_individuals.py setupdb/insert_genotypes.py
	@echo "Dropping the database and uploading data again"
	python setupdb/create_database.py 
	
	@echo "Inserting individuals which have Included_in_952 == 1 and Li == True in the database"
	python setupdb/insert_individuals.py
	python setupdb/fix_papuan.py
	
	@echo "Uploading genotypes"
	python setupdb/insert_genotypes.py

	@echo "Updating map (chromosome and position) information for snps"
	python setupdb/insert_mapinfos.py
	
	@make upload_transcripts

upload_transcripts:
	python setupdb/setup_refseqtranscripts.py
	python setupdb/insert_refseqtranscripts.py
	python setupdb/fix_transcripts.py

#upload_stats:
#	python setupdb/setup_statstable.py
#	python setupdb/insert_iHS_all.py

upload_iHS:
	python setupdb/insert_iHS_all.py

##### XPEHH
upload_xpehh: setup_xpehh $(addprefix upload__xpehh_, $(AUTOSOMAL_CHROMOSOMES)) xpehh_by_snp_table 
setup_xpehh:
	python setupdb/setup_XPEHH.py
upload__xpehh_%:
	python setupdb/insert_XPEHH.py $*
xpehh_by_snp_table:
	-echo "SELECT snp_id, s.chromosome, s.physical_position, ame, ame_p, csasia, csasia_p, easia, easia_p, eur, eur_p, mena, mena_p, oce, oce_p, ssafr, ssafr_p INTO OUTFILE '/home/gioby/Data/HGDP/Results/XPEHH/Rsb_7continents_Pvalue_22chromosomes/xpehh_by_snp.csv' FIELDS TERMINATED BY '\t' FROM xpehh x join snps s on x.snp_id = s.id" | mysql hgdp_test -u guest




######
upload_centrosome_annotations_%: 
	python setupdb/centrosomic.py $*
upload_all_centromosomes: $(addprefix upload_centrosome_annotations_, $(CHROMOSOMES))

