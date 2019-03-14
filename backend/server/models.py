from app import db

class Tutorial (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    level = db.Column(db.Integer, unique=True, nullable=False)

    def __init__(self, name, level):
        self.name = name
        self.level = level
    

    #def alreadyExists(self, name, level):
