from flask_restful import Resource
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash


class User(Resource):
    def put(self):
        from app import db
        from models import User

        db.create_all()

        try:
            args = request.args
            user = User.query.filter(
                User.username == args['username']).first()

            if not user:
                return jsonify({"succeed": False, "info": "User not found. Please try again."})

            user.password = generate_password_hash(args['password'])

            db.session.commit()

            return jsonify({"succeed": True})

        except:
            return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})

    def get(self):
        from app import db
        from models import User

        db.create_all()

        
        # Uncoment the following lines only when the whole database is clear, then comment them again
        '''
        admin = User("admin","")
        db.session.add(admin)
        db.session.commit()

        from models import Session
        adminSession = Session("admin",False)
        db.session.add(adminSession)
        db.session.commit()'''

        try:
            args = request.args
            user = User.query.filter(
                User.username == args['username']).first()
            
            if not user:
                return jsonify({"succeed": False, "info": "User not found. Please try again."})

            if not args['password'] and not user.password:
                return jsonify({"succeed": True})

            if args['password'] and user.password and check_password_hash(user.password, args['password']):
                return jsonify({"succeed": True})

            return jsonify({"succeed": False, "info": "User not found. Please try again."})

        except:
            return jsonify({"succeed": False, "info": "User not found. Please try again."})
