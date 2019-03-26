from flask_restful import Resource
from flask import Flask, jsonify, request
import shutil
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class ExerciseManagement(Resource):
    def post(self):
        from app import db
        from models import Exercise, ExerciseQuestion
        from exerciseschema import ExerciseSchema
        from exercisequestionschema import ExerciseQuestionSchema

        db.create_all()

        total = Exercise.query.count()
        total += 1
        data = request.json

        new_exercise = Exercise("Exercise " + str(total), data['uploadedfile'], data['type'])
        db.session.add(new_exercise)
        db.session.commit()

       
        for question in data['questions']:
            new_exercisequestion = ExerciseQuestion(
                new_exercise.id, question['title'], question['description'])
            db.session.add(new_exercisequestion)
            db.session.commit()

        return jsonify({"succeed": "true"})

    def put(self):
        from app import db
        from models import Exercise, ExerciseQuestion
        from exerciseschema import ExerciseSchema
        from exercisequestionschema import ExerciseQuestionSchema
        db.create_all()
        data = request.json

        ExerciseQuestion.query.filter(
        ExerciseQuestion.exercise_id == data['id']).delete()
        db.session.commit()

        exercise = Exercise.query.get(data['id'])
        previousFile = exercise.uploadedfile
        exerciseName = exercise.name
        exerciseType = exercise.exercisetype

        db.session.delete(exercise)
        db.session.commit()

        
        if data['uploadedfile'] is not None:
            userDirectory = ROOT_DIR + '/uploads/' + previousFile
            shutil.rmtree(userDirectory)
            uploadedfile = data['uploadedfile']
        else:
            uploadedfile = previousFile

        new_exercise = Exercise(exerciseName, uploadedfile, exerciseType)
        db.session.add(new_exercise)
        db.session.commit()

       
        for question in data['questions']:
            new_exercisequestion = ExerciseQuestion(
                new_exercise.id, question['title'], question['description'])
            db.session.add(new_exercisequestion)
            db.session.commit()

        return jsonify({"succeed": "true"})

    def get(self):
        from app import db
        from models import Exercise
        from exerciseschema import ExerciseSchema
        db.create_all()
        
        all_exercises = Exercise.query.all()
        exercises_shema = ExerciseSchema(many=True, strict=True)
        result = exercises_shema.dump(all_exercises)
        return jsonify(result.data)

    def delete(self):
        from app import db
        from models import Exercise, ExerciseQuestion
        from exerciseschema import ExerciseSchema
        db.create_all()
        args = request.args
        exerciseIDArg = args['exerciseid']

        exercise_by_id = Exercise.query.filter_by(id=exerciseIDArg).first()

        if exercise_by_id is None:
            return jsonify({"succeed": 'false', "info": "There is no exercise with that id."})

        ExerciseQuestion.query.filter(
            ExerciseQuestion.exercise_id == exerciseIDArg).delete()
        db.session.commit()

        exercise = Exercise.query.get(exerciseIDArg)
        db.session.delete(exercise)
        db.session.commit()
        tt = Exercise.query.count()
        return jsonify({"succeed": 'true', "total": tt})
