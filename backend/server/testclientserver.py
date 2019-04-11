from flask_restful import Resource
from flask import Flask, jsonify, request
from testresult import TestResult
from soapclient import Project


class TestClientServer(Resource):
    def get(self):
        args = request.args
        soapClient = Project()
        response = soapClient.testClientServer(
            args['clientEntryPoint'], args['dir'], args['selectedFileName'])
        results = TestResult()
        print(jsonify(results.getJsonFormated(response)))
        return jsonify(results.getJsonFormated(response))
