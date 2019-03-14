from flask_restful import Resource
from flask import Flask, jsonify, request
from result import Result
from soapclient import Project

class TestClientServer(Resource):
    def get(self):
        args = request.args
        soapClient = Project()
        response = soapClient.testClientServer(
            args['clientEntryPoint'], args['serverEntryPoint'], args['dir'], args['selectedFileName'])
        results = Result()
        print (jsonify(results.getJsonFormated(response)))
        return jsonify(results.getJsonFormated(response))
