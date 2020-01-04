from server.instance import server
import datetime
# from models.book import *
from models import *

db = server.db
now = datetime.datetime.now()

# init user
seed_user = User(
  id=12345678,
  name="Donkey Kong",
  email="dk@island.com",
  creation=now
)
# add some login events for the new user
seed_logins = [
  Login(user_id=seed_user.id, time=now),
  Login(user_id=seed_user.id, time=now),
  Login(user_id=seed_user.id, time=now)
]

# put everything in db with some logging
def seed_db():
  # add user
  db.session.add(seed_user)
  server.logging.info('DB_CREATE: %s', str(seed_user))
  # add user logins
  for instance in seed_logins:
    db.session.add(instance)
    server.logging.info('DB_CREATE: %s', str(instance))

  db.session.commit()
  server.logging.info('DB_SCRIPT: -> \U0001f44d Done.')


if __name__ == '__main__':
  seed_db()