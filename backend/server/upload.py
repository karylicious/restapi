from flask import Flask, jsonify, request
from flask_restful import Resource
import os
import datetime
import pathlib

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Upload(Resource):
    def post(self):
        file = request.files['file']

        if file:
            # secure_filename(file.filename) method changes modifies the file structure, for this reason it's not used
            filename = file.filename 
            userdir = f"{datetime.datetime.now():%Y%m%d%H%M%S}"

            uploadDirectory = ROOT_DIR + '/uploads/' + userdir
            pathlib.Path(uploadDirectory).mkdir(parents=True, exist_ok=True)

            file.save(os.path.join(uploadDirectory, filename))
            return jsonify({"succeed": True, "Info": "File uploaded successfully",  "d": userdir})

        return jsonify({"succeed": False, "Info": "File not uploaded"})
