from connection import *
from elixir import cleanup_all, drop_all

metadata.bind.echo = True
Population.query().all()
session.commit()
session.delete()

cleanup_all()
drop_all()