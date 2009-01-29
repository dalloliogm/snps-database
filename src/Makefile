

upload_database: setup/create_database.py setup/insert_individuals.py setup/insert_genotypes.py
	@echo "Dropping the database and uploading data again"
	python setup/create_database.py 
	@echo "Inserting individuals which have Included_in_952 == 1 and Li == True in the database"
	python setup/insert_individuals.py
	@echo "Uploading genotypes"
	python setup/insert_genotypes.py

