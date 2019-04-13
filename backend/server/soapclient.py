from zeep import Client
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Project:

    def readFileIntoByte(self, userDir, selectedFileName):
        try:
            userFile = ROOT_DIR + '\\uploads\\' + userDir
            return open(userFile, "rb").read()
        except:
            print("Exception on reading bytes of file")

    def testClient(self, clientEntryPoint, userDir, selectedFileName):
        try:
            CLIENT = Client("http://localhost:8080/ClieserValidator/Validator?wsdl")
            selectedFileBytes = self.readFileIntoByte(userDir, selectedFileName)
            return CLIENT.service.testClient(clientEntryPoint, selectedFileBytes, selectedFileName)
        except:
            print("Web service is down")

    def testClientServer(self, clientEntryPoint, userDir, selectedFileName):
        try:
            CLIENT = Client("http://localhost:8080/ClieserValidator/Validator?wsdl")
            selectedFileBytes = self.readFileIntoByte(userDir, selectedFileName)
            return CLIENT.service.testClientAndServer(clientEntryPoint, selectedFileBytes, selectedFileName)

        except:
            print("Web service is down")
        #selectedFileBytes = self.readFileIntoByte(userDir, selectedFileName)
        #return CLIENT.service.testClientAndServer(clientEntryPoint, selectedFileBytes, selectedFileName)


    def deployServer(self, userDir, selectedFileName):
        try:
            CLIENT = Client("http://localhost:8080/ClieserValidator/Validator?wsdl")
            selectedFileBytes = self.readFileIntoByte(userDir, selectedFileName)
            return CLIENT.service.deployServer(selectedFileBytes, selectedFileName)
        except:
            print("Web service is down")

    def undeployServer(self, selectedFileName):
        try:
            CLIENT = Client("http://localhost:8080/ClieserValidator/Validator?wsdl")
            return CLIENT.service.undeployServer(selectedFileName)
        except:
            print("Web service is down")

    def gradeClientServer(self, clientEntryPoint, userDir, selectedFileName, questions):
        try:
            CLIENT = Client("http://localhost:8080/ClieserValidator/Validator?wsdl")
            selectedFileBytes = self.readFileIntoByte(userDir, selectedFileName)
            return CLIENT.service.gradeClientAndServer(clientEntryPoint, selectedFileBytes, selectedFileName, questions)
        except:
            print("Web service is down")

    def gradeClient(self, clientEntryPoint, userDir, selectedFileName, questions):
        try:
            CLIENT = Client("http://localhost:8080/ClieserValidator/Validator?wsdl")
            selectedFileBytes = self.readFileIntoByte(userDir, selectedFileName)
            return CLIENT.service.gradeClient(clientEntryPoint, selectedFileBytes, selectedFileName, questions)
        except:
            print("Web service is down")