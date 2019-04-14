from flask_restful import Resource
from flask import Flask, jsonify, request, send_file
import shutil
import os
import datetime
import pathlib

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class ZipUserFile(Resource):
    def post(self):
        # This method will upload a zip file
        try:
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
        except:
            return jsonify({"succeed": False, "Info": "File not uploaded"})

    def delete(self):
        # This method will delete an uploaded file and its parent directory
        try:
            args = request.args
            userDirectory = ROOT_DIR + '/uploads/' + args['dir']

            if os.path.isdir(userDirectory):
                shutil.rmtree(userDirectory)
            return jsonify({"succeed": True})
        except:
            return jsonify({"succeed": False})

    def get(self):
        # This method will return the bytes of a zip file to enable the download of the file
        try:
            args = request.args

            userFile = ROOT_DIR + '/uploads/' + args['file']
            if not os.path.isfile(userFile):
                return jsonify({"succeed": False, "info": "File not found"})

            data = args['file'].split("/")
            fileName = data[1]
            return send_file(userFile, mimetype='application/x-zip-compressed', as_attachment=True, attachment_filename=fileName)
        except:
            return jsonify({"succeed": False})

