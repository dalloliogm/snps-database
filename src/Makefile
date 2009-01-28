

upload_database: schema/create_database.py scripts/insert_individuals.py scripts/insert_genotypes.py
	@echo "Dropping the database and uploading data again"
	python setup/create_database.py 
	python setup/insert_individuals.py
	python setup/insert_genotypes.py

