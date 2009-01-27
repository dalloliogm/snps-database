

upload_database: schema/create_database.py scripts/insert_individuals.py scripts/insert_genotypes.py
	@echo "Dropping the database and uploading data again"
	python schema/create_database.py 
	python scripts/insert_individuals.py
	python scripts/insert_genotypes.py

