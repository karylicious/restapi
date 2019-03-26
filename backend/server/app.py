from flask import Flask#, jsonify, request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os
from upload import Upload
from client import TestClient
from server import TestServer
from clientserver import TestClientServer
from directory import Directory
#from tutorialmodel import Tutorial
#from tutorialshema import TutorialSchema
from tutorial import TutorialManagement
from exercise import ExerciseManagement
from exercisequestion import ExerciseQuestionManagement

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(ROOT_DIR, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
marshmallow = Marshmallow(app)

CORS(app)
api = Api(app)


# Init shema
#tutorial_schema = TutorialSchema(strict=True)
#tutorials_shema = TutorialSchema(many=True, strict=True)

db.create_all()




api.add_resource(Upload, '/uploadfile')
api.add_resource(Directory, '/deletedir')
api.add_resource(TestClient, '/testclient')
api.add_resource(TestServer, '/testserver')
api.add_resource(TestClientServer, '/testclientserver')
api.add_resource(TutorialManagement, '/tutorial')
api.add_resource(ExerciseManagement, '/exercise')
api.add_resource(ExerciseQuestionManagement, '/exercisequestion')
if __name__ == '__main__':
    app.run(debug=True)