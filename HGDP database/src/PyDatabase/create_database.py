#!/ create database schema and tables


from schema import *
Base.metadata.create_all(engine)