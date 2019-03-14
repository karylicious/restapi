#from flask import Flask
from app import marshmallow
#import os
#from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow

#ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(ROOT_DIR, 'db.sqlite')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)
#marshmallow = Marshmallow(app)

class TutorialSchema(marshmallow.Schema):
    class Meta:
        fields = ('name', 'level')