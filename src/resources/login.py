from flask import Flask
from flask_restplus import Api, Resource, fields
from server.instance import server
from sqlalchemy import exc, update

from models.login import *
import datetime

# Capitalization is important here!
# Login => db.Model
# login => api spec object
now = datetime.datetime.now()
app, api = server.app, server.api
db = server.db

'''
  _____  ______  _____ _______   _____   ____  _    _ _______ ______  _____ 
 |  __ \|  ____|/ ____|__   __| |  __ \ / __ \| |  | |__   __|  ____|/ ____|
 | |__) | |__  | (___    | |    | |__) | |  | | |  | |  | |  | |__  | (___  
 |  _  /|  __|  \___ \   | |    |  _  /| |  | | |  | |  | |  |  __|  \___ \ 
 | | \ \| |____ ____) |  | |    | | \ \| |__| | |__| |  | |  | |____ ____) |
 |_|  \_\______|_____/   |_|    |_|  \_\\____/ \____/   |_|  |______|_____/ 
  
'''

# handles get and post requests
@api.route('/logins')
class LoginList(Resource):
  @api.marshal_list_with(login)
  def get(self):
    try:
      logins = db.session.query(Login).order_by(Login.id).all()
      for instance in logins:
        server.logging.info('DB_FIND: %s', str(instance))
      return logins
    except exc.SQLAlchemyError as exception: # default SQLAlchemy error caught
      return  api.abort(500, str(exception))
  
  @api.expect(login, validate=True)
  @api.marshal_with(login, code=200, description="Login event created.")
  def post(self):
    try:
      new_login = Login(
        user_id=api.payload["user_id"],
        time= (lambda: now, lambda: api.payload["time"])['time' in api.payload]() # lambda ternary statement, ensures key lookup only occurs if key exists in dict 
      )
      db.session.add(new_login)
      db.session.commit()
      server.logging.info('DB_CREATE: %s', str(new_login))
      return new_login
    except exc.SQLAlchemyError as exception:
      return  api.abort(500, str(exception))

@api.route('/login/<int:id>')
@api.param('id', 'The login id. (NOT user UID).')
class LoginLookup(Resource):
  # Utility methods
  def find_login(self, id):
    try:
      match = db.session.query(Login).get(id)
      server.logging.info('DB_FIND: %s', str(match))
      return match if match != None else api.abort(404, "Could not find login with provided id.")
    except exc.SQLAlchemyError as exception:
      return  api.abort(500, str(exception))

  @api.marshal_with(login)
  def get(self, id):
    return self.find_login(id=id)

  @api.marshal_with(login, code=200, description="Login event deleted.")
  def delete(self, id):
    try:
      match = self.find_login(id=id)
      db.session.delete(match)
      db.session.commit()
      server.logging.info('DB_DELETE: %s', str(match))
      return match
    except exc.SQLAlchemyError as exception:
      return  api.abort(500, str(exception))    
  
  @api.expect(login, validate=True)
  @api.marshal_with(login, code=200, description="Login event updated.")
  def put(self, id):
    try:
      put_login = Login(
        id=id,
        user_id=api.payload["user_id"],
        time= (lambda: now, lambda: api.payload["time"])['time' in api.payload]() # lambda ternary statement, ensures key lookup only occurs if key exists in dict 
      )
      match = db.session.query(Login).get(id)
      if match != None:
        db.session.delete(match)
        server.logging.info('DB_DELETE: %s', str(match))
      db.session.add(put_login)
      server.logging.info('DB_CREATE: %s', str(put_login))
      db.session.commit()
      return put_login
    except exc.SQLAlchemyError as exception:
      return  api.abort(500, str(exception))   

  @api.expect(login)
  @api.marshal_with(login, code=200, description="Login event updated.")
  def patch(self, id):
    try:
      match = self.find_login(id=id)
      server.logging.info('DB_FIND: %s', str(match))
      # verify fields in payload before attempting to replace db entry fields
      match.user_id = (lambda: match.user_id, lambda: api.payload["user_id"])["user_id" in api.payload]()
      match.time = (lambda: match.time, lambda: api.payload["time"])["time" in api.payload]()
      server.logging.info('DB_UPDATE: %s', str(match))
      db.session.commit()
      return match
    except exc.SQLAlchemyError as exception:
      return  api.abort(500, str(exception))   



'''
   _____ _    _  _____ _______ ____  __  __    _____   ____  _    _ _______ ______  _____ 
  / ____| |  | |/ ____|__   __/ __ \|  \/  |  |  __ \ / __ \| |  | |__   __|  ____|/ ____|
 | |    | |  | | (___    | | | |  | | \  / |  | |__) | |  | | |  | |  | |  | |__  | (___  
 | |    | |  | |\___ \   | | | |  | | |\/| |  |  _  /| |  | | |  | |  | |  |  __|  \___ \ 
 | |____| |__| |____) |  | | | |__| | |  | |  | | \ \| |__| | |__| |  | |  | |____ ____) |
  \_____|\____/|_____/   |_|  \____/|_|  |_|  |_|  \_\\____/ \____/   |_|  |______|_____/ 

'''



@api.route('/user/<int:id>/logins')
@api.param('id', 'User UID. This is provided by GeoAXIS.')
class UserLogins(Resource):
  @api.marshal_list_with(login)
  def get(self, id):
    try:
      logins = db.session.query(Login).filter_by(user_id=id).all()
      if len(logins) == 0:
        api.abort(404, 'No Login events have been registered for the provided UID.')
      for instance in logins:
        server.logging.info('DB_FIND: %s', str(instance))
      return logins
    except exc.SQLAlchemyError as exception: 
      return  api.abort(500, str(exception))
