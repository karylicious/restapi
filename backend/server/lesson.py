from flask_restful import Resource
from flask import Flask, jsonify, request


class Lesson(Resource):
    '''
    def delete(self):
        # This function is only meant to be used during the development mode
        from app import db
        from models import Lesson
        from lessonschema import LessonSchema

        db.create_all()
        args = request.args

        try:
            lesson = Lesson.query.get(
                args['lessonid'])

            if lesson is None:
                return jsonify({"succeed": False, "info": "There is no lesson with that id."})

            db.session.delete(lesson)
            db.session.commit()
            return jsonify({"succeed": True})

        except:
            db.session.close()
            return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})
    '''
    def get(self):
        from app import db
        from models import Tutorial, Lesson
        from lessonschema import LessonSchema

        try:
            # This will attempt to create database and tables again
            # Without it might generate an error about the table not exist on the database
            db.create_all()
            args = request.args        

            lessons = Lesson.query.filter_by(
                tutorial_id=args['tutorialid']).all()

            lessons_schema = LessonSchema(
                many=True, strict=True)
            result = lessons_schema.dump(lessons)
            return jsonify(result.data)

        except:
            db.session.close()
            return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})
