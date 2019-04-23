from flask_restful import Resource
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash


class User(Resource):
    def put(self):        
        # This method will update the user password
        
        from app import db
        from models import Users
        
        try:        
            args = request.args
            user = Users.query.filter(
                Users.username == args['username']).first()

            if not user:
                return jsonify({"succeed": False, "info": "User not found. Please try again."})

            user.password = generate_password_hash(args['password'])

            db.session.commit()

            return jsonify({"succeed": True})

        except:
            #db.session.close()
            return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})

    def get(self):
        # This method will essentially login a user

        from app import db
        from models import Users
       
        try:            
            args = request.args    
                   
            user = Users.query.filter(
                Users.username == args['username']).first()    
            print(user)         
            if not user:
                return jsonify({"succeed": False, "info": "User not found. Please try again."})

            # This condition will allow the admin login without having a password set
            if not args['password'] and not user.password:
                return jsonify({"succeed": True})

            # This condition will login the user if passwords match 
            if args['password'] and user.password and check_password_hash(user.password, args['password']):
                return jsonify({"succeed": True})

            return jsonify({"succeed": False, "info": "User not found. Please try again."})

        except:
            #db.session.close()
            return jsonify({"succeed": False, "info": "User not found. Please try again."})
