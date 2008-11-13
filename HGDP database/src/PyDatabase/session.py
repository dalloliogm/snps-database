from connection import engine
from sqlalchemy.orm import sessionmaker

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()
