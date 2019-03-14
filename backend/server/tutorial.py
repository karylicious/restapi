from flask_restful import Resource
from flask import Flask, jsonify, request
#import shutil
#import os
#from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
#from tutorialshema import TutorialSchema
#from models import Tutorial

#ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#app = Flask(__name__)
#app.config.from_pyfile('./app.py')
#init_app(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(ROOT_DIR, 'db.sqlite')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)
#marshmallow = Marshmallow(app)

# Init shema
#tutorial_schema = TutorialSchema(strict=True)
#tutorials_shema = TutorialSchema(many=True, strict=True)

class TutorialManagement(Resource):
    def post(self):
        from app import db
        from models import Tutorial
        from tutorialshema import TutorialSchema
        db.create_all()
        args = request.args
        nameArg = args['name']
        levelArg = args['level']

        if not levelArg.isdigit():
            return jsonify({"succeed": 'false', "info": "Invalid level."})

        tutorial_by_name = Tutorial.query.filter_by(name=nameArg).first()       
        tutorial_by_level = Tutorial.query.filter_by(level=levelArg).first()

        if tutorial_by_level is not None :
            return jsonify({"succeed": 'false', "info": "There is already a tutorial in that level! Please enter different one."})
        elif tutorial_by_name is not None :
            return jsonify({"succeed": 'false', "info": "There is already a tutorial with that name! Please enter different one."})
        
        new_tutorial = Tutorial(nameArg, levelArg)
        db.session.add(new_tutorial)
        db.session.commit()
        tutorial_schema = TutorialSchema(strict=True)
        return tutorial_schema.jsonify(new_tutorial)
        #return jsonify({"succeed": 'true'})

    def update(self):
        from app import db
        from models import Tutorial
        from tutorialshema import TutorialSchema
        db.create_all()
        
        args = request.args
        idArg = args['id']
        nameArg = args['name']
        levelArg = args['level']

        if not levelArg.isdigit():
            return jsonify({"succeed": 'false', "info": "Invalid level."})

        tutorial_by_name = Tutorial.query.filter_by(name=nameArg).first()       
        tutorial_by_level = Tutorial.query.filter_by(level=levelArg).first()

        if tutorial_by_level is not None :
            return jsonify({"succeed": 'false', "info": "There is already a tutorial in that level! Please enter different one."})
        elif tutorial_by_name is not None :
            return jsonify({"succeed": 'false', "info": "There is already a tutorial with that name! Please enter different one."})
        
        tutorial = Tutorial.query.get(idArg)
        tutorial.name = nameArg
        tutorial.level = levelArg

        db.session.commit()
        tutorial_schema = TutorialSchema(strict=True)
        return tutorial_schema.jsonify(tutorial)

    def get(self):
        from app import db
        from models import Tutorial
        from tutorialshema import TutorialSchema
        db.create_all()
        all_tutorials = Tutorial.query.all()
        tutorials_shema = TutorialSchema(many=True, strict=True)
        result = tutorials_shema.dump(all_tutorials)
        return jsonify(result.data)

    def delete(self):
        from app import db
        from models import Tutorial
        from tutorialshema import TutorialSchema
        db.create_all()
        args = request.args
        idArg = args['id']

        tutorial = Tutorial.query.get(idArg)
        db.session.delete(tutorial)
        db.session.commit()
        return jsonify({"succeed": 'true'})
        
