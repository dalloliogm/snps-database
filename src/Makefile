test_all: test_hgdpio test_schema

test_schema:
	(cd schema; nosetests --with-profile --profile-stats-file=../profiles/schema.prof)
	python -c "import hotshot.stats ; stats = hotshot.stats.load('./profiles/schema.prof') ; stats.sort_stats('time', 'calls') ; stats.print_stats(200)"

test_hgdpio:
	(cd HGDPIO; nosetests --with-profile --profile-stats-file=../profiles/HGDPIO.prof)
	python -c "import hotshot.stats ; stats = hotshot.stats.load('./profiles/HGDPIO.prof') ; stats.sort_stats('time', 'calls') ; stats.print_stats(200)"

upload_database: setup/create_database.py setup/insert_individuals.py setup/insert_genotypes.py
	@echo "Dropping the database and uploading data again"
	python setup/create_database.py 
	
	@echo "Inserting individuals which have Included_in_952 == 1 and Li == True in the database"
	python setup/insert_individuals.py
	
	@echo "Uploading genotypes"
	python setup/insert_genotypes.py

	@echo "Updating map (chromosome and position) information for snps"
	python setup/insert_mapinfos.py

