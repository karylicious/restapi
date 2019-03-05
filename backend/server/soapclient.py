from zeep import Client
import os
CLIENT = Client(
    "http://ec2-3-8-124-194.eu-west-2.compute.amazonaws.com:8080/thewebservice-1/ToolService?wsdl")
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Project:

    def readFileIntoByte(self, userDir, selectedFileName):
        userFile = ROOT_DIR + '\\uploads\\' + userDir + '\\' + selectedFileName + '.zip'
        return open(userFile, "rb").read()

    def testClient(self, clientEntryPoint, userDir, selectedFileName):
        selectedFileBytes = self.readFileIntoByte(userDir, selectedFileName)
        return CLIENT.service.testClient(clientEntryPoint, selectedFileBytes, selectedFileName)

    def testServer(self, serverEntryPoint, userDir, selectedFileName):     
        selectedFileBytes = self.readFileIntoByte(userDir, selectedFileName)
        return CLIENT.service.testServer(serverEntryPoint, selectedFileBytes, selectedFileName)

    def testClientServer(self, clientEntryPoint, serverEntryPoint, userDir, selectedFileName):
        selectedFileBytes = self.readFileIntoByte(userDir, selectedFileName)
        return CLIENT.service.testClientAndServer(clientEntryPoint, serverEntryPoint, selectedFileBytes, selectedFileName)
