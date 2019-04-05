from flask_restful import Resource
from flask import Flask, jsonify, request
import shutil
import os
from soapclient import Project

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class ExerciseManagement(Resource):
    def post(self):
        from app import db
        from models import Exercise, ExerciseQuestion
        from exerciseschema import ExerciseSchema
        from exercisequestionschema import ExerciseQuestionSchema
        
        db.create_all()

        data = request.json
        soapClient = Project()

        response = soapClient.deployServer(data['uploadedfile'], data['selectedFileName'])
        if response is None:
            return jsonify({"succeed": "false", "info": "Unexpected error has occured. Please try again."})
        if "/" not in response:
            return jsonify({"succeed": "false", "info": response})
        elif "/" in response:
            serverDirectoryNameOnDeployment = response   
            
            total = Exercise.query.count()
            total += 1
            
            
            new_exercise = Exercise("Exercise " + str(total), data['uploadedfile'], data['type'], data['description'], data['expectedClientEntryPoint'], serverDirectoryNameOnDeployment)
            db.session.add(new_exercise)
            db.session.commit()

        
            for question in data['questions']:
                new_exercisequestion = ExerciseQuestion(
                    new_exercise.id, question['title'], question['description'], question['expectedInvokedMethod'], question['expectedOutput'], question['points'])
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

        exercise_by_id = Exercise.query.filter_by(id=data['id']).first()

        if exercise_by_id is None:
            return jsonify({"succeed": 'false', "info": "There is no exercise with that id."})


        ExerciseQuestion.query.filter(
        ExerciseQuestion.exercise_id == data['id']).delete()
        db.session.commit()

        exercise = Exercise.query.get(data['id'])
        previousFile = exercise.uploadedfile
        exerciseName = exercise.name
        exerciseType = exercise.exerciseType
        previousServerDirectoryNameOnDeployment = exercise.serverDirectoryNameOnDeployment

        db.session.delete(exercise)
        db.session.commit()

        
        if data['uploadedfile'] is not None:
            directory = previousFile.split("/")
            userDirectory = ROOT_DIR + '/uploads/' + directory[0]
            if os.path.isdir(userDirectory):
                shutil.rmtree(userDirectory)
            uploadedfile = data['uploadedfile']

            soapClient = Project()
            response = soapClient.deployServer(data['uploadedfile'], data['selectedFileName'])
            if response is None:
                serverDirectoryNameOnDeployment = previousServerDirectoryNameOnDeployment
            else:
                serverDirectoryNameOnDeployment = response  
        else:
            uploadedfile = previousFile

        new_exercise = Exercise(exerciseName, uploadedfile, exerciseType, data['description'], data['expectedClientEntryPoint'], serverDirectoryNameOnDeployment)
        db.session.add(new_exercise)
        db.session.commit()

       
        for question in data['questions']:
            new_exercisequestion = ExerciseQuestion(
                new_exercise.id, question['title'], question['description'], question['expectedInvokedMethod'], question['expectedOutput'], question['points'])
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

        exercise = Exercise.query.get(exerciseIDArg)
        
        directory = exercise.uploadedfile.split("/")
        userDirectory = ROOT_DIR + '/uploads/' + directory[0]
        if os.path.isdir(userDirectory):
            shutil.rmtree(userDirectory)

        soapClient = Project()
        soapClient.undeployServer(exercise.serverDirectoryNameOnDeployment)


        ExerciseQuestion.query.filter(
            ExerciseQuestion.exercise_id == exerciseIDArg).delete()
        db.session.commit()

        
        db.session.delete(exercise)
        db.session.commit()
        tt = Exercise.query.count()
        return jsonify({"succeed": 'true', "total": tt})