class TestResult():
    def getJsonFormated(self, response):
        #Although the response['responseList'] is JSON serializable,
        #the response['testResultList'] is not (TypeError: Object of type testResult is not JSON serializable)
        #As a solution I use the following for loops 
        projects, titles, results =[], [], []

        #The following indexes come from the TestResult class of the webservice on Glassfish
        for row in response['testResultList']:
            projects.append(row['projectOwner'])
            titles.append(row['title'])
            results.append(row['hasPassed'])

        jsonData = [{"projectOwner": project,"title": title, "hasPassed": result} for project, title, result in zip(projects, titles, results)]
        return {'responseList' : response['responseList'], 'testResultList' : jsonData}
