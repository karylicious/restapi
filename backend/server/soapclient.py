from zeep import Client
import os
CLIENT = Client(
    "http://localhost:8080/ClieserValidator/Validator?wsdl")
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Project:

    def readFileIntoByte(self, userDir, selectedFileName):
        userFile = ROOT_DIR + '\\uploads\\' + userDir
        return open(userFile, "rb").read()

    def testClient(self, clientEntryPoint, userDir, selectedFileName):
        selectedFileBytes = self.readFileIntoByte(userDir, selectedFileName)
        return CLIENT.service.testClient(clientEntryPoint, selectedFileBytes, selectedFileName)
   
    def testClientServer(self, clientEntryPoint, userDir, selectedFileName):
        selectedFileBytes = self.readFileIntoByte(userDir, selectedFileName)
        return CLIENT.service.testClientAndServer(clientEntryPoint, selectedFileBytes, selectedFileName)


    def deployServer(self, userDir, selectedFileName):
        selectedFileBytes = self.readFileIntoByte(userDir, selectedFileName)
        return CLIENT.service.deployServer(selectedFileBytes, selectedFileName)

    def undeployServer(self, selectedFileName):
        return CLIENT.service.undeployServer(selectedFileName)

    def gradeClientServer(self, clientEntryPoint, userDir, selectedFileName):
        selectedFileBytes = self.readFileIntoByte(userDir, selectedFileName)
        return CLIENT.service.gradeClientAndServer(clientEntryPoint, selectedFileBytes, selectedFileName)

    def gradeClient(self, clientEntryPoint, userDir, selectedFileName):
        selectedFileBytes = self.readFileIntoByte(userDir, selectedFileName)
        return CLIENT.service.testClientAndServer(clientEntryPoint, selectedFileBytes, selectedFileName)
   