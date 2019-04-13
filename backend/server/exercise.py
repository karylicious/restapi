from flask_restful import Resource
from flask import Flask, jsonify, request
import shutil
import os
from soapclient import Project

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Exercise(Resource):
    def post(self):
        from app import db
        from models import Exercise, ExerciseQuestion

        db.create_all()
        data = request.json
        soapClient = Project()

        try:
            if data['uploadedfile']:
                # User has uploaded a zip file
                userFile = ROOT_DIR + '/uploads/' + data['uploadedfile']
                if not os.path.isfile(userFile):
                    return jsonify({"succeed": False, "info": "Uploaded file has not been found. Please upload it again."})

                serverDirectoryNameOnDeployment = ""

                if data['type'] == 'client':

                    response = soapClient.deployServer(
                        data['uploadedfile'], data['selectedFileName'])

                    if response is None:
                        directory = data['uploadedfile'].split("/")
                        self.deleteDirectoryFromUploadsDirectory(directory)
                        return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})

                    if "/" not in response:
                        # This means there is already a deployed web service with the same name as the one on the zip file
                        directory = data['uploadedfile'].split("/")
                        self.deleteDirectoryFromUploadsDirectory(directory)

                        return jsonify({"succeed": False, "info": response})

                    elif "/" in response:
                        serverDirectoryNameOnDeployment = response


                pathSplitted = data['uploadedfile'].split("/")

                os.rename(os.path.join(ROOT_DIR + '/uploads', pathSplitted[0]),
                os.path.join(ROOT_DIR + '/uploads', "exercise-"+pathSplitted[0]))
                uploadedfilePath = "exercise-"+pathSplitted[0]+'/'+pathSplitted[1]
               

                new_exercise = Exercise(uploadedfilePath, data['type'],
                                        data['description'], data['expectedClientEntryPoint'], serverDirectoryNameOnDeployment)
                db.session.add(new_exercise)
                db.session.commit()

                for question in data['questions']:
                    newExercisequestion = ExerciseQuestion(
                        new_exercise.id, question['title'], question['description'], question['expectedInvokedMethod'], question['expectedOutput'], question['points'])
                    db.session.add(newExercisequestion)
                    db.session.commit()

                return jsonify({"succeed": True})
        except:
            db.session.close()
            return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})

    def put(self):
        from app import db
        from models import Exercise, ExerciseQuestion

        db.create_all()
        data = request.json

        try:
            exercise = Exercise.query.get(data['id'])

            if exercise is None:
                return jsonify({"succeed": False, "info": "There is no exercise with that id."})

            if data['uploadedfile']:
                # User has uploaded a zip file
                userFile = ROOT_DIR + '/uploads/' + data['uploadedfile']
                if not os.path.isfile(userFile):
                    return jsonify({"succeed": False, "info": "Uploaded file has not been found. Please upload it again."})

                if data['type'] == 'client':
                    soapClient = Project()
                    response = soapClient.deployServer(
                        data['uploadedfile'], data['selectedFileName'])

                    if response is None:
                        return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})

                    if "/" not in response:
                        # This means there is already a deployed web service with the same name as the one on the zip file
                        directory = data['uploadedfile'].split("/")
                        self.deleteDirectoryFromUploadsDirectory(directory)

                        return jsonify({"succeed": False, "info": response})

                    elif "/" in response:
                        soapClient.undeployServer(
                            exercise.serverDirectoryNameOnDeployment)

                    exercise.serverDirectoryNameOnDeployment = response

                previousFile = exercise.uploadedfile
                directory = previousFile.split("/")
                self.deleteDirectoryFromUploadsDirectory(directory)

                
                pathSplitted = data['uploadedfile'].split("/")

                os.rename(os.path.join(ROOT_DIR + '/uploads', pathSplitted[0]),
                os.path.join(ROOT_DIR + '/uploads', "exercise-"+pathSplitted[0]))
                uploadedfilePath = "exercise-"+pathSplitted[0]+'/'+pathSplitted[1]

                exercise.uploadedfile = uploadedfilePath

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

            return jsonify({"succeed": True})
        except:
            db.session.close()
            return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})

    def deleteDirectoryFromUploadsDirectory(self, directory):
        userDirectory = ROOT_DIR + '/uploads/' + directory[0]
        if os.path.isdir(userDirectory):
            shutil.rmtree(userDirectory)

    def get(self):
        from app import db
        from models import Exercise
        from exerciseschema import ExerciseSchema

        db.create_all()

        try:
            if len(request.args):
                args = request.args
                exercise_schema = ExerciseSchema(strict=True)
                exercise = Exercise.query.get(args['exerciseid'])

                return exercise_schema.jsonify(exercise)

            all_exercises = Exercise.query.all()
            exercises_schema = ExerciseSchema(many=True, strict=True)
            result = exercises_schema.dump(all_exercises)
            return jsonify(result.data)
        except:
            db.session.close()
            return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})

    def delete(self):
        from app import db
        from models import Exercise, ExerciseQuestion
        from exerciseschema import ExerciseSchema

        db.create_all()        

        try:
            args = request.args
            exercise = Exercise.query.get(args['exerciseid'])
            
            if exercise is None:
                return jsonify({"succeed": False, "info": "There is no exercise with that id."})

            
            directory = exercise.uploadedfile.split("/")            
            userDirectory = ROOT_DIR + '/uploads/' + directory[0]
       
            if os.path.isdir(userDirectory):
                shutil.rmtree(userDirectory)
           
            if exercise.exerciseType == 'client':
                soapClient = Project()
                soapClient.undeployServer(exercise.serverDirectoryNameOnDeployment)
          
            ExerciseQuestion.query.filter(
                ExerciseQuestion.exercise_id == args['exerciseid']).delete()
            db.session.commit()

            db.session.delete(exercise)
            db.session.commit()
            
            return jsonify({"succeed": True})
        except:
            db.session.close()
            return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})
