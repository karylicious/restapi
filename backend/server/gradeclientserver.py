from flask_restful import Resource
from flask import Flask, jsonify, request
from gradingresult import GradingResult
from soapclient import Project


class GradeClientServer(Resource):
    def get(self):
        from app import db
        from models import ExerciseQuestion
        args = request.args
        
        try:
            questions = ExerciseQuestion.query.filter_by(
                    exercise_id=args['exerciseid']).all()
            xmlQuestionList = '<?xml version="1.0" encoding="UTF-8"?><questions>'
            for question in questions:
                xmlQuestionList += '<question>'
                xmlQuestionList += '<expectedinvokedmethod>'+ question.expectedInvokedMethod + '</expectedinvokedmethod>'    
                xmlQuestionList += '<points>' + str(question.points) +'</points>'  
                xmlQuestionList += '<expectedoutput>' + question.expectedOutput + '</expectedoutput>'
                xmlQuestionList += '</question>'            
            xmlQuestionList +='</questions>'      
            
            soapClient = Project()
            response = soapClient.gradeClientServer(
                args['clientEntryPoint'], args['dir'], args['selectedFileName'], xmlQuestionList)
            
            results = GradingResult()
            return jsonify(results.getJsonFormated(response))
        except:
            return {'finalGrade': [], 'responseList' : [], 'gradingResultList' : []}  
