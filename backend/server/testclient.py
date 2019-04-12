from flask_restful import Resource
from flask import Flask, jsonify, request
from testresult import TestResult
from soapclient import Project

class TestClient(Resource):
    def get(self):
        args = request.args
        soapClient = Project()
        response = soapClient.testClient(
            args['clientEntryPoint'], args['dir'], args['selectedFileName'])
        results = TestResult()
        return jsonify(results.getJsonFormated(response))