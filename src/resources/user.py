from flask import Flask
from flask_restplus import Api, Resource, fields
from server.instance import server
from sqlalchemy import exc, update

from models.user import *
import datetime

# Capitalization is important here!
# User => db.Model
# user => api spec object
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

# This class handles GET and POST to /user
@api.route('/users')
class UserList(Resource):
  @api.marshal_list_with(user) # Tells api to return response formatted as a <User> List
  def get(self):
    try:
      users = db.session.query(User).order_by(User.id).all()
      for instance in users:
        server.logging.info('DB_FIND: %s', str(instance))
      return users
    except exc.SQLAlchemyError as exception: # default SQLAlchemy error caught
      return  api.abort(500, str(exception))

  # Ask flask_restplus to validate the incoming payload
  @api.expect(user, validate=True)
  @api.marshal_with(user, code=200, description='User created.') # Tells api to return response formatted as a <User>
  def post(self):
    try:
      new_user = User(
        id=api.payload['id'],
        name=api.payload['name'],
        email=api.payload['email'],
        creation=(lambda: now, lambda: api.payload["creation"])['creation' in api.payload]()  # lambda ternary statement, ensures key lookup only occurs if key exists in dict
      )
      db.session.add(new_user)
      db.session.commit()
      server.logging.info('DB_CREATE: %s', str(new_user))
      return new_user
    except exc.SQLAlchemyError as exception:
      return  api.abort(500, str(exception))

# Handles GET, PUT, and PATCH to /user/:id
# The path parameter will be supplied as a parameter to every method
# All these routes return a single User Obj or error message
@api.route('/user/<int:id>')
@api.param('id', 'User UID. This is provided by GeoAXIS.')
class UserLookup(Resource):
  # Utility method
  def find_user(self, id):
    try:
      match = db.session.query(User).get(id)
      server.logging.info('DB_FIND: %s', str(match))
      return match if match != None else api.abort(404, "Could not find user with provided UID")
    except exc.SQLAlchemyError as exception:
      return  api.abort(500, str(exception))

  @api.marshal_with(user)
  def get(self, id):
    return self.find_user(id=id)

  @api.marshal_with(user, code=200, description='User deleted.')
  def delete(self, id):
    try:
      match = self.find_user(id=id)
      db.session.delete(match)
      db.session.commit()
      server.logging.info('DB_DELETE: %s', str(match))
      return match
    except exc.SQLAlchemyError as exception:
      return  api.abort(500, str(exception))

  @api.expect(user, validate=True)
  @api.marshal_with(user, code=200, description='User updated.')
  def put(self, id):
    try:
      put_user = User(
        id=id,
        name=api.payload['name'],
        email=api.payload['email'],
        creation=(lambda: now, lambda: api.payload["creation"])['creation' in api.payload]()  # lambda ternary statement, ensures key lookup only occurs if key exists in dict
      )
      match = db.session.query(User).get(id)
      if match != None:
        db.session.delete(match)
        server.logging.info('DB_DELETE: %s', str(match))
      db.session.add(put_user)
      server.logging.info('DB_CREATE: %s', str(put_user))
      db.session.commit()
      return put_user
    except exc.SQLAlchemyError as exception:
      return  api.abort(500, str(exception))
  
  @api.expect(user)
  @api.marshal_with(user, code=200, description='User updated.')
  def patch(self, id):
    try:
      match = self.find_user(id=id)
      server.logging.info('DB_FIND: %s', str(match))
      # verify fields in payload before attempting to replace db entry fields
      match.name = (lambda: match.name, lambda: api.payload["name"])["name" in api.payload]()
      match.email = (lambda: match.email, lambda: api.payload["email"])["email" in api.payload]()
      match.creation = (lambda: match.creation, lambda: api.payload["creation"])["creation" in api.payload]()
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

