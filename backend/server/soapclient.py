from zeep import Client
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CLIESER_WEB_SERVICE_HOSTNAME = 'http://ec2-52-56-160-237.eu-west-2.compute.amazonaws.com:8080'
#CLIESER_WEB_SERVICE_HOSTNAME = 'http://localhost:8080'

# This class invokes the web service that will test and grade automatically a project
class Project:

    def readFileIntoByte(self, userDir, selectedFileName):
        try:
            userFile = ROOT_DIR + '\\uploads\\' + userDir
            return open(userFile, "rb").read()
        except:
            print("Exception on reading bytes of file")

    def testClient(self, clientEntryPoint, userDir, selectedFileName):
        try:
            CLIENT = Client(CLIESER_WEB_SERVICE_HOSTNAME + "/ClieserAutomation/Automation?wsdl")
            selectedFileBytes = self.readFileIntoByte(userDir, selectedFileName)
            return CLIENT.service.testClient(clientEntryPoint, selectedFileBytes, selectedFileName)
        except:
            print("Web service is down")

    def testClientServer(self, clientEntryPoint, userDir, selectedFileName):
        try:
            CLIENT = Client(CLIESER_WEB_SERVICE_HOSTNAME + "/ClieserAutomation/Automation?wsdl")
            selectedFileBytes = self.readFileIntoByte(userDir, selectedFileName)
            return CLIENT.service.testClientAndServer(clientEntryPoint, selectedFileBytes, selectedFileName)

        except:
            print("Web service is down")        

    def deployServer(self, userDir, selectedFileName):
        try:
            CLIENT = Client(CLIESER_WEB_SERVICE_HOSTNAME + "/ClieserAutomation/Automation?wsdl")
            selectedFileBytes = self.readFileIntoByte(userDir, selectedFileName)
            return CLIENT.service.deployServer(selectedFileBytes, selectedFileName)
        except:
            print("Web service is down")

    def undeployServer(self, selectedFileName):
        try:
            CLIENT = Client(CLIESER_WEB_SERVICE_HOSTNAME + "/ClieserAutomation/Automation?wsdl")
            return CLIENT.service.undeployServer(selectedFileName)
        except:
            print("Web service is down")

    def gradeClientServer(self, clientEntryPoint, userDir, selectedFileName, questions):
        try:
            CLIENT = Client(CLIESER_WEB_SERVICE_HOSTNAME + "/ClieserAutomation/Automation?wsdl")
            selectedFileBytes = self.readFileIntoByte(userDir, selectedFileName)
            return CLIENT.service.gradeClientAndServer(clientEntryPoint, selectedFileBytes, selectedFileName, questions)
        except:
            print("Web service is down")

    def gradeClient(self, clientEntryPoint, userDir, selectedFileName, questions):
        try:
            CLIENT = Client(CLIESER_WEB_SERVICE_HOSTNAME + "/ClieserAutomation/Automation?wsdl")
            selectedFileBytes = self.readFileIntoByte(userDir, selectedFileName)
            return CLIENT.service.gradeClient(clientEntryPoint, selectedFileBytes, selectedFileName, questions)
        except:
            print("Web service is down")