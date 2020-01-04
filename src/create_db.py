# TO RUN LOCALLY: docker-compose exec api python src/create_db.py
from server.instance import server
db = server.db

# import models
from models import *

def create_db():
  db.drop_all()
  server.logging.info('DB_DROP_ALL_TABLES: -> Dropped.')
  db.create_all()
  server.logging.info('DB_CREATE_ALL_TABLES: -> Created.')
  db.session.commit()
  server.logging.info('DB_SCRIPT: -> \U0001f44d Done.')

if __name__ == '__main__':
  create_db()