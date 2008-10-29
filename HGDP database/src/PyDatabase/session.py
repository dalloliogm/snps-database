
from sqlalchemy.orm import sessionmaker

# create a configured "Session" class
sessionmaker(bind=engine)

# create a Session
session = Session()
