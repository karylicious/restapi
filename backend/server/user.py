from flask_restful import Resource
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash


class User(Resource):
    def put(self):        
        # This method will update the user password
        
        from app import db
        from models import User
        
        try:
            # This will attempt to create database and tables again
            # Without it might generate an error about the table not exist on the database
            db.create_all()
        
            args = request.args
            user = User.query.filter(
                User.username == args['username']).first()

            if not user:
                return jsonify({"succeed": False, "info": "User not found. Please try again."})

            user.password = generate_password_hash(args['password'])

            db.session.commit()

            return jsonify({"succeed": True})

        except:
            db.session.close()
            return jsonify({"succeed": False, "info": "Unexpected error has occured. Please try again."})

    def get(self):
        # This method will essentially login a user

        from app import db
        from models import User
        
        try:
            # This will attempt to create database and tables again
            # Without it might generate an error about the table not exist on the database
            db.create_all()
        
            # when the database is empty, this will create the admin user and the associated session
            # so that the admin can login without having a password set
            admin = User("admin","")
            db.session.add(admin)
            db.session.commit()

            from models import Session
            adminSession = Session("admin",False)
            db.session.add(adminSession)
            db.session.commit()

        except:
            print("Admin user already exists")
            db.session.close()

        try:
            args = request.args            
            user = User.query.filter(
                User.username == args['username']).first()
                
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
            db.session.close()
            return jsonify({"succeed": False, "info": "User not found. Please try again."})
