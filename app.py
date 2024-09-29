from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/flask_blog_site'
  app.config['JWT_SECRET_KEY'] = 'FLASK_APP_KEY'

  db.init_app(app)
  from routes import register_app
  register_app(app)
  migrate = Migrate(app, db)

  return app