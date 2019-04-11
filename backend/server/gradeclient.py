from flask_restful import Resource
from flask import Flask, jsonify, request
from gradingresult import GradingResult
from soapclient import Project

class GradeClient(Resource):
    def get(self):
        args = request.args
        soapClient = Project()
        response = soapClient.gradeClient(
            args['clientEntryPoint'], args['dir'], args['selectedFileName'])
        results = GradingResult()
        return jsonify(results.getJsonFormated(response))
