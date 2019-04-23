from flask_restful import Resource
from flask import Flask, jsonify, request


class Lesson(Resource):    
    def get(self):
        from app import db
        from models import Tutorial, Lesson
        from lessonschema import LessonSchema

        try:
            args = request.args        

            lessons = Lesson.query.filter_by(
                tutorial_id=args['tutorialid']).all()

            lessons_schema = LessonSchema(
                many=True, strict=True)
            result = lessons_schema.dump(lessons)
            return jsonify(result.data)

        except:
            #db.session.close()
            return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})
