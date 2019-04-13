from flask_restful import Resource
from flask import Flask, jsonify, request


class ExerciseQuestion(Resource):
    def delete(self):
        # This function is only used during debug mode
        from app import db
        from models import ExerciseQuestion

        db.create_all()
        args = request.args

        try:
            exerciseQuestion = ExerciseQuestion.query.get(
                args['exercisequestionid'])

            if exerciseQuestion is None:
                return jsonify({"succeed": False, "info": "There is no question with that id."})

            db.session.delete(exerciseQuestion)
            db.session.commit()
            return jsonify({"succeed": True})

        except:
            db.session.close()
            return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})

    def get(self):
        from app import db
        from models import ExerciseQuestion
        from exercisequestionschema import ExerciseQuestionSchema

        db.create_all()
        args = request.args

        try:
            questions = ExerciseQuestion.query.filter_by(
                exercise_id=args['exerciseid']).all()

            exercise_questions_schema = ExerciseQuestionSchema(
                many=True, strict=True)
            result = exercise_questions_schema.dump(questions)
            return jsonify(result.data)

        except:
            db.session.close()
            return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})
