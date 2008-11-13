#!/ create database schema and tables


from schema import Base, engine
Base.metadata.create_all(engine)