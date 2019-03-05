from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from werkzeug import secure_filename
from flask_cors import CORS
import os
import shutil
import pathlib
import datetime
import json
from soapclient import Project

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
CORS(app)
api = Api(app)

class Upload(Resource):
    def post(self):
        file = request.files['file']

        if file:
            # secure_filename(file.filename) method changes modifies the file structure, for this reason it's not used
            filename = file.filename 
            userdir = f"{datetime.datetime.now():%Y%m%d%H%M%S}"

            uploadDirectory = ROOT_DIR + '/uploads/' + userdir
            pathlib.Path(uploadDirectory).mkdir(parents=True, exist_ok=True)

            file.save(os.path.join(uploadDirectory, filename))
            return jsonify({"succeed": 'true', "Info": "File uploaded successfully",  "d": userdir})

        return jsonify({"succeed": 'false', "Info": "File not uploaded"})


class Directory(Resource):
    def delete(self):
        args = request.args
        userDirectory = ROOT_DIR + '/uploads/' + args['dir']
        shutil.rmtree(userDirectory)
        return jsonify({"succeed": 'true'})


class TestClient(Resource):
    def get(self):
        args = request.args
        soapClient = Project()
        response = soapClient.testClient(
            args['clientEntryPoint'], args['dir'], args['selectedFileName'])
        results = Result()
        return jsonify(results.getJsonFormated(response))


class TestServer(Resource):
    def get(self):
        args = request.args
        soapClient = Project()
        response = soapClient.testServer(
            args['serverEntryPoint'], args['dir'], args['selectedFileName'])     
        results = Result()
        return jsonify(results.getJsonFormated(response))


class TestClientServer(Resource):
    def get(self):
        args = request.args
        soapClient = Project()
        response = soapClient.testClientServer(
            args['clientEntryPoint'], args['serverEntryPoint'], args['dir'], args['selectedFileName'])
        results = Result()
        print (jsonify(results.getJsonFormated(response)))
        return jsonify(results.getJsonFormated(response))

class Result():
    def getJsonFormated(self, response):
        #Although the response['responseList'] is JSON serializable,
        #the response['testResultList'] is not (TypeError: Object of type testResult is not JSON serializable)
        #As a solution I use the following for loops 
        projects, titles, results =[], [], []
        for row in response['testResultList']:
            projects.append(row['projectOwner'])
            titles.append(row['title'])
            results.append(row['result'])

        jsonData = [{"projectOwner": project,"title": title, "result": result} for project, title, result in zip(projects, titles, results)]
        return {'responseList' : response['responseList'], 'testResultList' : jsonData}


api.add_resource(Upload, '/uploadfile')
api.add_resource(Directory, '/deletedir')
api.add_resource(TestClient, '/testclient')
api.add_resource(TestServer, '/testserver')
api.add_resource(TestClientServer, '/testclientserver')

if __name__ == '__main__':
    app.run(debug=True)