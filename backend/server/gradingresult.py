class GradingResult():
    def getJsonFormated(self, response):
        #Although the response['responseList'] is JSON serializable,
        #the response['testResultList'] is not (TypeError: Object of type testResult is not JSON serializable)
        #As a solution I use the following for loops 
        #projects, titles, results =[], [], [] uncoment
        #for row in response['testResultList']:
            #projects.append(row['projectOwner'])
            #titles.append(row['title'])
            #results.append(row['result'])

        #jsonData = [{"projectOwner": project,"title": title, "result": result} for project, title, result in zip(projects, titles, results)]
        #return {'responseList' : response['responseList'], 'gradingResultList' : jsonData}
        return {'responseList' : response['responseList'], 'gradingResultList' : ''}
