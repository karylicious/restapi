from flask_restful import Resource
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash


class Session(Resource):
    def put(self):
        from app import db
        from models import Session

        db.create_all()

        try:
            args = request.args
            session = Session.query.filter(
                Session.username == args['username']).first()

            if not session:
                return jsonify({"succeed": False, "info": "User not found."})

            if args['loggedin'] == "false":
                session.loggedin = False
            elif args['loggedin'] == "true":
                session.loggedin = True
             
            db.session.commit()

            return jsonify({"succeed": True})

        except:
            db.session.close()
            return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})

    def get(self):
        from app import db
        from models import Session

        db.create_all()       

        try:
            args = request.args
            session = Session.query.filter(
                Session.username == args['username']).first()
            
            if not session:
                return jsonify({"succeed": False, "info": "User not found."})           

            return jsonify({"succeed": True, "loggedin": session.loggedin})

        except:
            db.session.close()
            return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})
