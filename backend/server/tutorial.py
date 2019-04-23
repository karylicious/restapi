from flask_restful import Resource
from flask import Flask, jsonify, request

class Tutorial(Resource):
    def post(self):
        # This method will create a tutorial and its associated lessons

        from app import db
        from models import Tutorial, Lesson
        
        try:
            data = request.json
                  
            duplicatedTutorial = Tutorial.query.filter(
                Tutorial.title == data['title']).first()

            if duplicatedTutorial is not None:
                return jsonify({"succeed": False, "info": "There is already a tutorial with the same title."})
                 
            new_tutorial = Tutorial(data['title'])
            db.session.add(new_tutorial)
            db.session.commit()

            for lesson in data['lessons']:
                newLesson = Lesson(
                    new_tutorial.id, lesson['title'], lesson['description'], lesson['link'])
                db.session.add(newLesson)
                db.session.commit()

            return jsonify({"succeed": True})
        except:
            #db.session.close()
            return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})

    def put(self):
        # This method will update a tutorial and its associated lessons
        from app import db
        from models import Tutorial, Lesson
        
        try:
            data = request.json
        
            tutorial = Tutorial.query.get(data['id'])

            if tutorial is None:
                return jsonify({"succeed": False, "info": "There is no tutorial with that id."})

            duplicatedTutorial = Tutorial.query.filter(
                Tutorial.title == data['title']).first()
     
            if duplicatedTutorial is not None:
                if duplicatedTutorial.id != int(data['id']):
                    return jsonify({"succeed": False, "info": "There is already a tutorial with the same title."})
               

            tutorial.title = data['title']
            db.session.commit()

            Lesson.query.filter(
                Lesson.tutorial_id == data['id']).delete()
            db.session.commit()

            for lesson in data['lessons']:
                newLesson = Lesson(
                    data['id'], lesson['title'], lesson['description'], lesson['link'])

                db.session.add(newLesson)
                db.session.commit()

            return jsonify({"succeed": True})
        except:
            #db.session.close()
            return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})
    
    def get(self):
        from app import db
        from models import Tutorial
        from tutorialschema import TutorialSchema

        try:        
            if len(request.args):
                args = request.args
                tutorial_schema = TutorialSchema(strict=True)
                tutorial = Tutorial.query.get(args['tutorialid'])

                return tutorial_schema.jsonify(tutorial)

            all_tutorial = Tutorial.query.all()
            tutorials_schema = TutorialSchema(many=True, strict=True)
            result = tutorials_schema.dump(all_tutorial)
            return jsonify(result.data)
        except:
            #db.session.close()
            return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})

    def delete(self):
        from app import db
        from models import Tutorial, Lesson

        try:
            # This will attempt to create database and tables again
            # Without it might generate an error about the table not exist on the database
            #db.create_all()     
        
            args = request.args
            tutorial = Tutorial.query.get(args['tutorialid'])
            
            if tutorial is None:
                return jsonify({"succeed": False, "info": "There is no tutorial with that id."})
            
            Lesson.query.filter(
                Lesson.tutorial_id == args['tutorialid']).delete()
            db.session.commit()

            db.session.delete(tutorial)
            db.session.commit()
            
            return jsonify({"succeed": True})
        except:
            #db.session.close()
            return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})
