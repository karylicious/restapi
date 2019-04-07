from flask_restful import Resource
from flask import Flask, jsonify, request
import shutil
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Directory(Resource):
    def delete(self):
        args = request.args
        userDirectory = ROOT_DIR + '/uploads/' + args['dir']
        if os.path.isdir(userDirectory):
            shutil.rmtree(userDirectory)
        return jsonify({"succeed": True})
