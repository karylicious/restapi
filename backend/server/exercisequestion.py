from flask_restful import Resource
from flask import Flask, jsonify, request


class ExerciseQuestion(Resource):
    def get(self):
        from app import db
        from models import ExerciseQuestion
        from exercisequestionschema import ExerciseQuestionSchema
        
        try:
            args = request.args
        
            questions = ExerciseQuestion.query.filter_by(
                exercise_id=args['exerciseid']).all()

            exercise_questions_schema = ExerciseQuestionSchema(
                many=True, strict=True)

            result = exercise_questions_schema.dump(questions)
            return jsonify(result.data)

        except:
            #db.session.close()
            return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})
