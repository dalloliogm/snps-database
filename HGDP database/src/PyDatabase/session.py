from connection import engine
from sqlalchemy.orm import create_session

# create a Session
session = create_session(bind=engine, autocommit=True, autoflush=False)
