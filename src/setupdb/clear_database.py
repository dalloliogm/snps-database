from connection import *
from elixir import cleanup_all, drop_all

print metadata
metadata.bind.echo = True

def delete_all(records):
    print [record.delete() for record in records]
    


delete_all(Population.query().all())
delete_all(Individual.query().all())
delete_all(SNP.query().all())

        
cleanup_all()
#metadata.drop_all()