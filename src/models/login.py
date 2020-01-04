from flask_restplus import fields
from server.instance import server
from sqlalchemy import Sequence
db = server.db

login = server.api.model('Login', {
  'id': fields.Integer(description='(Auto-Generated) Primary Key.'),
  'user_id': fields.Integer(required=True, min_length=1, max_length=200, description='(Required) Foreign Key. Lookup for users table.  This is the UID as provided by GeoAxis.'),
  'time': fields.DateTime(description="(Optional) Time of login event. Defaults to current time.")
})

class Login(server.db.Model):
  __tablename__ = "logins"

  id = db.Column(db.Integer, Sequence('login_id_seq'), primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  time = db.Column(db.DateTime, nullable=False)
  # relationship def, more info @ https://docs.sqlalchemy.org/en/13/orm/tutorial.html
  user = db.relationship("User", back_populates="logins")


  def __repr__(self):
    return "<Login (user_id='%s', time='%s' )>" % (
      self.user_id, self.time)