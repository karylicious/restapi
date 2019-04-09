from flask_restful import Resource
from flask import Flask, jsonify, request, send_file
import shutil
import os
import datetime
import pathlib

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class ZipFile(Resource):
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

    def delete(self):
        args = request.args
        userDirectory = ROOT_DIR + '/uploads/' + args['dir']

        if os.path.isdir(userDirectory):
            shutil.rmtree(userDirectory)
        return jsonify({"succeed": True})

    def get(self):
        args = request.args

        userFile = ROOT_DIR + '/uploads/' + args['file']
        if not os.path.isfile(userFile):
            return jsonify({"succeed": False, "info": "File not found"})

        # return jsonify({"succeed": False, "info": "File not found"})

        data = args['file'].split("/")
        #userFile = ROOT_DIR + '/uploads/' + data[0]
        fileName = data[1]
        # uploads = os.path.join(current_app.root_path,
        #                       app.config['UPLOAD_FOLDER'])
        return send_file(userFile, mimetype='application/x-zip-compressed', as_attachment=True, attachment_filename=fileName)
