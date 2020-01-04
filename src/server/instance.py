import os
from collections import ChainMap
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api, Resource, fields
from environment.instance import environment_config
import logging
logging.basicConfig(level=logging.DEBUG)

class Server(object):
  def __init__(self):
    self.app = Flask(__name__)
    self.api = Api(self.app, 
      version='1.0', 
      title='Selfservice Metrics API',
      description='Metrics API', 
      doc = environment_config["swagger-url"]
    )
    self.logging = logging
    self.app.config.from_object("config.Config")
    self.db = SQLAlchemy(self.app)

  def run(self):
    print("Serving API on port {port} in {mode} mode...".format(
      port=environment_config["port"],
      mode=os.environ.get("PYTHON_ENV")))

    self.app.run(
      host = '0.0.0.0', #FOR DOCKER/Localhost port mapping
      debug = environment_config["debug"], 
      port = environment_config["port"]
    )

server = Server()