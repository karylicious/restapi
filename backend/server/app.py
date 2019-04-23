from flask import Flask  
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os
from testclient import TestClient
from testclientserver import TestClientServer
from gradeclient import GradeClient
from gradeclientserver import GradeClientServer

from userzipfile import UserZipFile
from tutorial import Tutorial
from lesson import Lesson
from exercise import Exercise
from exercisequestion import ExerciseQuestion
from user import User
from session import Session

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rzcnjathadjwui:3eab08850b0bb6f2b139cd9febc71aee3b9e17cff7a3ebda3da0c805d71ed0e6@ec2-174-129-208-118.compute-1.amazonaws.com:5432/d6bv138l59bvfm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Order matters: Flask-SQLAlchemy must be initialized before Flask-Marshmallow.
db = SQLAlchemy(app)

# marshmallow is a serialization/deserialization library
marshmallow = Marshmallow(app)

# The following line is just a workround for the error: cross-origin read blocking (corb) 
# blocked cross-origin response with mime type application/json
CORS(app)

#Creation of REST API 
api = Api(app)

# Resource Routing
api.add_resource(UserZipFile, '/zipfile')
api.add_resource(TestClient, '/testclient')
api.add_resource(TestClientServer, '/testclientserver')
api.add_resource(GradeClient, '/gradeclient')
api.add_resource(GradeClientServer, '/gradeclientserver')
api.add_resource(Tutorial, '/tutorial')
api.add_resource(Lesson, '/lesson')
api.add_resource(Exercise, '/exercise')
api.add_resource(ExerciseQuestion, '/exercisequestion')
api.add_resource(User, '/user')
api.add_resource(Session, '/session')

if __name__ == '__main__':
    app.run(debug=True)