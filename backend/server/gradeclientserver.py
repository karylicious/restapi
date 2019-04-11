from flask_restful import Resource
from flask import Flask, jsonify, request
from gradingresult import GradingResult
from soapclient import Project


class GradeClientServer(Resource):
    def get(self):
        args = request.args
        soapClient = Project()
        response = soapClient.gradeClientServer(
            args['clientEntryPoint'], args['dir'], args['selectedFileName'])

        #print(response)
        results = GradingResult()
        #print(jsonify(results.getJsonFormated(response)))
        return jsonify(results.getJsonFormated(response))
        #return jsonify({"succeed": True})
