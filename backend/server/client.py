from flask_restful import Resource
from flask import Flask, jsonify, request
from result import Result
from soapclient import Project

class TestClient(Resource):
    def get(self):
        args = request.args
        soapClient = Project()
        response = soapClient.testClient(
            args['clientEntryPoint'], args['dir'], args['selectedFileName'])
        results = Result()
        return jsonify(results.getJsonFormated(response))
