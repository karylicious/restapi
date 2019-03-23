from flask_restful import Resource
from flask import Flask, jsonify, request

class ExerciseQuestionManagement(Resource):
    def delete(self):
        from app import db
        from models import ExerciseQuestion
        from exercisequestionschema import ExerciseQuestionSchema
        db.create_all()
        args = request.args
        exerciseQuestionIDArg = args['exercisequestionid']

        exerciseQuestion_by_id = ExerciseQuestion.query.filter_by(id=exerciseQuestionIDArg).first()       
        
        if exerciseQuestion_by_id is None :
            return jsonify({"succeed": 'false', "info": "There is no question with that id."})
        
        exerciseQuestion = ExerciseQuestion.query.get(exerciseQuestionIDArg)
        db.session.delete(exerciseQuestion)
        db.session.commit()
        return jsonify({"succeed": 'true'})
        

    def get(self):
        from app import db
        from models import Exercise, ExerciseQuestion
        from exercisequestionschema import ExerciseQuestionSchema

        db.create_all()
        
        args = request.args
        exerciseIDArg = args['exerciseid']
        
        questions = ExerciseQuestion.query.filter_by(exercise_id=exerciseIDArg).all()
       
        exercise_questions_schema = ExerciseQuestionSchema(many=True, strict=True)
        result = exercise_questions_schema.dump(questions)
        return jsonify(result.data)
