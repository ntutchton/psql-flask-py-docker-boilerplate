from flask_restplus import fields
from server.instance import server
from sqlalchemy.orm import relationship
from models.login import *
db = server.db

user = server.api.model('User', {
  'id': fields.Integer(required=True, description='(Required) Primary Key. This is the user UID provided by GeoAXIS.'),
  'name': fields.String(required=True, min_length=1, max_length=200, description='(Required) Name'),
  'email': fields.String(required=True, min_length=1, max_length=200, description='(Required) Email'),
  'creation': fields.DateTime(description="(Optional) Time of self service account creation. Defaults to current time.")
})

class User(server.db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True) # This is user's UID
  name = db.Column(db.String(200))
  email = db.Column(db.String(200))
  creation = db.Column(db.DateTime)
  # table relationship def, more info @ https://docs.sqlalchemy.org/en/13/orm/tutorial.html
  logins = relationship(
    'Login', 
    order_by=Login.id, 
    back_populates='user', 
    cascade='all, delete, delete-orphan')

  def __repr__(self):
    return "<User (id='%s', name='%s', email='%s')>" % (
      self.id, self.name, self.email)