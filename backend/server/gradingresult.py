class GradingResult():
    def getJsonFormated(self, response):
        #Although the response['responseList'] is JSON serializable,
        #the response['testResultList'] is not (TypeError: Object of type testResult is not JSON serializable)
        #As a solution I use the following for loops 
        projects, titles, results, grades, actualTestOutputs =[], [], [], [], [] 
        #The following indexes come from the TestResult class of the webservice on Glassfish
        for row in response['gradingResultList']:
            projects.append(row['projectOwner'])
            titles.append(row['title'])
            results.append(row['hasPassed'])
            grades.append(row['grade'])
            actualTestOutputs.append(row['actualTestOutput'])

        jsonData = [{"projectOwner": project,"title": title, "hasPassed": result, "grade": grade, "actualTestOutput" : actualTestOutput} for project, title, result, grade, actualTestOutput in zip(projects, titles, results, grades, actualTestOutputs)]
     
        return {'finalGrade': response['finalGrade'], 'responseList' : response['responseList'], 'gradingResultList' : jsonData}
