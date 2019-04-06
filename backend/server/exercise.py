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

        response = soapClient.deployServer(
            data['uploadedfile'], data['selectedFileName'])

        if response is None:
            return jsonify({"succeed": "false", "info": "Unexpected error has occured. Please try again."})

        if "/" not in response:
            # This means there is already a deployed web service with the same name as the one on the zip file
            directory = data['uploadedfile'].split("/")
            self.deleteDirectoryFromUploadsDirectory(directory)

            return jsonify({"succeed": "false", "info": response})

        elif "/" in response:
            serverDirectoryNameOnDeployment = response
            total = Exercise.query.count() + 1

            new_exercise = Exercise("Exercise " + str(total), data['uploadedfile'], data['type'],
                                    data['description'], data['expectedClientEntryPoint'], serverDirectoryNameOnDeployment)
            db.session.add(new_exercise)
            db.session.commit()

            for question in data['questions']:
                newExercisequestion = ExerciseQuestion(
                    new_exercise.id, question['title'], question['description'], question['expectedInvokedMethod'], question['expectedOutput'], question['points'])
                db.session.add(newExercisequestion)
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

        exercise = Exercise.query.get(data['id'])
        soapClient = Project()

        if data['uploadedfile'] is not None:
            # User has uploaded a zip file
            userFile = ROOT_DIR + '/uploads/' + data['uploadedfile']
            if not os.path.isfile(userFile):
                return jsonify({"succeed": "false", "info": "Uploaded file has not been file. Please upload it again."})

            response = soapClient.deployServer(
                data['uploadedfile'], data['selectedFileName'])

            if response is None:
                return jsonify({"succeed": "false", "info": "Unexpected error has occured. Please try again."})

            if "/" not in response:
                # This means there is already a deployed web service with the same name as the one on the zip file
                directory = data['uploadedfile'].split("/")
                self.deleteDirectoryFromUploadsDirectory(directory)

                return jsonify({"succeed": "false", "info": response})

            elif "/" in response:
                soapClient.undeployServer(
                    exercise.serverDirectoryNameOnDeployment)

                previousFile = exercise.uploadedfile
                directory = previousFile.split("/")
                self.deleteDirectoryFromUploadsDirectory(directory)

                exercise.serverDirectoryNameOnDeployment = response
                exercise.uploadedfile = data['uploadedfile']

        exercise.description = data['description']
        exercise.expectedClientEntryPoint = data['expectedClientEntryPoint']
        db.session.commit()

        ExerciseQuestion.query.filter(
            ExerciseQuestion.exercise_id == data['id']).delete()
        db.session.commit()

        for question in data['questions']:
            newExerciseQuestion = ExerciseQuestion(
                data['id'], question['title'], question['description'], question['expectedInvokedMethod'], question['expectedOutput'], question['points'])

            db.session.add(newExerciseQuestion)
            db.session.commit()

        return jsonify({"succeed": "true"})

    def deleteDirectoryFromUploadsDirectory(self, directory):
        userDirectory = ROOT_DIR + '/uploads/' + directory[0]
        if os.path.isdir(userDirectory):
            shutil.rmtree(userDirectory)

    def get(self):
        from app import db
        from models import Exercise
        from exerciseschema import ExerciseSchema

        db.create_all()

        if len(request.args):
            args = request.args
            exercise_schema = ExerciseSchema(strict=True)
            exercise = Exercise.query.get(args['exerciseid'])

            return exercise_schema.jsonify(exercise)

        all_exercises = Exercise.query.all()
        exercises_schema = ExerciseSchema(many=True, strict=True)
        result = exercises_schema.dump(all_exercises)
        return jsonify(result.data)

    def delete(self):
        from app import db
        from models import Exercise, ExerciseQuestion
        from exerciseschema import ExerciseSchema

        db.create_all()
        args = request.args
        exerciseIDArg = args['exerciseid']

        exercise_by_id = Exercise.query.filter_by(
            id=exerciseIDArg).first()  # revise this line

        if exercise_by_id is None:
            return jsonify({"succeed": 'false', "info": "There is no exercise with that id."})

        # should be this line instead
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
        remaining = Exercise.query.count()
        return jsonify({"succeed": 'true', "total": remaining})
