from flask_restful import Resource
from flask import Flask, jsonify, request
from gradingresult import GradingResult
from soapclient import Project

class GradeClient(Resource):
    def get(self):
        # This method will essentially create a XML string based on the data passed on the request
        # Then it will grade the uploaded zip file

        from app import db
        from models import ExerciseQuestion        

        try:
            args = request.args
            questions = ExerciseQuestion.query.filter_by(
                    exercise_id=args['exerciseid']).all()

            xmlQuestionList = '<?xml version="1.0" encoding="UTF-8"?><questions>'

            for question in questions:
                xmlQuestionList += '<question>'
                xmlQuestionList += '<expectedinvokedmethod>'+ question.expectedinvokedmethod + '</expectedinvokedmethod>'    
                xmlQuestionList += '<points>' + str(question.points) +'</points>'  
                xmlQuestionList += '<expectedoutput>' + question.expectedoutput + '</expectedoutput>'
                xmlQuestionList += '</question>' 

            xmlQuestionList +='</questions>'      
            
            soapClient = Project()
            response = soapClient.gradeClient(
                args['clientEntryPoint'], args['dir'], args['selectedFileName'], xmlQuestionList)
            
            results = GradingResult()
            return jsonify(results.getJsonFormated(response))      
        except:
            return {'finalGrade': [], 'responseList' : [], 'gradingResultList' : []}  
